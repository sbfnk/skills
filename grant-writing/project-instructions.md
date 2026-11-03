# Template for the project's instruction file

`AGENTS.md`, or whichever file the agent reads first. Written at Step 0 and kept current. Every session reads it. It holds only what every session needs: the current step, the decisions that must not be reopened, and where everything else is. Replace the angle-bracket fields; delete nothing else without the applicant's approval.

```markdown
# <Scheme> application: <short title>

Follow the `grant-writing` skill. The current step is **<0 to 8>**. Nothing below the current
step's gate is drafted; see the skill for the gates.

## The one working document

`proposal.md`, one sentence per line, paragraphs labelled P01, P02, … `architecture.md`
holds the scheme criteria, the page budget, the register decision and the standing
decisions; `notes.md` holds alternatives and provenance by label. `archive/` is never read
as current.

## Register and novelty route

<Decided at Step 1, in the applicant's words, with the date. Until then: "undecided; no
paragraph prose".>

## Standing decisions

See `architecture.md`, section "Standing decisions". The ones every session needs:

- <Scope, in one sentence.>
- <Which named things are examples and which commitments.>
- <Promises the applicant refuses to make.>
- <Personal constraints, in the approved wording.>
- <Facts about other people that are not the applicant's to state.>

## The applicant

Facts, constraints and writing rules are in `<path to applicant.md>`. Assert nothing about
the applicant from memory. Run `<checker command>` on every edit. Write in the language
variant the applicant file names. Show
every change as the paragraph with the change marked, old and new, before the file changes.

## Review records

Returned reviews go into `sources/reviews/` and are committed on receipt. Reviews by
fresh-context agents use the briefs in the skill; the writer's adjudication sits next to
each review.

## Bets this application tests

The skill marks some rules **untested**. This application tests:

- <e.g. the component menu at Step 1 in place of exploratory drafts>
- <e.g. the whole-document assessment at the end of every session>

The `retrospective` skill will look for the evidence on each.

## Tools

- Render: `<command>` writes `exports/…` and reports the page count.
- References: `<commands>`; no citation without the full text and an evidence note.
- Prompts log: `<command>` (from the `retrospective` skill), run daily.
```
