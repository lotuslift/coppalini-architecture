# Coppalini Architecture

**Formal interface audit, reference preservation, and evidence-bearing closure.**

Coppalini Architecture is a formal systems architecture developed by **Anthony Vito Coppa** for preserving definitions, constraints, evidence, and claim boundaries as they move across representations and domains.

The working rule is simple:

> **No required relation is dropped; no unsupported relation is added.**

That sentence is a method-level compression, not a replacement for domain mathematics. Native mathematics, physics, law, engineering, and evidence retain native authority. The architecture supplies a typed interface for asking what survives a transformation, what does not, and what remains open.

## What is here

This repository begins deliberately small. Version 0.1 contains three layers:

1. **Method** — minimum public definitions, audit order, status law, and receipt discipline.
2. **Executable kernels** — a read-only reference auditor, a Lean reader-sufficiency kernel, and C++20 compile-time reference/claim-motion checks.
3. **Selected research applications** — compact papers chosen because they expose the same interface problem in distinct mathematical settings, plus one broader provenance/result paper retained as an archival witness.

The repository is not intended to be the complete research corpus.

## Core question

Let a source state be read through

\[
R:X\to C
\]

and let a downstream decision or property be

\[
D:X\to A.
\]

A necessary and sufficient condition for `D` to be determined by the information retained in `R` is that `D` be constant on every fiber of `R`:

\[
R(x)=R(y)\Longrightarrow D(x)=D(y).
\]

One witness

\[
R(x)=R(y),\qquad D(x)\neq D(y)
\]

is therefore an obstruction certificate: the read is insufficient for that declared decision. The Lean implementation is in [`tools/moneyroot`](tools/moneyroot/).

## Tools

### MIRROR_CUT

[`tools/mirror-cut`](tools/mirror-cut/) is a read-only reference audit sidecar. A candidate declares the exact SHA-256 digest of the reference it was composed against. Silent substitution is refused; an evidence-backed update may be proposed but is never committed by the auditor. The tool emits deterministic receipts and has a finite regression suite.

### MoneyRoot v0.2

[`tools/moneyroot`](tools/moneyroot/) contains the certified Lean 4.33.0 theorem kernel for reader sufficiency, decision collisions, exact recoverability, explicit reader→policy→controller composition, supplemental reads, and residual-distinction necessity. Empirical economic or legal adapters are outside the theorem kernel.

### C++20 atomic kernels

[`tools/cpp`](tools/cpp/) contains two deliberately neutral compile-time witnesses:

- `atomic_reference_kernel.cpp` — admissible transport, nontrivial Difference, exact Return, receipt growth, and refusal of broken/out-of-domain transport;
- `claim_motion_gate.cpp` — preserve/coarsen/refine/strengthen/scope-extension checks on **already-typed, externally validated** relations.

These files do not infer semantics from raw natural language. They check relations after an external reader or adapter has typed them.

## Selected papers

### Motion and Difference

[`papers/motion-and-difference`](papers/motion-and-difference/)

A broader compatibility construction spanning projective dynamics, Fibonacci structure, hyperbolic geometry, and a Lorentzian `SO(2)` gauge field. Its gauge sector supplies the exact-gluing/nonflatness witness cited by the continuum-closure paper. A Zenodo archival DOI is now a near-term release target.

### Continuum Closure in Covariant Loop Quantum Gravity

[`papers/continuum-closure-covariant-lqg`](papers/continuum-closure-covariant-lqg/)

A compatibility criterion separating exact gluing of local descriptions from physical flatness, then requiring gravitational-sector selection, refinement-compatible physical-state descent, and survival of a nonzero transverse-traceless spin-two residue. The model-specific UV test remains open.

### Compatibility Without Flatness

[`papers/compatibility-without-flatness`](papers/compatibility-without-flatness/)

A compact Lorentzian `SO(2)` witness showing that exact local gluing can coexist with nonzero source-free curvature, nontrivial holonomy, and unequal proper time. This is the immediate archival/DOI target supporting the continuum-closure paper.

### Coarse-Grained Entropy and Exterior Records

[`papers/coarse-grained-entropy-and-exterior-records`](papers/coarse-grained-entropy-and-exterior-records/)

A short companion note moving in the opposite direction: from a many-to-one macroscopic read to the compatible microscopic fiber, Boltzmann multiplicity, and the exact limit on what a downstream exterior record can reconstruct. Its black-hole use is explicitly semiclassical; microscopic quantum-gravity entropy remains outside its claim boundary.

## Method in one line

```text
type the relation -> audit its transport -> repair the interface -> certify what survives
```

The full public basis is in [`docs/METHODOLOGY_BASIS.md`](docs/METHODOLOGY_BASIS.md).

## Status discipline

This repository distinguishes at least:

- `DECLARED` — a definition, coordinate, convention, or chosen interface;
- `DERIVED` — follows from displayed premises;
- `COMPUTED` — verified by an explicit finite/deterministic computation;
- `CERTIFIED` — passed the declared proof or audit gate with a retained receipt;
- `OPEN` — a required map, warrant, calculation, or witness is still missing;
- `REFUSED` — a required gate fails;
- `UNAVAILABLE` — the required information is not presently accessible.

An open application does not reopen a closed generic theorem. A generic theorem does not certify an application whose own adapter or evidence is missing.

See [`STATUS.md`](STATUS.md) for the current component ledger.

## Reproduce the executable checks

```bash
make test
```

The default test target runs the Python MIRROR_CUT regression suite and compiles/runs both C++20 kernels with the available local compiler. The Lean source is pinned by `lean-toolchain`; its independent v0.2 elaboration receipt is preserved in the repository. `make test-lean` runs it when Lean 4.33.0 is installed.

## Repository boundary

This repository is the **architecture/tooling and selected-application surface**. The broader foundational field **Language Mechanics** is intentionally not folded into it. That field has its own charter, formal basis, root algebra, and proof sequence and is better published as a separate repository when ready.

Planned additions are listed in [`roadmap/PLANNED_ADDITIONS.md`](roadmap/PLANNED_ADDITIONS.md).

## Citation and archival releases

Repository-level citation metadata is in [`CITATION.cff`](CITATION.cff). Research use should cite the specific paper/result whenever possible.

Two immediate archival targets are **Compatibility Without Flatness** and **Motion and Difference**. Preparation files live under [`zenodo/`](zenodo/). CCLQG v1.1 already cites *Motion and Difference*; once that record receives a DOI, `scripts/apply_motion_difference_doi.py` generates a bibliography-only v1.1.1 source without changing the mathematical content.

## Licensing

No public license is silently assumed in this seed. A proposed split—permissive software license for code and CC BY for papers/documentation—is recorded in [`LICENSING.md`](LICENSING.md) for author selection before public release.
