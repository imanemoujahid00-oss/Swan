# questionnaire update

# Swan - Personalized Skincare Questionnaire

**Welcome to Swan!**

Let's find the skincare routine that suits your skin.

Answer a few questions about your skin, concerns, and preferences. Swan will help you discover a cleanser, moisturizer, and facial sunscreen tailored to your needs.

Your answers will help us personalize your recommendations.

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

*Required. "None of the above" cannot be combined with other options.*

Some answers may require additional questions, medical guidance, or a referral before Swan provides recommendations.

### **SECTION B — Your Skin Concerns**

**Q3. What would you like your skincare routine to focus on?**

*Select all that apply.*

- **Dryness and skin barrier concerns:** My skin often feels dry, tight, rough, or flaky.
- **Acne-prone skin and blemishes:** I experience pimples, blackheads, whiteheads, or clogged pores.
- **Sensitive or easily irritated skin:** My skin reacts easily with redness, stinging, or discomfort.
- I'm not sure
- Something else

*Required. "I'm not sure" and "Something else" are exclusive selections.*

**Q4. Which of your selected concerns is your main priority?**

*Only shown when more than one concern is selected.*

- [Display the concerns selected in Q3]

*Required for users with multiple concerns.*

### **SECTION C — Your Skin Characteristics**

**Q5. How would you describe your skin type?**

- Oily — My skin often looks shiny or feels greasy.
- Dry — My skin often feels tight, rough, or lacks moisture.
- Combination — Some areas are oily, while others feel normal or dry.
- Normal — My skin usually feels balanced.
- I'm not sure.

*Required.*

**Q6. How often does your skin feel dry, tight, rough, or flaky?**

- Never
- Occasionally
- Often
- Almost every day
- I'm not sure

*Shown when dryness/barrier concerns are selected or when Q5 is Dry. Also available to uncertain users.*

**Q7. Which signs of dryness or barrier discomfort do you experience?**

*Select all that apply.*

- Tightness, especially after washing
- Rough or flaky skin
- Dry patches
- Stinging when applying skincare
- Redness or discomfort
- None of these

*Shown when dryness/barrier concerns are selected. "None" is exclusive.*

**Q8. Which option best describes your blemishes right now?**

*Shown when acne-prone skin is selected.*

- No blemishes right now
- Level 1 — A few occasional spots or clogged pores
- Level 2 — Several small spots, blackheads, or whiteheads
- Level 3 — Frequent spots, sometimes red or inflamed
- Level 4 — Many inflamed or painful spots
- Level 5 — Deep, painful lumps under the skin or significant scarring

*Required for the acne-prone route.*

Higher levels may require professional assessment instead of an automatic routine.

**Q9. How often does your skin react to new skincare products?**

- Rarely or never
- Sometimes
- Often
- I'm not sure

*Required for all users.*

**Q10. What reactions have you experienced after applying skincare products?**

*Select all that apply.*

- Redness
- Stinging or burning
- Itching
- Dryness or tightness
- New blemishes or clogged pores
- No noticeable reactions
- I'm not sure

*Shown if Q9 is Sometimes or Often.*

"No noticeable reactions" and "I'm not sure" are exclusive selections.

### **SECTION D — Your Current Routine**

**Q11. Which skincare products do you currently use?**

*Select all that apply.*

- Facial cleanser
- Moisturizer
- Facial sunscreen
- Exfoliating products or active serums
- None — I don't currently follow a skincare routine

*Required. "None" is exclusive.*

**Q12. How does your skin usually feel after cleansing?**

- Comfortable and balanced
- Tight or dry
- Still oily
- Irritated or stinging
- I'm not sure / I don't use a cleanser

*Required.*

### **SECTION E — Product Preferences**

**Q13. What texture do you prefer for your moisturizer?**

- Lightweight gel or gel-cream
- Light lotion
- Rich cream
- No preference

*Optional.*

**Q14. What kind of finish do you prefer from your facial sunscreen?**

- Matte / shine-controlling
- Natural
- Hydrating / dewy
- No preference

*Optional.*

**Q15. Do you prefer tinted or non-tinted facial sunscreen?**

- Tinted
- Non-tinted
- No preference

*Optional.*

### **SECTION F — Ingredients & Budget**

**Q16. Are there any ingredients you prefer to avoid?**

*Select all that apply.*

- Fragrance
- Essential oils
- Other ingredients (please specify)
- No preference

*Required. "No preference" is exclusive.*

Selected exclusions must be respected across all three products.

**YOUR PERSONALIZED SWAN ROUTINE**

Based on your answers, Swan will identify suitable products for:

**Morning**

1. Facial cleanser, when needed
2. Moisturizer
3. Facial sunscreen

**Evening**

1. Facial cleanser
2. Moisturizer

