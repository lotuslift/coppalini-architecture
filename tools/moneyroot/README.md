# MoneyRoot v0.2

A minimum Lean kernel for the recurring distinction between a source state, a read/coordinate, and a downstream decision.

## Scope

The kernel is generic. It assumes arbitrary types and functions; it does not import an economic, legal, physical, or policy premise.

The central reader-sufficiency law is:

```text
R x = R y -> D x = D y
```

A same-read/different-decision witness is a `DecisionCollision` and refutes any factorization of `D` through `R` alone.

## Contents

- `EqKernel` — equality relation induced by an arbitrary reader;
- `FiberRefines` — downstream decision is constant on reader fibers;
- `ReadQuot` / `FactorsThroughRead` — quotient formulation of sufficiency;
- T1 — injectivity/read-equality relation;
- T2 — quotient factorization iff fiber refinement;
- T3 — decision-collision obstruction certificate;
- T4 — exact recovery requires injectivity;
- T5 — reader -> policy adapter -> controller path;
- T6 — joint supplemental reads and residual-distinction necessity.

T6 deliberately stops before asserting a canonical minimum supplement. Selecting a least repair requires an additional candidate class and selection order.

## Certified build

Pinned toolchain:

```text
leanprover/lean4:v4.33.0
```

The retained independent receipt records:

```text
lean MoneyRoot_v0_2.lean
exit code 0
stdout: empty
stderr: empty
source unchanged after run
0 sorry/admit/user-axiom matches
```

See `receipts/LEAN_RECEIPT_SUMMARY_v0_2.txt` for exact hashes and axiom-dependency inspection.

## Run

With Lean 4.33.0 available:

```bash
lean MoneyRoot_v0_2.lean
```

The theorem kernel certifies only its own generic formal statements. Application adapters require their own evidence and jurisdiction.
