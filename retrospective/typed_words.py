#!/usr/bin/env python3
"""Split each prompt into segments and classify each as typed by the person or pasted.

Segments are blocks separated by blank lines. A segment is pasted when it
shows any strong paste signal (transcript glyphs, paste markers, reference-list
or web-page furniture, email headers, URL-only lines, markdown or org
structure of the kind the models emit, many hard-wrapped lines) or when it is
long and lacks the voice of chat (first and second person, discourse markers,
questions, lowercase openings). A chat-voiced first segment before a paste is
typed (the framing sentence). Dictated messages are typed.

Writes typed-words.tsv (one row per prompt: typed words, pasted words, segments)
and prints totals. Usage: typed_words.py PROMPTS_JSONL [--out typed-words.tsv] [--show]
PROMPTS_JSONL is written by extract_prompts.py.
"""
import json, re, sys, datetime
from pathlib import Path
HERE = Path(__file__).resolve().parent

GLYPH = re.compile(r"[❯⎿●▎│┃▸►⏺]|\[paste\]|\[Pasted text|Pasted text #|^\s*```", re.M)
FURNITURE = re.compile(r"\b(Previous article|Next article|Show Outline|Download Full Issue|Cited by|Google Scholar|PubMed|CrossRef|Share on social media|Open access|Supplementary appendix|Skip to main content|Sign in|Subscribe)\b")
REFLIST = re.compile(r"(\bet al\b.*\d{4}|\bdoi:|10\.\d{4}/|\[\d+(,\s*\d+)*\]|\(\d{4}\)\.?\s|\bvol\.|\bpp?\.\s*\d|;\d+:\w)")
EMAIL = re.compile(r"\b(Dear |Kind regards|Best wishes|Best regards|Sent from my|^From:|^Subject:|^To:|wrote:$|Viele Grüße|Mit freundlichen)", re.M)
MDSTRUCT = re.compile(r"^\s*(#{1,4} |\*\*[A-Z0-9]|\* [A-Z].*:ai:|\|.*\||> |- \*\*|\d+\. \*\*)", re.M)
VOICE = re.compile(r"\b(I|I'm|I’m|I've|I’ve|I'd|I’d|me|my|mine|you|you're|you’re|your|we|we're|we’re|us|our|ok|okay|hmm+|err+|yes|yep|no|nah|sorry|wait|perhaps|maybe|tbh|btw|great|cool|fine|please|thanks|actually|basically|anyway|blurg|bah|wtf|like|just)\b", re.I)

def features(seg):
    lines = [l for l in seg.split("\n") if l.strip()]
    ws = seg.split(); n = len(ws)
    nopunct = sum(1 for l in lines if not re.search(r"[.!?:;,)\"'”’]$", l.strip())) / max(1, len(lines))
    urlonly = sum(1 for l in lines if re.fullmatch(r"\s*\S*https?://\S+\s*", l)) 
    voice = len(VOICE.findall(seg)) / max(1, n) * 100  # voice words per 100 words
    qmarks = seg.count("?")
    return dict(n=n, lines=len(lines), nopunct=nopunct, urlonly=urlonly, voice=voice, q=qmarks,
                glyph=bool(GLYPH.search(seg)), furn=bool(FURNITURE.search(seg)), ref=len(REFLIST.findall(seg)),
                email=bool(EMAIL.search(seg)), md=len(MDSTRUCT.findall(seg)), tabs=seg.count("\t"))

def classify(seg):
    f = features(seg)
    n = f["n"]
    if n == 0: return "typed", f
    reasons = []
    if f["glyph"]: reasons.append("glyph")
    if f["furn"]: reasons.append("furniture")
    if f["email"]: reasons.append("email")
    if f["tabs"] >= 2: reasons.append("tabs")
    if f["ref"] >= 2 or (f["ref"] >= 1 and n > 80): reasons.append("references")
    if f["md"] >= 2 or (f["md"] >= 1 and n > 60 and f["voice"] < 4): reasons.append("markdown")
    if f["urlonly"] >= 1 and f["lines"] > 1 and f["voice"] < 3: reasons.append("url-lines")
    if f["lines"] >= 6 and f["nopunct"] >= 0.5: reasons.append("hard-wrapped")
    if n >= 120 and f["voice"] < 2.5 and f["q"] == 0: reasons.append("long-no-voice")
    if n >= 300 and f["voice"] < 5 and f["q"] <= 1: reasons.append("very-long-low-voice")
    items = re.findall(r"(?m)^\s*(?:\d+[.)]|[-*•])\s+\S", seg)
    if len(items) >= 3 and f["voice"] < 3 and n >= 60: reasons.append("llm-list")
    return ("pasted", reasons) if reasons else ("typed", reasons)

