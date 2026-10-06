# -*- coding: utf-8 -*-
"""Figure helpers for CSBL posters.

One PNG per panel, each sized in *poster centimetres* so that a given fontsize
renders at the same physical size everywhere on the poster.  Import this from a
project-local `panels.py`, set OUT, and write one `p_*()` function per panel.

    import figkit as fk
    fk.OUT = "…/figs"
    fig, ax = fk.ax(w_cm=17.7, h_cm=6.0)
    ax.bar(…)
    fk.save(fig, "fig3a_success", tight=False)
"""
import os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# House palette.  accent = the same blue as the poster's section bars.
BLUE, NAVY, ORANGE = "#016694", "#1E3664", "#E07B39"
GREY, LGREY, TEAL, GREEN = "#A9B4BE", "#D7DEE4", "#3FA9B8", "#7CB342"
SERIES = [BLUE, ORANGE, TEAL, GREEN, NAVY, GREY]

plt.rcParams.update({
    "font.family": "Liberation Sans", "font.size": 13,
    "axes.labelsize": 13.5, "axes.titlesize": 15, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 1.1, "xtick.labelsize": 12, "ytick.labelsize": 12,
    "legend.frameon": False, "figure.dpi": 200, "savefig.dpi": 400,
})

OUT = "figs"                      # set this from your panels.py
IN = lambda cm: cm / 2.54         # poster cm -> figure inches, 1:1 font scale

# Inch margins shared by every panel that has to line up with its neighbours.
# Equal figure height + equal margins + save(tight=False) is what makes the
# plot boxes of adjacent panels start and end on the same pixel row.
MARGIN = dict(left=0.98, right=0.15, bottom=0.70, top=0.50)


def ax(w_cm, h_cm=None, plot_h_in=3.0, margin=None):
    """A panel axes `w_cm` wide, with fixed inch margins.

    Give `h_cm` for a standalone panel, or leave it out and give `plot_h_in`
    (the height of the plot box itself) for a set of panels that must align:
    pass the same `plot_h_in` and `margin` to each and their axes will match.
    """
    m = dict(MARGIN, **(margin or {}))
    W = IN(w_cm)
    H = IN(h_cm) if h_cm else m["bottom"] + plot_h_in + m["top"]
    fig, a = plt.subplots(figsize=(W, H))
    fig.subplots_adjust(left=m["left"] / W, right=1 - m["right"] / W,
                        bottom=m["bottom"] / H, top=1 - m["top"] / H)
    return fig, a


def canvas(w_cm, units_w=200.0, units_h=25.0):
    """A blank drawing surface in arbitrary units — for hand-drawn schematics.
    Returns (fig, ax) with x in [0, units_w], y in [0, units_h], no axes."""
    W = IN(w_cm); H = W * units_h / units_w
    fig = plt.figure(figsize=(W, H))
    a = fig.add_axes([0, 0, 1, 1])
    a.set_xlim(0, units_w); a.set_ylim(0, units_h); a.axis("off")
    return fig, a


def save(fig, name, tight=True):
    """tight=False keeps the exact inch margins, which is what lets panels align.
    Use tight=True only for standalone figures that nothing has to line up with."""
    os.makedirs(OUT, exist_ok=True)
    kw = dict(bbox_inches="tight", pad_inches=0.10) if tight else {}
    fig.savefig(f"{OUT}/{name}.png", facecolor="white", **kw)
    plt.close(fig); print("wrote", name)


