# Pi / WSL Setup

## Goal

Set up the lightweight packaging skill in a Linux environment without PowerShell.

This reference is aimed at:
- Raspberry Pi OS
- Ubuntu under WSL2
- other Debian-like environments with `python3`

## KCC Source Install

If `kcc-c2e` is not already installed, a reliable Linux path is:

```bash
git clone --depth 1 https://github.com/ciromattia/kcc.git /tmp/kcc-src
cd /tmp/kcc-src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
```

After that, verify:

```bash
source /tmp/kcc-src/venv/bin/activate
kcc-c2e --help
```

## Use the Skill Scripts

From the project root:

### Package only

```bash
python3 apps/manga-pipeline-lite/postprocess/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub \
  --kcc-cmd /tmp/kcc-src/venv/bin/kcc-c2e
```

### Package plus merge

```bash
python3 apps/manga-pipeline-lite/postprocess/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub \
  --kcc-cmd /tmp/kcc-src/venv/bin/kcc-c2e \
  --merge-output /data/manga/merged/series.epub \
  --title "Series Title" \
  --author "Unknown"
```

## Verified Result

Verified in WSL Ubuntu on `2026-03-18` with:
- KCC installed from source in a Python virtual environment
- `apps/manga-pipeline-lite/postprocess/manga_packager.py` creating chapter EPUBs
- `apps/manga-pipeline-lite/postprocess/make_merge_plan.py` generating a plan JSON
- `apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py` generating a merged anthology EPUB

## Notes

- If you rerun packaging into the same output directory, KCC may create suffixed filenames unless you pass `--skip-existing`.
- The skill stays intentionally lightweight:
  - no GUI
  - no AI upscaling
  - no PowerShell runtime dependency
