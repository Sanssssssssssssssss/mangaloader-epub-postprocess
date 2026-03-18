# STATE

## Current Status
- Phase: `Raspberry Pi delivery kit validated`
- Summary: The lightweight packaging skill, the Python headless downloader, and the repo-native product entry `apps/manga-pipeline-lite` now have a Pi-oriented delivery path. A minimal install script creates a repo-local KCC CLI wrapper under `.tools/`, and `config.pi5.json` provides a Pi-friendly default. This path has been validated in WSL with both `doctor` and a low-resource smoke run.

## Current Task
- Finalize user-facing defaults for the lightweight product, then decide whether token-assisted download paths or a standalone release bundle are worth adding.

## Next Step
- Decide the default KCC device profile for future users.
- Decide whether the default flow should be package-only or package-plus-merge.
- Decide whether token-assisted downloader paths are worth adding after the public-chapter slice.
- Decide whether the product should remain repo-native or later gain a standalone release bundle.

## Risks
- The core business context of `Lobster` is still ambiguous.
- Default KCC profile choice may affect output quality on different readers.
- The packaged skill still contains a few harmless placeholder files from the initializer, which may be cleaned later if they become noise.
- `copymanga-downloader` currently depends on a Tauri/Linux desktop stack, which is heavier than the current Pi target direction.
- Source-site or API changes may make downloader reuse more fragile than the packaging workflow.
- The current downloader slice has only been validated against a public sample and not yet against private or token-gated content.
- `manga-pipeline-lite` is currently repo-native, so a future standalone release artifact would need an explicit packaging decision.

## Active Assumptions
- The first deliverable should be intentionally small and headless.
- Packaging and merge are in scope.
- GUI and local upscaling are out of scope.
- The downloader slice should stay narrower than the imported desktop app unless a stronger need is confirmed.

## Handoff Notes
- Start each new session by reading, in order:
  1. `STATE.md`
  2. `PROJECT_BRIEF.md`
  3. `REQUIREMENTS.md`
  4. `DECISIONS.md`
  5. `TASKS.md`
  6. `ARCHITECTURE.md`
  7. `docs/import-review.md`
- Treat these files as authoritative unless explicitly updated.

## Compression Policy
- Do not append full historical narratives.
- Replace outdated detail with short summaries once decisions are captured elsewhere.
- Keep only:
  - current phase
  - current task
  - next step
  - active risks
  - essential handoff notes
