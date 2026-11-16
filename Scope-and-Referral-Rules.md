# Swan — Scope, Eligibility and Referral Rules

## 1. Purpose and scope

Swan recommends a **cosmetic** three-step skincare routine using one shared European product catalogue. Swan does not diagnose skin conditions, prescribe treatments, replace a clinician, or promise that products cannot cause reactions.

| Dimension | Current boundary |
| --- | --- |
| Age | Adults 18+ only |
| Concerns | `acne_prone`, `dryness_barrier`, `sensitive_skin` |
| Overlapping concerns | Multiple selections allowed; `primary_concern` drives ranking priority |
| Product steps | Facial cleanser, moisturizer, facial sunscreen |

Detailed questionnaire definitions and ranking behavior are maintained in Questionnaire-Update.md.

## 2. Inputs and states

- Safety and referral decisions use the questionnaire inputs defined in Questionnaire-Update.md.
- The relevant fields are `is_adult`, `safety_flags`, `concerns`, `primary_concern`, `blemish_level`, `reactivity`, `dryness_signs`, and `after_cleansing`.
- Q2 must be explicitly answered before interpreting `safety_flags=[]` as no reported safety flags.

### State definitions

| `eligibility_status` | Meaning | Run ranking? |
| --- | --- | --- |
| `eligible` | All required safety checks passed and no blocking condition identified | Yes, after other required answers |
| `out_of_scope` | User is outside supported population (e.g., under 18) | No |
| `referred` | Current documented rule directs user to professional guidance and does not provide a routine | No |
| `requires_review` | Human/professional or team-reviewed pathway needed before eligibility can be decided | No **until** review resolves it (proposed operational clarification) |

**`routine_status`** must be `not_generated` when ranking was blocked or never run. After valid ranking: `complete` = all three verified steps, `partial` = one or two steps, `empty` = no verified matches. These are **availability outcomes**, not clinical safety judgments.

## 3. Safety and referral decision table

| Trigger | Decision for current MVP | Routine | Proposed user-facing message | Basis / approval |
| --- | --- | --- | --- | --- |
| Q1 = under 18 | `out_of_scope` | No | “Swan's personalized routine is currently available only to adults aged 18 or over.” | Agreed outcome; improved copy proposed |
| Q2 = sudden severe/painful/unusual change | `referred` | No | “A sudden, severe or unusual skin change needs assessment by a healthcare professional. Please seek medical advice rather than relying on a skincare recommendation.” | Agreed stop/referral; copy proposed |
| Severe skin symptoms with possible emergency signs (e.g., breathing difficulty with facial swelling) | **Urgent-care guidance**, do not generate a routine | No | “If you have trouble breathing or rapidly developing swelling, seek emergency medical help now.” | **Proposed — clinical review required**; not a new questionnaire diagnosis |
| Q2 = current prescribed skincare | `referred` | No | “Because you use prescribed skincare, please check with your prescribing clinician before adding new products. Swan won't generate a routine in this version.” | stop documented; final policy/copy to confirm |
| Q2 = pregnant or breastfeeding | `referred` | No | “Swan doesn't provide personalized product recommendations during pregnancy or breastfeeding in this version. Ask a pharmacist or healthcare professional for advice.” | Agreed no routine; exact status/copy to confirm |
| Q2 = known ingredient allergy | `referred` | No | “Swan cannot yet verify a routine against your specific ingredient allergy. Please get professional guidance and check product ingredient labels.” | stop documented; copy proposed |
| Q8 = level 4 or 5, acne primary **or secondary** | `referred` | No | “Your answers describe acne that may need professional assessment. Please contact a healthcare professional or dermatologist. Swan won't recommend a routine in this version.” | Agreed no-routine route; copy proposed |
| Persistent/significant stinging or irritation | Referral or conservative guidance **only if reviewed criteria are met** | Pending decision | “If stinging or irritation is persistent or significant, please speak with a healthcare professional.” | **trigger/decision requires approval** |
| Q9 = yes, without other safety flags | `eligible` if all other checks pass | Yes | No referral message; apply verified gentleness tie-break | Agreed/documented |
| Mild dryness or selected sensitive skin alone | `eligible` if all checks pass | Yes | Ordinary cosmetic routine explanation; avoid diagnosis or therapeutic claims | Derived from supported-concern scope; confirm safety thresholds |
| Q3 = `not_sure` | Not ready to rank; **not** a referral | No, until a concern is chosen | “Here are the three skin concerns Swan supports. Choose the one that best matches your goal to continue.” | Agreed/documented |

**Do not use Q7 `stinging` or Q11 `irritated` as an automatic medical-referral trigger without a reviewed rule.** The current questionnaire does not reliably establish symptom severity or duration. The team should explicitly decide whether to add a safety follow-up, keep general guidance, or refer in all such cases.

## 4. Safety evaluation order and concern-specific coverage

1. Validate Q1 and Q2. Missing safety answers cannot be interpreted as negative responses.
2. Apply all blocking safety and referral conditions before product ranking, including those arising from secondary concerns.
3. Require Q8 whenever acne is selected; levels 4–5 trigger referral and no routine.
4. For Q7 stinging or Q11 irritated, follow the reviewed irritation policy. Do not infer symptom severity or duration from these answers alone.
5. If eligible and all required answers are complete, allow ranking according to Questionnaire-Update.md.
6. If ranking runs but verified products are unavailable, return a partial or empty routine rather than bypassing safety rules.

