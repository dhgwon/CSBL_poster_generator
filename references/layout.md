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

### What "minimum 11 pt" actually means

This trips people up, so settle it before you argue with yourself about it.
`Poster` builds on a **cm-true canvas** — the slide is the real poster — so a
point on the slide is a physical point on the finished poster. A 15 pt body on
a 57.4 cm canvas really is 15 pt on the DID panel, and the venue's "11 pt or
larger" is satisfied directly. The type scale already lands above that at
every canvas size; you only need to re-check if you shrink a figure's fonts by
hand.

What you must **not** do is build a screen poster on a nominal 13.33 × 7.5 in
slide and then reason about "11 pt at 96 dpi". That number is not the physical
size of anything, and it makes every later comparison meaningless.

Separately, for a screen poster it is worth knowing how tall the text lands in
the delivered PNG:

```
px = pt / 72 * px_width / (canvas_cm / 2.54)
```

A 574 mm panel showing 1080 px is only ~48 ppi, so 15 pt comes out around 10 px.
That is correct and legible on the panel itself, but it will look soft when
someone previews the PNG on a laptop. Say so when you hand the file over rather
than inflating the type to fix a problem the screen does not have.

Other rules that come from the venues:
- Screens often show only a **safe area** smaller than the panel (e.g. 500 × 700
  mm of a 574 × 1020 mm screen). Keep the margin at 1.6 cm and no text closer
  than that to any edge.
- For print, the PDF is the deliverable; make sure every embedded PNG is at
  least ~150 dpi at its placed size (`savefig.dpi 400` on a 17 cm panel is fine).

## The layout engine

`scripts/poster_lib.py`. `Poster.compose(bands)` gives each full-width band its
natural measured height and hands all remaining vertical space to the single
`("MID", …)` region, so the poster fills the page exactly without hand-tuning.
Inside a column, leftover height is distributed into the gaps that precede each
section bar — sections breathe, figures never stretch.

`MID` takes **as many column block-lists as you give it**:

```python
("MID", left, right)            # two columns — a tall portrait poster
("MID", left, middle, right)    # three — what a landscape canvas needs
```

Pick the count from the canvas, not from habit. On a 102 cm-wide landscape
poster a two-column body gives ~50 cm lines, which nobody reads; three columns
bring that to ~32 cm, about right. A tall portrait poster is the opposite — three
columns there leave each one too narrow for a figure with an axis label.

Blocks: `BAR` (section bar), `PIC` (one figure), `GRID` (a row of figures at
explicit cm widths), `SPLIT` (one figure left, a stack right), `TXT`, `HEAD`.

Read the console table it prints:

```
  [mid-L       ] content   25.2 cm | avail   25.6 cm | slack    0.4 cm
  [mid-R       ] content   25.3 cm | avail   25.6 cm | slack    0.3 cm
```

`*** OVERFLOW ***` means that column has more content than space. Fix it by
making a figure shorter (reduce its `plot_h_in`), trimming a caption, or moving
a block to another column — **never** by shrinking the margins or the type.

`<- under-filled` is the opposite and is just as worth fixing: the engine will
spread the slack into the gaps, but a column padded out with air reads as a
column you ran out of things to say about. Act on it — raise the panels'
`plot_h_in`, widen the `GRID` widths so the row spans the column, promote one
figure to full width, or add the caption sentence you were going to leave out.
Rebuild and check the table again; two or three passes to get every band near
zero slack is normal and is most of what makes the result look deliberate.

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
