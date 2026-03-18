# Manga Pipeline Lite Product Design

## Goal
- Turn the verified downloader-to-EPUB chain into a clearer product entrypoint.
- Keep the runtime lightweight enough for Raspberry Pi and WSL.
- Avoid introducing new heavyweight frameworks or background services.

## Product Shape
- Product directory: `apps/manga-pipeline-lite`
- Main entrypoint: `pipeline.py`
- Supporting files:
  - `README.md`
  - `config.example.json`

## Why this shape
- It creates one obvious product surface for users and future agents.
- It keeps the implementation thin by reusing:
  - `apps/copymanga-headless-lite/copymanga_downloader.py`
  - `skills/manga-epub-packager-lite/scripts/manga_packager.py`
  - `skills/manga-epub-packager-lite/scripts/make_merge_plan.py`
  - `skills/manga-epub-packager-lite/scripts/merge_epub_by_order.py`
- It avoids code duplication while still making the repo feel productized.

## Commands
- `init-config`
  - writes a starter config JSON
- `run`
  - loads config
  - resolves comic/group names
  - downloads chapter folders
  - packages chapter EPUBs
  - builds merge plan
  - merges final EPUB
  - writes a run summary JSON

## Output Layout
- `runs/<job-name>/`
  - `config.lock.json`
  - `result.json`
  - `downloads/`
  - `epubs/`
  - `merged/`

## Design Choices
- Explicit multi-step orchestration is preferred over a hidden monolith.
- Product logic should call package and merge as separate steps.
- The product should use stable defaults:
  - `KS` profile
  - `default` group
  - UTF-8 JSON config

## Out of Scope
- GUI
- daemon/service mode
- database
- favorites integration
- token rotation or account pooling
- standalone installer packaging

