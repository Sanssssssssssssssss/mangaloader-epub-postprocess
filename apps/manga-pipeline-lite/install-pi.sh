#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./apps/manga-pipeline-lite/install-pi.sh [--skip-apt] [--kcc-version <tag>]

Options:
  --skip-apt            Skip apt-get install steps.
  --kcc-version <tag>   KCC git tag to install. Default: v9.6.2

Environment:
  PICLAW_ROOT           Override the install root. Defaults to the repo root.
  KCC_REPO_URL          Override the KCC git repository URL.
  RUSTUP_INIT_URL       Override the rustup install script URL.
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="${PICLAW_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
TOOLS_DIR="$ROOT_DIR/.tools/manga-pipeline-lite"
KCC_SRC_DIR="$TOOLS_DIR/kcc-src"
KCC_VENV_DIR="$TOOLS_DIR/kcc-venv"
KCC_BIN_DIR="$TOOLS_DIR/bin"
KCC_REPO_URL="${KCC_REPO_URL:-https://github.com/ciromattia/kcc.git}"
RUSTUP_INIT_URL="${RUSTUP_INIT_URL:-https://sh.rustup.rs}"
KCC_VERSION="v9.6.2"
SKIP_APT=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-apt)
      SKIP_APT=1
      shift
      ;;
    --kcc-version)
      KCC_VERSION="${2:-}"
      if [[ -z "$KCC_VERSION" ]]; then
        echo "Missing value for --kcc-version" >&2
        exit 64
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

if [[ "$SKIP_APT" -eq 0 ]]; then
  sudo apt-get update
  sudo apt-get install -y \
    build-essential \
    ca-certificates \
    curl \
    git \
    perl \
    p7zip-full \
    pkg-config \
    python3 \
    python3-pip \
    python3-venv \
    python3-packaging \
    python3-pil \
    python3-psutil \
    python3-slugify
fi

mkdir -p "$TOOLS_DIR" "$KCC_BIN_DIR"

if ! command -v cargo >/dev/null 2>&1; then
  curl --proto '=https' --tlsv1.2 -sSf "$RUSTUP_INIT_URL" | sh -s -- -y --profile minimal
fi

if [[ -f "$HOME/.cargo/env" ]]; then
  # shellcheck disable=SC1090
  source "$HOME/.cargo/env"
fi

if [[ -d "$KCC_SRC_DIR/.git" ]]; then
  git -C "$KCC_SRC_DIR" fetch --depth 1 origin "refs/tags/$KCC_VERSION:refs/tags/$KCC_VERSION"
  git -C "$KCC_SRC_DIR" checkout --force "$KCC_VERSION"
else
  git clone --depth 1 --branch "$KCC_VERSION" "$KCC_REPO_URL" "$KCC_SRC_DIR"
fi

python3 -m venv "$KCC_VENV_DIR"
"$KCC_VENV_DIR/bin/pip" install --upgrade pip setuptools wheel
"$KCC_VENV_DIR/bin/pip" install \
  packaging \
  requests \
  natsort \
  numpy \
  distro \
  python-slugify \
  PyMuPDF \
  mozjpeg-lossless-optimization \
  pillow \
  psutil

cat > "$KCC_BIN_DIR/kcc-c2e" <<EOF
#!/usr/bin/env bash
set -euo pipefail
exec "$KCC_VENV_DIR/bin/python3" "$KCC_SRC_DIR/kcc-c2e.py" "\$@"
EOF

chmod +x "$KCC_BIN_DIR/kcc-c2e"
printf '%s\n' "$KCC_VERSION" > "$TOOLS_DIR/kcc-version.txt"

cargo build --release --locked --manifest-path "$ROOT_DIR/apps/copymanga-headless-rs/Cargo.toml"
cp "$ROOT_DIR/apps/copymanga-headless-rs/target/release/copymanga-headless-rs" \
  "$KCC_BIN_DIR/copymanga-headless-rs"
chmod +x "$KCC_BIN_DIR/copymanga-headless-rs"

cat <<EOF
Install complete.

Repo root: $ROOT_DIR
KCC source: $KCC_SRC_DIR
KCC venv:   $KCC_VENV_DIR
KCC wrapper:$KCC_BIN_DIR/kcc-c2e
Rust downloader:$KCC_BIN_DIR/copymanga-headless-rs

Next steps:
  1. Edit apps/manga-pipeline-lite/config.pi5.json if needed.
  2. Run:
     ./apps/manga-pipeline-lite/bin/manga-pipeline-lite doctor --config apps/manga-pipeline-lite/config.pi5.json
     ./apps/manga-pipeline-lite/bin/manga-pipeline-lite run --config apps/manga-pipeline-lite/config.pi5.json
EOF
