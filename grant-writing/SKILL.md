---
name: grant-writing
description: >
  Write a research proposal or grant application with the applicant, from the
  first conversation to submission: set-up, aim and register, architecture,
  sentence skeleton, paragraph-by-paragraph expansion, review rounds,
  supporting documents, freeze. Use when a new application starts, when a
  draft is revised, or when a review comes back. Derrington's framework is
  applied as a checklist (derrington-checklist.md), never as a template.
---

# Writing a grant proposal with an applicant

A complete, plausible draft of a proposal arrives in an hour, and polishing a misshapen one always feels productive. The applicant's judgement is the scarce input. This skill spends it on the smallest unit the applicant can approve in a line, and builds the document from the applicant's own words upward. Where the skill comes from is at the end.

Rules marked **untested** have not been tried in a measured project. The project's instruction file lists which of them the application is testing, and the `retrospective` skill, run after submission, keeps, revises or drops them from the evidence.

Terms used throughout. The *working document* is the proposal source, one sentence per line, paragraphs labelled P01, P02 and so on. The *architecture file* holds the scheme's criteria, the page budget, the register decision and the standing decisions. The *notes file* holds alternatives and provenance by paragraph label. The *applicant file* is the applicant's private record of facts, constraints, preferences and writing rules (`applicant-template.md` gives its headings). The *checker* is a script that applies the applicant's writing rules and the checklist's style rules to a file. The *reference pipeline* is the route a citation takes: bibliography entry, full text fetched and converted, the claim checked against the text, the supporting passage recorded in an evidence note. A *fresh-context reviewer* is a model run that has seen nothing of the writing sessions. The *summary* is whatever the scheme calls the short account at the front, whether abstract, summary or précis.

## Principles

1. **The applicant supplies the claim and the frame.** The model supplies components, structure, checks and joins. It offers options as a menu with provenance and never proposes the organising frame.
2. **Framework before prose, with approval at every level.** Page budget, sections, statement of the case, one sentence per paragraph with its join, then paragraphs. Nothing is expanded until the level above is approved.
3. **One working document, one architecture file, one notes file.** Superseded material goes to `archive/`, which is never read as current or mined for facts.
4. **Show, then apply.** The paragraph with the change marked, old and new, before the file changes. One approved change per commit, one sentence per line. Approval of a plan is not approval to apply its stages.
5. **No citation without the full text** and a recorded check of the claim against it.
6. **The checker runs on every edit**, however small.
7. **Reviews are fresh-context, filed and adjudicated against the architecture.** Two reviewers agreeing on a defect is the signal; agreement on keeping the text is weaker. A batch of review fixes is checked for narrowing before it is applied.
8. **Calibrate against what won.** The applicant's funded proposals set the register and funded precedents for the scheme set the house style. When a framework or a reviewer disagrees with a measured precedent, follow the precedent and say which is which.
9. **A habit the applicant repeats is a method.** When the applicant does something by hand a second time, offer the command or the file that does it for them. Never advise them to stop.
10. **Frameworks are tests, never templates.** Derrington's questions, the paragraph targets and the checker say what a finished text must contain and pass. None says how to write it. The applicant chooses the shape and the framework is run on the result. A model given a framework as a construction method writes mechanically and in the framework's voice. This rule binds the model; an applicant who wants to write ten sentences first may.

## The procedure

Each step ends with a gate: a condition the applicant confirms in words. Silence never opens a gate, the model never opens one itself, and the model never declares the document ready.

### Step 0. Set up, before any writing

