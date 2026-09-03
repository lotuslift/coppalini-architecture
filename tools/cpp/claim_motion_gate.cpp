#include <cstdint>

// Coppalini Architecture — Claim Motion Gate v0.1
// C++20 compile-time admissibility checks on already-typed relations.
//
// Important: this kernel does not decide whether a natural-language relation is
// true. `relation_validated` is an externally supplied witness. The kernel only
// checks what additional authority is required by the declared motion.

namespace coppalini::claim_motion {

enum class Motion : std::uint8_t {
    preserve,
    coarsen,
    refine,
    strengthen,
    extend_scope
};

enum class Verdict : std::uint8_t { can, refuse, unknown };

struct Witness {
    Motion motion{};
    bool relation_validated{false};
    bool bridge_present{false};
    bool strength_warrant{false};
    bool scope_warrant{false};
};

[[nodiscard]] consteval Verdict audit(Witness w) {
    if (!w.relation_validated) return Verdict::unknown;

    switch (w.motion) {
        case Motion::preserve:
        case Motion::coarsen:
            return Verdict::can;
        case Motion::refine:
            return w.bridge_present ? Verdict::can : Verdict::refuse;
        case Motion::strengthen:
            return w.strength_warrant ? Verdict::can : Verdict::refuse;
        case Motion::extend_scope:
            return w.scope_warrant ? Verdict::can : Verdict::refuse;
    }
    return Verdict::unknown;
}

static_assert(audit({Motion::preserve,     true, false, false, false}) == Verdict::can);
static_assert(audit({Motion::coarsen,      true, false, false, false}) == Verdict::can);
static_assert(audit({Motion::refine,       true, false, false, false}) == Verdict::refuse);
static_assert(audit({Motion::refine,       true, true,  false, false}) == Verdict::can);
static_assert(audit({Motion::strengthen,   true, false, false, false}) == Verdict::refuse);
static_assert(audit({Motion::strengthen,   true, false, true,  false}) == Verdict::can);
static_assert(audit({Motion::extend_scope, true, false, false, false}) == Verdict::refuse);
static_assert(audit({Motion::extend_scope, true, false, false, true }) == Verdict::can);
static_assert(audit({Motion::extend_scope, false, true, true, true}) == Verdict::unknown);

} // namespace coppalini::claim_motion

int main() { return 0; }
