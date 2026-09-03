# MIRROR_CUT v0.1

**Read-only reference auditor with deterministic receipts.**

MIRROR_CUT compares one explicit candidate motion against one explicit active reference, makes a bounded admissibility cut, and emits a SHA-256-addressed receipt.

```text
active reference
      |
      v
candidate motion -> mirror -> Exact | MotionPreserved | ClassBroken | Unknown
                                |          |              |           |
                                +---- can --+           refuse      defer
```

It does not generate the candidate, rewrite the source, or infer hidden model state.

## Reference binding

A candidate declares the exact SHA-256 digest of the reference against which it was composed. A stale or absent base digest is therefore visible before any later semantic/application adapter is consulted.

An explicit candidate move may be:

- `observe` — add non-protected content;
- `preserve` — reproduce a protected lock exactly;
- `update` — propose a changed protected value with explicit evidence;
- `substitute` — silently replace a protected value; always rejected.

An evidence-backed `update` may be classified as permitted motion, but MIRROR_CUT does **not** commit it. The output contains only a proposed next-reference digest.

## Classification

`Exact`
: protected reference returns unchanged.

`MotionPreserved`
: nontrivial lawful motion occurs while the protected reference survives, or an evidence-backed update is proposed without commit.

`ClassBroken`
: stale base, silent substitution, false preservation claim, unearned update, or upstream host refusal.

`Unknown`
: the declared packet does not contain enough information to classify safely.

Gate:

```text
Exact            -> can
MotionPreserved  -> can
ClassBroken      -> refuse
Unknown          -> defer
```

## Evidence/status boundary

Reference packets may carry evidence labels such as:

```text
CERT | DERIVED | DECLARED | POLICY | UNKNOWN | UNAVAILABLE | OPEN
```

These labels are kept distinct from the motion classification. In particular:

```text
UNAVAILABLE != impossible
UNKNOWN     != false
POLICY      != theorem
```

## CORDIS self-description

```text
Codomain  AuditReceipt {Exact | MotionPreserved | ClassBroken | Unknown}
Operation mirror_cut(reference, candidate, tolerance_stage)
Receipt   deterministic SHA-256 audit receipt
Domain    one active reference + one candidate bound to its base digest
Invariant read-only audit; no silent overwrite of protected locks
Symmetry  canonical JSON key ordering leaves semantics/digests unchanged
```

Inspect it directly:

```bash
python3 mirror_cut.py cordis
```

## Regression checks

```bash
python3 mirror_cut.py self-test
python3 test_mirror_cut.py
```

Expected test-suite output:

```text
PASS: 12 protocol checks + 64 D4 transport pairs
```

The D4 census is a finite regression witness for the classification machinery. It is **not** a claim that natural-language semantics are D4.

## Example

A complete valid packet and its deterministic receipt are included under `examples/`:

```bash
python3 mirror_cut.py audit examples/example_packet.json
```

Exit codes:

```text
0  can
2  malformed packet
3  defer
4  refuse
```

## Recommended use with language models

A model need not expose private chain-of-thought. It can construct a small public audit packet containing only externally meaningful commitments:

1. declare the relevant protected references;
2. bind the candidate to that exact reference digest;
3. describe candidate motions as `observe`, `preserve`, `update`, or `substitute`;
4. run the mirror;
5. revise/stop on `defer` or `refuse`;
6. append the returned receipt after an admitted motion.

The packet is an interface record, not a hidden-reasoning transcript.

## Scope wall

MIRROR_CUT v0.1 does not:

- access model weights, hidden activations, training state, or private reasoning;
- replace host safety/security policy;
- infer semantic truth from the D4 regression witness;
- autonomously rewrite persistent memory;
- perform broad natural-language fact checking.

Those require separate readers, authorities, and adapters.
