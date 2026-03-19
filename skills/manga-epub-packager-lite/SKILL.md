---
name: manga-epub-packager-lite
description: Lightweight manga packaging and EPUB merge workflow for headless environments. Use when the user wants to turn manga image folders into EPUB files, or merge chapter EPUBs into one ordered anthology, without GUI or AI upscaling. Especially useful on Raspberry Pi, Linux servers, or other low-resource setups where KCC/comic2ebook plus simple helper scripts are preferred.
---

# Manga Epub Packager Lite

## Overview

Use this skill to package manga image folders into EPUB with the lightest practical path:
- package chapter folders with `../../apps/manga-pipeline-lite/postprocess/manga_packager.py`
- generate merge plans with `../../apps/manga-pipeline-lite/postprocess/make_merge_plan.py`
- merge chapter EPUBs with `../../apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py`

If the user wants the full downloader-to-EPUB path, prefer the product entry `../../apps/manga-pipeline-lite/pipeline.py`, which now defaults to the Rust upstream-core downloader backend.

Default to:
- no GUI
- no AI upscaling
- explicit commands and file paths

## Workflow

### 1. Decide the mode

Choose the narrowest workflow that solves the task:
- Package only: image folders -> chapter EPUBs
- Merge only: existing chapter EPUBs -> one ordered anthology
- Full lightweight flow: image folders -> chapter EPUBs -> merged anthology

If the user asks for GUI setup, MangaJaNai, or local super-resolution, this skill is the wrong tool for that part.

### 2. Inspect the inputs

Before running commands:
- identify whether the input is image folders or existing EPUBs
- identify whether ordering matters
- identify the desired output directory
- identify the target reader profile if the user gives one

If there is no explicit device/profile, use a conservative KCC preset and state the assumption.

For expected folder shapes and command templates, read [references/workflow.md](references/workflow.md).

### 3. Detect the packaging command

Prefer the Linux-native Python wrapper as the primary entry point:
- use `../../apps/manga-pipeline-lite/postprocess/manga_packager.py` for package-only
- use `../../apps/manga-pipeline-lite/postprocess/manga_packager.py` with `--merge-output` for package-plus-merge
- use `../../apps/manga-pipeline-lite/postprocess/make_merge_plan.py` plus `../../apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py` for merge-only

The wrapper probes `kcc-c2e` first, then `comic2ebook`, unless the user passes `--kcc-cmd`.

### 4. Package chapter folders

When the input is chapter directories:
- use `../../apps/manga-pipeline-lite/postprocess/manga_packager.py`
- write outputs to a dedicated directory
- keep filenames stable and readable
- avoid heavyweight processing flags unless the user explicitly asks for them

If the user only needs per-chapter EPUBs, stop here.

### 5. Generate a merge plan

When the user wants one merged anthology:
- use `../../apps/manga-pipeline-lite/postprocess/make_merge_plan.py` to build the plan JSON
- prefer an explicit order file when the desired order is non-trivial
- if no order file exists, explain that filename-natural-sort will be used

### 6. Merge EPUBs

Use `../../apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py --plan <plan.json>` to create the final anthology EPUB.

After merging:
- confirm the output file exists
- report where it was written
- mention whether ordering came from an order file or filename sorting

## Output Rules

- Always show the exact command you ran or recommend.
- Always report assumptions, especially:
  - KCC command name
  - device profile
  - output directory
  - merge ordering source
- Prefer the lightest possible path.
- Do not introduce GUI steps, Docker, or upscale dependencies.

## Resources

- [references/workflow.md](references/workflow.md): lightweight workflow, input layout, command patterns, troubleshooting
- [references/pi-wsl-setup.md](references/pi-wsl-setup.md): Linux/WSL setup path for KCC and the skill
- [references/smoke-test.md](references/smoke-test.md): small verification recipes
- `../../apps/manga-pipeline-lite/postprocess/manga_packager.py`: Linux-native package-only or package-plus-merge entry point
- `../../apps/manga-pipeline-lite/postprocess/make_merge_plan.py`: generate merge-plan JSON from an EPUB directory
- `../../apps/manga-pipeline-lite/postprocess/merge_epub_by_order.py`: merge ordered chapter EPUBs into one anthology EPUB
