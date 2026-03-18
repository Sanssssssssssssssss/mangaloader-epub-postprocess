# TASKS

## Operating Rule
- Keep tasks short, current, and deduplicated.
- Move finished items to `Done` with a short outcome note instead of preserving full history.
- When the file grows, compress older completed items into a monthly summary line.

## To Do
- Clarify what `Lobster` means in this project context.
- Decide the default KCC device profile for the packaging skill.
- Decide whether the first skill should default to chapter EPUB only or chapter EPUB plus merged anthology.
- Add lightweight smoke-test examples for the skill.
- Decide whether the downloader slice should remain public-chapter-only or later add token-assisted paths.
- Decide whether `manga-pipeline-lite` should later gain a release bundle outside the repo, or remain repo-native.

## In Progress
- Define the default user-facing packaging preset for `manga-epub-packager-lite`.
- Decide whether `manga-pipeline-lite` should later gain a standalone release artifact outside the repo.

## Blocked
- None.

## Done
- Established the requirement that project context must be externalized to disk-based memory files.
- Created the first version of `PROJECT_BRIEF.md`, `REQUIREMENTS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `TASKS.md`, and `STATE.md`.
- Created the first bootstrap execution plan in `docs/plans/2026-03-16-project-bootstrap.md`.
- Initialized Git for the root workspace.
- Confirmed or reused the existing fork of `MangaEpubAutomation`.
- Cloned `MangaEpubAutomation` into `imports/MangaEpubAutomation`.
- Confirmed that the first lightweight milestone excludes GUI and upscaling.
- Built `skills/manga-epub-packager-lite` with lightweight workflow instructions and bundled helper scripts.
- Validated and packaged the skill to `dist/manga-epub-packager-lite.skill`.
- Converted the skill's primary execution path from PowerShell-oriented examples to Linux-native Python helpers and bash/python command patterns.
- Verified the Linux-native packaging and merge flow inside WSL Ubuntu with real EPUB outputs.
- Cloned `copymanga-downloader` into `imports/copymanga-downloader`.
- Completed a Raspberry Pi feasibility review for `copymanga-downloader` and for combining it with the existing packaging skill and `MangaEpubAutomation`.
- Wrote the downloader design note in `docs/plans/2026-03-18-copymanga-headless-lite-design.md`.
- Added `apps/copymanga-headless-lite/copymanga_downloader.py` as the first Pi-friendly headless downloader slice.
- Added `apps/manga-pipeline-lite` as a product-level entrypoint with `pipeline.py`, `config.example.json`, and product README.
- Verified the product entrypoint in WSL with a single-volume smoke run and a config-driven `runs/<job>` output layout.
- Expanded `manga-pipeline-lite` into a clearer lightweight product with `doctor`, stage subcommands, resume-friendly config, and a Linux wrapper under `apps/manga-pipeline-lite/bin/`.
- Re-verified the productized entry in WSL with a low-resource public smoke run that produced a merged EPUB under `runs/fire-force-public-smoke/`.
- Added a Raspberry Pi delivery kit with `apps/manga-pipeline-lite/install-pi.sh`, `apps/manga-pipeline-lite/config.pi5.json`, and a repo-local `.tools` install target for the KCC CLI wrapper.
- Verified the Pi delivery path in WSL using the install script, the Pi config, and a low-resource smoke run that produced `runs/pi5-delivery-smoke/merged/Fire_Force_Pi_Smoke.epub`.
- Added `scripts/verify_wsl_copymanga_headless.sh` and verified the downloader in WSL with a live public chapter smoke test.
- Added `scripts/run_wsl_copymanga_to_epub.sh` as a reusable Linux end-to-end helper for downloader -> package -> merge.
- Verified the downloader -> package -> merge flow in WSL with `炎炎之消防隊` volumes 1-3 and produced a merged EPUB artifact under `runs/2026-03-18-fire-force-e2e/`.
