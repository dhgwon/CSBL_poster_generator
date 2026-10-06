# -*- coding: utf-8 -*-
"""Build the poster.  Run with a python that has python-pptx + Pillow.

    ~/miniconda3/bin/python3 build_poster.py
"""
import os, sys
SKILL = os.path.expanduser("~/.claude/skills/CSBL_poster_generator")
sys.path.insert(0, f"{SKILL}/scripts")
from poster_lib import Poster, BAR, PIC, TXT, HEAD, GRID, SPLIT
from pptx.util import Pt

ROOT    = os.path.dirname(os.path.abspath(__file__)) + "/.."
FIGS    = f"{ROOT}/figs"
VERSION = "v1"
OUT     = f"{ROOT}/POSTER_{VERSION}.pptx"

# --- canvas: ask the user, never assume ------------------------------------
# print A0 portrait 90 x 120 cm   |   DID 9:16 screen 57.4 x 102.0 cm
W_CM, H_CM = 57.4, 102.0

P = Poster(w_cm=W_CM, h_cm=H_CM, figs=FIGS)
P.header(
    title=["Title line one",
           "title line two"],
    authors="First Author¹ and Corresponding Author¹˒²*",
    affils=["¹Department of …, Soongsil University, Seoul 06978, Republic of Korea",
            "²School of …, Soongsil University, Seoul 06978, Republic of Korea",
            "*Corresponding author: Name (email@ssu.ac.kr)"],
    logo=f"{SKILL}/assets/ssu_logo.png",
)

ABSTRACT = ("…")

P.compose([
    ("F", [BAR("Abstract"), TXT(ABSTRACT)], "abstract"),
    ("F", [BAR("Overall scheme of the study"), PIC("fig1_scheme")], "scheme"),
    ("MID",
     [BAR("Left section"),
      PIC("fig2_left"),
      GRID(["fig2a", "fig2b"], [12.8, 12.8], gap_cm=0.5),
      TXT("What the left column shows, with the real numbers.")],
     [BAR("Right section"),
      PIC("fig3_right", frac=0.85),
      GRID(["fig3a", "fig3b"], [13.4, 12.6], gap_cm=0.5),
      TXT("What the right column shows.")]),
    ("F", [BAR("Results"),
           GRID(["fig4a", "fig4b", "fig4c"], [17.7, 17.7, 17.7], gap_cm=0.55),
           TXT("One paragraph reading the three panels together.")], "results"),
    ("F", [BAR("Conclusions"),
           TXT("First claim, with its number.",
               "Second claim.",
               "Third claim.", bullets=True, space_after=Pt(4)),
           HEAD("Acknowledgements", sec=False),
           TXT("Funding sentence.   References   1. …   2. …", size=Pt(12))], "end"),
])
P.save(OUT)
