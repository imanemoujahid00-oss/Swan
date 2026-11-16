# Swan — Personalized Skincare Questionnaire

**Welcome to Swan!**

Let's find the skincare routine that suits your skin.

Answer a few questions about your skin, concerns, and preferences. Swan will help you discover a cleanser, moisturizer, and facial sunscreen tailored to your needs.

Swan gives cosmetic skincare guidance, not medical diagnosis or treatment.

## Questions

### **Section A - Eligibility and Safety**

**Q1. Are you 18 or older?**

- yes
- no

*Required.*

*If no: Stop. Swan is currently designed for adults.*

**Q2. Are any of the following true for you?**

*Select all that apply.*

- I currently use a skincare treatment prescribed by a healthcare professional.
- I am pregnant or breastfeeding.
- I have a sudden, severe, painful, or unusual skin change.
- I have a known allergy to a skincare ingredient.
- None of the above.

*Required. “None of the above” is exclusive. Safety and referral decisions are evaluated before product ranking. For pregnancy/breastfeeding, the review draft specifies no routine; see the safety section.*

### **SECTION B — Your Skin Concerns**

**Q3. What would you like your skincare routine to focus on?**

*Select all that apply.*

- **Dryness and skin barrier concerns:** My skin often feels dry, tight, rough, or flaky.
- **Acne-prone skin and blemishes:** I experience pimples, blackheads, whiteheads, or clogged pores.
- **Sensitive or easily irritated skin:** My skin reacts easily with redness, stinging, or discomfort.
- I'm not sure

*Required. “I'm not sure” is exclusive. Display examples of the three concerns and allow the user to return to Q3; do not rank until a supported concern is selected, per the working review draft.*

**Q4. Which of your selected concerns is your main priority?**

- [Display only supported concerns selected in Q3]

*Only shown and required when more than one supported concern is selected. If exactly one is selected, set it automatically as `primary_concern`.*

### **SECTION C — Your Skin Characteristics**

**Q5. How would you describe your skin type?**

- Oily — My skin often looks shiny or feels greasy.
- Dry — My skin often feels tight, rough, or lacks moisture.
- Combination — Some areas are oily, while others feel normal or dry.
- Normal — My skin usually feels balanced.
- I'm not sure.

*Required for eligible users.*

**Q6. How often does your skin feel dry, tight, rough, or flaky?**

- Never
- Occasionally
- Often
- Almost every day
- I'm not sure

*Conditional: shown if dryness/barrier is selected or Q5 is Dry. Its effect on ranking has not yet been agreed.*

**Q7. Which signs of dryness or barrier discomfort do you experience?**

*Select all that apply.*

- Tightness, especially after washing
- Stinging when applying skincare
- Redness or discomfort
- None of these

*Conditional: shown when dryness/barrier is selected. “None of these” is exclusive. Its effect on ranking has not yet been agreed.*

**Q8. Which option best describes your blemishes right now?**

- No blemishes right now
- Level 1 — A few occasional spots or clogged pores
- Level 2 — Several small spots, blackheads, or whiteheads
- Level 3 — Frequent spots, sometimes red or inflamed
- Level 4 — Many inflamed or painful spots
- Level 5 — Deep, painful lumps under the skin or significant scarring

*Required whenever acne-prone is selected, including when it is a secondary concern. “No blemishes right now” maps to `blemish_level: 0`. Level 4–5 enters the existing guidance/referral pathway before ranking.*

**Q9. Does your skin react easily to new skincare products?**

- Yes
- No
- Not sure

*Required for eligible users.*

### **SECTION D — Your Current Routine**

**Q10. Which skincare products do you currently use?**

*Select all that apply.*

- Facial cleanser
- Moisturizer
- Facial sunscreen
- Exfoliating products or active serums
- None — I don't currently follow a skincare routine

*Required. "None" is exclusive.*

**Q11. How does your skin usually feel after cleansing?**

- Comfortable and balanced
- Tight or dry
- Still oily
- Irritated or stinging
- I'm not sure / I don't use a cleanser

*Required.*

### **SECTION E — Product Preferences**

**Q12. What texture do you prefer for your moisturizer?**

- Lightweight gel or gel-cream
- Light lotion
- Rich cream
- No preference

*Optional.*

