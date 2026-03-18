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
- Build and verify the next Pi-oriented deliverable beyond the skill.

## In Progress
- Define the default user-facing packaging preset for `manga-epub-packager-lite`.

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
