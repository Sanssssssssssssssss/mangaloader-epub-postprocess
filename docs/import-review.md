# Imported Project Review

## Candidate
- Repository: `MangaEpubAutomation`
- Upstream: `https://github.com/YuxuanHan0326/MangaEpubAutomation`
- Fork: `https://github.com/Sanssssssssssssssss/MangaEpubAutomation`
- Local path: `imports/MangaEpubAutomation`
- Review date: `2026-03-16`

## Goal of Review
- Determine whether this project can be adapted into a lightweight version that runs on `Raspberry Pi 5 4GB`.

## Repository Snapshot
- Primary language: PowerShell
- Secondary components:
  - WPF GUI in C#
  - Python script for merged EPUB flow
- Core workflow:
  - image upscale
  - chapter EPUB packaging
  - merged EPUB generation

## Evidence
- GUI targets Windows only:
  - `gui/MangaEpubAutomation.Gui/MangaEpubAutomation.Gui.csproj`
  - `TargetFramework=net8.0-windows`
  - `UseWPF=true`
  - `UseWindowsForms=true`
- GUI launches `powershell.exe` directly:
  - `gui/MangaEpubAutomation.Gui/Services/ProcessRunner.cs`
- GUI view model uses Windows UI APIs such as `System.Windows` and `System.Windows.Forms`:
  - `gui/MangaEpubAutomation.Gui/ViewModels/MainViewModel.cs`
- CLI scripts default to Windows dependency paths:
  - `Invoke-MangaEpubAutomation.ps1`
  - `Invoke-EpubUpscalePipeline.ps1`
- CLI currently assumes a Windows `.exe` KCC binary:
  - `kcc_c2e_9.4.3.exe`
- The main pipeline already supports `-SkipUpscale`, which is important for a Pi-friendly degraded mode:
  - `Invoke-MangaEpubAutomation.ps1`

## Feasibility Verdict
- Running the project unchanged on Raspberry Pi 5 4GB is **not feasible**.
- Building a lightweight Pi-oriented variant is **feasible with scope reduction**.

## Why the Original Project Does Not Fit Pi Directly
- WPF GUI is Windows-only.
- The GUI assumes `powershell.exe`, not cross-platform `pwsh`.
- Dependency discovery is based on `%APPDATA%` and `%LOCALAPPDATA%`.
- KCC is wired to a Windows executable path.
- Local MangaJaNai upscaling is the highest risk area for CPU, RAM, and ARM compatibility.

## Recommended Adaptation Path

### Path A: Recommended
- Keep only CLI/headless flow for the first Pi milestone.
- Make local upscaling optional or disabled by default.
- Focus first on:
  - packaging existing images into chapter EPUBs
  - merged EPUB generation
  - Linux-compatible config and dependency resolution

### Path B: Higher Risk
- Keep local upscaling on Pi.
- Requires validating Python, model runtime, inference speed, and peak memory on ARM.
- Likely much slower and less reliable on 4GB RAM.

## Recommended First Pi MVP
- Input: already prepared image directories
- Output:
  - chapter EPUBs
  - merged EPUB
- Excluded from first milestone:
  - WPF GUI
  - local GUI-driven configuration
  - mandatory local AI upscaling

## Required Refactors
- Replace Windows-only launcher assumptions with `pwsh` or direct script execution.
- Replace hard-coded default dependency paths with config-first resolution.
- Replace `.exe` KCC default with Linux-compatible KCC entrypoint.
- Isolate GUI-specific code from core CLI pipeline expectations.
- Add a documented Pi profile with safe defaults.

## Open Questions
- Is local AI upscaling mandatory for the first Pi milestone?
- Will the Pi run a full Linux desktop, or should we assume headless operation only?
- Should the first deliverable be a simple command, a small TUI, or a local web panel?

---

## Candidate
- Repository: `copymanga-downloader`
- Upstream: `https://github.com/lanyeeee/copymanga-downloader`
- Local path: `imports/copymanga-downloader`
- Review date: `2026-03-18`

