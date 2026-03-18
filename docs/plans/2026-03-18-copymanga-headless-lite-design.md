# Copymanga Headless Lite Design

## Goal
- Add the smallest practical headless downloader that fits the Raspberry Pi direction.
- Reuse what we learned from `imports/copymanga-downloader` without inheriting its Tauri desktop stack.
- Produce chapter image folders that can feed `manga-epub-packager-lite` directly.

## Scope
- In scope:
  - public API search
  - comic metadata lookup
  - group chapter listing
  - chapter image download into stable folders
  - Linux-friendly CLI execution
- Out of scope:
  - GUI
  - Tauri reuse in the first implementation
  - account pool auto-registration
  - favorites workflow
  - CBZ/PDF/EPUB export inside the downloader

## Approaches Considered

### Option A: Extract a Rust headless adapter from `copymanga-downloader`
- Pros:
  - highest direct reuse of upstream logic
  - closer behavioral match with the imported project
- Cons:
  - current code is wired around `AppHandle`, Tauri state, and desktop packaging
  - slower to reach a Pi-friendly runnable slice
  - would still leave us inside a Rust/Tauri-heavy maintenance surface

### Option B: Build a smaller Python CLI around the confirmed public API
- Pros:
  - lowest runtime and setup cost on Pi
  - easy to verify in WSL and Linux
  - can write chapter folders in the exact shape our packaging skill already consumes
- Cons:
  - partial reimplementation instead of direct code reuse
  - narrower feature coverage than upstream

### Option C: Keep the Tauri app on a stronger machine and only document transfer to Pi
- Pros:
  - almost no new code
  - uses upstream as-is
- Cons:
  - does not create a Pi-native automated path
  - weaker long-term automation fit

## Chosen Approach
- Choose Option B for the next milestone.
- Reason:
  - it best matches `D-014`
  - it satisfies the lightweight Pi constraint
  - the critical public API path has already been verified live:
    - search
    - comic metadata
    - group chapters
    - chapter page URLs
    - image fetch

## Proposed Deliverable
- Add `apps/copymanga-headless-lite/copymanga_downloader.py`.
- Provide these CLI commands:
  - `search`
  - `comic`
  - `chapters`
  - `download-chapter`
  - `download-group`
- Output layout:
  - `<output-root>/<comic-title>/<group-title>/<chapter-index> <chapter-name>/<page>.webp|jpg`

## Integration Path
- Step 1: use the downloader to materialize chapter image folders
- Step 2: point `skills/manga-epub-packager-lite/scripts/manga_packager.py` at one group folder
- Step 3: optionally merge the resulting EPUBs

## Assumptions
- Public chapter content remains accessible for the targeted workflow.
- Token-less access is enough for the first lightweight slice.
- If some content later requires login, token support can be added without changing the folder contract.

## Verification Plan
- Verify `search` against the live API in WSL.
- Verify `comic` and `chapters` against a known public title.
- Verify `download-chapter --max-images 2` writes at least two page files in WSL.

