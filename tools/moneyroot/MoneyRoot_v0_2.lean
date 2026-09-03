/-!
# MoneyRoot v0.1

A minimum typed kernel for the recurring read / coordinate / decision distinction
in *The Root Dictionary of Money*.

Scope:
* pure type-theoretic / set-theoretic claims only;
* no economic, legal, or empirical premise is smuggled into the kernel;
* application claims require separately typed witnesses.

The key correction is to use the **kernel pair** of an arbitrary reader rather
than the algebraic kernel of a homomorphism.  For `R : X → C`, the relevant
relation is simply `R x = R y`.
-/

set_option autoImplicit false

universe uX uC uA uU uB

namespace MoneyRoot

/-- The equivalence relation induced by a read: two states are indistinguishable
    at the declared coordinate exactly when the reader gives the same output. -/
def EqKernel {X : Type uX} {C : Type uC} (R : X → C) (x y : X) : Prop :=
  R x = R y

/-- `D` preserves every distinction collapsed by `R`: if the read cannot tell
    two states apart, neither can the downstream decision. -/
def FiberRefines {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) : Prop :=
  ∀ ⦃x y : X⦄, R x = R y → D x = D y

/-- A read collision: distinct source states share one coordinate. -/
def Collapses {X : Type uX} {C : Type uC} (R : X → C) : Prop :=
  ∃ x y : X, R x = R y ∧ x ≠ y

/-- A decision collision: the reader identifies two states that the downstream
    decision must distinguish.  This is the finite obstruction certificate. -/
def DecisionCollision {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) : Prop :=
  ∃ x y : X, R x = R y ∧ D x ≠ D y

/-- The quotient of source states by equality at the declared reader. -/
def ReadQuot {X : Type uX} {C : Type uC} (R : X → C) : Type uX :=
  Quot (fun x y : X => R x = R y)

/-- Send a source state to its read-equivalence class. -/
def qread {X : Type uX} {C : Type uC} (R : X → C) (x : X) : ReadQuot R :=
  Quot.mk (fun a b : X => R a = R b) x

/-- `D` is completely determined by the information retained by `R` exactly
    when it descends to the read quotient. -/
def FactorsThroughRead {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) : Prop :=
  ∃ G : ReadQuot R → A, ∀ x : X, D x = G (qread R x)

/-! ## T1 — read equality reflects state equality iff injectivity is supplied -/

/-- The exact meaning of injectivity: equality at the reader reflects equality
    of source states. -/
theorem T1_injective_iff_read_equality_reflects_state
    {X : Type uX} {C : Type uC} (R : X → C) :
    Function.Injective R ↔ (∀ ⦃x y : X⦄, R x = R y → x = y) := by
  rfl

/-- A concrete read collision refutes injectivity. -/
theorem T1_collision_refutes_injective
    {X : Type uX} {C : Type uC} {R : X → C}
    (h : Collapses R) : ¬ Function.Injective R := by
  intro hInjective
  cases h with
  | intro x hx =>
      cases hx with
      | intro y hxy =>
          exact hxy.2 (hInjective hxy.1)

/-! ## T2 — Read-Sufficiency / quotient-factorization theorem -/

/-- A downstream decision is determined by a read exactly when it is constant
    on every fiber of that read.  This is the universal property of the read
    quotient specialized to the present kernel. -/
theorem T2_factorization_iff_fiber_refinement
    {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) :
    FactorsThroughRead R D ↔ FiberRefines R D := by
  constructor
  · intro hFactors
    cases hFactors with
    | intro G hG =>
        intro x y hRead
        calc
          D x = G (qread R x) := hG x
          _ = G (qread R y) := congrArg G (Quot.sound hRead)
          _ = D y := (hG y).symm
  · intro hFiber
    let G : ReadQuot R → A :=
      Quot.lift D (by
        intro x y hRead
        exact hFiber hRead)
    refine ⟨G, ?_⟩
    intro x
    rfl

/-- Kernel-pair inclusion is the same condition, stated relationally.  For
    arbitrary functions this is the exact replacement for the informal phrase
    `ker R ⊆ ker D`. -/
theorem T2_eqkernel_inclusion_iff_fiber_refinement
    {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) :
    (∀ ⦃x y : X⦄, EqKernel R x y → EqKernel D x y) ↔ FiberRefines R D := by
  rfl

