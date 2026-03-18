# MangaLoader + EPUB Postprocess

`MangaLoader + EPUB Postprocess` is a lightweight Linux-first manga workflow for:
- downloading public manga chapter images
- packaging chapter folders into EPUB
- merging chapter EPUBs into one collected EPUB

The current target is Raspberry Pi 5 4GB and similar low-resource Linux environments.

## What This Project Is

This repo combines two practical pieces:
- a lightweight headless downloader
- a lightweight EPUB postprocess pipeline

The main product entry lives here:
- `apps/manga-pipeline-lite`

It is intentionally:
- headless
- CLI-first
- PowerShell-free
- GUI-free
- upscaling-free

## Quick Start

### Raspberry Pi

```bash
git clone https://github.com/Sanssssssssssssssss/piclaw.git
cd piclaw
chmod +x apps/manga-pipeline-lite/install-pi.sh
chmod +x apps/manga-pipeline-lite/bin/manga-pipeline-lite
./apps/manga-pipeline-lite/install-pi.sh
./apps/manga-pipeline-lite/bin/manga-pipeline-lite doctor --config apps/manga-pipeline-lite/config.pi5.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite run --config apps/manga-pipeline-lite/config.pi5.json
```

### Main Commands

```bash
./apps/manga-pipeline-lite/bin/manga-pipeline-lite init-config --output my-job.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite doctor --config my-job.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite download --config my-job.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite package --config my-job.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite merge --config my-job.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite run --config my-job.json
```

## How To Use

1. Install the Pi toolchain with `install-pi.sh`.
2. Copy `apps/manga-pipeline-lite/config.pi5.json` or `config.example.json`.
3. Edit these fields:
   - `comic_path_word`
   - `group_path_word`
   - `chapter_limit`
   - `author`
   - `title`
4. Run `doctor` first to confirm dependencies and metadata access.
5. Run `run` for the full pipeline, or use `download/package/merge` separately.

Each job writes outputs to:

```text
runs/<job-name>/
  downloads/
  epubs/
  merged/
  config.lock.json
  result.json
```

## Folder Guide

These folders are the ones you will most often see:

- `apps/`
  - runnable product code
  - `apps/copymanga-headless-lite`: lightweight downloader
  - `apps/manga-pipeline-lite`: main product entry and Pi delivery scripts
- `skills/`
  - reusable packaging skill and helper scripts
- `scripts/`
  - development and verification helpers used to test the workflow
- `docs/`
  - product notes, design notes, and implementation records
- `dist/`
  - generated packaged artifacts, currently including the packaging skill bundle

These folders are local/runtime-oriented and may exist only after setup or testing:

- `.tools/`
  - local install artifacts such as the repo-local KCC wrapper
  - ignored by git
- `runs/`
  - output folders created by real jobs and smoke tests
  - ignored by git
- `imports/`
  - local copies of upstream repositories used during evaluation
  - ignored by git

## Acknowledgements

This project stands on top of excellent open-source work.

Special thanks to:
- Ciro Mattia Gonano and Pawel Jastrzebski for [Kindle Comic Converter (KCC)](https://github.com/ciromattia/kcc)
- lanyeeee for [copymanga-downloader](https://github.com/lanyeeee/copymanga-downloader)

Their work made it much faster to build a practical lightweight manga workflow.

## License

This repository is released under the MIT License. See [LICENSE](LICENSE).
