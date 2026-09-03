# Coppalini Architecture — Methodology Basis

## 1. Purpose

Coppalini Architecture audits transformations whose outputs will be trusted by another reader or used for another decision.

The central object is not a slogan or a universal physical ontology. It is an **interface**:

```text
source -> read/representation -> operation -> downstream decision
```

The method asks whether the information, constraints, definitions, and evidentiary authority required downstream survive that passage.

## 2. Native authority

Every application begins inside the native domain.

- A physical theorem keeps the hypotheses and variables of its physical source.
- A legal rule keeps its jurisdiction and authority chain.
- A contract keeps its controlled source and change procedure.
- A dataset keeps its measurement and provenance limits.
- A formal proof keeps its exact assumptions and proof system.

Cross-domain vocabulary does not create a theorem. A transfer requires an explicit adapter whose preservation burden can be inspected.

## 3. Minimum audit object

A claim-level audit can be represented as

\[
\mathcal A=(J,C,Q,T,R,I,W,F,\Sigma),
\]

where:

- `J` — jurisdiction / domain of authority;
- `C` — entry condition;
- `Q` — continuation constraint;
- `T` — operation or transport;
- `R` — reader / representation;
- `I` — preservation target or invariant;
- `W` — witness;
- `F` — falsifier / failure condition;
- `Σ` — receipt sufficient to inspect the claim later.

The letters are local notation only; the office is primary.

## 4. Audit order

The public first-failure order is:

```text
Type
  -> Condition
  -> Constraint
  -> Transport
  -> Preservation
  -> Return
  -> Receipt
  -> Witness
  -> Falsifier
```

A downstream gate is not used to repair an upstream typing failure.

### Type
What are the source objects, outputs, maps, decisions, and authorities? Are similarly named objects actually of the same type?

### Condition
When does this operation begin to have authority?

### Constraint
What must remain true for continuation to be admissible?

### Transport
What operation actually carries the source into the new representation or state?

### Preservation
Which relations must survive the transport?

### Return
What counts as the same reference being recovered after the operation? Return is always declared relative to a reader or invariant; it is not automatically full state identity.

### Receipt
What record lets another reader reconstruct what was done, under which source, version, and evidence?

### Witness
What explicit object, calculation, example, proof term, or dataset shows the claim is inhabited?

### Falsifier
What observable failure would defeat the claim?

## 5. Reader sufficiency

Let

\[
R:X\to C
\]

be a read and

\[
D:X\to A
\]

be a downstream decision/property. The generic sufficiency condition is

\[
R(x)=R(y)\Longrightarrow D(x)=D(y).
\]

Equivalently, `D` factors through the quotient induced by equality at `R`.

A **decision collision** is an explicit pair

\[
R(x)=R(y),\qquad D(x)\neq D(y).
\]

One such pair refutes every rule that attempts to determine `D` from `R` alone.

This theorem is implemented in `tools/moneyroot` and deliberately contains no economic, legal, or physical premise.

## 6. Atomic motion classes

Once a relation has been typed and externally validated, a candidate operation may be classified by what it asks the relation to do.

- **Preserve** — carry the relation without changing its strength or scope.
- **Coarsen** — deliberately discard distinctions not required by the declared downstream use.
- **Refine** — add resolution; requires a bridge or additional source.
- **Strengthen** — promote the logical force of a claim; requires independent warrant.
- **Extend scope** — carry a claim into a broader jurisdiction; requires scope authority.

The motion label does not prove the relation. It only exposes the additional authority required by the requested operation.

## 7. Drop, add, strengthen

Three failure modes are kept separate:

- **Drop** — a required relation is no longer recoverable.
- **Add** — an unsupported relation enters the output.
- **Strengthen** — a source relation is preserved in subject matter but promoted beyond its warranted logical force.

The method-level target is zero required drop and zero unsupported addition, with claim strength no greater than its source warrant unless an explicit strengthening proof is supplied.

## 8. Adapters

An adapter is a declared map between independently typed offices or representations. A valid adapter states:

1. source and target domains;
2. the operation performed;
3. the relations promised to survive;
4. the information deliberately lost or left unresolved;
5. the decision for which the translation is intended;
6. the evidence that licenses the transfer.

A useful presentation may be highly reader-specific while still preserving one invariant source. Tailoring the entrance is permitted; changing the theorem is not.

## 9. Read before write

An audit operation must not silently overwrite the reference it reads.

`MIRROR_CUT` implements this mechanically: a candidate is bound to the SHA-256 digest of the active reference; evidence-backed changes are returned as proposed next references; commit remains outside the auditor.

This separates:

```text
inspect -> classify -> propose -> commit
```

instead of allowing inspection itself to rewrite the inspected state.

## 10. Receipts

Receipts are append-only evidence of occurrence, not substitutes for proof.

A useful receipt records, as applicable:

- source/version/hash;
- declared jurisdiction;
- inputs and outputs;
- operation performed;
- status;
- witness or proof command;
- first failure, if any;
- remaining open edge.

A later application may reuse a result only at the resolution its receipt warrants.

## 11. Status law

The minimum public statuses are:

- `DECLARED`
- `DERIVED`
- `COMPUTED`
- `CERTIFIED`
- `OPEN`
- `REFUSED`
- `UNAVAILABLE`

Uncertainty belongs to the proposition that owns it. `OPEN` is not `false`; `UNAVAILABLE` is not `impossible`; a policy declaration is not a theorem.

## 12. Construction as well as audit

The method is not limited to rejecting bad translations. When a seam fails, the constructive operation is:

```text
type the relation
-> locate the first failed interface
-> determine the residual distinction
-> construct the smallest warranted adapter/supplement
-> rerun the audit
-> retain the receipt
```

No canonical “smallest” repair is assumed to exist without a declared candidate class and selection order. `MoneyRoot` makes this stop line explicit.

## 13. Domain stress testing

The selected papers in this repository are stress tests of the same interface discipline across different native mathematics:

- gauge/gluing geometry: compatibility without forcing flatness;
- covariant LQG: refinement/physical-state closure while retaining a spin-two physical witness;
- thermodynamics: coarse reads, compatible microstate multiplicity, and the limits of record reconstruction.

The shared architecture does not make these fields identical. Each application imports its own native mathematics and keeps its own open frontier.