/-! ## T3 — finite obstruction certificate -/

/-- One same-read / different-decision pair is enough to refute every decision
    rule that uses only information retained by the read. -/
theorem T3_collision_refutes_factorization
    {X : Type uX} {C : Type uC} {A : Type uA}
    {R : X → C} {D : X → A}
    (hCollision : DecisionCollision R D) : ¬ FactorsThroughRead R D := by
  intro hFactors
  have hFiber : FiberRefines R D :=
    (T2_factorization_iff_fiber_refinement R D).mp hFactors
  cases hCollision with
  | intro x hx =>
      cases hx with
      | intro y hxy =>
          exact hxy.2 (hFiber hxy.1)

/-- Direct coordinate-only version of T3.  It avoids any claim about values of
    a decision rule away from the actual image of the reader. -/
theorem T3_collision_refutes_coordinate_only_rule
    {X : Type uX} {C : Type uC} {A : Type uA}
    {R : X → C} {D : X → A}
    (hCollision : DecisionCollision R D) :
    ¬ (∃ g : C → A, ∀ x : X, D x = g (R x)) := by
  intro hRule
  cases hRule with
  | intro g hg =>
      cases hCollision with
      | intro x hx =>
          cases hx with
          | intro y hxy =>
              apply hxy.2
              calc
                D x = g (R x) := hg x
                _ = g (R y) := congrArg g hxy.1
                _ = D y := (hg y).symm

/-! ## T4 — exact recoverability requires injectivity -/

/-- If a decoder recovers every source state exactly after reading it, then the
    reader must be injective.  Compression with collisions cannot also be exact
    state recovery. -/
theorem T4_left_inverse_implies_injective
    {X : Type uX} {C : Type uC}
    {R : X → C} {decode : C → X}
    (hLeft : Function.LeftInverse decode R) : Function.Injective R := by
  intro x y hRead
  calc
    x = decode (R x) := (hLeft x).symm
    _ = decode (R y) := congrArg decode hRead
    _ = y := hLeft y

/-- A collision therefore rules out any exact decoder. -/
theorem T4_collision_refutes_exact_decoder
    {X : Type uX} {C : Type uC} {R : X → C}
    (hCollision : Collapses R) :
    ¬ (∃ decode : C → X, Function.LeftInverse decode R) := by
  intro hDecoder
  cases hDecoder with
  | intro decode hLeft =>
      exact T1_collision_refutes_injective hCollision
        (T4_left_inverse_implies_injective hLeft)

/-! ## T5 — typed reader → policy adapter → controller path -/

/-- A policy adapter converts a coordinate into an action. -/
def InducedAction {X : Type uX} {C : Type uC} {U : Type uU}
    (R : X → C) (κ : C → U) : X → U :=
  fun x => κ (R x)

/-- A plant/update law consumes the current state and selected action. -/
def ClosedLoop {X : Type uX} {C : Type uC} {U : Type uU}
    (T : X → U → X) (R : X → C) (κ : C → U) : X → X :=
  fun x => T x (κ (R x))

/-- A reader-only policy necessarily selects the same action for every pair of
    source states that the reader identifies. -/
theorem T5_same_read_same_induced_action
    {X : Type uX} {C : Type uC} {U : Type uU}
    {R : X → C} {κ : C → U} {x y : X}
    (hRead : R x = R y) :
    InducedAction R κ x = InducedAction R κ y := by
  exact congrArg κ hRead

/-- Equivalently, every induced reader-only action is fiber-refining. -/
theorem T5_induced_action_fiber_refines
    {X : Type uX} {C : Type uC} {U : Type uU}
    (R : X → C) (κ : C → U) :
    FiberRefines R (InducedAction R κ) := by
  intro x y hRead
  exact T5_same_read_same_induced_action hRead

/-- The read actually enters a causal update only through the explicitly typed
    composition `T x (κ (R x))`. -/
theorem T5_closed_loop_unfold
    {X : Type uX} {C : Type uC} {U : Type uU}
    (T : X → U → X) (R : X → C) (κ : C → U) (x : X) :
    ClosedLoop T R κ x = T x (κ (R x)) := by
  rfl