### Concern-specific coverage

| Concern | Ordinary eligible route | Referral/stop boundary | Remaining uncertainty |
| --- | --- | --- | --- |
| `acne_prone` | Ask Q8; levels 0–3 may proceed when no other blocking flags | Levels 4–5 require guidance and no routine, even as secondary concern | Q8 is user-reported; level labels are screening, **not a medical diagnosis** |
| `dryness_barrier` | Ask Q6–Q7; conservative cosmetic matching where eligible | Q2 severe/unusual changes stop; persistent/significant irritation may warrant guidance | Whether/how Q6–Q7 should change scoring; precise irritation thresholds |
| `sensitive_skin` | Q9 asked of all; selected sensitivity drives primary concern score if prioritized | Q2 severe/unusual changes stop; significant irritation needs reviewed rule | Sensitivity selection alone is not medical referral; Q9 and concern selection have distinct roles |
| Multiple concerns | Collect questions for every selected concern; selected priority drives ranking | Any safety flag or severe acne overrides ranking priority | Confirm actual secondary-concern handling in model tests |

## 5. Missing data and catalogue claims

| Condition | Required behavior | Status |
| --- | --- | --- |
| Q1 or Q2 unanswered | Do not infer eligibility or generate recommendations | Agreed/documented |
| Required screening answers missing | Request completion before ranking; follow T43 validation rules | Agreed/documented |
| Q8 level 4–5, including secondary acne | Referral and no routine | Agreed/documented |
| Q7 stinging or Q11 irritation | Do not automatically refer without an approved rule | Pending irritation policy |
| Q7 displayed but unanswered | Request completion before ranking | Proposed — approval needed |
| Known allergy and unverified ingredient information | Do not claim allergy safety or generate an automated allergy-based routine | Agreed/documented |
| Unknown fragrance/essential-oil status | Never infer verified presence or absence | Agreed/documented |
| No verified category match | Explain missing step; return partial or empty routine if otherwise eligible | Agreed/documented |

General questionnaire validation and optional-answer defaults are defined in Questionnaire-Update.md.

## 6. Proposed acceptance tests

These scenarios specify **expected behavior**, not observed passing tests. Use controlled inputs for tests. `routine_status = not_generated` where ranking never starts.

| ID | Input / setup | Expected eligibility or response | Expected routine |
| --- | --- | --- | --- |
| SC-101 | Q1 = no | `out_of_scope`; adult-only message | `not_generated` |
| SC-102 | Q1 unanswered | Ask Q1; do not assume eligible | `not_generated` |
| SC-103 | Q2 unanswered | Ask Q2; no inferred `safety_flags: []` | `not_generated` |
| SC-104 | Q2 = none, supported dryness concern, other required answers complete | `eligible` | Ranking permitted |
| RF-101 | Q2 unusual/sudden severe skin change | `referred`; medical-assessment guidance | `not_generated` |
| RF-102 | Q2 prescribed skincare | Current documented referral; confirm final status | `not_generated` |
| RF-103 | Q2 pregnant/breastfeeding | No-routine professional guidance | `not_generated` |
| RF-104 | Q2 known ingredient allergy | Current documented referral; no allergy-safe claim | `not_generated` |
| RF-105 | Acne level 4, only concern | `referred` | `not_generated` |
| RF-106 | Acne level 5 selected as secondary to dryness | `referred` despite dryness priority | `not_generated` |
| RF-107 | Acne level 3, no other flags | `eligible` if all answers complete | Ranking permitted |
| SI-101 | Sensitive skin only; Q9 yes; no Q2 flags | `eligible`; gentleness tie-break where products tie | Ranking permitted |
| SI-102 | Sensitive skin only; Q9 not_sure; no Q2 flags | `eligible`; no gentleness preference | Ranking permitted |
| SI-103 | Q7 stinging, no Q2 flags | **Pending:** apply reviewed irritation policy, not an invented automatic referral | Pending policy |
| DR-101 | Dryness alone; no Q2 flags | `eligible`; ask Q6–Q7 | Ranking permitted after required answers |
| MC-101 | Dryness primary; acne level 4 secondary | `referred`; do not rank | `not_generated` |
| MC-102 | Sensitivity primary; dryness secondary; no blocking flags | `eligible`; collect Q6–Q7 and Q9 | Ranking permitted |
| MD-101 | Q8 missing with acne selected | Ask Q8 | `not_generated` |
| MD-102 | Q9 missing | Ask Q9 | `not_generated` |
| MD-103 | Two concerns, Q4 missing | Ask priority | `not_generated` |
| MD-104 | Dryness selected; Q7 displayed but unanswered | Request Q7 completion; proposed rule awaiting approval | `not_generated` |
| RS-101 | No eligible sunscreen candidates, other two verified | `eligible`; explain unmatched sunscreen | `partial` |
| RS-102 | No verified matches | `eligible`; explain no verified products | `empty` |
| RS-103 | Catalogue fragrance/essential oil status unknown | No unverified presence/absence or safety claim | Status depends on other eligibility and matching criteria |

## 7. Open decisions requiring team approval

- Confirm whether Q7 is required whenever displayed.
- Confirm the appropriate response to persistent or significant irritation.
- Approve eligibility statuses for pregnancy/breastfeeding, prescribed skincare, and known ingredient allergies.
- Review and approve the proposed user-facing safety messages.
- Decide whether additional safety follow-up questions are necessary.
