#!/bin/bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -d /workspace/openrsi-game ]; then ROOT_DIR=/workspace/openrsi-game; fi
mkdir -p "$ROOT_DIR/candidate"
cp "$ROOT_DIR/reference/policy.py" "$ROOT_DIR/candidate/policy.py"
