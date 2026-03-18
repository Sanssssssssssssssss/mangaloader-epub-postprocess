# Copymanga Headless Lite

Internal runtime module used by `MangaLoader + EPUB Postprocess`.

Small Linux-friendly CLI for materializing manga chapter image folders from the public CopyManga API.

## Why this exists
- `imports/copymanga-downloader` was useful as a reference, but it is a Tauri desktop app.
- The Raspberry Pi path in this project is intentionally headless and lightweight.
- This tool keeps only the narrow downloader slice needed for later EPUB postprocess work.

## Commands

```bash
python3 copymanga_downloader.py search "haizeiwang"
python3 copymanga_downloader.py comic haizeiwang
python3 copymanga_downloader.py chapters haizeiwang --group default
python3 copymanga_downloader.py download-chapter haizeiwang --chapter-uuid 4bd05882-c7bc-11e8-881a-024352452ce0 --output-root ./downloads
python3 copymanga_downloader.py download-group haizeiwang --group default --limit 3 --output-root ./downloads
```

## Output shape

The downloader writes folders like:

```text
<output-root>/
  <comic-title>/
    <group-title>/
      0001 <chapter-name>/
        0001.webp
        0002.webp
```

Point the postprocess helper at one group directory:

```bash
python3 ../manga-pipeline-lite/postprocess/manga_packager.py \
  --input-root "<output-root>/<comic-title>/<group-title>" \
  --output-root ./epubs
```

## Notes
- This is intentionally smaller than the upstream desktop app.
- It does not implement favorites, account pooling, or built-in export.
- If some content later requires login, token support can be added without changing the current folder contract.
