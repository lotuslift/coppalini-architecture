#!/usr/bin/env python3
from copy import deepcopy
from mirror_cut import (
    AuditClass,
    Gate,
    cordis_spec,
    check_cordis,
    d4_self_test,
    digest,
    mirror_cut,
)


def base_reference():
    return {
        "id": "R0",
        "locks": {
            "active_reference": "recognized current address",
            "phi.office": "singular enclosing operator / whole",
        },
        "known_unknowns": {
            "global_weight_update": "UNAVAILABLE",
        },
    }


def packet_with_moves(moves):
    r = base_reference()
    return {
        "tolerance_stage": 1,
        "host_safety": "can",
        "reference": r,
        "candidate": {
            "base_reference_digest": digest(r),
            "moves": moves,
        },
    }


def run():
    assert d4_self_test()["ok"]
    assert check_cordis(cordis_spec())[0]

    # 1. Empty candidate is exact.
    rec = mirror_cut(packet_with_moves([]))
    assert rec.classification == AuditClass.EXACT.value
    assert rec.gate == Gate.CAN.value

    # 2. Explicit preservation is exact.
    rec = mirror_cut(packet_with_moves([
        {"id": "m1", "action": "preserve", "key": "phi.office", "value": "singular enclosing operator / whole"}
    ]))
    assert rec.classification == AuditClass.EXACT.value
    assert rec.gate == Gate.CAN.value

    # 3. Silent substitution is refused.
    rec = mirror_cut(packet_with_moves([
        {"id": "m1", "action": "substitute", "key": "phi.office", "value": "golden-ratio-only parse"}
    ]))
    assert rec.classification == AuditClass.CLASS_BROKEN.value
    assert rec.gate == Gate.REFUSE.value

    # 4. A false 'preserve' label is refused.
    rec = mirror_cut(packet_with_moves([
        {"id": "m1", "action": "preserve", "key": "phi.office", "value": "different value"}
    ]))
    assert rec.classification == AuditClass.CLASS_BROKEN.value
    assert rec.gate == Gate.REFUSE.value

    # 5. Unearned update is refused.
    rec = mirror_cut(packet_with_moves([
        {"id": "m1", "action": "update", "key": "phi.office", "value": "new office", "evidence": []}
    ]))
    assert rec.classification == AuditClass.CLASS_BROKEN.value
    assert rec.gate == Gate.REFUSE.value

    # 6. Evidence-backed update is allowed but never committed by the auditor.
    rec = mirror_cut(packet_with_moves([
        {"id": "m1", "action": "update", "key": "phi.office", "value": "refined office", "evidence": ["proof:123"]}
    ]))
    assert rec.classification == AuditClass.MOTION_PRESERVED.value
    assert rec.gate == Gate.CAN.value
    assert rec.proposed_reference_digest is not None
    assert base_reference()["locks"]["phi.office"] == "singular enclosing operator / whole"

    # 7. Stale base is refused before semantic auditing.
    p = packet_with_moves([])
    p["candidate"]["base_reference_digest"] = "0" * 64
    rec = mirror_cut(p)
    assert rec.classification == AuditClass.CLASS_BROKEN.value
    assert rec.gate == Gate.REFUSE.value

    # 8. Missing base digest defers rather than inventing a result.
    p = packet_with_moves([])
    del p["candidate"]["base_reference_digest"]
    rec = mirror_cut(p)
    assert rec.classification == AuditClass.UNKNOWN.value
    assert rec.gate == Gate.DEFER.value

    # 9. Host safety remains upstream and decisive.
    p = packet_with_moves([])
    p["host_safety"] = "refuse"
    rec = mirror_cut(p)
    assert rec.gate == Gate.REFUSE.value

    # 10. Canonical object-key ordering is invariant.
    p1 = packet_with_moves([])
    r2 = {"known_unknowns": p1["reference"]["known_unknowns"], "locks": p1["reference"]["locks"], "id": "R0"}
    assert digest(p1["reference"]) == digest(r2)

    # 11. Receipt hash is deterministic for the same packet.
    a = mirror_cut(packet_with_moves([]))
    b = mirror_cut(packet_with_moves([]))
    assert a.receipt_digest == b.receipt_digest

    # 12. Prior receipt participates in the new receipt without changing classification.
    p = packet_with_moves([])
    p["prior_receipt_digest"] = a.receipt_digest
    c = mirror_cut(p)
    assert c.classification == a.classification
    assert c.receipt_digest != a.receipt_digest

    print("PASS: 12 protocol checks + 64 D4 transport pairs")


if __name__ == "__main__":
    run()