- Repository: the working document, the architecture file, the notes file, `references.bib` and `references/` (the pipeline's PDFs, converted text and evidence notes), `exports/` (generated, ignored by git), `sources/` (scheme documents, precedents, past proposals and their reviews, returned reviews, committed on receipt), `archive/`.
- Write the project's instruction file (`AGENTS.md`, or whichever file the agent reads first) from `project-instructions.md` in this skill.
- Read the scheme documents into the first section of the architecture file: selection criteria in the funder's words; who reads; page and format limits; required sections and attachments and what each is for.
- Measure precedents: two or three funded proposals for the scheme, the applicant's own funded proposals with their reviews, the last rejection with its reviews. Record length, structure, novelty vocabulary and where the track record sits. These measurements are what principle 8 means by a measured precedent.
- Install, before writing, the tools the project will need. The applicant supplies or approves each: a render command that strips scaffolding, resolves citations and reports the page count; the reference pipeline; the checker, loaded with the applicant's rules and the checklist's style rules; the review-record template (`review-record.md`); the prompts log extractor from the `retrospective` skill, run from day one so that the logs survive.
- Read the applicant file. For an applicant without one, derive a first set of writing rules from their funded proposals and their first ten corrections, and add a rule at every later correction (**untested**).
- Start the external dependencies now: costing, host and institutional letters, portal registration, consent from anyone to be named. The administrative thread gets its own file and runs in parallel to the end; expect it to take a tenth to a fifth of all prompts.
- Schedule two conversations with the host or a trusted reader: on register, before Step 2; on the work plan, before Step 6.

Gate: the applicant confirms the scheme section of the architecture file and the applicant file, and the render, the pipeline and the checker each run once.

### Step 1. The aim and the register, in the applicant's words

Design the work first and fit the question to it. Refining the question first has no natural end.

- The applicant talks or writes freely, by dictation if easier: what they want to know, what they will not do, what they bring, why here and now.
- The model keeps an inventory of components with provenance: what the applicant has said in this project, in past proposals, talks and calls; what the field needs that this applicant could do. It presents the inventory as a menu, never as a draft (**untested** as a replacement for the exploratory drafts that produced the same selection in the measured projects). It extracts candidate aims from the applicant's words only. If every candidate is refused it stops generating and asks what the applicant genuinely does not know and has wondered about.
- Four tests for any proposed piece of work: does it answer something nobody knows; would the answer change what someone does; can only this applicant do it; is the instrument specified and repeatable. Material that happens to be in reach is evidence about the field, never a source of experiments. One example the applicant mentions is one example, never the frame.
- At the end of every exploratory session the applicant writes the state in their own words. Scheduling this removes the bad draft that otherwise provokes it.
- Decide the register (a project with testable aims, or a profile-led programme) and the route to the scheme's novelty criterion. Record both in the architecture file so that no later reviewer reopens them.

Gate: the register, the novelty route and the applicant's own statement of the substance are written in the architecture file and confirmed; a first aim sentence exists in the applicant's words; and the applicant confirms on a later day that they still agree with it. The aim sentence will keep moving; when it does, the propagation rule in Step 4 applies. No paragraph prose before Step 2's gate.

### Step 2. Architecture, budget, statement of the case

- Sections in the funder's order, a page allocation each, a fixed working layout so that length is measurable from day one. Aims or strands with a word allowance each.
- The applicant writes the statement of the case in their own shape. The model runs section 1 of `derrington-checklist.md` on it and reports what is missing, never a sentence order or a template.
- Tag phrases: one wording per concept, copied, never paraphrased. The model's default is variation. The architecture file lists the tag phrases, and the glossary pass (Step 5) checks the text against the list.
- Hostage check: no strand may depend on a particular result of another; fallbacks go in the architecture.
- Standing decisions start here, in the architecture file: scope; which named things are examples and which commitments; promises the applicant refuses to make; the applicant's personal constraints in approved wording; facts about other people that are not the applicant's to state. Every later "should we" is answered from this file or added to it in the same turn.
- The model asserts nothing about the applicant from memory; the applicant file is the only source.

Gate: the applicant confirms the architecture, the budget and the statement of the case.

### Step 3. The sentence skeleton

- One labelled sentence per paragraph, each followed by the sentence that joins it to the one before. Read whole, the skeleton is the argument. If it does not persuade at this length it will not persuade at twenty times the length.
- Review it as a document. A fresh-context reviewer answers the skeleton form of the five-minute test (`derrington-checklist.md`, section 6) and reports failures only; then the applicant reads it. Fix the argument here, where a change costs one line.
- Run checklist section 2 (structure) on the skeleton.
- Record per paragraph the evidence it will need, so that the reference pipeline runs during Step 4.

Gate: the fresh-context review and the structure check have run and the applicant confirms every skeleton sentence.

### Step 4. Expansion

- One paragraph at a time, in order. Draft to the allowance, run the checker, show the paragraph in context with the skeleton visible, wait. The applicant answers in a line. One commit, then the next paragraph.
- Examples flagged as examples. No site, study, collaborator or number the applicant has not approved; propose specifics in chat first.
- An aside the applicant labels as one ("aside", "just out of interest") gets a one-paragraph answer and no change to the document.
- Every reported change names the file and the paragraphs the applicant needs to read.
- Every citation through the pipeline before it appears.
- An insertion or a cut is never approved on its own. Show the whole paragraph with the change marked, the last sentence of the paragraph before and the first of the one after, and state what each pronoun and demonstrative in the new text refers to. The sentence proposed for removal may be the join.
- A sentence the applicant has corrected twice gets two or three options, or the question "is this sentence needed?", never a fourth variant.
- Any change touching more than one paragraph (a reframing, a batch of review fixes, a new aim sentence) is first a numbered plan in the architecture file, approved, then executed one step per commit with completion recorded.
- When the aim sentence or a standing decision changes, the plan lists every place that repeats it (summary, section openers, tables, supporting documents) and all change in the same batch.
- Parallel sessions are specialised by file, never two on the same file. Alternatives and provenance go in the notes file, keyed by label.
- Render daily. Report the page count when it crosses the budget or when the applicant asks.

Gate: the applicant has confirmed every paragraph, the render is within the page budget, and the checker and a seam pass (Step 5) have run on the whole.

### Step 5. Review, in rounds

The briefs are in `reviewer-brief.md`, with the rules for filing and adjudicating reviews. Reviewers see the render, the architecture file, the writing-rules section of the applicant file and one brief, and they never edit. The applicant reads the filed record.

- **The applicant's read on paper**, at least twice in the project. The marks come back as an annotated PDF or photographs, committed before extraction, then extracted into a record (`review-record.md`) and applied stage by stage, each stage shown and confirmed separately.
- **Structured adversarial review** with the standing briefs: specialist, panel generalist, sceptic.
- **One vendor or two.** Fresh context is the main effect and one vendor supplies it. A second vendor adds error independence; use it for a few high-stakes reads, the claims audit and the final assessment, never as a second writer.
- **The whole-document assessment** whenever the applicant asks and at the end of every session (**untested** as a scheduled step). The answer is the ranked list in the brief, never odds.
- **The applicant's mock review**, in the voice of the least sympathetic likely reader.
- **A fresh-context review of each day's diff**.
- **The narrowing check before any batch of review fixes is applied.** Each request for precision pulls a programme towards a project.
- **The seam pass, after every round of insertions and before the next review.** Fresh-context reviewer first, with that brief alone, then the applicant's read for the breaks of flow a model passes over. Insertions and seam passes alternate; neither is skipped because the other was done.
- **Passes, run as revision and never as drafting constraints.** Each is a brief: arc; referents in the paragraphs changed since the last pass (the writer supplies the list); proportion; the promises audit; the claims audit; the glossary pass against the tag-phrase list; the checker; checklist sections 4 and 5, style and paragraph targets (the targets **untested**). Sentences that say a result will matter without saying what it will change are cut. When the model's explanation of a passage in chat is clearer than the passage, it proposes the explanation as the replacement, shown in context like any other change.
- **One outside human reader** at the applicant's level in a neighbouring field, half an hour, with the five-minute test (**untested**).

Gate: the applicant has read the latest render whole and says in words that there is nothing more to change.

### Step 6. Supporting documents

- The architecture file says what each document is for, so that nothing is said twice. Draft each from the confirmed proposal in the voice of its signatories; statements others sign must be self-contained.
- The summary is written from the confirmed proposal and checked with checklist section 3: the summary, the first page, a skim and the whole give the same picture, and no single result, number or study appears in the summary or in a signed statement.
- CV, publication list and key publications from one source, generated.
- Figures from a written brief, once the text they illustrate has stopped moving, with editable sources under version control.

Gate: the applicant confirms each supporting document, and the summary has passed checklist section 3.

### Step 7. Length and typography

Cut to length from the strands, never from the framing the reviews praised. Run checklist section 1 again on the cut text. Typography last.

Gate: the render is within every limit and the applicant confirms the cut text.

### Step 8. Freeze and record

A build command rebuilds every upload from source, reports page counts and sizes against the limits and runs the checker. Compare the submitted text with the working copy and record any difference. Within a week, run the `retrospective` skill.

Gate: the submission is in and the retrospective has been run.

## Early warnings that the procedure has been left

- A second full draft exists before the aim is agreed.
- More than one planning document, or the model asking which file holds the current decision.
- The model has proposed an organising frame.
- The model is writing to a framework's template.
- The applicant is reviewing a long document in a word processor.
- A page count reported every turn.
- Two tools editing the same files.
- The same decision argued for the third time.
- The whole-document assessment returning the same top item three times: the fix being applied is local and the problem is structural.
- A sentence rewritten five times before anyone asked whether it is needed.
- Sentences inserted from a review and committed without anyone re-reading the paragraph whole.
- Figures commissioned while the text they illustrate is still moving.

## What the applicant does themselves

States the aim in their own words and restates it whenever the model drifts. Decides the register and the novelty route and records them. Writes the state at the end of each exploratory session. Reviews on paper, on the whole, at least twice, and writes one mock review. Writes the hardest paragraphs when stuck and lets the model take them nearly verbatim. Supplies the facts the model cannot know. Turns each correction into a checker rule.

## Time

A guess, for a four-to-five-page case with a dossier and a project already designed in the applicant's head: Step 0 half a day; Step 1 one to two days; Step 2 half a day; Step 3 one to two days; Step 4 four to six days; Step 5 three days over two or three rounds; Step 6 two days; Steps 7 and 8 one day.

## Where this comes from

Two applications written in 2026 with coding agents, a five-year project grant and a fellowship nomination with a dossier, reconstructed from their session logs and git histories with the `retrospective` skill. Both failed the same way first: about thirty working hours over eleven or twelve active days on complete drafts the applicant judged wrong, each recovered on the day the work moved to one confirmed sentence at a time. The whole projects took 70 and 120 working hours over 30 and 59 calendar days. No model-generated frame survived in either. The administrative thread took a tenth of one project's prompts and a fifth of the other's. The two host conversations each settled in a day what the sessions had circled for a week. The applicant's end-of-session statements were the turning points of both projects. One project needed about forty corrections of facts about the applicant. The paragraph loop in Step 4 ran at one to fifteen minutes per paragraph on the good days. A second vendor's independent contribution showed in claim checking and one argument, never in framing. The seam pass ran only when the applicant asked for it and found something every time. The readiness condition in Step 1's gate, the five-minute test and the checklist are Parker Derrington's. Three habits the first retrospective called wasteful (relaying reviews between tools, asking "what are my chances?", putting one question to two readers) were all steering, which is where principle 9 comes from.

## Files in this skill

- `derrington-checklist.md`: Derrington's statement of the case, structure, summary consistency, style, paragraph targets and five-minute test, as tests run at Steps 2, 3, 5, 6 and 7.
- `reviewer-brief.md`: the standing briefs for fresh-context reviewers, the pass briefs, the whole-document assessment, the narrowing check and the mock review, with the filing and adjudication rules.
- `review-record.md`: the template for extracting a handwritten review.
- `project-instructions.md`: the template for the project's instruction file.
- `applicant-template.md`: the headings for the applicant file. The filled file is private, one per applicant, kept outside this repository at the path the project's instruction file names.
- `referees.md`: responding to referees and to rejection.