**Q13. What kind of cleanser do you prefer?**

- Rinse-off cleanser — I wash it off with water.
- No-rinse cleanser — I remove it with a cotton pad or soft cloth, without rinsing.
- No preference

*Optional.*

**YOUR PERSONALIZED SWAN ROUTINE**

Based on your answers, Swan will identify suitable products for:

1. Facial cleanser
2. Moisturizer
3. Facial sunscreen

For every selected product, Swan will explain:

- Why it matches your skin profile
- Relevant ingredients and formulation characteristics
- How to incorporate it into your routine
- Any uncertainties or limitations in the product information

If Swan cannot verify a suitable product for a step, it will explain why instead of suggesting an unverified alternative.

**Important:** Swan provides cosmetic skincare guidance, not medical diagnosis or treatment. Individual skin tolerance varies. Always check the product packaging, especially if you have allergies.

## Routing specification — questions displayed and expected outcomes

| Scenario | Conditional questions | Expected behavior |
| --- | --- | --- |
| Acne only | Q8; Q9 asked | Auto-set acne as primary; require Q8; rank for acne if safely eligible |
| Dryness only | Q6–Q7; Q9 asked | Auto-set dryness as primary; rank for dryness if safely eligible |
| Sensitivity only | Q9 asked; no Q8/Q6–Q7 unless Q5 = Dry | Auto-set sensitivity as primary; use sensitivity concern score; Q9 separately controls gentleness tie-break |
| Acne + dryness | Q4, Q6–Q8, Q9 | Rank using selected primary concern; collect Q8 even if acne is secondary |
| Acne + sensitivity | Q4, Q8, Q9 | Rank using selected primary concern; apply Q8 safety checks |
| Dryness + sensitivity | Q4, Q6–Q7, Q9 | Rank using selected primary concern |
| All three | Q4, Q6–Q8, Q9 | Rank using selected primary concern; apply all safety checks |
| One supported concern | Skip Q4 | Derive `primary_concern` from Q3 |
| Skin type Dry, without dryness selected | Q6; Q9 | Q6 collected; Q7 not shown unless dryness selected; ranking impact of Q6 pending |
| Q3 = I'm not sure | No ranking yet | Display concern explanations and return to Q3 |
| Q8 = level 0 | Q8 answered | Continue acne route; 0 is a valid answer |
| Q8 missing when acne selected | Q8 required | Ask for missing answer before ranking |
| Q8 = level 4 or 5 | Safety guidance | Do not generate routine in the current reviewed route |
| Q9 = Yes | Q9 answered | At equal concern score, favor verified gentle candidate before moisturizer texture tie-break |
| Q9 = No or Not sure | Q9 answered | No gentleness tie-break preference |

### Ranking behavior for overlapping concerns

For the current Swan version:

1. **Primary concern:** Determines ranking priority. With one concern, assign it automatically.
2. **Secondary concerns:** Retain in the profile; do not assume additional scoring weights.
3. **Reactivity:** When concern scores tie and Q9 is yes, prefer a catalogue-verified gentle product.
4. **Skin-type:** For tied moisturizers, oily skin favors lightweight textures; dry skin favors rich textures, after the reactivity tie-break.
5. **Unconfirmed effects:** Q6–Q7 and Q10–Q13 do not have confirmed additional ranking effects.

Safety and referral checks always precede ranking (see Scope-and-Referral-Rules.md).

## Safety and referral handling

Swan applies eligibility and safety checks before generating recommendations.

Users who meet a documented stop or referral condition do not receive a personalized routine.

The authoritative eligibility rules, referral triggers, user-facing messages, and unresolved safety decisions are maintained in Scope-and-Referral-Rules.md.

Q8 acne levels 4–5 trigger the no-routine referral pathway, even when acne is a secondary concern. Q9 reactivity alone does not trigger referral.

## Profile Schema

### A. Safety & Eligibility

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `is_adult` | Q1 | `true` / `false` | Yes | — |
| `safety_flags` | Q2 | `prescribed_treatment`, `pregnant_or_breastfeeding`, `unusual_skin_change`, `known_allergy` | Yes | — |

- `—` means no automatic default; a required answer must be collected.
- `safety_flags=[]` is valid only after Q2 is answered with "None of the above".

