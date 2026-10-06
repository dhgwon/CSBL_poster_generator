# Drawing the figures

A poster is read from four metres away and then from forty centimetres. What
carries the first reading is the figures, so most of the work is here. The
guiding rule: **a poster panel is not a paper panel**. Fewer series, bigger
type, the conclusion written on the plot.

## Sizing and alignment

Panels are sized in *poster centimetres* (`figkit.IN`) so that `fontsize=13`
means 13 pt on the finished poster regardless of which panel it is in. Never
let the layout scale a figure up or down to fit — `GRID` honours the width you
give it, and the height follows from the PNG's aspect.

Panels sitting in the same row must have their plot boxes line up, or the row
looks broken even when every panel is individually fine. Three things together
achieve that, and all three are required:

1. the same **plot-box height in inches** (`fk.ax(w_cm, plot_h_in=2.95)`),
2. the same **inch margins** (`fk.MARGIN`, or a `margin=` override passed to
   every panel in the row),
3. `save(fig, name, tight=False)`.

`bbox_inches="tight"` crops each figure by a different amount — that is exactly
what destroys the alignment. Use `tight=True` only for standalone figures.

If two panels in a row show the same quantity on an axis (both counting
molecules, both in the same unit), give them the **same limits and ticks** too.
A reader compares bar lengths across panels whether or not you meant them to.

## Type and line weight

Readable at poster distance, from the house style already in `figkit`:

| element | size |
|---|---|
| panel title `(A) …` | 15 pt bold |
| axis label | 13.5 pt |
| tick label | 11.5–12 pt |
| in-plot annotation / the number you want read | 14–17 pt bold, accent or orange |
| legend | 11.5 pt, inside the axes when there is room |

Lines: axes 1.1, the highlighted series ~3.4 and the rest ~2.4. For chemical
structures or any line drawing, go thicker than feels right on screen —
hairlines disappear in print. Put legends **inside** the plot (`loc="lower
right"`, `framealpha=0.88`) when the data leaves a corner free; that reclaims
the width the legend would have eaten.

Titles centre on the *axes*, not the figure, so a long title over a panel with a
wide left margin gets clipped. Shorten the title rather than widening the panel.

## Panel titles and the sentence under them

Label panels `(A)`, `(B)`, `(C)` and refer to them in the caption paragraph
under the row. The caption's job is to say what the reader should conclude, not
to restate the axes: "improved in 53 of 57 superclasses" beats "Δ similarity by
superclass". Where one number carries the poster, also write it *on* the plot in
orange with an arrow — that is what someone walking past will read.

## Drawing schematics yourself

Most posters need at least one figure that no plotting library produces: the
overall scheme, a method pipeline, a worked example. Draw them with
`figkit.canvas` + `box`/`arrow`/`flow` rather than hunting for an image.

- `fk.flow(boxes, name, w_cm, stages=…)` is the "overall scheme of the study"
  band: a chain of titled boxes with arrows, and optional stage chips above
  them that group the boxes into phases. Vertical with `vertical=True` for a
  narrow column.
- `fk.canvas(w_cm, units_w, units_h)` gives a blank surface in arbitrary units;
  lay out boxes by hand with `fk.box` and join them with `fk.arrow`. Sizing the
  canvas in units and then converting once keeps the aspect honest.
- `fk.embed(fig, path, …)` drops a native screenshot (a data record, an
  existing schematic) into such a canvas with its aspect preserved.

**Size boxes from measured text, not by eye.** The recurring failure in these
figures is text spilling past a hand-drawn box: it renders fine at the size you
tested and clips at the size you ship. Compute the box height from the number of
lines times the line spacing, leave a visible pad, and re-render and *look* at
the PNG after every change.

## Grouping inside the figure

When a figure shows several cases that each have sub-rows (e.g. two molecules,
each compared across two models), do the grouping **inside the figure**: a light
grey `fk.group_box` per case, and tinted blocks (`fk.box(fc=tint, ec="none")`)
per sub-row within it. One tint per model, used consistently, lets the reader
see the structure at a glance. Drawing frames in PowerPoint around separate
pictures instead adds a nesting level that reads as clutter.

## Making honest results look good

Weak-ish results are normal on a conference poster. Present them well without
misrepresenting them:

- **Show the metric that is actually strong.** Top-K accuracy, success rate,
  per-class win counts and paired deltas are all legitimate views of the same
  run. Choosing which to show is editorial; inventing one is not.
- **Compare against the one baseline that matters.** Lining up every model you
  ever trained dilutes the story and invites questions you cannot win. Pick the
  published baseline and compare like-for-like.
- **Paired statistics** on the same evaluation set (Wilcoxon signed-rank, with
  the p-value stated) are both more honest and more persuasive than two bars.
- **Say "improved in 53 of 57 classes"** rather than showing 57 noisy bars with
  no summary.
- Where a comparison is not apples-to-apples, leave it out and tell the user you
  did, with the reason. Never leave an unfair comparison on the poster because
  it flatters.

Every number on the poster must come from a file you actually read. If a figure
needs a distribution or a count, compute it from the real artefact and cache it
to JSON next to the panel code; do not fill it in from memory. A fabricated
number on a poster is an error the user will be asked about in front of a
judge.
