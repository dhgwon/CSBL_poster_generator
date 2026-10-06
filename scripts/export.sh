#!/usr/bin/env bash
# Export a poster .pptx to PDF and (for screen posters) a pixel-exact PNG.
#   export.sh poster.pptx [PX_W PX_H]
# PX_W/PX_H: the submission resolution, e.g. 1080 1920 for a 9:16 DID screen.
set -euo pipefail
PPTX="$1"; DIR="$(cd "$(dirname "$PPTX")" && pwd)"; BASE="$(basename "${PPTX%.pptx}")"
soffice --headless --convert-to pdf --outdir "$DIR" "$PPTX" >/dev/null 2>&1
echo "pdf  -> $DIR/$BASE.pdf"
if [ "$#" -ge 3 ]; then
  PW="$2"; PH="$3"
  pdftoppm -png -r 300 -singlefile "$DIR/$BASE.pdf" "$DIR/.$BASE.tmp"
  python3 - "$DIR/.$BASE.tmp.png" "$DIR/$BASE.png" "$PW" "$PH" <<'PY'
import sys
from PIL import Image
src, dst, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
Image.open(src).convert("RGB").resize((w, h), Image.LANCZOS).save(dst)
PY
  rm -f "$DIR/.$BASE.tmp.png"
  echo "png  -> $DIR/$BASE.png  (${PW}x${PH})"
fi
