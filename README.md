# skills

Agent skills, one directory each, a `SKILL.md` with its name and description in each. Any agent that reads the skill format can load them.

| Skill | What it does |
|---|---|
| `grant-writing/` | Write a research proposal with the applicant, from set-up to submission: aim and register in the applicant's words, architecture, sentence skeleton, one paragraph at a time, review in rounds, supporting documents, freeze. Parker Derrington's framework is applied as a checklist, never as a template. |
| `retrospective/` | Reconstruct how a project was made from the tool logs and the git history: working time by phase, typed against pasted words, what was tried and discarded, what the person stopped iterating on, and what the governing skill should change. Scripts included. |

## Install

Clone the repository and link each skill directory into the directory your agent reads skills from:

```sh
git clone https://github.com/sbfnk/skills ~/code/skills
ln -s ~/code/skills/grant-writing ~/code/skills/retrospective <your agent's skills directory>/
```

`grant-writing` expects a private applicant file outside this repository; `grant-writing/applicant-template.md` gives its headings, and the project's instruction file names its path.

## Provenance

Written from two applications made in 2026 and the retrospective of their session logs. Rules those projects did not test are marked **untested** in the skill; the `retrospective` skill resolves them after each use.