# ------------------------------------------------------------------ schematics
def flow(boxes, name, w_cm, stages=None, box_w=29.0, gap=5.2, box_h=20.0,
         title_pt=15, body_pt=11.5, vertical=False, accent=BLUE):
    """The "overall scheme of the study" band: a chain of titled boxes joined by
    arrows, optionally with stage chips above them.

    boxes  : [(title, [line, line, …]), …]   '\\n' in a title makes it two lines
    stages : [(box_index, "1. Data"), …]     chips drawn above those boxes
    """
    n = len(boxes)
    if vertical:
        units_w = box_w + 2.0
        units_h = n * box_h + (n - 1) * gap + (3.0 if stages else 1.0)
    else:
        units_w = n * box_w + (n - 1) * gap
        units_h = box_h + (4.0 if stages else 1.6)
    fig, a = canvas(w_cm, units_w, units_h)
    by = 0.8

    pos = []
    for i, (title, lines) in enumerate(boxes):
        if vertical:
            x, y = 1.0, units_h - (3.0 if stages else 1.0) - (i + 1) * box_h - i * gap
        else:
            x, y = i * (box_w + gap), by
        pos.append((x, y))
        a.add_patch(FancyBboxPatch((x, y), box_w, box_h,
                                   boxstyle="round,pad=0.0,rounding_size=1.4",
                                   fc="white", ec=accent, lw=2.2, zorder=2))
        nt = title.count("\n") + 1
        a.text(x + box_w / 2, y + box_h - 1.6, title, ha="center", va="top",
               fontsize=title_pt, fontweight="bold", color=accent,
               linespacing=1.25, zorder=3)
        a.text(x + box_w / 2, y + box_h - 3.4 - 2.5 * nt, "\n".join(lines),
               ha="center", va="top", fontsize=body_pt, color="#333333",
               linespacing=1.42, zorder=3)

    for i in range(n - 1):
        x, y = pos[i]
        if vertical:
            arrow(a, (x + box_w / 2, y - 0.6), (x + box_w / 2, y - gap + 0.6))
        else:
            arrow(a, (x + box_w + 0.6, y + box_h / 2),
                  (x + box_w + gap - 0.6, y + box_h / 2))

    for i, lab in (stages or []):
        a.text(pos[i][0] + box_w / 2, units_h - 0.6, lab, ha="center", va="top",
               fontsize=12.5, fontweight="bold", color="white",
               bbox=dict(boxstyle="round,pad=0.38", fc=accent, ec="none"), zorder=5)
    save(fig, name)


def arrow(a, xy0, xy1, color=NAVY, lw=2.4, scale=20, label=None, label_pt=11):
    a.add_patch(FancyArrowPatch(xy0, xy1, arrowstyle="-|>", mutation_scale=scale,
                                lw=lw, color=color, zorder=4))
    if label:
        a.text((xy0[0] + xy1[0]) / 2, (xy0[1] + xy1[1]) / 2 + 1.0, label,
               ha="center", va="bottom", fontsize=label_pt, color=color, zorder=5)


def box(a, x, y, w, h, title=None, lines=None, ec=BLUE, fc="white", lw=2.0,
        title_pt=15, body_pt=11.5, align="left", zorder=2):
    """A rounded info box. Returns nothing; draw text yourself for fine control."""
    a.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=1.1",
                               fc=fc, ec=ec, lw=lw, zorder=zorder))
    cx = x + (w / 2 if align == "center" else 2.2)
    ha = "center" if align == "center" else "left"
    yy = y + h - 2.2
    if title:
        a.text(cx, yy, title, ha=ha, va="top", fontsize=title_pt,
               fontweight="bold", color=ec, zorder=zorder + 1)
        yy -= 1.9 * (title.count("\n") + 1) + 1.2
    if lines:
        a.text(cx, yy, "\n".join(lines), ha=ha, va="top", fontsize=body_pt,
               color="#333333", linespacing=1.42, zorder=zorder + 1)


def embed(fig, path, x_frac, y_frac, w_frac):
    """Drop a native screenshot/diagram PNG into a `canvas` figure, preserving
    its aspect. Fractions are of the figure, measured from bottom-left."""
    img = mpimg.imread(path)
    ih, iw = img.shape[:2]
    fw, fh = fig.get_size_inches()
    h_frac = w_frac * (fw / fh) * ih / iw
    a = fig.add_axes([x_frac, y_frac, w_frac, h_frac])
    a.imshow(img); a.axis("off")
    return a


def group_box(a, x, y, w, h, label=None, ec="#9FB0BC", fc="white", lw=1.6,
              label_pt=13, zorder=1):
    """A light grey grouping frame — use it inside a figure to show that several
    sub-rows belong to the same case, with tinted `box(fc=…, ec='none')` blocks
    nested inside for the sub-grouping. Grouping inside the figure reads far
    better than drawing frames in PowerPoint around separate pictures."""
    a.add_patch(FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.0,rounding_size=1.4",
                               fc=fc, ec=ec, lw=lw, zorder=zorder))
    if label:
        a.text(x + 1.2, y + h - 1.2, label, ha="left", va="top", fontsize=label_pt,
               fontweight="bold", color="#45566A", zorder=zorder + 1)


def bar_labels(a, xs, vs, fmt="{:.1f}", dy=1.5, pt=14, best=None, color="#444"):
    """Value labels over bars; `best` = index to emphasise in the accent colour."""
    for i, (x, v) in enumerate(zip(xs, vs)):
        a.text(x, v + dy, fmt.format(v), ha="center", va="bottom", fontsize=pt,
               fontweight="bold" if i == best else "normal",
               color=BLUE if i == best else color)