/-! ## Four dictionary proving grounds

These are deliberately **schema witnesses**, not empirical economic claims.
Their only job is to demonstrate that each dictionary office can inhabit the
same exact obstruction type without identifying the offices with one another.
-/

namespace PriceSchema
inductive Case where
  | needA
  | needB
  deriving DecidableEq

def price : Case → Nat
  | .needA => 100
  | .needB => 100

def access : Case → Bool
  | .needA => true
  | .needB => false

theorem collision : DecisionCollision price access := by
  refine ⟨.needA, .needB, ?_, ?_⟩
  · rfl
  · decide

theorem no_price_only_access_rule :
    ¬ (∃ g : Nat → Bool, ∀ x : Case, access x = g (price x)) := by
  exact T3_collision_refutes_coordinate_only_rule collision
end PriceSchema

namespace AbundanceSchema
inductive Case where
  | usefulA
  | usefulB
  deriving DecidableEq

def price : Case → Nat
  | .usefulA => 0
  | .usefulB => 0

def useRead : Case → Nat
  | .usefulA => 1
  | .usefulB => 9

theorem collision : DecisionCollision price useRead := by
  refine ⟨.usefulA, .usefulB, ?_, ?_⟩
  · rfl
  · decide

theorem price_not_sufficient_for_use_read : ¬ FactorsThroughRead price useRead := by
  exact T3_collision_refutes_factorization collision
end AbundanceSchema

namespace LivingSchema
inductive Case where
  | viableA
  | viableB
  deriving DecidableEq

def moneyRead : Case → Nat
  | .viableA => 0
  | .viableB => 0

def continuation : Case → Bool
  | .viableA => true
  | .viableB => false

theorem collision : DecisionCollision moneyRead continuation := by
  refine ⟨.viableA, .viableB, ?_, ?_⟩
  · rfl
  · decide

theorem money_read_not_sufficient_for_continuation :
    ¬ FactorsThroughRead moneyRead continuation := by
  exact T3_collision_refutes_factorization collision
end LivingSchema

namespace SettlementSchema
structure State where
  grossIn : Int
  grossOut : Int
  deriving DecidableEq

def net (s : State) : Int := s.grossIn - s.grossOut

def grossTotal (s : State) : Int := s.grossIn + s.grossOut

def s₁ : State := ⟨1, 1⟩
def s₂ : State := ⟨2, 2⟩

theorem collision : DecisionCollision net grossTotal := by
  refine ⟨s₁, s₂, ?_, ?_⟩
  · decide
  · decide

theorem net_not_sufficient_for_gross_exposure :
    ¬ FactorsThroughRead net grossTotal := by
  exact T3_collision_refutes_factorization collision
end SettlementSchema


/-! ## T6 — supplemental reads and residual distinctions

T1–T5 establish only generic facts about arbitrary functions and their fibers.
T6 does not add an economic premise.  It types the next constructive question:
when a base reader `R` is insufficient for a downstream decision `D`, what must
any additional reader `S` preserve in order for the joint read `(R,S)` to be
sufficient?

The theorem below gives a necessity law, not a canonical-minimum selector.
Choosing a *least* supplement requires a separately declared candidate class
and information/refinement order; no such selector is smuggled into this
kernel.
-/

/-- Combine the original reader with an additional reader without identifying
their codomains or offices. -/
def JointRead {X : Type uX} {C : Type uC} {B : Type uB}
    (R : X → C) (S : X → B) : X → C × B :=
  fun x => (R x, S x)

/-- `S` is sufficient *relative to* `R` for decision `D` exactly when `D` is
constant on every joint `(R,S)` fiber. -/
def SupplementSufficient
    {X : Type uX} {C : Type uC} {B : Type uB} {A : Type uA}
    (R : X → C) (S : X → B) (D : X → A) : Prop :=
  FiberRefines (JointRead R S) D

/-- Unpacked joint-fiber form of supplemental sufficiency. -/
theorem T6_supplement_sufficient_iff_joint_equalities
    {X : Type uX} {C : Type uC} {B : Type uB} {A : Type uA}
    (R : X → C) (S : X → B) (D : X → A) :
    SupplementSufficient R S D ↔
      (∀ ⦃x y : X⦄, R x = R y → S x = S y → D x = D y) := by
  constructor
  · intro hSupp x y hR hS
    apply hSupp
    exact Prod.ext hR hS
  · intro hJoint x y hPair
    exact hJoint (congrArg Prod.fst hPair) (congrArg Prod.snd hPair)

