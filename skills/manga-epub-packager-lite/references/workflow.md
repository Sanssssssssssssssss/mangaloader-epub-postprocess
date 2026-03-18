# Lightweight Workflow

## Scope

Use this workflow only for lightweight packaging:
- no GUI
- no AI upscaling
- no Windows-only assumptions

## Input Shapes

### Package only

Use when the input is chapter folders of images:

```text
<chapters-root>/
  001/
    001.jpg
    002.jpg
  002/
    001.jpg
    002.jpg
```

### Merge only

Use when the input is already chapter EPUBs:

```text
<epub-root>/
  001.epub
  002.epub
  003.epub
```

### Optional order file

Use a plain text file with one chapter stem per line when lexical order is not enough:

```text
001
002
003
```

## KCC Detection

Probe the command instead of assuming one name:

```bash
kcc-c2e --help
comic2ebook --help
```

Prefer whichever exists. If neither exists, stop and ask for KCC installation.

## Primary Entry Point

Prefer the bundled Linux-native wrapper:

```bash
python3 ./scripts/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub
```

For package plus merge:

```bash
python3 ./scripts/manga_packager.py \
  --input-root /data/manga/chapters \
  --output-root /data/manga/epub \
  --merge-output /data/manga/merged/series.epub \
  --title "Series Title" \
  --author "Unknown"
```

This wrapper:
- detects `kcc-c2e` or `comic2ebook`
- packages chapter folders in natural-sort order
- can generate the merge plan and call the merge script

## Low-Level Packaging Pattern

These flags follow the lightweight behavior inferred from the imported baseline:
- `-f EPUB`
- `--nokepub`
- `-n`
- `--forcecolor`

If you need manual control, use a loop like this in bash:

```bash
KCC="kcc-c2e"
INPUT_ROOT="/data/manga/chapters"
OUTPUT_ROOT="/data/manga/epub"
mkdir -p "$OUTPUT_ROOT"

find "$INPUT_ROOT" -mindepth 1 -maxdepth 1 -type d | sort | while read -r chapter_dir; do
  "$KCC" -p KS -f EPUB --nokepub -n --forcecolor -o "$OUTPUT_ROOT" "$chapter_dir"
done
```

Notes:
- If the user specifies a different device profile, replace `KS`.
- Keep the profile explicit in the final answer.
- If the user only wants chapter EPUBs, stop after this step.

## Merge Plan Generation

Use the bundled helper script:

```bash
python3 ./scripts/make_merge_plan.py \
  --epub-dir /data/manga/epub \
  --output /data/manga/merged/series.epub \
  --title "Series Title" \
  --author "Unknown" \
  --plan /data/manga/merged/merge-plan.json
```

If a manual order file exists:

```bash
python3 ./scripts/make_merge_plan.py \
  --epub-dir /data/manga/epub \
  --output /data/manga/merged/series.epub \
  --title "Series Title" \
  --author "Unknown" \
  --order-file /data/manga/merge-order.txt \
  --plan /data/manga/merged/merge-plan.json
```

## Merge Execution

Run:

```bash
python3 ./scripts/merge_epub_by_order.py --plan /data/manga/merged/merge-plan.json
```

Expected:
- one merged EPUB at the `output_epub_path`
- stable non-zero exit code on merge failure

## Troubleshooting

### KCC not found
- Probe `kcc-c2e` first, then `comic2ebook`.
- If both fail, stop and report missing dependency.

### Wrong chapter order
- Generate an explicit order file and rerun `make_merge_plan.py`.

### Output filename surprises
- Explain that KCC controls chapter EPUB filenames unless the wrapper script or calling loop renames them afterwards.

### Merge fails on missing files
- Inspect the generated plan JSON and verify each `epub_path` exists.
