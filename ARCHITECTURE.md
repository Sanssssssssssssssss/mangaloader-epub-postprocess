# ARCHITECTURE

## Status
- Version: `v0.3`
- Maturity: `Working architecture direction`
- Constraint: The first deliverable is now a lightweight packaging skill, not a full adapted application

## Architecture Goal
- Define only the minimum structure needed to keep the project coherent while major product and stack decisions are still open.

## Guiding Principles
- Keep the first version modular and easy to replace.
- Separate domain logic from adapters and automation glue.
- Prefer explicit interfaces over hidden coupling.
- Defer irreversible framework choices until the first runnable use case is confirmed.

## Proposed Repository Structure
```text
/
|-- PROJECT_BRIEF.md
|-- REQUIREMENTS.md
|-- ARCHITECTURE.md
|-- DECISIONS.md
|-- TASKS.md
|-- STATE.md
|-- docs/
|   |-- plans/
|   `-- import-review.md
|-- imports/       # cloned external projects for evaluation/adaptation
|-- skills/        # project-owned reusable skills
|-- apps/          # runnable app(s) once a concrete target exists
|-- packages/      # shared libraries/modules once needed
|-- scripts/       # dev/bootstrap/automation helper scripts
`-- tests/         # project-level verification where applicable
```

## Logical Modules

### 1. Project Memory Layer
- Purpose: Preserve goals, requirements, decisions, state, and tasks across sessions.
- Artifacts: root Markdown files.

### 2. Imported Baseline Layer
- Purpose: Hold third-party or forked candidate projects under evaluation.
- Current baselines:
  - `imports/MangaEpubAutomation`
  - `imports/copymanga-downloader`

### 3. Skill Layer
- Purpose: Hold reusable agent skills derived from project learnings.
- Current target: `skills/manga-epub-packager-lite`

### 4. Core Domain Layer
- Purpose: Hold reusable `Lobster` business logic.
- Constraint: Should not depend directly on UI or automation runtime details.

### 5. Adapter Layer
- Purpose: Connect the core domain to concrete runtimes such as CLI, UI, local services, or external automation entry points.
- Current runnable adapter candidates:
  - `skills/manga-epub-packager-lite/scripts/manga_packager.py`
  - `apps/copymanga-headless-lite/copymanga_downloader.py`
  - `apps/manga-pipeline-lite/pipeline.py`
  - `apps/manga-pipeline-lite/bin/manga-pipeline-lite`

### 6. Automation Integration Layer
- Purpose: Host future scheduled or event-driven workflows.
- Constraint: Must consume stable interfaces from the core domain instead of embedding business logic inline.

## Data and Interface Principles
- Inputs and outputs should be explicit and serializable when possible.
- Configuration should be externalized instead of hard-coded.
- Each imported repo should be wrapped or adapted behind project-owned boundaries before deep integration.
- Skills should bundle only the minimum scripts and references needed for repeatable execution.

## Current Working Direction
- Imported baselines:
  - `imports/MangaEpubAutomation`
  - `imports/copymanga-downloader`
- Target environment: Linux on Raspberry Pi 5 4GB
- Recommended first slice: a self-contained lightweight packaging skill
- Recommended composition path after the skill:
  - downloader or downloader-adapter
  - then packaging skill
- Current downloader prototype:
  - `apps/copymanga-headless-lite`
- Current product entry:
  - `apps/manga-pipeline-lite`
  - stage-oriented commands: `doctor`, `download`, `package`, `merge`, `run`
  - Pi delivery helpers: `install-pi.sh`, `config.pi5.json`, repo-local KCC wrapper under `.tools/manga-pipeline-lite/bin/`
- Deferred from first slice:
  - WPF GUI
  - Windows-only file pickers
  - hard-coded `.exe` dependency defaults
  - local AI upscaling
  - Linux desktop GUI adaptation of the Tauri downloader

## Current Unknowns
- Final language/runtime for later Pi deliverables
- Packaging strategy beyond the skill
- Test framework
- Persistence layer needs
- Default KCC profile for end users

## Immediate Architectural Priority
- Preserve optionality while preparing one narrow, reusable packaging skill.
