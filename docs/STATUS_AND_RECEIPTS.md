# Status and Receipt Law

Coppalini Architecture separates the truth-status of a proposition from the availability of evidence and from the administrative status of a project artifact.

## Core statuses

`DECLARED`
: A definition, coordinate choice, convention, scope, or interface has been explicitly fixed. Declaration is not proof.

`DERIVED`
: The result follows from stated premises by displayed reasoning, but may not yet have an independent executable/proof receipt.

`COMPUTED`
: A deterministic calculation or finite search has been executed and retained. The status is exact only for the declared computation domain.

`CERTIFIED`
: The claim passed its declared proof/audit gate and has an inspectable receipt.

`OPEN`
: A required calculation, map, adapter, witness, or source authority remains missing.

`REFUSED`
: A required gate fails. The failed operation is not admitted under the current conditions.

`UNAVAILABLE`
: Information required to evaluate the proposition is not accessible in the current environment. This is not a proof of impossibility or falsity.

## Status monotonicity

A stronger status must carry the receipt that licenses the upgrade. A label cannot upgrade itself.

Examples:

- a finite regression pass does not become a universal proof;
- a theorem about arbitrary functions does not become an empirical economic claim;
- a semiclassical black-hole identity does not become a microscopic quantum-gravity derivation;
- a missing model-specific calculation remains open even when the surrounding compatibility theorem is closed.

## First-failure receipt

When an audit fails, record the first load-bearing obstruction before editing the candidate. A minimum failure receipt contains:

```text
source/version
operation
first failed gate
required relation
observed residual
status
next admissible repair, if one is known
```

This prevents later repairs from erasing the reason the repair was needed.

## Append-only principle

A new receipt may supersede an earlier status for a later version, but it does not rewrite the earlier occurrence. Preserve hashes/version identifiers so the transition itself remains inspectable.
