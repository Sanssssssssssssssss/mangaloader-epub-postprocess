# PROJECT_BRIEF

## Project
- Name: `Piclaw` (working name)
- Type: Long-term software project for building reusable skills, tools, and later automation workflows for `Lobster`
- Status: `Raspberry Pi delivery kit prepared and validated in WSL`

## Goal
- Build a stable, maintainable software foundation that can host multiple `Lobster`-related skills and tools, then evolve into an automation-ready platform.

## Problem Statement
- The project will likely span many sessions and multiple imported codebases.
- Chat history is not a reliable memory layer for long-running delivery.
- We need a disk-based source of truth that lets a future session rebuild context quickly and continue execution consistently.

## Scope
- Establish persistent project memory and execution protocol.
- Clarify product direction and hard constraints before major implementation.
- Import or clone candidate projects into this workspace and evaluate reuse potential.
- Deliver a first runnable version of one focused `Lobster` use case.
- Keep the foundation compatible with later automation integration.

## Confirmed Constraints
- First imported baseline project: `MangaEpubAutomation`
- First target hardware: `Raspberry Pi 5 4GB`
- First deliverable: a lightweight skill for manga packaging
- Exclude for the first deliverable:
  - AI upscaling
  - GUI
  - heavyweight runtime assumptions

## Success Criteria
- The project can be resumed in a new session by reading the memory files only.
- Every implemented change maps to documented requirements.
- A first runnable version exists for one narrowly defined use case.
- The codebase remains simple enough to extend with future skills and automations.

## Non-Goals
- Do not define the full long-term product in one pass.
- Do not over-design architecture before the first concrete use case is chosen.
- Do not adopt a tech stack without a documented reason.
- Do not expand scope beyond confirmed requirements.

## Current Assumptions
- `Lobster` is the target operator, runtime, or business context for the tools, but the exact environment is not yet confirmed.
- Existing external repos may be cloned into this workspace and adapted rather than built from scratch.
- The first Pi milestone should prefer CLI or headless execution over a desktop GUI.
- The most useful first artifact is a reusable skill that teaches and assists lightweight manga packaging.
- The next Pi-oriented slice can be a narrow downloader that outputs chapter image folders for the packaging skill.
- The current product direction is a repo-native lightweight CLI with a stable per-job output layout.
- The current Pi delivery path uses a repo-local KCC CLI wrapper under `.tools/` plus a Pi-oriented default config.

## Open Questions
- What exactly is `Lobster` in this project context: user persona, product codename, bot runtime, or business workflow?
- What is the preferred first packaging scope: single-chapter EPUB only, or chapter EPUB plus merged anthology?
- Which target reader/device profile should be the default KCC preset when the user does not specify one?