## Goal of Review
- Determine whether this project can be reused on `Raspberry Pi 5 4GB`.
- Determine whether it composes well with:
  - `skills/manga-epub-packager-lite`
  - `imports/MangaEpubAutomation`

## Repository Snapshot
- Primary frontend: `Vue 3 + Vite + pnpm`
- Primary runtime: `Tauri 2 + Rust`
- Main behavior:
  - search or favorite-based manga selection
  - chapter image download
  - CBZ export
  - PDF export and optional PDF merge

## Evidence
- This is a desktop app, not a ready-made CLI:
  - `package.json` only exposes `vite`, `build`, `preview`, and `tauri`
  - `src-tauri/src/lib.rs` mounts Tauri commands and events through `invoke_handler`
- The Rust backend does contain useful reusable download logic:
  - `src-tauri/src/commands.rs`
  - `src-tauri/src/download_manager.rs`
- The downloader writes chapter images into configurable directories:
  - `src-tauri/src/config.rs`
  - `src-tauri/src/download_manager.rs`
- Downloaded image formats are already lightweight and packaging-friendly:
  - `webp`
  - `jpg`
- Built-in export targets are `cbz` and `pdf`, not `epub`:
  - `src-tauri/src/commands.rs`
  - `src-tauri/src/export.rs`
- WSL Linux probe:
  - `cargo check` reached dependency compilation but failed on missing Linux system build prerequisites before app logic completed
  - first observed blocker: `pkg-config` / OpenSSL discovery
- Official Tauri docs still state that Linux uses `webkit2gtk`, which confirms a desktop WebView dependency chain.

## Feasibility Verdict
- Running `copymanga-downloader` unchanged on Raspberry Pi 5 4GB is **not a lightweight fit**.
- Reusing its Rust download core for a future headless adapter is **feasible**.
- Using it together with `manga-epub-packager-lite` is **the most feasible composition path** among the current options.
- Using it together with original `MangaEpubAutomation` on Pi is **not recommended**.

## Why It Does Not Fit the Current Pi Target Directly
- Tauri brings Linux desktop runtime dependencies that are heavier than the current headless target.
- The repo does not currently expose a documented CLI entrypoint.
- The first verified Linux probe already failed on system dependency setup rather than business logic.
- Even if Linux desktop build becomes possible, that still conflicts with the current lightweight-first direction.

## Why It Still Has Reuse Value
- The Rust backend already knows how to:
  - talk to the source API
  - fetch chapter image URLs
  - download image files with concurrency control
  - write chapter directories in stable order
- Those chapter directories are exactly the kind of input our EPUB packaging skill already accepts.

## Combined Feasibility

### `copymanga-downloader` + `manga-epub-packager-lite`
- Verdict: **Feasible and recommended**
- Best use:
  - use `copymanga-downloader` as downloader/image materializer
  - use `manga-epub-packager-lite` to package downloaded chapter folders into EPUB
  - optionally merge resulting EPUBs into an anthology
- Required future work for a smooth Pi path:
  - either extract a headless downloader wrapper from the Rust core
  - or document an intermediate transfer workflow from a stronger machine to Pi

### `copymanga-downloader` + original `MangaEpubAutomation`
- Verdict: **Poor fit on Pi**
- Reason:
  - one side is Tauri desktop/Linux desktop oriented
  - the other side is Windows/PowerShell oriented
  - both together increase setup weight instead of reducing it

### All three together on Pi
- Verdict: **Not recommended for first Pi path**
- Recommended simplification:
  - `copymanga-downloader` or future headless downloader adapter
  - then `manga-epub-packager-lite`
  - keep `MangaEpubAutomation` only as reference material for workflow ideas

## Recommended Next Step
- Do not adapt the full Tauri GUI for Pi first.
- If downloader automation is needed on Pi, extract or reimplement a headless downloader path from the Rust backend.
- Otherwise, keep the current Pi path focused on packaging and treat downloader integration as the next milestone.
