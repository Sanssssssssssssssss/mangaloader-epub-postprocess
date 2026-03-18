# Manga Pipeline Lite

`manga-pipeline-lite` is a lightweight Linux-first product entry for:
- downloading manga chapter image folders
- packaging chapter folders into EPUB
- merging chapter EPUBs into one anthology

It keeps the runtime small by using:
- Python stdlib for orchestration
- the existing lightweight headless downloader
- KCC only for EPUB generation

## Product layout

```text
apps/manga-pipeline-lite/
  bin/
    manga-pipeline-lite
  config.example.json
  config.pi5.json
  install-pi.sh
  pipeline.py
  README.md
```

## Main commands

```bash
python3 pipeline.py init-config --output my-job.json
python3 pipeline.py doctor --config my-job.json
python3 pipeline.py run --config my-job.json
```

You can also run one stage at a time:

```bash
python3 pipeline.py download --config my-job.json
python3 pipeline.py package --config my-job.json
python3 pipeline.py merge --config my-job.json
```

On Linux or Raspberry Pi, the wrapper script is:

```bash
./bin/manga-pipeline-lite doctor --config my-job.json
./bin/manga-pipeline-lite run --config my-job.json
```

## Raspberry Pi 5 quick start

From the repo root:

```bash
chmod +x apps/manga-pipeline-lite/install-pi.sh
chmod +x apps/manga-pipeline-lite/bin/manga-pipeline-lite
./apps/manga-pipeline-lite/install-pi.sh
./apps/manga-pipeline-lite/bin/manga-pipeline-lite doctor --config apps/manga-pipeline-lite/config.pi5.json
./apps/manga-pipeline-lite/bin/manga-pipeline-lite run --config apps/manga-pipeline-lite/config.pi5.json
```

The Pi installer:
- installs only the CLI-oriented KCC runtime path
- avoids the KCC GUI packaging route
- creates a repo-local wrapper at `./.tools/manga-pipeline-lite/bin/kcc-c2e`

`config.pi5.json` is the Pi-oriented default:
- lower `image_workers`
- repo-local KCC wrapper path
- ready to edit for a real comic job

## Per-job output layout

Each job creates:

```text
runs/<job-name>/
  config.lock.json
  result.json
  downloads/
  epubs/
  merged/
```

`result.json` is the main handoff file. It records the resolved output paths for the current job.

## Config notes

Important config fields:
- `job_name`: output directory name under `runs/`
- `kcc_cmd`: KCC executable path or command name
- `profile`: KCC device profile
- `skip_existing`: lets repeated runs resume without redoing finished files
- `max_images_per_chapter`: useful for very cheap smoke tests
- `steps`: enables or disables `download`, `package`, `merge` for `run`

## Lightweight defaults

- No GUI
- No PowerShell
- No local AI upscaling
- No database
- No background service

## Dependency notes

- `python3`
- `kcc-c2e` or `comic2ebook`

The downloader and pipeline orchestration themselves do not require third-party Python packages.
