# Record of a handwritten review: template

Use when the applicant returns an annotated PDF, photographs of a printout or a marked render. Commit the original to `sources/reviews/` before anything is extracted. Fill the record, show it to the applicant, then apply it stage by stage, each stage shown and approved separately.

```markdown
# <Applicant>'s handwritten review of <document>: changes and interpretation

Review supplied on <date> as `<path>`; the original is preserved unchanged. SHA-256: `<hash>`.
The marked render is <n> pages at commit `<hash>`; locations below refer to the regenerated
render at commit `<hash>`. The revision starts from commit `<hash>`.

## Decisions the review changes

<Any change to the aim, the register, the standing decisions or the order of sections,
stated in one paragraph each, before the item table. These go into architecture.md in
the same commit as this record.>

## Completeness

<How every mark was accounted for: pages with ink, pages without, how clusters of ink were
counted and matched to items, which marks remain ambiguous. If native annotations exist,
their count. The reader must be able to see that nothing was missed.>

| Page | Marks | Items |
|---|---:|---|
| 1 | | A1 to A… |

## Page 1

| Item | Marked wording or instruction | Judgement | Action and current location |
|---|---|---|---|
| A1 | <the applicant's words, verbatim where legible> | accepted / pushed back: <reason> / needs the applicant | <what changed, or the proposed text in context>. **P00 (p. 1).** |

<One section per marked page.>

## Stages

1. <Items applied first, usually the decisions and the structural moves.> Commit `<hash>`.
2. <Wording items by section.> Commit `<hash>`.
3. <Items that needed the applicant's answer, with the answer.> Commit `<hash>`.

## Left open

<Items the applicant has not yet ruled on, with the question.>
```

Rules:

- Every mark gets an item, including ticks, question marks and brackets with no words. An ambiguous mark is recorded as ambiguous with the reading adopted.
- Push-backs are recorded, never silently dropped: the applicant's instruction, the reason for not following it, the applicant's ruling.
- Each item names the paragraph label and the page in the current render.
- The proposed text for an item is shown in its paragraph, with the sentences on either side, before the file changes.
- A stage is a commit. Approval of the record is not approval of the stages.
