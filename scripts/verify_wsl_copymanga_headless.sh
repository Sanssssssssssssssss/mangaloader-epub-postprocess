#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP="$ROOT_DIR/apps/copymanga-headless-lite/copymanga_downloader.py"
TMP_DIR="${TMPDIR:-/tmp}/copymanga-headless-lite-test"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

python3 "$APP" search haizeiwang --limit 1 --json >"$TMP_DIR/search.json"
python3 "$APP" comic haizeiwang --json >"$TMP_DIR/comic.json"
python3 "$APP" chapters haizeiwang --group default --json >"$TMP_DIR/chapters.json"
python3 "$APP" download-chapter haizeiwang \
  --chapter-uuid 4bd05882-c7bc-11e8-881a-024352452ce0 \
  --output-root "$TMP_DIR/downloads" \
  --max-images 2

find "$TMP_DIR/downloads" -type f | sort >"$TMP_DIR/files.txt"
test -s "$TMP_DIR/search.json"
test -s "$TMP_DIR/comic.json"
test -s "$TMP_DIR/chapters.json"
test "$(wc -l < "$TMP_DIR/files.txt")" -ge 2

echo "WSL verification passed"
echo "Artifacts: $TMP_DIR"
