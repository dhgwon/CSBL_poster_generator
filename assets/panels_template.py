# -*- coding: utf-8 -*-
"""One function per figure panel.  Each writes a single PNG into ../figs.

    ~/miniconda3/bin/python3 panels.py            # all panels
    ~/miniconda3/bin/python3 panels.py p_results  # just one, while iterating
"""
import os, sys
SKILL = os.path.expanduser("~/.claude/skills/CSBL_poster_generator")
sys.path.insert(0, f"{SKILL}/scripts")
import numpy as np
import figkit as fk
from figkit import BLUE, NAVY, ORANGE, GREY, TEAL, GREEN, IN, save

ROOT = os.path.dirname(os.path.abspath(__file__)) + "/.."
fk.OUT = f"{ROOT}/figs"

# Poster geometry — keep in step with build_poster.py so a 13 pt label is 13 pt
# on the printed poster.
COL_CM, FULL_CM = 26.50, 54.20          # one column / both columns
CELL3 = (COL_CM - 1.0) / 3

# Panels that sit in the same row must share these, and save with tight=False.
ROW_W, ROW_PLOT_H = 17.7, 2.95


def p_scheme():
    """Overall scheme of the study — the full-width band under the abstract."""
    fk.flow(
        [("Data", ["source A  n = …", "source B  n = …"]),
         ("Method", ["step one", "step two"]),
         ("Model", ["architecture", "training setting"]),
         ("Evaluation", ["benchmark", "metric"])],
        "fig1_scheme", w_cm=FULL_CM,
        stages=[(0, "1. Data"), (2, "2. Model"), (3, "3. Evaluation")])


def p_results_a():
    fig, ax = fk.ax(ROW_W, plot_h_in=ROW_PLOT_H)
    v = [60.0, 75.0, 90.0]
    ax.bar(np.arange(3), v, 0.62, color=[GREY, TEAL, BLUE])
    fk.bar_labels(ax, np.arange(3), v, best=2)
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(["Baseline", "Ours", "Ours+"], fontsize=11.5)
    ax.set_ylabel("…"); ax.set_ylim(0, 118)
    ax.set_title("(A) …")
    save(fig, "fig4a", tight=False)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("p_")]
    if len(sys.argv) > 1:
        fns = [globals()[n] for n in sys.argv[1:]]
    for f in fns:
        f()
