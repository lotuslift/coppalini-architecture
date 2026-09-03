#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/receipts/SHA256SUMS"
cd "$ROOT"
find docs tools papers zenodo -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum > "$OUT"
echo "wrote $OUT"
