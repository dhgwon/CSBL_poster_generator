# The CSBL (Soongsil) poster format

## What the format is

A single PowerPoint slide sized to the real poster, built as:

```
┌──────────────────────────────────────────────┐
│  blue rounded header: logo · title · authors │
│  · affiliations (+ optional QR on the right) │
├──────────────────────────────────────────────┤
│ ███ Abstract ███  (full-width blue bar)      │
│ justified paragraph                          │
│ ███ Overall scheme of the study ███          │
│ one wide schematic                           │
├───────────────────────┬──────────────────────┤
│ ███ Section ███       │ ███ Section ███      │   ← the elastic middle
│ figures + caption     │ figures + caption    │
├───────────────────────┴──────────────────────┤
│ ███ Results ███   row of aligned panels      │
│ ███ Conclusions ███  bullets + acknowledge.  │
└──────────────────────────────────────────────┘
```

Fixed house traits, worth keeping because they are what makes it recognisable:

- **Accent blue `#016694`** for every section bar, box border and emphasis;
  `#1E3664` navy for arrows and outlines, `#E07B39` orange for the one number
  you want read first. White text on the bars.
- **Section bars span the full width of their column.** No boxes around
  sections, no drop shadows.
- **Arial on the slide, Liberation Sans in the figures** — metrically the same,
  so measured text heights match what PowerPoint renders.
- Every figure is a **separate picture object**, so the user can nudge one
  without re-exporting the rest.
- Reading order is top-to-bottom through the full-width bands, with the two
  middle columns read left then right. Nothing important is below the fold of
  the lower third, because that part is at knee height on a printed poster.

## Canvas sizes — always ask

The ratio decides the whole layout, so it is the one thing never to assume.
Common cases:

| Where | Size | Export |
|---|---|---|
| Printed poster board (KSBB, most domestic conferences) | 90 × 120 cm portrait | PDF at 300 dpi |
| A0 portrait | 84.1 × 118.9 cm | PDF |
| DID / screen poster, 9:16 | 57.4 × 102.0 cm | PDF **and** PNG at 1080 × 1920 px |
| DID / screen poster, 16:9 | 102.0 × 57.4 cm (landscape: use 3 columns) | PNG 1920 × 1080 |

Rules that come from the venues:
- **Screen posters: nothing below 11 pt.** `Poster` scales its type with the
  canvas width, so a 57.4 cm canvas lands at body 15 pt / bar 19 pt — already
  safe. If you shrink a figure's fonts by hand, re-check them.
- Screens often show only a **safe area** smaller than the panel (e.g. 500 × 700
  mm of a 574 × 1020 mm screen). Keep the margin at 1.6 cm and no text closer
  than that to any edge.
- For print, the PDF is the deliverable; make sure every embedded PNG is at
  least ~150 dpi at its placed size (`savefig.dpi 400` on a 17 cm panel is fine).

## The layout engine

`scripts/poster_lib.py`. `Poster.compose(bands)` gives each full-width band its
natural measured height and hands all remaining vertical space to the single
`("MID", left, right)` region, so the poster fills the page exactly without
hand-tuning. Inside a column, leftover height is distributed into the gaps that
precede each section bar — sections breathe, figures never stretch.

Blocks: `BAR` (section bar), `PIC` (one figure), `GRID` (a row of figures at
explicit cm widths), `SPLIT` (one figure left, a stack right), `TXT`, `HEAD`.

Read the console table it prints:

```
  [mid-L       ] content   25.2 cm | avail   25.6 cm | slack    0.4 cm
  [mid-R       ] content   25.3 cm | avail   25.6 cm | slack    0.3 cm
```

`*** OVERFLOW ***` means that column has more content than space. Fix it by
making a figure shorter (reduce its `plot_h_in`), trimming a caption, or moving
a block to the other column — **never** by shrinking the margins or the type.

## Filling the width

A row of figures should span its column. `GRID` centres whatever you give it,
so pick widths that add up: for a 26.5 cm column with a 0.5 cm gap, three
panels are 8.4 cm each; two are 13.4 + 12.6 when one needs more room. For the
full 54.2 cm width, three panels at 17.7 cm with 0.55 cm gaps fill it exactly.
Leaving a column half-empty is the most common way these posters look amateur.

## Versioning

Posters get revised a lot. Keep every build: `POSTER_v1.pptx/pdf`, then `_v2`,
`_v3` … Set `VERSION` at the top of `build_poster.py` and bump it for each
round of changes, so the user can compare and roll back. Never overwrite a
version the user has already seen.

## Export

```bash
~/.claude/skills/CSBL_poster_generator/scripts/export.sh POSTER_v3.pptx 1080 1920
```

LibreOffice renders the PDF; the PNG is resampled from a 300 dpi render to the
exact submission pixel size. Omit the pixel arguments for print posters.

Always open the rendered PDF/PNG and look at it before reporting done —
measured heights can be right while a figure's own internal text overflows its
hand-drawn box, and that only shows up visually.

## Dependencies

`python-pptx` and `Pillow` are needed for the build, `matplotlib` for the
figures. On this machine `~/miniconda3/bin/python3` has python-pptx; a project
venv usually does not. Check before writing a long script:

```bash
~/miniconda3/bin/python3 -c "import pptx, PIL, matplotlib; print('ok')"
```