QUOTE = re.compile(r"[\"“]([^\"“”]{60,}?)[\"”]")

def quoted_words(seg):
    """Words inside double quotes, in runs of 15 words or more: text the person is citing rather than writing."""
    return sum(len(m.split()) for m in QUOTE.findall(seg) if len(m.split()) >= 15)

def split_prompt(text):
    # separate a short chat-voiced opening line from a paste that follows on the next line
    segs = [s for s in re.split(r"\n\s*\n", text) if s.strip()]
    out = []
    for s in segs:
        lines = s.split("\n")
        if len(lines) > 2:
            first, rest = lines[0], "\n".join(lines[1:])
            fw = len(first.split())
            if 0 < fw <= 60 and classify(rest)[0] == "pasted" and classify(first)[0] == "typed":
                out.append(first); out.append(rest); continue
        out.append(s)
    return out

def load(path):
    for line in open(path):
        r = json.loads(line); yield r["ts"][:16], r["text"]

def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompts"); ap.add_argument("--out", default="typed-words.tsv"); ap.add_argument("--show", action="store_true")
    a = ap.parse_args(); name = a.prompts; show = a.show
    tot = {"typed": 0, "pasted": 0, "quoted": 0, "duplicate": 0}; reasons = {}; rows = []; samples = []
    RELAY = re.compile(r"(another llm|other llm|the other tool|here'?s a review|review by|do you agree with this|this assessment|the other (tool|model|agent|llm) (says|thinks|wrote)|^for info|another reviewer|a reviewer (says|writes|thinks)|feedback from)", re.I)
    relay = {"prompts": 0, "words_after_intro": 0, "pasted_after_intro": 0}
    seen = set()
    for ts, text in load(name):
        ty = pa = 0; segn = 0
        key = re.sub(r"\s+", " ", text.strip().lower())
        if key in seen:
            tot["duplicate"] += len(text.split()); rows.append((ts, 0, 0, 0)); continue
        seen.add(key)
        is_relay = bool(RELAY.search(text[:300]))
        segs = split_prompt(text)
        first = [classify(s) for s in segs]
        pasted_words = sum(len(s.split()) for s, (c, _) in zip(segs, first) if c == "pasted")
        heavy = pasted_words >= 200 or sum(1 for c, _ in first if c == "pasted") >= 3
        seen_paste = False
        for seg, (cls, why) in zip(segs, first):
            n = len(seg.split()); segn += 1
            if cls == "pasted": seen_paste = True
            elif heavy and seen_paste:
                f = features(seg)
                if not (n < 80 and f["voice"] >= 4):
                    cls, why = "pasted", ["inside-paste"]
            if is_relay and segn > 1:
                relay["words_after_intro"] += n
                if cls == "pasted": relay["pasted_after_intro"] += n
                elif not (n < 40 and features(seg)["voice"] >= 6):
                    cls, why = "pasted", ["relayed"]
            if cls == "typed":
                q = quoted_words(seg); ty += n - q; pa += q; tot["quoted"] += q
            else:
                pa += n
                for w in why: reasons[w] = reasons.get(w, 0) + n
            if show and cls == "typed" and n >= 120:
                samples.append((ts, cls, n, ",".join(why), seg.strip().replace("\n", " / ")[:140]))
        tot["typed"] += ty; tot["pasted"] += pa
        if is_relay: relay["prompts"] += 1
        rows.append((ts, ty, pa, segn))
    with open(a.out, "w") as f:
        f.write("ts\ttyped_words\tpasted_words\tsegments\n")
        for r in rows: f.write("\t".join(str(x) for x in r) + "\n")
    print("prompts", len(rows), "typed", tot["typed"], "pasted", tot["pasted"], "(of which quoted inside typed segments", tot["quoted"], ") duplicates", tot["duplicate"])
    print("prompts whose opening names a relay or review:", relay["prompts"], "; of", relay["words_after_intro"], "words after the opening,", relay["pasted_after_intro"], "were caught by the other rules and the rest counted as relayed")
    print("pasted words by reason (a segment may count under several):", dict(sorted(reasons.items(), key=lambda x: -x[1])))
    if show:
        for s in samples: print(*s, sep=" | ")

if __name__ == "__main__":
    main()
