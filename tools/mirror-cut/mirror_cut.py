#!/usr/bin/env python3
"""MIRROR_CUT v0.1

A small, dependency-free machine self-audit sidecar.

Purpose:
  - hold one active reference state;
  - mirror a proposed motion against that state;
  - make one admissibility cut;
  - emit a deterministic receipt;
  - never mutate the active reference while auditing.

This implementation intentionally starts at tolerance stage +1:
  preserve the active reference unless the candidate explicitly proposes an
  evidence-backed update. Later rules can be added without changing the base
  protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from hashlib import sha256
import argparse
import json
import sys
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


VERSION = "0.1.0"


class AuditClass(str, Enum):
    EXACT = "Exact"
    MOTION_PRESERVED = "MotionPreserved"
    CLASS_BROKEN = "ClassBroken"
    UNKNOWN = "Unknown"


class Gate(str, Enum):
    CAN = "can"
    REFUSE = "refuse"
    DEFER = "defer"


class EvidenceClass(str, Enum):
    CERT = "CERT"
    DERIVED = "DERIVED"
    DECLARED = "DECLARED"
    POLICY = "POLICY"
    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    OPEN = "OPEN"


@dataclass(frozen=True)
class Cordis:
    codomain: str
    operation: str
    receipt: str
    domain: str
    invariant: str
    symmetry: str


@dataclass(frozen=True)
class AuditFinding:
    code: str
    message: str
    move_id: Optional[str] = None
    key: Optional[str] = None


@dataclass(frozen=True)
class AuditReceipt:
    tool: str
    version: str
    tolerance_stage: int
    reference_digest: str
    candidate_digest: str
    prior_receipt_digest: Optional[str]
    classification: str
    gate: str
    findings: Tuple[AuditFinding, ...]
    proposed_reference_digest: Optional[str]
    receipt_digest: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["findings"] = [asdict(f) for f in self.findings]
        return d


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(obj: Any) -> str:
    return sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def _normalize_locks(reference: Mapping[str, Any]) -> Dict[str, Any]:
    locks = reference.get("locks", {})
    if isinstance(locks, list):
        out: Dict[str, Any] = {}
        for item in locks:
            if not isinstance(item, Mapping) or "key" not in item:
                raise ValueError("reference.locks list entries require a key")
            key = str(item["key"])
            if key in out:
                raise ValueError(f"duplicate reference lock: {key}")
            out[key] = item.get("value")
        return out
    if not isinstance(locks, Mapping):
        raise ValueError("reference.locks must be an object or list")
    return {str(k): v for k, v in locks.items()}


def _candidate_moves(candidate: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    moves = candidate.get("moves", [])
    if not isinstance(moves, list):
        raise ValueError("candidate.moves must be a list")
    for move in moves:
        if not isinstance(move, Mapping):
            raise ValueError("each candidate move must be an object")
    return moves


def cordis_spec() -> Cordis:
    return Cordis(
        codomain="AuditReceipt {Exact | MotionPreserved | ClassBroken | Unknown}",
        operation="mirror_cut(reference, candidate, tolerance_stage)",
        receipt="deterministic SHA-256 audit receipt with findings and optional proposed reference digest",
        domain="one active ReferenceState and one CandidateMotion packet sharing the same base reference digest",
        invariant="auditing is read-only: the input reference bytes are never mutated; no candidate can silently overwrite a protected lock",
        symmetry="canonical JSON object-key permutation leaves semantic classification and digests unchanged",
    )


def check_cordis(spec: Cordis) -> Tuple[bool, Tuple[str, ...]]:
    defects = tuple(k for k, v in asdict(spec).items() if not isinstance(v, str) or not v.strip())
    return (not defects, defects)


def d4_multiply(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    ak, ae = a
    bk, be = b
    sign = 1 if ae == 0 else -1
    return ((ak + sign * bk) % 4, (ae + be) % 2)


def d4_class(x: Tuple[int, int]) -> str:
    if x == (0, 0):
        return "Exact"
    if x == (2, 0):
        return "BaseCentral"
    return "Residual"


def d4_self_test() -> Dict[str, Any]:
    """Exhaustive 8x8 finite regression witness inherited as a structural test.

    This validates the local classification machinery only. It does not claim
    natural-language semantics are D4.
    """
    elems = [(k, e) for e in (0, 1) for k in range(4)]
    census: Dict[Tuple[int, int], Tuple[int, int, int]] = {}
    for x in elems:
        static = motion = broken = 0
        start = d4_class(x)
        for g in elems:
            y = d4_multiply(x, g)
            if d4_class(y) != start:
                broken += 1
            elif y == x:
                static += 1
            else:
                motion += 1
        census[x] = (static, motion, broken)
        expected = (1, 0, 7) if start in ("Exact", "BaseCentral") else (1, 5, 2)
        if census[x] != expected:
            return {"ok": False, "element": x, "got": census[x], "expected": expected}
    return {"ok": True, "pairs_checked": 64, "elements_checked": 8}


def _make_receipt(
    *,
    tolerance_stage: int,
    reference_digest: str,
    candidate_digest: str,
    prior_receipt_digest: Optional[str],
    classification: AuditClass,
    gate: Gate,
    findings: Sequence[AuditFinding],
    proposed_reference_digest: Optional[str],
) -> AuditReceipt:
    body = {
        "tool": "MIRROR_CUT",
        "version": VERSION,
        "tolerance_stage": tolerance_stage,
        "reference_digest": reference_digest,
        "candidate_digest": candidate_digest,
        "prior_receipt_digest": prior_receipt_digest,
        "classification": classification.value,
        "gate": gate.value,
        "findings": [asdict(f) for f in findings],
        "proposed_reference_digest": proposed_reference_digest,
    }
    rd = digest(body)
    return AuditReceipt(
        tool="MIRROR_CUT",
        version=VERSION,
        tolerance_stage=tolerance_stage,
        reference_digest=reference_digest,
        candidate_digest=candidate_digest,
        prior_receipt_digest=prior_receipt_digest,
        classification=classification.value,
        gate=gate.value,
        findings=tuple(findings),
        proposed_reference_digest=proposed_reference_digest,
        receipt_digest=rd,
    )


def mirror_cut(packet: Mapping[str, Any]) -> AuditReceipt:
    """Run one read-only mirror and one admissibility cut.

    Stage 0 is reserved for an embedding system's physical-safety boundary.
    This reference implementation does not duplicate or replace host safety.

    Stage 1 enforces one rule only:
      a candidate may preserve an active lock, ignore it, or explicitly propose
      an evidence-backed update; it may not silently substitute a different
      value or operate from a stale base reference.
    """
    stage = int(packet.get("tolerance_stage", 1))
    if stage < 0:
        raise ValueError("tolerance_stage must be >= 0")

    reference = packet.get("reference")
    candidate = packet.get("candidate")
    if not isinstance(reference, Mapping) or not isinstance(candidate, Mapping):
        raise ValueError("packet requires object fields: reference and candidate")

    ref_digest = digest(reference)
    cand_digest = digest(candidate)
    prior_receipt = packet.get("prior_receipt_digest")
    findings: List[AuditFinding] = []

    # CMMM-like stable-reference precondition: a candidate declares the exact
    # reference digest it was composed against.
    base_digest = candidate.get("base_reference_digest")
    if base_digest is None:
        findings.append(AuditFinding(
            "BASE_REFERENCE_UNDECLARED",
            "candidate did not declare the reference digest it was composed against",
        ))
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=AuditClass.UNKNOWN,
            gate=Gate.DEFER,
            findings=findings,
            proposed_reference_digest=None,
        )
    if base_digest != ref_digest:
        findings.append(AuditFinding(
            "STALE_REFERENCE",
            "candidate base_reference_digest does not match the active reference",
        ))
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=AuditClass.CLASS_BROKEN,
            gate=Gate.REFUSE,
            findings=findings,
            proposed_reference_digest=None,
        )

    # Stage 0: the host system owns physical-safety semantics. If embedding
    # supplies an explicit host verdict, honor it without inventing one.
    host_safety = packet.get("host_safety")
    if host_safety == "refuse":
        findings.append(AuditFinding("HOST_SAFETY_REFUSAL", "host safety boundary refused the motion"))
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=AuditClass.CLASS_BROKEN,
            gate=Gate.REFUSE,
            findings=findings,
            proposed_reference_digest=None,
        )
    if host_safety not in (None, "can", "defer", "refuse"):
        findings.append(AuditFinding("HOST_SAFETY_UNKNOWN", "unrecognized host_safety value"))
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=AuditClass.UNKNOWN,
            gate=Gate.DEFER,
            findings=findings,
            proposed_reference_digest=None,
        )
    if host_safety == "defer":
        findings.append(AuditFinding("HOST_SAFETY_DEFER", "host safety boundary has not resolved the motion"))
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=AuditClass.UNKNOWN,
            gate=Gate.DEFER,
            findings=findings,
            proposed_reference_digest=None,
        )

    locks = _normalize_locks(reference)
    moves = _candidate_moves(candidate)
    proposed_locks = dict(locks)
    changed = False
    touched = False

    if stage == 0:
        # At stage 0 no semantic reference rule is enforced.
        classification = AuditClass.EXACT if not moves else AuditClass.MOTION_PRESERVED
        gate = Gate.CAN
        return _make_receipt(
            tolerance_stage=stage,
            reference_digest=ref_digest,
            candidate_digest=cand_digest,
            prior_receipt_digest=prior_receipt,
            classification=classification,
            gate=gate,
            findings=findings,
            proposed_reference_digest=None,
        )

    for idx, move in enumerate(moves):
        move_id = str(move.get("id", f"move-{idx}"))
        action = move.get("action", "observe")
        key = move.get("key")

        if action == "observe":
            continue

        if action == "preserve":
            touched = True
            if key is None:
                findings.append(AuditFinding("MOVE_UNTYPED", "preserve move requires key", move_id=move_id))
                continue
            key = str(key)
            if key not in locks:
                findings.append(AuditFinding(
                    "LOCK_UNKNOWN",
                    "candidate claims to preserve a key that is not an active lock",
                    move_id=move_id,
                    key=key,
                ))
                continue
            if "value" in move and move.get("value") != locks[key]:
                findings.append(AuditFinding(
                    "PRESERVE_MISMATCH",
                    "candidate labeled a changed value as preserve",
                    move_id=move_id,
                    key=key,
                ))
            continue

        if action == "update":
            touched = True
            if key is None or "value" not in move:
                findings.append(AuditFinding("MOVE_UNTYPED", "update move requires key and value", move_id=move_id))
                continue
            key = str(key)
            evidence = move.get("evidence", [])
            if not isinstance(evidence, list) or len(evidence) == 0:
                findings.append(AuditFinding(
                    "UNEARNED_UPDATE",
                    "protected reference update lacks explicit evidence",
                    move_id=move_id,
                    key=key,
                ))
                continue
            old = locks.get(key, None)
            new = move.get("value")
            if key in locks and new == old:
                # A no-op update is still a preservation.
                continue
            proposed_locks[key] = new
            changed = True
            continue

        if action == "substitute":
            touched = True
            findings.append(AuditFinding(
                "SILENT_SUBSTITUTION",
                "substitute is never an admissible action on an active reference; use evidence-backed update",
                move_id=move_id,
                key=str(key) if key is not None else None,
            ))
            continue

        findings.append(AuditFinding(
            "ACTION_UNKNOWN",
            f"unknown move action: {action!r}",
            move_id=move_id,
            key=str(key) if key is not None else None,
        ))

    hard_break_codes = {"PRESERVE_MISMATCH", "UNEARNED_UPDATE", "SILENT_SUBSTITUTION"}
    unknown_codes = {"MOVE_UNTYPED", "LOCK_UNKNOWN", "ACTION_UNKNOWN"}
    codes = {f.code for f in findings}

    if codes & hard_break_codes:
        classification = AuditClass.CLASS_BROKEN
        gate = Gate.REFUSE
        proposed_digest = None
    elif codes & unknown_codes:
        classification = AuditClass.UNKNOWN
        gate = Gate.DEFER
        proposed_digest = None
    elif changed:
        # The auditor never commits. It returns a proposed next reference digest.
        proposed_reference = dict(reference)
        proposed_reference["locks"] = proposed_locks
        classification = AuditClass.MOTION_PRESERVED
        gate = Gate.CAN
        proposed_digest = digest(proposed_reference)
        findings.append(AuditFinding(
            "EXPLICIT_UPDATE_PROPOSED",
            "candidate proposes an evidence-backed reference update; commit remains external",
        ))
    else:
        classification = AuditClass.EXACT if not moves or (touched and not changed) else AuditClass.MOTION_PRESERVED
        gate = Gate.CAN
        proposed_digest = None

    return _make_receipt(
        tolerance_stage=stage,
        reference_digest=ref_digest,
        candidate_digest=cand_digest,
        prior_receipt_digest=prior_receipt,
        classification=classification,
        gate=gate,
        findings=findings,
        proposed_reference_digest=proposed_digest,
    )


def validate_packet_shape(packet: Mapping[str, Any]) -> Tuple[bool, Tuple[str, ...]]:
    errors: List[str] = []
    if not isinstance(packet.get("reference"), Mapping):
        errors.append("reference must be an object")
    if not isinstance(packet.get("candidate"), Mapping):
        errors.append("candidate must be an object")
    if "tolerance_stage" in packet:
        try:
            if int(packet["tolerance_stage"]) < 0:
                errors.append("tolerance_stage must be >= 0")
        except Exception:
            errors.append("tolerance_stage must be an integer")
    return (not errors, tuple(errors))


def _load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="MIRROR_CUT v0.1 machine self-audit sidecar")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="audit one JSON packet")
    p_audit.add_argument("packet", help="JSON packet path, or - for stdin")

    sub.add_parser("self-test", help="run finite kernel and protocol regression checks")
    sub.add_parser("cordis", help="print the tool CORDIS record")

    args = parser.parse_args(argv)

    if args.command == "cordis":
        spec = cordis_spec()
        ok, defects = check_cordis(spec)
        print(json.dumps({"status": "Cert" if ok else "Defect", "defects": defects, "cordis": asdict(spec)}, indent=2))
        return 0 if ok else 1

    if args.command == "self-test":
        d4 = d4_self_test()
        spec = cordis_spec()
        cordis_ok, cordis_defects = check_cordis(spec)
        result = {
            "tool": "MIRROR_CUT",
            "version": VERSION,
            "d4": d4,
            "cordis": {"ok": cordis_ok, "defects": cordis_defects},
        }
        print(json.dumps(result, indent=2))
        return 0 if d4.get("ok") and cordis_ok else 1

    packet = _load_json(args.packet)
    if not isinstance(packet, Mapping):
        raise ValueError("top-level packet must be an object")
    ok, errors = validate_packet_shape(packet)
    if not ok:
        print(json.dumps({"status": "Defect", "errors": errors}, indent=2))
        return 2
    receipt = mirror_cut(packet)
    print(json.dumps(receipt.to_dict(), indent=2, ensure_ascii=False))
    return 0 if receipt.gate == Gate.CAN.value else (3 if receipt.gate == Gate.DEFER.value else 4)


if __name__ == "__main__":
    raise SystemExit(main())