/-- Residual-distinction necessity law: whenever `R` collapses a pair that `D`
must distinguish, every sufficient supplement must distinguish that pair. -/
theorem T6_sufficient_supplement_separates_residual_pair
    {X : Type uX} {C : Type uC} {B : Type uB} {A : Type uA}
    {R : X → C} {S : X → B} {D : X → A} {x y : X}
    (hSupp : SupplementSufficient R S D)
    (hR : R x = R y)
    (hD : D x ≠ D y) :
    S x ≠ S y := by
  intro hS
  apply hD
  exact (T6_supplement_sufficient_iff_joint_equalities R S D).mp hSupp hR hS

/-- A decision collision therefore forces any sufficient supplement to carry at
least one nontrivial distinction inside the collided `R`-fiber. -/
theorem T6_decision_collision_forces_supplement_distinction
    {X : Type uX} {C : Type uC} {B : Type uB} {A : Type uA}
    {R : X → C} {S : X → B} {D : X → A}
    (hCollision : DecisionCollision R D)
    (hSupp : SupplementSufficient R S D) :
    ∃ x y : X, R x = R y ∧ S x ≠ S y := by
  cases hCollision with
  | intro x hx =>
      cases hx with
      | intro y hxy =>
          refine ⟨x, y, hxy.1, ?_⟩
          exact T6_sufficient_supplement_separates_residual_pair hSupp hxy.1 hxy.2

/-- The downstream decision itself is always a (generally non-minimal)
sufficient supplement.  This is an existence upper bound only; it does not say
that `D` is an appropriate observable or policy input. -/
theorem T6_decision_read_is_sufficient_supplement
    {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) :
    SupplementSufficient R D D := by
  apply (T6_supplement_sufficient_iff_joint_equalities R D D).mpr
  intro x y hR hD
  exact hD

/-- A supplement carrying no distinctions at all is sufficient exactly when the
base reader was already sufficient.  Thus a genuine decision collision rules
out the trivial supplement. -/
theorem T6_trivial_supplement_iff_base_sufficient
    {X : Type uX} {C : Type uC} {A : Type uA}
    (R : X → C) (D : X → A) :
    SupplementSufficient R (fun _ : X => PUnit.unit) D ↔ FiberRefines R D := by
  constructor
  · intro hSupp x y hR
    exact (T6_supplement_sufficient_iff_joint_equalities
      R (fun _ : X => PUnit.unit) D).mp hSupp hR rfl
  · intro hBase
    apply (T6_supplement_sufficient_iff_joint_equalities
      R (fun _ : X => PUnit.unit) D).mpr
    intro x y hR hUnit
    exact hBase hR

/-- Information preorder between two reads, allowing different codomains:
`S ≤info T` means every equality preserved by `T` is also preserved by `S`.
Equivalently, `T` carries at least every distinction carried by `S`.
This is supplied for later minimum-selection work; T6 does not assert that a
least sufficient supplement exists without a declared selection domain. -/
def ReadNoMoreInformative
    {X : Type uX} {B : Type uB} {C : Type uC}
    (S : X → B) (T : X → C) : Prop :=
  ∀ ⦃x y : X⦄, T x = T y → S x = S y

/-- The information preorder is reflexive. -/
theorem T6_info_refl
    {X : Type uX} {B : Type uB} (S : X → B) :
    ReadNoMoreInformative S S := by
  intro x y h
  exact h

/-- The information preorder is transitive across heterogeneous codomains. -/
theorem T6_info_trans
    {X : Type uX} {A : Type uA} {B : Type uB} {C : Type uC}
    {R₁ : X → A} {R₂ : X → B} {R₃ : X → C}
    (h12 : ReadNoMoreInformative R₁ R₂)
    (h23 : ReadNoMoreInformative R₂ R₃) :
    ReadNoMoreInformative R₁ R₃ := by
  intro x y h3
  exact h12 (h23 h3)

end MoneyRoot
