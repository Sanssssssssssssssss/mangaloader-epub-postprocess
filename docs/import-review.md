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
