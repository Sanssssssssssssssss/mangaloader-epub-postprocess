#!/usr/bin/env bash
set -euo pipefail

TESTROOT=/tmp/piclaw-manga-test
WORKROOT=/mnt/d/GPT_Project/Piclaw
KCC_ROOT=/tmp/kcc-src
KCC_VENV="$KCC_ROOT/venv"

rm -rf "$TESTROOT"
mkdir -p "$TESTROOT/chapters/001" "$TESTROOT/chapters/002" "$TESTROOT/out" "$TESTROOT/merged"

source "$KCC_VENV/bin/activate"

python - <<'PY'
from PIL import Image, ImageDraw
from pathlib import Path

root = Path("/tmp/piclaw-manga-test/chapters")
for chapter in ("001", "002"):
    for index in range(1, 3):
        img = Image.new("RGB", (240, 320), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((20, 20), f"chapter {chapter} page {index}", fill=(0, 0, 0))
        img.save(root / chapter / f"{index:03d}.png")
PY

cd "$WORKROOT"

python3 skills/manga-epub-packager-lite/scripts/manga_packager.py \
  --input-root "$TESTROOT/chapters" \
  --output-root "$TESTROOT/out" \
  --kcc-cmd "$KCC_VENV/bin/kcc-c2e"

python3 skills/manga-epub-packager-lite/scripts/manga_packager.py \
  --input-root "$TESTROOT/chapters" \
  --output-root "$TESTROOT/out" \
  --kcc-cmd "$KCC_VENV/bin/kcc-c2e" \
  --skip-existing \
  --merge-output "$TESTROOT/merged/series.epub" \
  --title "Piclaw Test Series" \
  --author "Piclaw"

find "$TESTROOT" -maxdepth 2 -type f | sort
