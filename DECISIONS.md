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
