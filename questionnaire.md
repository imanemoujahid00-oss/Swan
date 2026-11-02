# Swan questionnaire and profile schema

## Scope

Decided at the Meet on 26/10: adults with acne-prone skin and mild blemishes. Swan suggests 3 alternative moisturizers, not three products to apply together. Products sold in France for now.
Swan does not diagnose or treat. We say "acne-prone skin", not "acne treatment".
Changes since v1 (25/10): moisturizers only, France only, Q3 is now a 1 to 5 scale, reactivity is yes/no, texture is removed.

## Questions

Questions 1 to 4 come first. Stop at a referral or out-of-scope result; later answers are not required. For Q4 and Q7, "None" cannot be selected with another answer.

1. Are you 18 or older? (yes / no)
2. What would you like help with? (a routine for acne-prone skin / something else)
3. How would you describe your blemishes? (1 to 5, see below)
4. Do any of these apply to you? (several answers possible)
    - I use a skin treatment prescribed by a doctor
    - I have a sudden, painful flare-up or a skin change that worries me
    - I am pregnant or breastfeeding
    - None of these
5. What is your skin type? (oily / combination / normal / dry / not sure)
6. Does your skin react easily, for example stinging or redness? (yes / no)
7. Are there ingredients you prefer to avoid? (fragrance / essential oils / none). Optional.

Note under Q7: "Ingredient lists can be incomplete. If you have an allergy, check the packaging or ask a pharmacist."

### Q3 levels

Based on the NHS description of acne, from "a few spots" to "deep, painful lumps under your skin".

| Level | What the user reads | Result |
|---|---|---|
| 1 | A few blackheads or small spots now and then | products |
| 2 | Some small spots, often in the same area | products |
| 3 | Small spots in several areas, not painful | products |
| 4 | Lots of red or swollen spots | referral |
| 5 | Deep, painful lumps, or spots that leave scars | referral |

## Profile

| Field | Question | Values | Required | Default |
|---|---|---|---|---|
| `is_adult` | Q1 | `true` / `false` | yes | |
| `concern` | Q2 | `acne_prone` / `other` | yes | |
| `blemish_level` | Q3 | `1` to `5` | yes | |
| `referral_flags` | Q4 | `prescribed_treatment`, `unusual_lesion`, `pregnant_or_breastfeeding` | yes | `[]` |
| `skin_type` | Q5 | `oily` / `combination` / `normal` / `dry` / `not_sure` | if not referred | |
| `reactivity` | Q6 | `true` / `false` | if not referred | |
| `avoid` | Q7 | `fragrance`, `essential_oils` | no | `[]` |

Example:

```json
{"is_adult": true, "concern": "acne_prone", "blemish_level": 2, "referral_flags": [],
 "skin_type": "oily", "reactivity": true, "avoid": ["fragrance"]}
```

## When we don't recommend products

| Situation | Result | Message |
|---|---|---|
| Under 18 | referral | "Swan is made for adults. Please ask a specialized doctor if needed." |
| Something else than acne-prone skin | out of scope | "Swan only covers acne-prone skin for now." |
| Q3 level 4 or 5 | referral | "Lots of red, painful or deep spots, or scars, are worth showing to a doctor or dermatologist." |
| Prescribed treatment | referral | "Check with the person who prescribed your treatment before adding new products." |
| Sudden flare-up or worrying change | referral | "A sudden or unusual change in your skin should be checked by a doctor." |
| Pregnant or breastfeeding | referral | "This MVP does not suggest products during pregnancy or breastfeeding. Please ask a pharmacist or your healthcare professional for advice." |

## Other points and ranking for scoring :
- Avoid fragrance filters `parfum` only, not fragrance allergens automatically.
- Normal and not-sure skin follow the same provisional scoring rule as combination skin.
- Keep the anti-acne ingredient bonus in the baseline score.
- Test profiles include `expected_traits`; results report texture fit against our current proxies.
- Under 18: referral. Other concern: out of scope.
