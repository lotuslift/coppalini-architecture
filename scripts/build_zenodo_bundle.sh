#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/papers/compatibility-without-flatness"
META="$ROOT/zenodo/compatibility-without-flatness-v0.1/METADATA_DRAFT.txt"
OUTDIR="${1:-$ROOT/build/zenodo-compatibility-without-flatness-v0.1}"
mkdir -p "$OUTDIR"
cp "$SRC/COMPATIBILITY_WITHOUT_FLATNESS_v0_1.pdf" "$OUTDIR/"
cp "$SRC/COMPATIBILITY_WITHOUT_FLATNESS_v0_1.tex" "$OUTDIR/"
cp "$META" "$OUTDIR/"
(
  cd "$OUTDIR"
  sha256sum COMPATIBILITY_WITHOUT_FLATNESS_v0_1.pdf \
            COMPATIBILITY_WITHOUT_FLATNESS_v0_1.tex \
            METADATA_DRAFT.txt > ZENODO_SHA256SUMS.txt
)
echo "$OUTDIR"
