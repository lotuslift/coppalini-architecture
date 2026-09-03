# Minimum Definitions

These are the domain-general offices used by Coppalini Architecture. They are intentionally smaller than the separate Language Mechanics formalism.

| Office | Minimum definition |
|---|---|
| **Jurisdiction** | The domain in which a statement, map, source, or rule has declared authority. |
| **Reference** | The source relation, state, version, or comparison target that an operation is required to preserve or explicitly update. |
| **Difference** | A declared distinction between typed objects. Difference need not be numerical unless the native domain supplies a numerical residual. |
| **Reader** | A map `R : X -> C` that exposes a declared coordinate or representation of a source state. |
| **Decision** | A downstream property/action/read `D : X -> A` whose required distinctions determine whether a reader is sufficient. |
| **Condition** | A requirement for entering an operation or claim jurisdiction. |
| **Constraint** | A relation that must hold for continuation to remain admissible. |
| **Operation** | A typed transformation with declared inputs, outputs, and authority. |
| **Transport** | An operation viewed specifically as carrying a reference or structure from one address/representation/state to another. |
| **Adapter** | An explicit map between independently typed representations or domains, together with its preservation burden. |
| **Invariant** | A declared relation that remains recoverable under the operation at the relevant reader. |
| **Return** | Recovery of the declared reference/invariant after transport. Return is reader-relative unless full state identity is explicitly proved. |
| **Receipt** | Retained evidence of what operation occurred, against which source/version, with what status and witness. |
| **Witness** | A concrete inhabitant of a claim: proof term, explicit construction, finite model, computation, dataset, or source evidence as appropriate. |
| **Falsifier** | A condition or witness that would defeat the declared claim. |
| **Admissibility** | The gate decision that the declared continuation satisfies every claim-relevant condition and constraint. |
| **Open edge** | A required relation, calculation, adapter, or evidence item that has not yet been supplied. |

## Reader sufficiency

For `R : X -> C` and `D : X -> A`, define reader sufficiency by

\[
R(x)=R(y)\Rightarrow D(x)=D(y).
\]

The decision can then descend through the equivalence classes induced by the reader.

A pair with the same read and different required decision is a **decision collision** and refutes read-only determination.

## Reference-preserving transport

For a transport `T` and reference reader `q`, a minimum return condition is

\[
q(Tx)=q(x).
\]

This does not imply `Tx=x`. A system may change while its declared reference remains recognizable.

## Receipt growth

A successful operation may preserve its reference while still producing a new occurrence:

\[
\Sigma_{n+1}=\Sigma_n\frown o_{n+1}.
\]

Thus returned reference and retained occurrence are separate offices.

## Exact-fit audit compression

For a declared operation:

```text
required relations present   -> no DROP
unsupported relations absent -> no ADD
claim force source-bounded   -> no unwarranted STRENGTHEN
```

When all claim-relevant requirements are witnessed, the local continuation may be certified. Missing authority remains `OPEN`; failed required gates are `REFUSED`.
