# C++20 Atomic Audit Kernels

These programs are the public, domain-neutral core of the current C++20 `static_assert` work.

They intentionally avoid the older thematic/color vocabulary used in exploratory models. The purpose here is to expose the minimum mechanics that are reusable across domains.

## `atomic_reference_kernel.cpp`

Types:

```text
Reference
Receipt
State
ReferenceTransport
Gate
Refusal
```

Compile-time witnesses check:

1. a nontrivial quarter-turn traverses Difference and returns the reference;
2. a successful return advances an occurrence receipt;
3. identity transport may still produce a new occurrence;
4. a broken inverse is refused without receipt advance;
5. an out-of-domain reference is refused before transport.

## `claim_motion_gate.cpp`

Types candidate relation motion as:

```text
preserve | coarsen | refine | strengthen | extend_scope
```

The relation itself must already be validated by an external reader/adapter. The kernel checks only the additional warrant required by the declared motion:

```text
refine       -> bridge required
strengthen   -> strength warrant required
extend_scope -> scope warrant required
```

An unvalidated relation returns `unknown` rather than manufacturing authority from its motion label.

## Compile

```bash
g++ -std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror \
  atomic_reference_kernel.cpp -o atomic_reference_kernel
./atomic_reference_kernel

g++ -std=c++20 -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror \
  claim_motion_gate.cpp -o claim_motion_gate
./claim_motion_gate
```
