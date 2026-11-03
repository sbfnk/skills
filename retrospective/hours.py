#!/usr/bin/env python3
"""Working time from prompt timestamps.

A session is a run of prompts with gaps of at most GAP minutes (default 20);
its duration is last prompt minus first prompt plus a TAIL (default 5 minutes)
for reading the final answer, so an isolated prompt counts as five minutes.
A 10-minute break to do something else stays inside a session; a lunch break,
a day or a week does not. Calendar days and active days (five or more prompts)
are reported alongside, because calendar time is when ideas stew and is
reported apart from work. The 45-minute figure is an upper bound.

Usage: hours.py PROMPTS_JSONL [--phases FILE] [--gap 20] [--tail 5] [--out hours-by-phase.tsv]
PROMPTS_JSONL is written by extract_prompts.py. The phases file has one phase
per line, tab-separated: name, first day, last day (ISO dates); without it one
phase spans the whole corpus.
"""
import argparse, collections, datetime, json


def read_times(path):
    out = []
    for line in open(path):
        r = json.loads(line)
        out.append(datetime.datetime.fromisoformat(r["ts"]))
    return sorted(out)


def read_phases(path, ts):
    if not path:
        return [("total", ts[0].date().isoformat(), ts[-1].date().isoformat())]
    out = []
    for line in open(path):
        if not line.strip() or line.startswith("#"):
            continue
        name, d0, d1 = line.rstrip("\n").split("\t")[:3]
        out.append((name, d0, d1))
    return out


def sessions(ts, gap):
    ts = sorted(ts)
    if not ts:
        return []
    out, start, n = [], ts[0], 1
    for i in range(1, len(ts) + 1):
        if i == len(ts) or (ts[i] - ts[i - 1]).total_seconds() > gap * 60:
            out.append((start, ts[i - 1], n))
            if i < len(ts):
                start, n = ts[i], 0
        n += 1
    return out


def hours(ts, gap, tail):
    return sum(((e - s).total_seconds() / 60 + tail) / 60 for s, e, n in sessions(ts, gap))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prompts")
    ap.add_argument("--phases", default=None)
    ap.add_argument("--gap", type=float, default=20)
    ap.add_argument("--tail", type=float, default=5)
    ap.add_argument("--out", default="hours-by-phase.tsv")
    a = ap.parse_args()
    all_ts = read_times(a.prompts)
    rows = []
    for name, d0, d1 in read_phases(a.phases, all_ts):
        ts = [t for t in all_ts if d0 <= t.date().isoformat() <= d1]
        days = collections.Counter(t.date() for t in ts)
        cal = (datetime.date.fromisoformat(d1) - datetime.date.fromisoformat(d0)).days + 1
        ses = sessions(ts, a.gap)
        rows.append((name, len(ts), cal, len(days), sum(1 for v in days.values() if v >= 5), len(ses),
                     sum(1 for s in ses if s[2] == 1), round(hours(ts, a.gap, a.tail), 1), round(hours(ts, 45, a.tail), 1)))
    hdr = ("phase", "prompts", "calendar_days", "days_with_prompts", "active_days_5plus", f"sessions_{a.gap:g}min",
           "isolated_prompts", f"hours_{a.gap:g}min_sessions", "hours_45min_sessions")
    with open(a.out, "w") as f:
        f.write("\t".join(hdr) + "\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    w = [max(len(str(x)) for x in col) for col in zip(hdr, *rows)]
    for r in [hdr] + rows:
        print("  ".join(str(x).ljust(w[i]) for i, x in enumerate(r)))


if __name__ == "__main__":
    main()
