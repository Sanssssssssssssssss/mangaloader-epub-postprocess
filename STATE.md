# STATE

## Current Status
- Phase: `Lightweight packaging skill completed`
- Summary: The first lightweight deliverable exists as `manga-epub-packager-lite`. Its primary runtime path is Linux-native, and WSL Ubuntu verification has confirmed both chapter packaging and merged anthology generation.

## Current Task
- Decide the default packaging preset and add lightweight smoke-test examples for the skill.

## Next Step
- Decide the default KCC device profile for future users.
- Decide whether the default flow should be package-only or package-plus-merge.
- Then move on to the next Pi-oriented deliverable beyond the skill.
- Then move on to the next Pi-oriented deliverable beyond the skill.

## Risks
- The core business context of `Lobster` is still ambiguous.
- Default KCC profile choice may affect output quality on different readers.
- The packaged skill still contains a few harmless placeholder files from the initializer, which may be cleaned later if they become noise.

## Active Assumptions
- The first deliverable should be intentionally small and headless.
- Packaging and merge are in scope.
- GUI and local upscaling are out of scope.

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
