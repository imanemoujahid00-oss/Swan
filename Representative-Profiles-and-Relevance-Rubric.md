# Swan — Representative Profiles and Product-Relevance Rubric

## 1. Purpose and boundary

This document defines representative **user profiles** and a proposed **human product-relevance rubric** for Swan's three supported concerns: `acne_prone`, `dryness_barrier`, and `sensitive_skin`.

It supports evaluation of cleansers, moisturizers, and facial sunscreens.

Questionnaire inputs and ranking behavior are defined in Questionnaire-Update.md. Eligibility and referral rules are defined in Scope-and-Referral-Rules.md.

These labels do not replace production model scores or establish clinical product safety. The evaluation scenarios are specifications, not executed tests.

## 2. Representative profiles

Profiles use the questionnaire schema defined in Questionnaire-Update.md.

Unless otherwise specified, eligible profiles assume: `is_adult=true`, Q2 explicitly completed with `safety_flags=[]`, `skin_type=normal`, `reactivity=no`, `current_products=["none"]`, `after_cleansing=comfortable`, `moisturizer_texture=no_preference`, and `cleanser_type=no_preference`.

Conditional questions follow Questionnaire-Update.md. Unanswered required questions are not treated as completed responses. Before recommendation generation, `routine_status=not_generated`.

### 2.1 Representative eligible concern profiles

| ID | Concerns (`primary` first) | Distinguishing answered fields | Expected route / safety | Intended evaluation contrast |
|---|---|---|---|---|
| AC-01 | acne | `blemish_level=2`, `skin_type=combination` | Eligible; ask Q8; prioritize acne | Basic acne suitability |
| AC-02 | acne | `blemish_level=0`, `skin_type=oily` | Eligible; zero is valid, not missing | No current blemishes vs unanswered |
| AC-03 | acne | `blemish_level=3`, `reactivity=yes` | Eligible if no Q2 flags; gentleness tie-break | Acne score versus gentle candidate tie |
| DR-01 | dryness | `skin_type=dry`, `dryness_frequency=almost_daily`, `dryness_signs=["tightness"]` | Eligible; ask Q6–Q7 | Dryness relevance and moisturizer texture |
| DR-02 | dryness | `skin_type=oily`, `dryness_frequency=often`, `dryness_signs=["tightness"]` | Eligible; hydration concern remains primary | Oily skin does not erase dryness concern |
| DR-03 | dryness | `skin_type=normal`, `dryness_frequency=occasionally`, `dryness_signs=["none"]` | Eligible if Q7 completed | Explicit none versus missing signs |
| SI-01 | sensitivity | `reactivity=no`, `skin_type=normal` | Eligible; sensitivity concern still drives ranking | Sensitivity concern vs Q9 answer |
| SI-02 | sensitivity | `reactivity=yes`, `skin_type=oily` | Eligible; verified gentleness tie-break | Gentle versus nongentle tied candidates |
| SI-03 | sensitivity | `reactivity=not_sure`, `skin_type=combination` | Eligible; no gentleness preference | Valid uncertainty |
| MC-01 | acne, dryness | `blemish_level=2`, `dryness_frequency=often`, `dryness_signs=["tightness"]` | Eligible; acne primary; Q6–Q8 | Acne priority with dryness retained |
| MC-02 | dryness, acne | Same answers as MC-01; switch `primary_concern` | Eligible; dryness priority; Q6–Q8 | Priority-change test with same concerns |
| MC-03 | acne, sensitivity | `blemish_level=2`, `reactivity=yes` | Eligible; acne primary | Acne priority with gentleness tie-break |
| MC-04 | sensitivity, acne | Same answers as MC-03; switch `primary_concern` | Eligible; sensitivity primary | Primary concern priority comparison |
| MC-05 | dryness, sensitivity | `skin_type=dry`, `dryness_frequency=often`, `dryness_signs=["redness"]`, `reactivity=yes` | Eligible absent other safety flags; irritation policy pending | Hydration plus gentleness evidence |
| MC-06 | sensitivity, dryness | Same concern answers as MC-05, sensitivity primary | Eligible absent other safety flags | Different priority, same concern set |
| MC-07 | acne, dryness, sensitivity | `blemish_level=2`, `dryness_frequency=often`, `dryness_signs=["tightness"]`, `reactivity=yes` | Eligible; acne priority; all conditional questions | Three-concern combination |
| MC-08 | dryness, acne, sensitivity | Same answers as MC-07, dryness primary | Eligible; dryness priority | Three-concern priority switch |
| ST-01 | acne | `blemish_level=1`, `skin_type=oily` | Eligible | Light moisturizer tie-break |
| ST-02 | acne | Same as ST-01 except `skin_type=dry`; Q6 required | Eligible after Q6 | Rich moisturizer tie-break |
| RT-01 | dryness | `current_products=["cleanser","moisturizer"]`, Q6–Q7 completed | Eligible | Usage context, no unsupported ranking effect |

