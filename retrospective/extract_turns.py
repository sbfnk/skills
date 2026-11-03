#!/usr/bin/env python3
"""Extract a readable transcript (user prompts, assistant text, tool-call names)
from a coding-agent session log, within a time window.

Usage: extract_turns.py LOG --from 2026-10-09T09:00 --to 2026-10-09T20:00 --out OUT.md [--max-chars 2500]
Times are in --tz (default: the machine's zone). Tool results are omitted; tool calls are shown as one line.
"""
import argparse, json, os, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_prompts import clean, to_local

LONDON = None

def summarise_input(name, inp):
    if not isinstance(inp, dict):
        return str(inp)[:200]
    for k in ("file_path", "path", "command", "cmd", "pattern", "description", "prompt", "query"):
        if k in inp:
            v = inp[k]
            if isinstance(v, list): v = " ".join(map(str, v))
            return f"{k}={str(v)[:200]}"
    return json.dumps(inp)[:200]

def records(path):
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = d.get("timestamp"); typ = d.get("type")
        msg = d.get("message") if isinstance(d.get("message"), dict) else None
        if typ == "user" and msg and not d.get("isMeta"):
            c = msg.get("content")
            texts = [c] if isinstance(c, str) else [x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text"] if isinstance(c, list) else []
            for t in texts:
                ct = clean(t)
                if ct: yield ts, "USER", ct
        elif typ == "assistant" and msg:
            for x in msg.get("content") or []:
                if not isinstance(x, dict): continue
                if x.get("type") == "text" and x.get("text", "").strip():
                    yield ts, "ASSISTANT", x["text"]
                elif x.get("type") == "tool_use":
                    yield ts, "TOOL", f"{x.get('name')}: {summarise_input(x.get('name'), x.get('input'))}"
        elif typ == "response_item":
            p = d.get("payload") or {}
            pt = p.get("type")
            if pt == "message" and p.get("role") == "user":
                for x in p.get("content") or []:
                    if isinstance(x, dict) and x.get("type") in ("input_text", "text"):
                        ct = clean(x.get("text", ""))
                        if ct: yield ts, "USER", ct
            elif pt == "message" and p.get("role") == "assistant":
                for x in p.get("content") or []:
                    if isinstance(x, dict) and x.get("type") in ("output_text", "text") and x.get("text", "").strip():
                        yield ts, "ASSISTANT", x["text"]
            elif pt in ("function_call", "custom_tool_call", "local_shell_call"):
                args = p.get("arguments") or p.get("input") or ""
                yield ts, "TOOL", f"{p.get('name', pt)}: {str(args)[:200]}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log"); ap.add_argument("--from", dest="start", required=True); ap.add_argument("--to", dest="end", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--max-chars", type=int, default=2500)
    ap.add_argument("--tz", default=None)
    a = ap.parse_args()
    global LONDON
    LONDON = ZoneInfo(a.tz) if a.tz else datetime.now().astimezone().tzinfo
    import extract_prompts; extract_prompts.LONDON = LONDON
    start = datetime.fromisoformat(a.start).replace(tzinfo=LONDON); end = datetime.fromisoformat(a.end).replace(tzinfo=LONDON)
    n = 0; last_tool = None
    with open(a.out, "w") as fh:
        fh.write(f"# {os.path.basename(a.log)} {a.start} to {a.end}\n\n")
        seen_assistant = set()
        for ts, kind, text in records(a.log):
            dt = to_local(ts)
            if not dt or dt < start or dt > end: continue
            if kind == "ASSISTANT":
                key = text[:200]
                if key in seen_assistant: continue
                seen_assistant.add(key)
            if kind == "TOOL":
                if text == last_tool: continue
                last_tool = text
                fh.write(f"- {dt.strftime('%m-%d %H:%M')} [tool] {text}\n")
                continue
            body = text if len(text) <= a.max_chars else text[:a.max_chars] + f" […{len(text)-a.max_chars} more chars]"
            fh.write(f"\n### {dt.strftime('%m-%d %H:%M')} {kind}\n\n{body}\n")
            n += 1
    print(f"{n} turns -> {a.out}")

if __name__ == "__main__":
    main()
