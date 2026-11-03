---
name: retrospective
description: >
  Reconstruct how a piece of work was made with a coding agent from the
  agent's session logs and the git history: working time by phase, words typed
  against words pasted, what was tried and discarded, what the person stopped
  iterating on, which corrections repeated, and what the skill that governed
  the work should change. Use after any project done this way (a grant, a
  paper, a report, a package), within a week of finishing, or when a false
  start needs understanding mid-project.
---

# Retrospective of a project written with an agent

The logs hold every prompt the person typed with its time; the repository holds every change with its time. Together they show what the person decided, what the model proposed, what survived and what it cost. The output is a set of measured documents and a proposed change to the governing skill. Nothing in it is a claim without a prompt or a commit behind it.

## What it produces

In `retrospective/` inside the project. The prompt corpus is private and ignored by git; the measures and documents are committed with the project.

- `corpus/prompts.jsonl` and `corpus/prompts.md`: every prompt, in order, with tool and time (from `extract_prompts.py`).
- `corpus/prompts-typed.md`: the same with each pasted segment cut to its first 40 words. This is the digest, the version to read.
- `corpus/daily-stats.tsv`: prompts, words and model turns per day (from `extract_prompts.py`).
- `corpus/hours-by-phase.tsv`: working time per phase (from `hours.py`).
- `corpus/typed-words.tsv`: typed against pasted words per prompt (from `typed_words.py`).
- Git measures, from `git log` and `git blame`: commits and lines changed per day, lines of the final document by the day they were last changed, and files deleted. There is no script for these; the commands are in the procedure below.
- `timeline.md`: phases, the frames tried, the notable days, the measures.
- `what-worked.md`: the moments the person stopped iterating and the practices that preceded them.
- `what-was-wasted.md`: dead ends, their process cause and what each cost.
- `examples.md`: verbatim prompts showing what the person's steering looked like.
- `reviews/`: a fresh-context review of the retrospective and the adjudication of each finding.
- A proposed diff to the governing skill, with each change marked by its evidence.

## Measurement rules

- **Working time.** A session is a run of prompts no more than 20 minutes apart, timed from first to last prompt plus five minutes. A turn to other work of about ten minutes stays inside a session. A single prompt after a long gap counts as five minutes, the time it takes to register an idea. Pauses of an hour, a day or a week are excluded. Report the figure for 45-minute gaps as well, as an upper bound, since the two differ most where the person was working in short bursts.
- **Days.** Calendar span, days with any prompt, and active days (five or more prompts) are three different numbers; report all three. Ideas stew between sessions. The calendar span matters for that reason and is reported apart from effort.
- **Words.** Only words the person typed count as theirs. A segment is pasted if its formatting says so: characters that only a terminal transcript contains, web-page or reference-list furniture, email headers, URL-only lines, markdown or outline structure of the kind models emit, six or more hard-wrapped lines, a numbered list of full sentences without the first and second person and discourse markers of chat, a long passage with no first or second person and no question, anything after the first paste in a paste-heavy prompt, anything after an opening that announces a relay ("here is a review by another model"), runs of fifteen or more words inside quotation marks, and a prompt sent twice. Validate on the prompts that announce a relay: if the other rules catch fewer than four words in five of what follows the announcement, add rules before using the count.
- **Survival.** Lines in the final document by the day they were last changed, from blame; and lines written per day against lines surviving.
- **Phases.** Cut at the resets the person named in their prompts and at changes of tool or method, never at round dates. Give each phase its own row of every measure. Keep the phase definitions and the scripts stable between projects, so that two projects measured the same way can be compared.

## Procedure

1. **Extract the corpus.** Run `extract_prompts.py` with the project's path filter and, if the logs are not in the default locations, the log globs. Agents purge their logs on a schedule. In anything governed by the `grant-writing` skill this runs from the project's first day, and on a finished project it runs immediately, while the logs still exist. Copy logs from other machines before they go.
2. **Measure.** `hours.py` with a phases file, `typed_words.py`, and the git measures:

   ```sh
   git log --format='%ad %h' --date=short --shortstat
   git blame --date=short FINAL_DOCUMENT | cut -d' ' -f2 | sort | uniq -c
   git log --diff-filter=D --name-only --format='%ad' --date=short
   ```

   Print the phase table before reading anything, so that the reading is checked against the numbers.
3. **Read the digest whole**, in order, once. Mark: every organising frame proposed and by whom; every message in which the person stated the substance in their own words; every reset; every correction, and whether it repeats an earlier one; every aside the model built into the text; every "which file, which paragraph"; every request for a pass over the whole (arc, seams, referents); every request for an overall verdict and what the person did with the answer.
4. **Write the four documents** from the marks, with verbatim quotes and dates. A finding without a quote or a commit is removed. Where the person's judgement differed from the model's or a reviewer's, say what the person decided and when, never who was right.
5. **Audit the governing skill.** For every rule the skill marks **untested**, find the evidence in this project: followed and worked, followed and failed, not followed, or no occasion. Promote, revise or drop, and write the reason. For every rule the skill states, list the prompts in which the person had to restate it anyway. Those are the rules the skill is failing to make cheap.
6. **Fresh-context review.** Give the documents and the digest to a model that has seen none of the sessions, with two briefs: an adversarial read of the retrospective's claims against the corpus, and an independent taxonomy of the person's recurring requests built without sight of the skill. Adjudicate every finding in a file next to the review.
7. **Propose the diff** to the governing skill: rules added, rules revised, untested marks resolved, early warnings added. Each change names its evidence. The person applies it to the skill; the retrospective never edits the skill, and the project's measures stay with the project.
8. **Report** the phase table, the comparison with any earlier project measured the same way, and the diff.

## Rules for writing it

- Name the person's habits as method, never as waste, until the record shows a habit cost something and produced nothing.
- Mark every statement by source: measured in this project, learned in an earlier one, taken from a published framework, untested, or the person's instruction with its date.
- Never write that something happened "the same day" or "in one message" without the timestamps in front of you.
- The retrospective is itself text the person will read; run their writing rules on it.

## Scripts

All four live next to this file and take their inputs as arguments; run `--help` on each.

- `extract_prompts.py OUT_DIR --project NAME`: the corpus, the digest and the daily statistics from the session logs. It reads the two log layouts its parsers know, in their default locations, and takes `--claude-glob` and `--codex-glob` for others, `--tz` for the time zone.
- `extract_turns.py LOG --from T --to T --out FILE`: a readable transcript (prompts, model text, tool-call names) for one log and time window.
- `hours.py PROMPTS_JSONL --phases FILE`: sessions, active days and hours per phase. The phases file has one phase per line: name, first day, last day, tab-separated. Without it, one phase spans the whole corpus.
- `typed_words.py PROMPTS_JSONL`: typed against pasted words per prompt, with the reasons.

## Where this comes from

The rules and the scripts were made in the retrospective of two applications written in 2026. Its first draft summed 45-minute gaps and double-counted the hours, called three of the person's steering habits wasteful, and got calendar claims wrong in both directions, which is where the measurement rules and the rules for writing come from.