### 2.2 Safety, missing-input, and result-availability profiles

| ID | Input / setup | Expected outcome | Product relevance labeling? |
|---|---|---|---|
| RF-01 | `is_adult=false` | `out_of_scope`, `not_generated` | No — stop before ranking |
| RF-02 | Q2 `unusual_skin_change` | `referred`, `not_generated` | No |
| RF-03 | Q2 `pregnant_or_breastfeeding` | No routine under current reviewed flow; exact status pending team sign-off | No |
| RF-04 | Q2 `prescribed_treatment` | No routine under current reviewed flow; status/copy pending | No |
| RF-05 | Q2 `known_allergy` | No automated allergy-safe routine; status/copy pending | No |
| RF-06 | Acne only, `blemish_level=4` | `referred`, `not_generated` | No |
| RF-07 | Dryness primary, acne secondary, `blemish_level=5` | `referred`, `not_generated` | No — primary concern never overrides stop |
| RF-08 | Q7 `stinging` or Q11 `irritated`, no Q2 flags | **Pending irritation policy**; cannot infer duration/severity | Conditional; do not declare automatic referral |
| MD-01 | Q1/Q2 unanswered | Request safety response; no ranking | No |
| MD-02 | Q3=`not_sure` | Help select supported concern; no ranking | No |
| MD-03 | Two concerns; Q4 unanswered | Request primary concern; no ranking | No |
| MD-04 | Acne selected; Q8 unanswered (`null`) | Request Q8; no ranking | No |
| MD-05 | Q9 unanswered (distinct from `not_sure`) | Request Q9; no ranking | No |
| MD-06 | Dryness selected; displayed Q7 unanswered | **Proposed** request completion before ranking; team approval pending | No under proposed rule |
| RS-01 | Eligible user; verified cleanser and moisturizer only | `partial`; sunscreen step explained | Label available products; no invented sunscreen |
| RS-02 | Eligible user; no verified matches | `empty` with explanation | No fake recommendations |
| RS-03 | Product fragrance/essential-oil presence unknown | No claim of confirmed absence or presence | Label uncertainty; do not fabricate |

## 3. Product-relevance rubric (proposed for human evaluation)

### 3.1 Evaluation order: safety first, relevance second

1. **Eligibility:** Apply Scope-and-Referral-Rules.md safety rules. Blocked profiles receive `NE_blocked`, not a relevance score.
2. **Evidence:** Verify product identity, category, and relevant attributes; unknown is not false.
3. **Relevance:** Evaluate primary-concern fit and document secondary concerns without inventing weights.
4. **Tie-break:** Follow Questionnaire-Update.md's verified gentleness and moisturizer-texture rules.
5. **Uncertainty:** Use `NE_insufficient_evidence` when essential product evidence is missing.

### 3.2 Relevance labels (human labeling proposal; not the production scoring algorithm)

| Label | Definition | Evidence required | Example interpretation |
|---|---|---|---|
| `3_high` | Clear, verified fit with the primary concern and product category; no documented conflict with another selected concern or stated safety gate | Product category plus supported relevant formulation/attributes; concerns assessed | Suitable category and verified relevant attributes for profile |
| `2_moderate` | Plausible fit with primary concern, but secondary-concern compatibility, a preference, or one noncritical attribute remains uncertain | Verifiable category and at least some primary-concern relevance | Relevant but incomplete support for all considerations |
| `1_low` | Weak concern fit or a documented, non-safety mismatch; not a preferred choice | Evidence of category and reason for low fit | Appropriate category but poorer profile fit than alternatives |
| `0_not_relevant` | Verified mismatch with the product step/concern or evidence of an incompatible feature; **never** use to represent an unverified safety-critical question | Documented reason; avoid speculative contradictions | Wrong product category for requested step |
| `NE_insufficient_evidence` | Insufficient reliable catalogue evidence to evaluate a necessary claim | Identify the exact missing field/source | Missing relevant product data |
| `NE_blocked` | User/profile fails safety, scope, or required-answer gate; no relevance assessment permitted | Record the blocked profile reason, not product attributes | Acne level 5, Q2 flag, or required Q8 missing |

