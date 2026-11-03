#!/usr/bin/env python3
"""Extract the person's own prompts from coding-agent session logs.

Writes a chronological Markdown log and a per-day statistics table, so the
course of a long LLM-assisted writing project can be read back from what the
user actually typed.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

LONDON = None  # set from --tz in main()

HARNESS_PREFIXES = (
    "<system-reminder>", "<command-name>", "<command-message>", "<local-command",
    "<bash-input>", "<bash-stdout>", "<bash-stderr>", "<user-prompt-submit-hook>",
    "Caveat: The messages below", "Base directory for this skill", "# AGENTS.md instructions",
    "<environment_context>", "<turn_context", "<permissions", "<task-notification",
    "<INSTRUCTIONS>", "[Request interrupted", "<attachment", "<ide_", "<pasted_content",
)
COMPACTION = "This session is being continued from a previous conversation"


def clean(text):
    """Strip harness wrappers; return None if nothing the user wrote remains."""
    if not isinstance(text, str):
        return None
    t = text.strip()
    if not t:
        return None
    if t.startswith(COMPACTION):
        return "[context compaction]"
    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S).strip()
    t = re.sub(r"<pasted_content[^>]*>", "[paste] ", t)
    t = re.sub(r"</pasted_content[^>]*>", "", t).strip()
    # Slash-command invocations: keep the command name only.
    m = re.match(r"<command-name>(.*?)</command-name>", t, flags=re.S)
    if m:
        args = re.search(r"<command-args>(.*?)</command-args>", t, flags=re.S)
        return "/" + m.group(1).strip().lstrip("/") + (" " + args.group(1).strip() if args and args.group(1).strip() else "")
    for p in HARNESS_PREFIXES:
        if t.startswith(p):
            return None
    if not t:
        return None
    return t


def claude_records(path):
    sid = os.path.basename(path).split(".")[0]
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = d.get("timestamp")
        typ = d.get("type")
        msg = d.get("message") if isinstance(d.get("message"), dict) else None
        if typ == "user" and msg and not d.get("isMeta"):
            c = msg.get("content")
            texts = []
            if isinstance(c, str):
                texts.append(c)
            elif isinstance(c, list):
                for x in c:
                    if isinstance(x, dict) and x.get("type") == "text":
                        texts.append(x.get("text", ""))
            for t in texts:
                ct = clean(t)
                if ct:
                    yield {"ts": ts, "tool": "claude", "session": sid, "kind": "prompt", "text": ct}
        elif typ == "assistant" and msg:
            usage = msg.get("usage") or {}
            yield {"ts": ts, "tool": "claude", "session": sid, "kind": "assistant",
                   "msgid": msg.get("id"), "out": usage.get("output_tokens", 0),
                   "tools": sum(1 for x in (msg.get("content") or []) if isinstance(x, dict) and x.get("type") == "tool_use")}


def codex_records(path):
    sid = os.path.basename(path).split(".")[0][-36:]
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts = d.get("timestamp")
        p = d.get("payload") or {}
        if d.get("type") == "response_item":
            if p.get("type") == "message" and p.get("role") == "user":
                for x in p.get("content") or []:
                    if isinstance(x, dict) and x.get("type") in ("input_text", "text"):
                        ct = clean(x.get("text", ""))
                        if ct:
                            yield {"ts": ts, "tool": "codex", "session": sid, "kind": "prompt", "text": ct}
            elif p.get("type") == "message" and p.get("role") == "assistant":
                yield {"ts": ts, "tool": "codex", "session": sid, "kind": "assistant", "msgid": None, "out": 0, "tools": 0}
            elif p.get("type") in ("function_call", "custom_tool_call", "local_shell_call"):
                yield {"ts": ts, "tool": "codex", "session": sid, "kind": "toolcall"}
        elif d.get("type") == "token_usage_record":
            info = p.get("info") or p
            last = info.get("last_token_usage") or {}
            yield {"ts": ts, "tool": "codex", "session": sid, "kind": "tokens", "out": last.get("output_tokens", 0)}


def to_local(ts):
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt.astimezone(LONDON)


def main(out_dir, project, claude_globs, codex_globs, tz):
    global LONDON
    LONDON = ZoneInfo(tz)
    recs = []
    for g in claude_globs:
        for f in glob.glob(os.path.expanduser(g)):
            recs.extend(claude_records(f))
    for g in codex_globs:
        for f in glob.glob(os.path.expanduser(g)):
            with open(f, encoding="utf-8", errors="replace") as fh:
                head = fh.read(4000)
            if project not in head:
                continue
            recs.extend(codex_records(f))
    for r in recs:
        r["dt"] = to_local(r["ts"])
    recs = [r for r in recs if r["dt"]]
    recs.sort(key=lambda r: r["dt"])

    # Deduplicate streamed assistant records by message id (keep max output).
    seen = {}
    prompts = []
    stats = defaultdict(lambda: defaultdict(int))
    for r in recs:
        day = r["dt"].strftime("%Y-%m-%d")
        if r["kind"] == "prompt":
            prompts.append(r)
            stats[day]["prompts_" + r["tool"]] += 1
            stats[day]["prompt_words"] += len(r["text"].split())
        elif r["kind"] == "assistant":
            key = r.get("msgid") or id(r)
            if key in seen:
                seen[key] = max(seen[key], r["out"])
                continue
            seen[key] = r["out"]
            stats[day]["assistant_turns_" + r["tool"]] += 1
            stats[day]["tool_calls"] += r.get("tools", 0)
            stats[day]["claude_out_tokens"] += r["out"]
        elif r["kind"] == "toolcall":
            stats[day]["tool_calls"] += 1
        elif r["kind"] == "tokens":
            stats[day]["codex_out_tokens"] += r["out"]

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "prompts.md"), "w") as fh:
        fh.write(f"# Every prompt in the {project} project\n\n")
        fh.write(f"{len(prompts)} prompts, {sum(len(p['text'].split()) for p in prompts)} words, "
                 f"{prompts[0]['dt'].date()} to {prompts[-1]['dt'].date()}. Times are {tz}. "
                 "Harness-injected text is excluded; slash commands are kept by name.\n")
        day = None
        for p in prompts:
            d = p["dt"].strftime("%Y-%m-%d")
            if d != day:
                fh.write(f"\n## {d}\n")
                day = d
            tag = f"{p['tool']}:{p['session'][:8]}"
            body = "\n> ".join(p["text"].splitlines())
            fh.write(f"\n**{p['dt'].strftime('%H:%M')}** `{tag}`\n\n> {body}\n")
    with open(os.path.join(out_dir, "daily-stats.tsv"), "w") as fh:
        cols = ["prompts_codex", "prompts_claude", "prompt_words", "assistant_turns_codex",
                "assistant_turns_claude", "tool_calls", "claude_out_tokens", "codex_out_tokens"]
        fh.write("day\t" + "\t".join(cols) + "\n")
        for day in sorted(stats):
            fh.write(day + "\t" + "\t".join(str(stats[day][c]) for c in cols) + "\n")
    with open(os.path.join(out_dir, "prompts.jsonl"), "w") as fh:
        for p in prompts:
            fh.write(json.dumps({"ts": p["dt"].isoformat(), "tool": p["tool"], "session": p["session"], "text": p["text"]}) + "\n")
    print(f"{len(prompts)} prompts written to {out_dir}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out_dir", help="directory for prompts.md, prompts.jsonl and daily-stats.tsv")
    ap.add_argument("--project", required=True,
                    help="substring that identifies the project in a log's path or first lines, e.g. the repository directory name")
    ap.add_argument("--claude-glob", action="append", default=None,
                    help="glob for session logs in the first layout (default: ~/.claude/projects/*PROJECT*/*.jsonl)")
    ap.add_argument("--codex-glob", action="append", default=None,
                    help="glob for session logs in the second layout (default: ~/.codex/sessions/*/*/*/*.jsonl, filtered by PROJECT)")
    ap.add_argument("--tz", default=None, help="IANA time zone for the output (default: the machine's)")
    a = ap.parse_args()
    tz = a.tz or (datetime.now().astimezone().tzinfo.key if hasattr(datetime.now().astimezone().tzinfo, "key") else "UTC")
    main(a.out_dir, a.project,
         a.claude_glob or [f"~/.claude/projects/*{a.project}*/*.jsonl"],
         a.codex_glob or ["~/.codex/sessions/*/*/*/*.jsonl"], tz)
