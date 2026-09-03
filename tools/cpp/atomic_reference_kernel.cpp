#include <concepts>
#include <cstdint>

// Coppalini Architecture — Atomic Reference Kernel v0.1
// C++20 compile-time reference/transport/return checks.
//
// Scope: a deliberately small finite witness layer. It proves only the
// relations encoded below. It does not infer semantic relations from raw text.

namespace coppalini::atomic_reference {

enum class Gate : std::uint8_t { can, refuse };
enum class Refusal : std::uint8_t {
    none,
    outside_transport_domain,
    broken_return
};

struct Reference {
    std::uint32_t address{0};
    constexpr bool operator==(const Reference&) const noexcept = default;
};

struct Receipt {
    std::uint32_t occurrences{0};
    constexpr bool operator==(const Receipt&) const noexcept = default;
};

struct State {
    Reference reference{};
    Receipt receipt{};
    constexpr bool operator==(const State&) const noexcept = default;
};

template<class T>
concept ReferenceTransport = requires(const T& t, Reference r) {
    { t.accepts(r) } noexcept -> std::same_as<bool>;
    { t.forward(r) } noexcept -> std::same_as<Reference>;
    { t.inverse(r) } noexcept -> std::same_as<Reference>;
};

struct AuditResult {
    Gate gate{Gate::refuse};
    Refusal refusal{Refusal::none};
    State before{};
    State after{};
    Reference traversed{};
};

template<ReferenceTransport T>
[[nodiscard]] consteval AuditResult audit_transport(State before, const T& transport) {
    if (!transport.accepts(before.reference)) {
        return {Gate::refuse, Refusal::outside_transport_domain,
                before, before, before.reference};
    }

    const Reference traversed = transport.forward(before.reference);
    const Reference returned = transport.inverse(traversed);

    if (!(returned == before.reference)) {
        return {Gate::refuse, Refusal::broken_return,
                before, before, traversed};
    }

    State after = before;
    after.reference = returned;
    after.receipt.occurrences += 1;

    return {Gate::can, Refusal::none, before, after, traversed};
}

struct QuarterTurn {
    static constexpr std::uint32_t period = 4;

    [[nodiscard]] constexpr bool accepts(Reference r) const noexcept {
        return r.address < period;
    }

    [[nodiscard]] constexpr Reference forward(Reference r) const noexcept {
        return {(r.address + 1U) % period};
    }

    [[nodiscard]] constexpr Reference inverse(Reference r) const noexcept {
        return {(r.address + period - 1U) % period};
    }
};

struct IdentityTransport {
    [[nodiscard]] constexpr bool accepts(Reference) const noexcept { return true; }
    [[nodiscard]] constexpr Reference forward(Reference r) const noexcept { return r; }
    [[nodiscard]] constexpr Reference inverse(Reference r) const noexcept { return r; }
};

struct BrokenReturn {
    static constexpr std::uint32_t period = 4;

    [[nodiscard]] constexpr bool accepts(Reference r) const noexcept {
        return r.address < period;
    }

    [[nodiscard]] constexpr Reference forward(Reference r) const noexcept {
        return {(r.address + 1U) % period};
    }

    // Deliberately not an inverse of forward().
    [[nodiscard]] constexpr Reference inverse(Reference r) const noexcept {
        return r;
    }
};

static_assert(ReferenceTransport<QuarterTurn>);
static_assert(ReferenceTransport<IdentityTransport>);
static_assert(ReferenceTransport<BrokenReturn>);

consteval bool canonical_witnesses() {
    constexpr State s0{{0}, {7}};

    // Nontrivial transport; reference returns; occurrence is retained and grows.
    constexpr auto turn = audit_transport(s0, QuarterTurn{});
    static_assert(turn.gate == Gate::can);
    static_assert(turn.after.reference == s0.reference);
    static_assert(turn.traversed != s0.reference);
    static_assert(turn.after.receipt.occurrences == s0.receipt.occurrences + 1U);

    // Trivial transport may still produce a new occurrence receipt.
    constexpr auto identity = audit_transport(s0, IdentityTransport{});
    static_assert(identity.gate == Gate::can);
    static_assert(identity.traversed == s0.reference);
    static_assert(identity.after.receipt.occurrences == s0.receipt.occurrences + 1U);

    // Broken return is refused and does not advance the receipt.
    constexpr auto broken = audit_transport(s0, BrokenReturn{});
    static_assert(broken.gate == Gate::refuse);
    static_assert(broken.refusal == Refusal::broken_return);
    static_assert(broken.after == s0);

    // Out-of-domain input is refused before transport.
    constexpr State outside{{4}, {7}};
    constexpr auto rejected = audit_transport(outside, QuarterTurn{});
    static_assert(rejected.gate == Gate::refuse);
    static_assert(rejected.refusal == Refusal::outside_transport_domain);
    static_assert(rejected.after == outside);

    return true;
}

static_assert(canonical_witnesses());

} // namespace coppalini::atomic_reference

int main() { return 0; }