For every selected product, Swan will explain:

- Why it matches your skin profile
- Relevant ingredients and formulation characteristics
- How to incorporate it into your routine
- Any uncertainties or limitations in the product information

If Swan cannot verify a suitable product for a step, it will explain why instead of suggesting an unverified alternative.

**Important:** Swan provides cosmetic skincare guidance, not medical diagnosis or treatment. Individual skin tolerance varies. Always check the product packaging, especially if you have allergies.

## How many questions will users actually answer?

Although the full questionnaire contains 17 questions, conditional routing means most users won't see all of them.

| User profile | Likely questions shown |
| --- | --- |
| Acne-prone only | Q1–5, Q8–9, Q11–16 |
| Dryness only | Q1–7, Q9, Q11–16 |
| Sensitive only | Q1–5, Q9–16 with Q10 conditional |
| Multiple concerns | All relevant concern-specific questions |
| No reported reactivity | Skip Q10 |
| One concern selected | Skip Q4 |

For an average user, I would aim for approximately 11–13 short questions, including optional preferences. This is a design target to validate in usability testing, not a measured completion estimate.

## How Swan should use each answer

Not every question should influence ranking equally. Some determine safety, some identify suitable formulations, and others improve the experience.

| Question | Main purpose | Impact |
| --- | --- | --- |
| Q1 Age | Eligibility | Hard requirement |
| Q2 Safety | Identify referral or special review needs | Safety gate |
| Q3 Concerns | Determine relevant matching criteria | High |
| Q4 Priority | Prioritize overlapping concerns | High |
| Q5 Skin type | Guide formulation suitability | Medium |
| Q6 Dryness frequency | Assess hydration needs | High for dryness |
| Q7 Dryness signs | Inform barrier-related matching | Medium |
| Q8 Blemish level | Screen acne severity | Safety and scope |
| Q9 Reactivity | Identify sensitivity considerations | High once validated |
| Q10 Reaction types | Identify tolerability considerations | Medium |
| Q11 Current routine | Tailor usage instructions | Low for product ranking |
| Q12 After cleansing | Guide cleanser selection | High once validated |
| Q13 Moisturizer texture | Personal preference | Medium |
| Q14 Sunscreen finish | Personal preference | Medium |
| Q15 Sunscreen tint | Personal preference | Medium |
| Q16 Ingredient avoidance | Filter eligible products | Hard restriction |

## How the recommendation system should handle overlapping concerns

For the full version, I recommend replacing three independent concern-specific ranking routes with a shared profile that combines the user's concerns.

Example: A user with multiple concerns

Primary concern: Acne-prone skin

Additional concern: Dryness

Skin type: Combination

Reactivity: Often

Ingredient restrictions: Avoid fragrance

**Expected matching approach**

Cleanser: A gentle, non-stripping cleanser suitable for acne-prone skin and dryness.

Moisturizer: A hydrating formulation with appropriate evidence of suitability for acne-prone skin.

Sunscreen: A comfortable, low-irritation formula with verified SPF and UVA protection.

## Safety and referral decisions for the final version

The final app should adopt the following rules, subject to professional review.

| Situation | Suggested handling |
| --- | --- |
| Under 18 | Stop: outside Swan's current scope |
| Sudden severe reaction, swelling, blistering, or unusual lesion | Stop and provide appropriate medical guidance; urgent symptoms warrant urgent care |
| Deep, painful blemishes or significant scarring | Refer for professional evaluation |
| Using prescription skincare | Avoid modifying treatment; use a reviewed compatibility pathway or refer |
| Pregnant or breastfeeding | Use a specifically reviewed eligibility and product pathway, or defer personalized recommendations |
| Known ingredient allergy | Collect the exact allergen through a separate safety flow; only use verified exclusions |
| Frequent stinging or irritation | Apply conservative suitability criteria and offer professional guidance if symptoms persist or are significant |

## Test scenarios to add before launch

The original 11 profiles remain valuable. For the full app, I would extend them to cover the new functionality.

| ID | Test scenario | Expected outcome |
| --- | --- | --- |
| MC-01 | Acne-prone + dryness | Products satisfy both concerns |
| MC-02 | Acne-prone + sensitivity | Low-irritation routine, appropriate acne suitability |
| MC-03 | Dryness + sensitivity | Gentle, hydrating routine |
| MC-04 | All three concerns | Prioritized, compatible routine |
| DR-01 | Oily skin with frequent dryness | Hydration needs are not ignored |
| SI-03 | Frequent stinging after cleansing | Conservative cleanser matching and safety screening |
| SP-01 | Tinted sunscreen preference | Prefer verified tinted candidates |
| SP-02 | No sunscreen matches restrictions | Show partial routine and explain the missing step |
| AL-01 | Known allergy | Strict verified exclusion or referral |
| UN-01 | Unknown skin type and concerns | Provide a conservative basic routine if eligible |
| RT-01 | User already has a routine | Adapt usage instructions without assuming existing products are suitable |

