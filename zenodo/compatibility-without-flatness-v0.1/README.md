# Zenodo deposit preparation — Compatibility Without Flatness v0.1

The immediate archival objective is a **paper-specific DOI** for `Compatibility Without Flatness`, so that `Continuum Closure in Covariant Loop Quantum Gravity` can cite the exact supporting witness rather than a broad corpus item.

Recommended deposit files:

```text
papers/compatibility-without-flatness/COMPATIBILITY_WITHOUT_FLATNESS_v0_1.pdf
papers/compatibility-without-flatness/COMPATIBILITY_WITHOUT_FLATNESS_v0_1.tex
ZENODO_SHA256SUMS.txt
```

The working metadata are in `METADATA_DRAFT.txt`.

After DOI assignment:

1. preserve the deposited file hashes;
2. add the DOI to this directory and the paper README;
3. make a citation-only v1.1.1 revision of the continuum-closure paper;
4. verify that no mathematical equation/theorem changed in that revision;
5. retain a new SHA-256 receipt.

The repository itself can receive a separate software/repository DOI later. The immediate scientific citation should point to the specific supporting paper.
