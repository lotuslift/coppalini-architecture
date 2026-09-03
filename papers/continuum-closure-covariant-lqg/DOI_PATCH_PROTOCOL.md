# CCLQG v1.1 -> v1.1.1 DOI-only protocol

The current v1.1 source already cites *Motion and Difference* as `CoppaMotionDifference2026`. Once the Zenodo DOI is known, the intended revision adds exactly one line to that bibliography item:

```tex
\bibitem{CoppaMotionDifference2026}
A. V. Coppa,
``Motion and Difference,''
Coppalini Architecture preprint (2026).
doi:10.5281/zenodo.XXXXXXX.
```

Run:

```bash
python scripts/apply_motion_difference_doi.py 10.5281/zenodo.XXXXXXX
```

The generated source is `CONTINUUM_CLOSURE_COVARIANT_LQG_CANONICAL_v1_1_1.tex`.

## Verified layout expectation

A dry run with a same-form placeholder Zenodo DOI was compiled against the canonical v1.1 source. The resulting PDF remained seven pages, and pixel comparison showed pages 1-6 byte-render-equivalent at the comparison resolution; only page 7 changed, inside the final Motion and Difference reference entry.

This protocol therefore preserves the user's instruction: **references page only**.
