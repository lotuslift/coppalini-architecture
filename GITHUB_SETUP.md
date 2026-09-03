# GitHub publication setup

## Repository

Recommended public repository name:

```text
coppalini-architecture
```

Display title:

```text
Coppalini Architecture
```

Suggested GitHub description:

> Formal interface audit, reference preservation, reader sufficiency, proof receipts, and selected mathematical applications.

Suggested topics:

```text
formal-methods
verification
lean4
cpp20
static-analysis
reproducible-research
interface-design
mathematical-physics
audit
provenance
```

## First publication sequence

1. Review `LICENSING.md` and select the public code/document licenses.
2. Create a public GitHub repository named `coppalini-architecture`.
3. Push this seed to the default `main` branch.
4. Confirm the GitHub Actions `core-checks` workflow passes.
5. Keep the repository at `v0.1.0` scope: method + three executable kernels + the three selected papers.
6. Build the paper-specific Zenodo packet:

   ```bash
   ./scripts/build_zenodo_bundle.sh
   ```

7. Deposit `Compatibility Without Flatness v0.1` as its own Zenodo research object and preserve the assigned DOI plus deposited hashes.
8. Replace the broad supporting citation in CCLQG with the new DOI in a citation-only `v1.1.1` revision; verify that the mathematical body is byte/semantic-equivalent except for bibliography/citation-access text.
9. Send the Han package only after that DOI is live.
10. Create a repository-wide tagged release/DOI later, after the public software identity and licensing are stable.

## Why the first repository stays small

The purpose of v0.1 is to let an unfamiliar reader answer three questions quickly:

1. **What is the method?** — `docs/`
2. **Is any of it executable?** — `tools/`
3. **What has it produced under hard formal stress?** — `papers/`

The larger corpus can be added after these three interfaces are legible.

## Language Mechanics

Do not place the Language Mechanics field packet under this repository merely because it is related. Publish it separately when its minimum root formalism and charter are ready. Cross-link the repositories later.
