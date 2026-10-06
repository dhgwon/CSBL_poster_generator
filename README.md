# CSBL_poster_generator

A [Claude Code](https://claude.com/claude-code) skill that builds a conference
research poster in the CSBL / Soongsil University house format, as an editable
`.pptx` plus PDF and a pixel-exact PNG, starting from whatever a research
project directory already contains.

It surveys the project, proposes a section flow for the author to approve,
draws the figures — including schematics it composes itself — lays the slide
out with a measuring engine, and keeps `_vN` versions across revisions.

## Install

```bash
git clone https://github.com/<you>/CSBL_poster_generator.git \
  ~/.claude/skills/CSBL_poster_generator
```

Claude Code picks the skill up on the next session. Ask for a poster
("이 프로젝트로 학회 포스터 만들어줘") and it triggers.

## What's in here

| path | what it is |
|---|---|
| `SKILL.md` | the workflow: survey → ask canvas size & flow → build → version |
| `scripts/poster_lib.py` | layout engine — measured blocks on a cm canvas, elastic middle region |
| `scripts/figkit.py` | figure kit — poster-cm sizing, row alignment, flow/box/arrow schematics |
| `scripts/survey.sh` | structured look at a research directory |
| `scripts/export.sh` | pptx → PDF → PNG at a submission resolution |
| `references/layout.md` | the house format, canvas sizes, venue rules, versioning |
| `references/figures.md` | panel sizing and alignment, type scale, honest presentation |
| `assets/` | starter `panels.py` / `build_poster.py`, university logo |

## Requirements

`python-pptx`, `Pillow`, `matplotlib`, and LibreOffice (`soffice`) plus
`pdftoppm` for the export.

## Canvas sizes

The canvas is the one thing the skill never assumes — it asks, because the
ratio decides the column count and the type scale. Printed boards are commonly
90 × 120 cm portrait; DID screen posters are commonly 9:16 at 57.4 × 102.0 cm
submitted as 1080 × 1920 px.
