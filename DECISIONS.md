# DECISIONS

## Decision Log

### D-001 Use Markdown Files as Project Memory
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Use root-level Markdown files as the long-term source of truth for project context.
- Reason: Multi-session continuity is a hard requirement, and chat history is not reliable enough.

### D-002 Keep Bootstrap Scope Narrow
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Focus initialization on memory, requirements, planning, and the path to one runnable version.
- Reason: Scope control is necessary until the first concrete use case is confirmed.

### D-003 Defer Final Tech Stack Selection
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Do not lock in a framework or language before evaluating the first actual runnable target and imported repositories.
- Reason: Premature stack choices would create unnecessary migration risk.

### D-004 Prefer Simple, Stable, Traceable Delivery
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Default to simple, maintainable solutions that map clearly to requirements.
- Reason: This matches the user's execution protocol and reduces long-term drift.

### D-005 Use MangaEpubAutomation as the First Imported Baseline
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Use `MangaEpubAutomation` as the first external project to evaluate and adapt inside this workspace.
- Reason: The user explicitly selected it as the first conversion target.

### D-006 Treat Raspberry Pi 5 4GB as the First Runtime Constraint
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: Evaluate all near-term changes against Raspberry Pi 5 4GB feasibility.
- Reason: This is now the first concrete runtime target and the main driver of scope reduction.

### D-007 First Pi Milestone Is CLI-First and Headless
- Date: `2026-03-16`
- Status: `Accepted`
- Decision: The first Pi-focused milestone will target CLI/headless execution rather than preserving the existing WPF desktop GUI.
- Reason: The imported GUI targets `net8.0-windows`, uses WPF/Windows Forms, and launches `powershell.exe`, which is incompatible with a Linux Raspberry Pi target.

### D-008 First Deliverable Excludes GUI and Upscaling
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: The first deliverable will not include GUI or local AI upscaling.
- Reason: The user explicitly narrowed scope to lightweight packaging only.

### D-009 First Deliverable Is a Packaging Skill
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: The first concrete deliverable will be a reusable skill for packaging manga into EPUB, with optional merge support.
- Reason: A skill is the fastest lightweight artifact that captures the workflow in a reusable form.

### D-010 First Skill Supports Packaging and Optional Merge
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: The first skill will cover both chapter EPUB packaging and optional ordered anthology merge.
- Reason: This stays lightweight while covering the most practical end-to-end packaging workflow.

### D-011 PowerShell Is Out of Scope for the First Skill Runtime
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: The first packaging skill will use Linux-native Python helpers as its primary execution path instead of `.ps1` wrappers.
- Reason: The user explicitly stated that PowerShell scripts are not usable in the target environment.

### D-012 Linux-Native Skill Path Verified in WSL
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Treat the Linux-native Python packaging path as the validated baseline for the first skill.
- Reason: WSL Ubuntu verification succeeded for chapter packaging and merged anthology generation using KCC plus the bundled Python helpers.

### D-013 Use `copymanga-downloader` as the Second Imported Evaluation Baseline
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Track `copymanga-downloader` as the second imported repository under evaluation.
- Reason: The user explicitly selected it for Pi feasibility assessment and possible reuse.

### D-014 Prefer `Downloader -> Packaging Skill` Over Reusing Full Desktop Apps on Pi
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: If downloader automation is needed on Raspberry Pi, prefer a headless downloader path feeding `manga-epub-packager-lite` instead of combining the original desktop applications.
- Reason: `copymanga-downloader` is Tauri/Linux-desktop oriented, while `MangaEpubAutomation` is Windows/PowerShell oriented; both are weaker fits for the current lightweight Pi target than a narrow downloader-to-packager pipeline.

### D-015 Implement the First Downloader Slice as a Small Python CLI
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Implement the first downloader slice as a small Python CLI under `apps/copymanga-headless-lite` instead of first extracting a Rust headless adapter from the imported Tauri app.
- Reason: The public API path was verified directly in WSL, and a Python stdlib CLI is the fastest path to a Pi-friendly headless downloader that can feed the existing packaging skill.

### D-016 Validate the Downloader-to-EPUB Path with a Small Real Sample First
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Validate the end-to-end pipeline on a small real sample set before attempting a full-series run.
- Reason: This preserves the lightweight execution model while still proving that downloader output, KCC packaging, and EPUB merge cooperate correctly.

### D-017 Productize the Lightweight Chain as `manga-pipeline-lite`
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Productize the current lightweight chain as a single-entry CLI app under `apps/manga-pipeline-lite`, using config-driven runs and a stable `runs/<job>` output structure.
- Reason: This keeps the chain lightweight and explicit while making it feel like a usable product instead of a loose collection of scripts.

### D-018 Keep the Product Repo-Native and Stage-Oriented for Now
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Keep `manga-pipeline-lite` as a repo-native lightweight product with a Linux wrapper, `doctor` command, and stage-oriented subcommands instead of introducing a heavier standalone packaging system right now.
- Reason: This improves usability and directory clarity without adding background services, installers, or duplicated code that would work against the Pi-first lightweight constraint.

### D-019 Deliver the Pi Variant with a Repo-Local KCC Wrapper
- Date: `2026-03-18`
- Status: `Accepted`
- Decision: Ship the Raspberry Pi delivery path as a minimal install script plus a Pi-oriented config, and place the KCC CLI wrapper under `.tools/manga-pipeline-lite/bin/kcc-c2e`.
- Reason: This keeps the install path explicit and repeatable while avoiding a heavy standalone packaging format or a global system dependency assumption.
