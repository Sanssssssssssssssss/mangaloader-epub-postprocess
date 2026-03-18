# Smoke Test

## Package Only

Prepare:
- one input directory with at least two chapter folders
- KCC installed as `kcc-c2e` or `comic2ebook`

Run:

```bash
python3 ./apps/manga-pipeline-lite/postprocess/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub \
  --dry-run
```

Expect:
- one `RUN:` line per chapter directory
- no PowerShell usage

## Package Plus Merge

Run:

```bash
python3 ./apps/manga-pipeline-lite/postprocess/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub \
  --merge-output /data/manga/merged/series.epub \
  --title "Series Title" \
  --author "Unknown" \
  --dry-run
```

Expect:
- packaging commands
- one merge-plan generation command
- one merge command

## Merge Only

Run:

```bash
python3 ./apps/manga-pipeline-lite/postprocess/make_merge_plan.py \
  --epub-dir /data/manga/epub \
  --output /data/manga/merged/series.epub \
  --title "Series Title" \
  --plan /data/manga/merged/merge-plan.json

python3 ./apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py --plan /data/manga/merged/merge-plan.json
```

Expect:
- plan JSON created
- merged EPUB created if all inputs are valid