### B. Skin Concerns

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `concerns` | Q3 | `dryness_barrier`, `acne_prone`, `sensitive_skin`, `not_sure` | Yes | — |
| `primary_concern` | Q4 | `dryness_barrier`, `acne_prone`, `sensitive_skin` | If multiple concerns selected | — |

`concerns` is a list, allowing users to select multiple concerns. `not_sure` is an exclusive choice.

### C. Skin Characteristics

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `skin_type` | Q5 | `oily`, `combination`, `normal`, `dry`, `not_sure` | If eligible | — |
| `dryness_frequency` | Q6 | `never`, `occasionally`, `often`, `almost_daily`, `not_sure` | When displayed | `null` |
| `dryness_signs` | Q7 | `tightness`, `stinging`, `redness`, `none` | Proposed: when displayed | `null` |
| `blemish_level` | Q8 | `0` to `5` | If acne-prone | `null` |
| `reactivity` | Q9 | `yes`, `no`, `not_sure` | Eligible users | No default |

**Notes:**

- `blemish_level = 0` means no current blemishes.
- `blemish_level = null` means the question was not applicable or not answered.

### D. Current Skincare Routine

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `current_products` | Q10 | `cleanser`, `moisturizer`, `sunscreen`, `actives`, `none` | If eligible | — |
| `after_cleansing` | Q11 | `comfortable`, `tight_dry`, `still_oily`, `irritated`, `not_sure` | If eligible | — |

- `current_products=["none"]` represents an explicit Q10 "None" selection.

### E. Product Preferences

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `moisturizer_texture` | Q12 | `gel`, `lotion`, `rich_cream`, `no_preference` | No | `no_preference` |
| `cleanser_type` | Q13 | `rinse_off`, `no_rinse`, `no_preference` | No | `no_preference` |

## Additional System Fields

These fields are calculated by Swan rather than answered directly by the user.

| Field | Values | Purpose |
| --- | --- | --- |
| `eligibility_status` | `eligible`, `out_of_scope`, `requires_review`, `referred` | Determines whether recommendations may proceed |
| `routine_status` | `complete`, `partial`, `empty`, `not_generated` | Describes recommendation completeness |

## Validation and missing-data behavior

1. Require Q1–Q2 before proceeding. Missing safety answers must never be treated as negative answers.
2. Q3 supports multiple concerns; not_sure is exclusive. Q4 is required for multiple concerns and automatically derived for a single concern.
3. Q6 appears for dryness concern or dry skin type. Q7 appears for dryness concern; requiring its completion is pending team approval.
4. Q8 is required whenever acne is selected, including as a secondary concern. 0 is valid; null is not equivalent to zero.
5. Q9 is required for eligible users. not_sure is a valid answer, distinct from unanswered.
6. The "None" selections in Q2, Q7, and Q10 are exclusive. Distinguish skipped or unanswered questions from explicitly selecting "None".
7. Optional Q12–Q13 default to no_preference; do not assume unconfirmed ranking effects.
8. Never infer ingredient absence from unknown catalogue data.
9. routine_status is complete for three verified steps, partial for one or two, empty for none, and not_generated when ranking never runs.

See **Scope-and-Referral-Rules.md** for detailed safety and referral handling.

## Representative testing

Representative single-concern, overlapping-concern, reactivity, skin-type, safety, missing-answer, and product-availability scenarios are maintained in:

- Scope-and-Referral-Rules.md: Safety and referral acceptance tests.

- Representative-Profiles-and-Relevance-Rubric.md: Canonical profiles and controlled ranking comparisons.

**Example user profile**

A user with combination skin, acne-prone skin, dryness, and skin reactivity.

```json
{
"is_adult": true,
"safety_flags": [],

"concerns": [
"acne_prone",
"dryness_barrier"
],
"primary_concern": "acne_prone",

"skin_type": "combination",
"dryness_frequency": "often",
"dryness_signs": ["tightness"],
"blemish_level": 2,

"reactivity": "yes",
"current_products": ["cleanser", "moisturizer"],
"after_cleansing": "tight_dry",

"moisturizer_texture": "lotion",
"cleanser_type": "rinse_off",

"eligibility_status": "eligible",
"routine_status": "not_generated"
}
```
