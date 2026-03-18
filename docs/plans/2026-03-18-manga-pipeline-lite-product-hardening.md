# Manga Pipeline Lite Product Hardening

## Goal
- Keep the downloader-to-EPUB chain lightweight while making it feel like a usable product instead of a loose script collection.

## Scope
- Stay repo-native.
- Avoid new heavy dependencies.
- Add a clearer product command surface.
- Keep per-job outputs predictable.

## Chosen Shape
- Product root: `apps/manga-pipeline-lite`
- Main Python entry: `pipeline.py`
- Linux wrapper: `bin/manga-pipeline-lite`
- Example config: `config.example.json`

## Command Surface
- `init-config`: write a starter JSON config
- `doctor`: validate component paths, KCC availability, and optional network metadata
- `download`: run only the downloader stage
- `package`: run only the EPUB packaging stage
- `merge`: run only the merge stage
- `run`: execute all enabled stages from config

## Lightweight Choices
- No GUI wrapper
- No installer
- No database
- No background daemon
- No extra Python dependency beyond the existing downloader and KCC runtime

## Output Model
- `runs/<job>/downloads`
- `runs/<job>/epubs`
- `runs/<job>/merged`
- `runs/<job>/config.lock.json`
- `runs/<job>/result.json`

## Validation
- `doctor --check-network` verified the public metadata path in WSL.
- `run --config config.example.json` verified the wrapper-driven product path in WSL with a low-resource sample and produced a merged EPUB.
