#!/usr/bin/env bash
# A fast structured look at a research directory, to ground the poster interview.
#   survey.sh [DIR]
DIR="${1:-.}"; cd "$DIR"
echo "=== $PWD"
echo; echo "--- top level (by size) ---"
du -sh -- */ 2>/dev/null | sort -hr | head -25
echo; echo "--- notes / docs ---"
find . -maxdepth 3 \( -iname '*.md' -o -iname '*.txt' -o -iname '*.pdf' -o -iname '*.docx' \) \
  -not -path '*/.*' -printf '%TY-%Tm-%Td  %10s  %p\n' 2>/dev/null | sort -r | head -30
echo; echo "--- results / tables / figures ---"
find . -maxdepth 4 \( -iname '*.csv' -o -iname '*.tsv' -o -iname '*.json' -o -iname '*.png' -o -iname '*.svg' \) \
  -not -path '*/.*' -not -path '*/node_modules/*' -printf '%TY-%Tm-%Td  %10s  %p\n' 2>/dev/null \
  | sort -r | head -40
echo; echo "--- entry points / configs ---"
find . -maxdepth 3 \( -iname 'run*.py' -o -iname 'main.py' -o -iname 'train*.py' -o -iname '*.yaml' -o -iname 'config*.json' -o -iname 'Makefile' \) \
  -not -path '*/.*' 2>/dev/null | head -25
echo; echo "--- most recently touched files ---"
find . -type f -not -path '*/.*' -printf '%TY-%Tm-%Td %TH:%TM  %p\n' 2>/dev/null | sort -r | head -20
echo; echo "--- git ---"
git log --oneline -15 2>/dev/null || echo "(not a git repo)"