## Profile

### A. Safety & Eligibility

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `is_adult` | Q1 | `true` / `false` | Yes | — |
| `safety_flags` | Q2 | `prescribed_treatment`, `pregnant_or_breastfeeding`, `unusual_skin_change`, `known_allergy` | Yes | `[]` |

### B. Skin Concerns

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `concerns` | Q3 | `dryness_barrier`, `acne_prone`, `sensitive_skin`, `not_sure`, `other` | Yes | `[]` |
| `primary_concern` | Q4 | `dryness_barrier`, `acne_prone`, `sensitive_skin` | If multiple concerns selected | — |

`concerns` is a list, allowing users to select multiple concerns. `not_sure` and `other` are exclusive choices.

### C. Skin Characteristics

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `skin_type` | Q5 | `oily`, `combination`, `normal`, `dry`, `not_sure` | If eligible | — |
| `dryness_frequency` | Q6 | `never`, `occasionally`, `often`, `almost_daily`, `not_sure` | Conditional | `null` |
| `dryness_signs` | Q7 | `tightness`, `flaking`, `dry_patches`, `stinging`, `redness`, `none` | Conditional | `[]` |
| `blemish_level` | Q8 | `0` to `5` | If acne-prone | `null` |
| `reactivity` | Q9 | `rarely_never`, `sometimes`, `often`, `not_sure` | If eligible | — |
| `reaction_types` | Q10 | `redness`, `stinging_burning`, `itching`, `dryness_tightness`, `breakouts`, `none`, `not_sure` | Conditional | `[]` |

**Notes:**

- `blemish_level = 0` means no current blemishes.
- `blemish_level = null` means the question was not applicable or not answered.
- Q6–Q7 appear for relevant dryness/barrier profiles.
- Q10 appears when reactivity is `sometimes` or `often`.

### D. Current Skincare Routine

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `current_products` | Q11 | `cleanser`, `moisturizer`, `sunscreen`, `actives`, `none` | If eligible | `[]` |
| `after_cleansing` | Q12 | `comfortable`, `tight_dry`, `still_oily`, `irritated`, `not_sure` | If eligible | — |

### E. Product Preferences

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `moisturizer_texture` | Q13 | `gel`, `lotion`, `rich_cream`, `no_preference` | No | `no_preference` |
| `sunscreen_finish` | Q14 | `matte`, `natural`, `dewy`, `no_preference` | No | `no_preference` |
| `sunscreen_tint` | Q15 | `tinted`, `non_tinted`, `no_preference` | No | `no_preference` |

### F. Ingredients & Budget

| Field | Question | Values | Required | Default |
| --- | --- | --- | --- | --- |
| `avoid` | Q16 | `fragrance`, `essential_oils`, `other` | No | `[]` |
| `other_avoid_ingredients` | Q16 | List of ingredient names | If `other` selected | `[]` |

---

## Additional System Fields

These fields are calculated by Swan rather than answered directly by the user.

| Field | Values | Purpose |
| --- | --- | --- |
| `eligibility_status` | `eligible`, `out_of_scope`, `requires_review`, `referred` | Determines whether recommendations may proceed |
| `routine_status` | `complete`, `partial`, `empty`, `not_generated` | Describes recommendation completeness |

## Validation Rules

1. Q1 and Q2 are required before continuing.
2. If the user is under 18, stop the questionnaire.
3. If a safety flag is selected, apply the corresponding safety pathway before product ranking.
4. Allow multiple skin concerns, but only one primary concern.
5. Require `blemish_level` only for acne-prone users.
6. Allow `blemish_level = 0` to represent no current blemishes.
7. Use `null` for questions that were not asked.
8. Apply verified ingredient exclusions to all three product categories.
9. Do not automatically remove restrictions to produce a complete routine.
10. If a product category has no eligible matches, return a partial or empty routine with an explanation.

**Example user profile**

A user with combination skin, acne-prone skin, dryness, frequent reactivity, and fragrance avoidance

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
"dryness_signs": [
"tightness",
"dry_patches"
],
"blemish_level": 2,

"reactivity": "often",
"reaction_types": [
"redness",
"stinging_burning"
],

"current_products": [
"cleanser",
"moisturizer"
],
"after_cleansing": "tight_dry",

"moisturizer_texture": "lotion",
"sunscreen_finish": "natural",
"sunscreen_tint": "non_tinted",

"avoid": ["fragrance"],
"other_avoid_ingredients": [],

"eligibility_status": "eligible",
"routine_status": "not_generated"
}
```
