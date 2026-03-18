# MangaEpubAutomation Pi Lightweight Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Adapt `imports/MangaEpubAutomation` into a lightweight Raspberry Pi 5 4GB friendly variant that can run a headless CLI workflow.

**Architecture:** Keep the imported PowerShell CLI as the short-term base, remove Windows-only assumptions, and make the first Pi milestone packaging-and-merge oriented. Defer the WPF GUI and treat local AI upscaling as optional until ARM feasibility is proven.

**Tech Stack:** PowerShell Core (`pwsh`), Linux-compatible KCC invocation, optional Python dependency for merge and future upscale.

---

### Task 1: Freeze the Pi MVP Boundary

**Files:**
- Modify: `PROJECT_BRIEF.md`
- Modify: `REQUIREMENTS.md`
- Modify: `STATE.md`
- Modify: `TASKS.md`
- Modify: `docs/import-review.md`

**Step 1: Confirm the first runnable scope**

Lock the first Pi milestone to:
- headless CLI execution
- chapter EPUB packaging
- merged EPUB generation

**Step 2: Mark local upscale as optional**

Document that local upscaling remains optional until ARM feasibility is verified.

**Step 3: Update blockers**

Keep only the unresolved decision about whether local upscale is mandatory.

### Task 2: Prepare a Pi-Friendly Workspace Layout

**Files:**
- Create: `imports/MangaEpubAutomation/docs/pi/README.md`
- Create: `imports/MangaEpubAutomation/config/pi.deps.example.json`
- Create: `imports/MangaEpubAutomation/config/pi.config.json`

**Step 1: Add Pi docs folder**

Create a small Pi-focused setup document under the imported repo.

**Step 2: Add explicit dependency config example**

Replace Windows default-path assumptions with a Linux example config that points to:
- `pwsh`
- python interpreter
- KCC entrypoint
- optional backend/model paths

**Step 3: Add a Pi-safe runtime config**

Create a config file that prefers:
- `SkipUpscale`
- conservative image/output defaults
- packaging and merge enabled

### Task 3: Remove Windows-Only Launcher Assumptions from the Main CLI

**Files:**
- Modify: `imports/MangaEpubAutomation/Invoke-MangaEpubAutomation.ps1`
- Modify: `imports/MangaEpubAutomation/Invoke-EpubUpscalePipeline.ps1`

**Step 1: Write a failing compatibility check**

Define a simple Linux expectation:
- when explicit dependency paths are provided, the scripts must not require `%APPDATA%`, `%LOCALAPPDATA%`, or `.exe` defaults to proceed.

**Step 2: Add platform-aware dependency resolution**

Implement minimal code that:
- prefers explicit JSON/config values
- uses Linux-safe defaults only when appropriate
- stops assuming `python.exe` and `kcc_c2e_9.4.3.exe`

**Step 3: Preserve Windows compatibility**

Keep the existing Windows path logic as fallback rather than deleting it outright.

**Step 4: Verify script parsing**

Run:

```powershell
pwsh -NoProfile -File .\Invoke-MangaEpubAutomation.ps1 -PlanOnly -SkipUpscale -TitleRoot "<sample>"
```

Expected:
- script parses
- preflight reflects missing inputs/deps without crashing on Windows-only defaults

### Task 4: Add a Dedicated Pi Entry Path

**Files:**
- Create: `imports/MangaEpubAutomation/Invoke-MangaEpubAutomation.Pi.ps1`
- Create: `imports/MangaEpubAutomation/Invoke-EpubUpscalePipeline.Pi.ps1`

**Step 1: Create thin Pi wrappers**

Wrap the existing scripts with Pi-safe defaults so the first user path is simple.

**Step 2: Default to lightweight behavior**

Set the wrapper defaults to:
- headless mode
- `SkipUpscale` on the directory pipeline
- explicit Pi config locations

**Step 3: Keep wrappers thin**

Do not duplicate core pipeline logic inside the wrapper.

### Task 5: Decouple the First Deliverable from the GUI

**Files:**
- Modify: `imports/MangaEpubAutomation/README.md`
- Create: `imports/MangaEpubAutomation/docs/pi/GUI_STATUS.md`

**Step 1: Mark GUI as unsupported for Pi milestone**

Document that the WPF GUI remains Windows-only and is excluded from the first Pi deliverable.

**Step 2: Point Pi users to the wrapper scripts**

Make the Pi run path obvious from the repo documentation.

### Task 6: Validate the Merge and Packaging Flow on a Minimal Fixture

**Files:**
- Create: `imports/MangaEpubAutomation/tests/fixtures/README.md`
- Create: `imports/MangaEpubAutomation/tests/pi-smoke-test.md`

**Step 1: Define a smoke-test contract**

Document the minimum fixture shape needed to exercise packaging and merge.

**Step 2: Define verification commands**

Include exact commands for:
- plan-only directory pipeline
- packaging-only run
- merge-only run

**Step 3: Record expected artifacts**

Document expected output directories, logs, and failure modes.

### Task 7: Decide the Future of Local Upscaling

**Files:**
- Modify: `docs/import-review.md`
- Modify: `DECISIONS.md`
- Modify: `TASKS.md`
- Modify: `STATE.md`

**Step 1: Test or document ARM feasibility**

After the lightweight path runs, decide whether local upscale on Pi is:
- feasible
- deferred
- offloaded

**Step 2: Record the decision**

Capture the outcome in `DECISIONS.md` and remove stale blockers from `TASKS.md`.

**Step 3: Prepare the next implementation slice**

Set the next milestone to either:
- optimize the Pi CLI workflow
- or add an optional upscale path
