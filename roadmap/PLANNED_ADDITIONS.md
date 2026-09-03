# Planned Additions

This list is intentionally nonbinding. Each item enters only after its source, status, verifier, and public boundary are clean.

## Near-term Coppalini Architecture additions

- **Exact Constraint Certificates in Standard-Model Gauge Structure** — paper plus exact verifier, once the canonical public artifact and receipt are assembled.
- **Motion & Difference** — broader provenance/result paper; useful as a flagship application, but not required for the first Han/Zenodo release because `Compatibility Without Flatness` now carries the relevant gauge witness more directly.
- **Mirror_Audit v1.0** — publish as a domain-general first-obstruction protocol after separating the generic instrument from application-specific historical receipts.
- **MoneyRoot v0.3 / T7** — add only after the exact v0.3 Lean source receives an elaboration/axiom receipt comparable to v0.2.
- **Architecture Receipt schema** — machine-readable source -> reader -> operation -> decision -> status -> open-edge record.
- **CI for pinned Lean** — run the exact MoneyRoot source in the declared Lean 4.33.0 environment on each tagged release.

## Separate repository: Language Mechanics

Language Mechanics should remain a distinct publication surface. Its role is foundational field formalism rather than the architecture/tooling surface collected here.

Candidate initial sequence:

```text
000  Field Basis and Charter
001  Condition & Constraint
002  Form & Fit
003  Form Λ Fit Δ Function
004  Identity & Reference
005  Matrix Admissibility
006  Minimum Formal / Mechanical Reference
007  Memory Return
008  Persistence & Endurance
009  Dihedral Phase Constraint
010  Minimum Root Algebra
011  Occurrence and the Twenty-Eight-Seam Reader
```

Mirror Audit and the Closed Results Register can be referenced from both repositories without merging their jurisdictions.
