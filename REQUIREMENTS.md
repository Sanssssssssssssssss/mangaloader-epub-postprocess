# REQUIREMENTS

## Requirement Status
- Version: `v0.5`
- Confidence: `Medium`
- Basis: User bootstrap instructions, imported baseline review, Raspberry Pi target constraint, and clarified lightweight scope

## Functional Requirements

### FR-001 Persistent Project Memory
- The project must use disk-based memory files as the primary long-term context layer.
- Required files:
  - `PROJECT_BRIEF.md`
  - `REQUIREMENTS.md`
  - `ARCHITECTURE.md`
  - `DECISIONS.md`
  - `TASKS.md`
  - `STATE.md`

### FR-002 Context Rebuild Protocol
- At the start of each task, the agent must rebuild context from the project files before making changes.
- If chat content conflicts with project files, the latest confirmed file state wins and the conflict must be called out explicitly.

### FR-003 Structured Execution Output
- Before starting work, the agent must report:
  - current project goal
  - current task
  - known hard constraints
  - related historical decisions
  - risks and uncertainties
- After finishing work, the agent must report:
  - completed work
  - impacted requirements
  - new or changed decisions
  - update suggestions for `TASKS.md`, `STATE.md`, and `DECISIONS.md`

### FR-004 Requirements Discipline
- No undocumented feature expansion.
- No unjustified architectural reversal.
- All implementation must map back to a requirement in this file.
- Missing information must be listed with assumptions used.

### FR-005 Bootstrap the Project
- The workspace must be initialized with first-pass memory documents and a bootstrap execution plan.
- The plan must cover the path from requirement clarification to the first runnable version.

### FR-006 Imported Repository Evaluation
- The project must support cloning external repositories into the workspace for evaluation and adaptation.
- Imported code must be assessed against documented requirements before deep modification.

### FR-007 First Runnable Version
- The first delivery milestone must produce one runnable software slice for a single confirmed use case.
- The runnable version must include a basic start/run path and minimal validation instructions.

### FR-008 Automation Readiness
- The project should separate reusable logic from environment-specific glue so future automation integration is possible without major rewrites.

### FR-009 Raspberry Pi Lightweight Variant
- The first adaptation target is `Raspberry Pi 5 4GB`.
- The first runnable version for this target must avoid mandatory Windows-only components.
- The first runnable version should prefer a CLI or headless flow if that materially improves feasibility and resource usage.
- The first runnable version must not require GUI or local AI upscaling.

### FR-010 Manga Packaging Skill
- The first concrete deliverable must be a reusable skill for lightweight manga packaging.
- The skill must teach and support:
  - packaging manga image folders into EPUB
  - optionally merging multiple EPUBs into one ordered anthology
  - troubleshooting lightweight/headless usage
- The skill should bundle any helper scripts needed for repeatable merge-plan generation or EPUB merging.

### FR-011 Linux-Native Execution
- The lightweight packaging workflow must not depend on PowerShell scripts.
- The primary runnable helpers for the first skill must be Linux-friendly scripts suitable for Raspberry Pi environments.
- Command examples should prefer Python or POSIX shell usage over Windows-only shells.

### FR-012 Headless Manga Downloader Slice
- The next Pi-oriented slice may provide a lightweight headless downloader for manga chapter image folders.
- The downloader slice must avoid GUI and Tauri runtime requirements in its primary execution path.
- The downloader slice should support:
  - searching public manga metadata
  - inspecting comic groups
  - listing chapters for one group
  - downloading chapter images into stable folders
- The downloader output should be compatible with the packaging skill's chapter-folder input model.

### FR-013 Productized Pipeline Entry
- The project should provide a clear product-level entrypoint for the lightweight downloader-to-EPUB workflow.
- The product entry should expose one stable run command rather than requiring users to manually assemble multiple internal scripts.
- The product entry should create a clear per-job output structure for downloads, chapter EPUBs, merged EPUBs, and run metadata.

## Non-Functional Requirements

### NFR-001 Maintainability
- Prefer simple, well-scoped, low-coupling solutions.

### NFR-002 Session Continuity
- Future sessions should recover project state quickly by reading concise summaries instead of long historical logs.

### NFR-003 Traceability
- Important changes must be traceable to requirements and decisions.

### NFR-004 Incremental Delivery
- Work should be broken into small, verifiable milestones.

### NFR-005 Resource Awareness
- The Pi-targeted variant should minimize memory pressure, background services, and heavyweight UI dependencies.

### NFR-006 Skill Portability
- The packaging skill should be as self-contained as practical and avoid depending on GUI-only or Windows-only helpers.

### NFR-007 Downloader Simplicity
- The downloader slice should prefer low-dependency execution that is realistic on Raspberry Pi and WSL.
- Avoid desktop shells, embedded webviews, or heavyweight framework requirements in the primary runnable path.

## Business Rules
- BR-001: Project files are the source of truth for ongoing delivery.
- BR-002: Unconfirmed assumptions must remain labeled as assumptions.
- BR-003: The first runnable version should optimize for learning speed, not breadth.

## Acceptance Criteria
- AC-001: The six memory files exist and contain usable initial content.
- AC-002: A new session can identify current status and next step from `STATE.md`.
- AC-003: A bootstrap plan exists for moving from clarification to a runnable version.
- AC-004: Future code changes can be traced to at least one requirement ID.
- AC-005: A feasibility assessment exists for the imported baseline project on Raspberry Pi 5 4GB.
- AC-006: The first Pi milestone has a documented runnable scope even if some original features are deferred.
- AC-007: A usable packaging skill exists in the workspace with runnable helper scripts or explicit command recipes.
- AC-008: A lightweight headless downloader slice exists or has been proven feasible with a runnable Linux-friendly command path.
- AC-009: A product-level lightweight pipeline entry exists with a stable config-driven run path and clear output directories.

## Missing Information
- MI-001: Definition of `Lobster` within this project.
- MI-002: First business scenario to support beyond lightweight packaging.
- MI-003: Preferred default KCC device profile when the user does not specify one.
- MI-004: Whether the first skill should default to chapter EPUB only or chapter EPUB plus merged anthology.

## Working Assumptions
- A single-use-case MVP is preferred over a broad platform MVP.
- External repos may provide a faster base than greenfield implementation.
- Architecture will stay intentionally lightweight until the first runnable target is selected.
- For the first milestone, packaging and merge are in scope, while local upscaling and GUI are out of scope.
- For the next Pi slice, downloader behavior should stay narrower than the imported desktop downloader unless a broader need is confirmed.