The 0–3 scale and thresholds are **proposed annotation conventions**. They do **not** assert that the implementation uses numeric relevance scores, nor imply clinical proof of product suitability.

### 3.3 Evidence and conflict checklist for each product step

| Product step | Check first | Relevant evidence to inspect (when catalogue provides it) | Do **not** infer |
|---|---|---|---|
| Cleanser | Category verified as facial cleanser | Confirmed formulation/usage characteristics; verified gentleness flag for Q9 tie-break; rinse-off/no-rinse if usable catalogue data exists | That a product is gentle simply because it is marketed for sensitivity; that a preference is a scored feature |
| Moisturizer | Category verified as facial moisturizer | Model-supported primary-concern fit; verified gentle flag; verified light/rich texture for documented skin-type tie-break | That all rich creams are good for dryness or all gels suit acne; unverified compatibility |
| Facial sunscreen | Category verified as facial sunscreen | Source-supported facial-sunscreen classification and any verified sun-protection attributes the system actually requires; model-supported concern fit | SPF/UVA protection from product name alone; pregnancy safety or allergy safety |

**Catalogue attribute provenance:** For each label record `verified_fields`, `unknown_fields`, and `evidence_source`. If a criterion has no catalogue support or no agreed model mapping, write `unknown`/`not_scored` and explain, rather than force a label based on intuition.

### 3.4 Annotation records

Actual profile–product annotations are maintained in Profile-Product-Relevance-catalogue-v2.md and provisional_label_pairs.csv.

Each annotation records the profile ID, product ID, proposed label, supporting evidence, uncertainties, rationale, and review status.

Eligibility, product availability, and product relevance remain separate outcomes.

## 4. Controlled comparison tests for the rubric

Use a small controlled catalogue with products whose attributes and scores are documented. Do not use real items until their data is inspected. Expected outcomes below test ordering **only** where the current rules provide it.

| Test ID | Controlled comparison | Expected observation |
|---|---|---|
| EV-01 | Same primary-concern product score; Q9=no vs yes; one candidate verified gentle | With Q9=yes, gentle candidate preferred at tie; with no, gentleness does not decide tie |
| EV-02 | Tied moisturizer concern scores, verified light vs rich; oily vs dry skin | Oily prefers light; dry prefers rich, if no higher gentleness tie-break applies |
| EV-03 | Tied moisturizers: verified gentle rich vs nongentle light; oily, Q9=yes | Verified gentleness breaks tie before light texture |
| EV-04 | Same two concerns with primary priority reversed (MC-01 vs MC-02) | The profile's primary concern changes; actual product order requires model/code and controlled scores to verify |
| EV-05 | Missing gentleness flag on candidate, Q9=yes | Flag remains unknown; no claim of verified gentleness; fallback ordering requires model clarification |
| EV-06 | Unknown fragrance or essential oil | Do not claim either verified presence or absence |
| EV-07 | Candidate outside required product category | Mark `0_not_relevant` for that step, with category evidence |
| EV-08 | Eligible profile, no verified candidate for sunscreen | `partial` or `empty` routine depending on other steps; no fabricated product |
| EV-09 | Secondary acne at level 4/5 | `NE_blocked` for all candidate pairs, even with dryness/sensitivity primary |
| EV-10 | Unanswered required Q8 or Q9 | `NE_blocked`; request completion |
| EV-11 | Q7 shown but unanswered for dryness | **Provisional T13 policy:** request answer before ranking; do not treat as `none` |
| EV-12 | Q12/Q13 preference changes without verified feature/rule | Do not claim a ranking shift caused by preference; record as unverified |

## 5. Labeling procedure

1. Use the canonical profiles and reviewed Swan catalogue.
2. Apply Scope-and-Referral-Rules.md eligibility and safety checks before assessing relevance.
3. Assign proposed relevance labels using the Section 3 rubric and documented product evidence.
4. Validate actual ranking behavior against the implemented model separately.
5. Labels remain provisional until the team approves the rubric and annotations.

## 6. Open decisions for team review

1. Approve or revise the human relevance labels and criteria.
2. Confirm catalogue attributes supporting concern fit, gentleness, moisturizer texture, and sunscreen evidence.
3. Confirm whether secondary concerns affect implemented ranking beyond profile retention.
4. Decide whether Q12–Q13 preferences will affect ranking.
