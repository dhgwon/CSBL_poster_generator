---
name: CSBL_poster_generator
description: Build a conference research poster in the CSBL / Soongsil University house format as an editable .pptx plus PDF/PNG, from whatever a research project directory already contains. Use this whenever the user asks for a poster, 포스터, 학회 포스터, conference poster, DID/screen poster, or wants to turn a project, paper, abstract or set of results into a poster — and also when they ask to revise, resize, re-export or make a new version of a poster built this way. The skill surveys the project directory, proposes a section flow for the user to approve, draws the figures (including hand-drawn schematics), and manages _vN versions.
---

# CSBL poster generator

A research poster is one slide that has to survive being read from four metres
and then interrogated from forty centimetres. This skill builds that slide in
the lab's house format: a measured PowerPoint layout engine, matplotlib panels
sized in poster centimetres, and a PDF/PNG export.

The user is usually standing in their research directory with results scattered
across scripts, CSVs and notebooks, and no clear idea of the poster's shape.
Your job is to find the story in what is there, propose it, and then build it.
Do not ask them to hand you a structure — work one out and let them correct it.

## 1. Survey before you ask anything

Start by looking at the project, so your questions are informed rather than
generic:

```bash
~/.claude/skills/CSBL_poster_generator/scripts/survey.sh [project dir]
```

Then read what matters: any abstract, README, paper draft or notes (these
usually contain the intended narrative already), the results tables, the
existing figures, and the scripts that produced them. If an abstract exists,
the poster must agree with it — it is what the user already committed to.

Note what you can actually back with data, and what has no evidence behind it.
That distinction drives everything downstream.

## 2. Ask the two things you cannot infer

**The canvas size, always.** This is never assumable: it decides the ratio,
the column count and the type scale. Ask which venue and which format — printed
board (commonly 90 × 120 cm portrait), or a DID/screen poster (commonly 9:16 at
57.4 × 102.0 cm, submitted as 1080 × 1920 px). Ask for the conference's own
guideline text if they have it; venues specify safe areas and minimum font
sizes that change the layout. See `references/layout.md` for the table.

**The flow, as a recommendation they can accept or edit.** Offer 2–3 concrete
section outlines derived from the survey, each as an ordered list of section
titles, saying what evidence you found for each and which figure would carry
it. Make a recommendation rather than a menu of equals — the user knows their
work far better than the outline, so they correct fastest when given something
specific to react to.

A flow that works for most method/model papers, as a starting point:

> Abstract → Overall scheme of the study → *(two columns: data & method | what
> you built)* → Results → Conclusions + Acknowledgements

Use `AskUserQuestion` for both of these together. Also confirm the title,
author list, affiliations and funding line if you cannot find them in the
abstract. Once the flow is agreed, build the whole thing before coming back —
do not check in section by section.

## 3. Build

Work in `<project>/poster/`, with `_work/` for code and `figs/` for panels.
Copy the two templates as a starting point:

```bash
mkdir -p <project>/poster/{_work,figs}
cp ~/.claude/skills/CSBL_poster_generator/assets/panels_template.py <project>/poster/_work/panels.py
cp ~/.claude/skills/CSBL_poster_generator/assets/build_template.py  <project>/poster/_work/build_poster.py
```

`scripts/figkit.py` draws the panels, `scripts/poster_lib.py` lays out the
slide. Both are documented in their own docstrings; read
`references/figures.md` before writing the first panel and
`references/layout.md` before the first build.

Order of work:

1. **Figures first, one function per panel** in `panels.py`, each writing one
   PNG. Keeping them separate means the user can ask to change one panel
   without a full rebuild, and each stays an independent object in PowerPoint.
2. **Draw the schematics yourself.** Almost every poster needs an "overall
   scheme of the study" and often a worked example; `fk.flow` and
   `fk.canvas`/`fk.box`/`fk.arrow` exist for this. A figure you draw to fit the
   argument beats a screenshot of something adjacent to it.
3. **Build and read the console table.** `poster_lib` prints content vs
   available height for every band. `*** OVERFLOW ***` must be fixed before
   export.
4. **Export, then actually look at it.** `scripts/export.sh poster_v1.pptx
   [1080 1920]`. Render the PDF to PNG and open it. Measured heights can all be
   correct while a hand-drawn box inside a figure clips its own text — only
   looking catches that.

Run the build with a Python that has python-pptx; on this machine that is
`~/miniconda3/bin/python3`, not the project venv.

## 4. Numbers, and making the work look good

Everything on the poster must trace to a file you read. Compute counts,
distributions and statistics from the real artefacts and cache them to JSON
beside the panel code; never fill a plausible-looking number in from memory.
The user will be standing next to this poster answering questions about it.

Within that constraint, present the work at its best — that is a legitimate
part of the job, not a compromise. Choose the view of the results that is
genuinely strongest (top-K rather than mean, success rate, per-class win
counts, paired statistics), compare against the one baseline that matters
instead of every model ever trained, and write the single most important number
on the plot in orange. Where a comparison would be unfair in the user's favour,
leave it off and tell them you did and why. `references/figures.md` goes into
detail.

If the results genuinely do not support a claim the user wants to make, say so
plainly and offer the strongest honest framing instead.

## 5. Revise in versions

Posters get many rounds of changes. Bump `VERSION` in `build_poster.py` for
each round — `POSTER_v1` → `_v2` → `_v3` — and export both .pptx and .pdf (plus
.png for screen posters) each time. Never overwrite a version the user has
already seen; they compare against it and sometimes want it back.

When the user asks for a change, change that thing and rebuild the whole
poster. Keep a one-line note of what each version changed so the history is
readable.

## Reference files

- `references/layout.md` — the house format, canvas sizes and venue rules, how
  `compose` distributes space, filling the column width, export, versioning.
- `references/figures.md` — panel sizing and the three-part alignment rule,
  type and line weights, drawing schematics, grouping inside a figure, and how
  to present honest results well.
