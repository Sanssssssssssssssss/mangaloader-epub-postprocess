# Raspberry Pi Delivery Kit

## Goal
- Make `manga-pipeline-lite` easier to hand off to a Raspberry Pi agent without introducing a heavy installer or GUI packaging flow.

## Chosen Shape
- Add `apps/manga-pipeline-lite/install-pi.sh`
- Add `apps/manga-pipeline-lite/config.pi5.json`
- Install KCC into repo-local `.tools/manga-pipeline-lite/`
- Expose a wrapper at `.tools/manga-pipeline-lite/bin/kcc-c2e`

## Why This Shape
- Keeps the runtime Linux-first and lightweight
- Avoids global dependency assumptions
- Makes the Pi path repeatable for both humans and agents
- Keeps product directories predictable

## Validation
- `install-pi.sh --skip-apt` succeeded in WSL
- `doctor --config apps/manga-pipeline-lite/config.pi5.json --check-network` succeeded
- A low-resource smoke run succeeded and produced `runs/pi5-delivery-smoke/merged/Fire_Force_Pi_Smoke.epub`
