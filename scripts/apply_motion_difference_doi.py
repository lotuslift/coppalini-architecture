#!/usr/bin/env python3
"""Create the citation-only CCLQG v1.1.1 source after Motion and Difference gets a DOI.

The only permitted source mutation is the Motion and Difference bibliography item.
No theorem, equation, body text, date, or other reference is changed.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "papers" / "continuum-closure-covariant-lqg" / "CONTINUUM_CLOSURE_COVARIANT_LQG_CANONICAL_v1_1.tex"
DEFAULT_OUTPUT = ROOT / "papers" / "continuum-closure-covariant-lqg" / "CONTINUUM_CLOSURE_COVARIANT_LQG_CANONICAL_v1_1_1.tex"

OLD_BLOCK = r'''\bibitem{CoppaMotionDifference2026}
A. V. Coppa,
``Motion and Difference,''
Coppalini Architecture preprint (2026).'''

DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("doi", help="DOI only, e.g. 10.5281/zenodo.12345678")
    ap.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()

    doi = args.doi.strip()
    if doi.lower().startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    if not DOI_RE.fullmatch(doi):
        raise SystemExit(f"Refusing malformed DOI: {doi!r}")

    src = args.input.read_text(encoding="utf-8")
    if src.count(OLD_BLOCK) != 1:
        raise SystemExit("Expected exactly one canonical Motion and Difference bibliography block; refusing patch.")

    new_block = OLD_BLOCK + f"\ndoi:{doi}."
    out = src.replace(OLD_BLOCK, new_block)

    # Strong mutation guard: remove the one intended added line and demand byte-identical source.
    restored = out.replace(f"\ndoi:{doi}.", "", 1)
    if restored != src:
        raise SystemExit("Mutation guard failed; refusing output.")

    args.output.write_text(out, encoding="utf-8")

    diff = "".join(difflib.unified_diff(
        src.splitlines(True), out.splitlines(True),
        fromfile=str(args.input), tofile=str(args.output), n=3,
    ))
    print(diff, end="")
    print(f"WROTE: {args.output}")
    print("SCOPE: bibliography-only DOI addition for CoppaMotionDifference2026")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
