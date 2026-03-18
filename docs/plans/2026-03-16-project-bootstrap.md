# Project Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Move from project clarification to one first runnable `Lobster (龙虾)` software slice with stable project memory and controlled scope.

**Architecture:** Start with persistent project documentation and imported-repo evaluation before choosing a final stack. Build one narrow runnable path behind project-owned boundaries so future automation work can reuse the same core logic.

**Tech Stack:** TBD after MVP clarification and imported project review; documentation-first bootstrap in Markdown.

---

### Task 1: Lock Project Memory and Resume Protocol

**Files:**
- Create: `PROJECT_BRIEF.md`
- Create: `REQUIREMENTS.md`
- Create: `ARCHITECTURE.md`
- Create: `DECISIONS.md`
- Create: `TASKS.md`
- Create: `STATE.md`

**Step 1: Create the initial memory files**

Write concise bootstrap versions for the six required files.

**Step 2: Verify cross-file consistency**

Check that goals, assumptions, blockers, and next steps do not conflict across files.

**Step 3: Record bootstrap decisions**

Log decisions for memory strategy, scope control, and stack deferral in `DECISIONS.md`.

**Step 4: Update current state**

Set `STATE.md` to point to requirement clarification as the next real milestone.

### Task 2: Clarify the First Runnable Use Case

**Files:**
- Modify: `PROJECT_BRIEF.md`
- Modify: `REQUIREMENTS.md`
- Modify: `TASKS.md`
- Modify: `STATE.md`

**Step 1: Confirm product meaning**

Document what `Lobster (龙虾)` means in this project and what users or operators need from it.

**Step 2: Choose one MVP scenario**

Reduce scope to one narrow, testable workflow that can be run locally.

**Step 3: Define acceptance criteria**

Add concrete "done" conditions for the chosen MVP scenario to `REQUIREMENTS.md`.

**Step 4: Update tasks and blockers**

Remove resolved ambiguities and reflect the new priority order in `TASKS.md` and `STATE.md`.

### Task 3: Prepare the Workspace for Implementation

**Files:**
- Create: `imports/.gitkeep`
- Create: `apps/.gitkeep`
- Create: `packages/.gitkeep`
- Create: `scripts/.gitkeep`
- Create: `tests/.gitkeep`
- Modify: `TASKS.md`
- Modify: `STATE.md`

**Step 1: Initialize repository structure**

Create the basic workspace directories needed for imports, apps, shared code, scripts, and tests.

**Step 2: Initialize version control**

Run: `git init`

Expected: a new Git repository is created in the workspace root.

**Step 3: Reflect readiness**

Update `STATE.md` to show that the workspace is ready for repo import and evaluation.

### Task 4: Import and Assess Candidate Projects

**Files:**
- Create: `docs/import-review.md`
- Modify: `DECISIONS.md`
- Modify: `TASKS.md`
- Modify: `STATE.md`

**Step 1: Clone candidate repositories into `imports/`**

Use one folder per external project.

**Step 2: Review each candidate**

For each imported project, record:
- purpose
- language/runtime
- current run status
- overlap with MVP
- estimated adaptation effort
- major risks

**Step 3: Pick a baseline**

Choose one repo to adapt, or explicitly decide to go greenfield.

**Step 4: Log the decision**

Record the selected baseline and reasons in `DECISIONS.md`.

### Task 5: Freeze the Initial Stack and Architecture Slice

**Files:**
- Modify: `ARCHITECTURE.md`
- Modify: `DECISIONS.md`
- Modify: `REQUIREMENTS.md`
- Create: `docs/mvp-slice.md`

**Step 1: Confirm runtime shape**

Document whether the MVP is CLI, desktop, web, service, or hybrid.

**Step 2: Define the minimal architecture slice**

Specify the entry point, core logic boundary, adapter boundary, configuration approach, and test approach.

**Step 3: Lock stack choice**

Document the selected language/framework and why it fits the chosen baseline and MVP.

### Task 6: Build the First Runnable Version

**Files:**
- Modify: `apps/...`
- Modify: `packages/...`
- Modify: `scripts/...`
- Modify: `tests/...`
- Modify: `TASKS.md`
- Modify: `STATE.md`

**Step 1: Create a failing run or test expectation**

Define the minimal expected runnable behavior before implementation.

**Step 2: Implement the smallest working path**

Build only enough code to complete the MVP scenario.

**Step 3: Verify local run path**

Run the narrowest possible verification command for the chosen stack.

**Step 4: Document how to run**

Add the exact local run steps and known limitations.

**Step 5: Update state and tasks**

Move bootstrap tasks to done and set the next milestone.

### Task 7: Stabilize for Multi-Session Delivery

**Files:**
- Modify: `STATE.md`
- Modify: `TASKS.md`
- Modify: `DECISIONS.md`

**Step 1: Compress history**

Replace outdated details with a concise summary.

**Step 2: Record unresolved risks**

Keep only active blockers and decisions that still influence implementation.

**Step 3: Prepare handoff**

Ensure the next session can continue without depending on chat memory.
