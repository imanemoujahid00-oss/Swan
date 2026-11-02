## The 31 profiles

| Profiles | What they test | Expected |
|---|---|---|
| P01 to P20 | Every skin type (5) × reactive or not (2) × avoids fragrance or not (2). Blemish level goes 1, 2, 3 in turn | 3 products |
| P21, P22 | The other two Q7 answers: avoid essential oils, avoid both | 3 products |
| P23 | Under 18 | referral |
| P24 | Something else than acne-prone skin | out of scope |
| P25, P26 | Blemish level 4 and 5 | referral |
| P27, P28, P29 | Prescribed treatment, worrying skin change, pregnant or breastfeeding | referral |
| P30 | Two Q4 answers at once (pregnant + prescribed treatment) | referral |
| P31 | Blemish level 3, just below the threshold | 3 products |

**`swan_test_profiles_v1.csv`**, one row per profile:

| Column | Meaning |
|---|---|
| `profile_id` | P01 to P31 |
| `kind` | `recommendation` or `edge case: ...` |
| `is_adult` ... `avoid` | the answers, same names and values as in `questionnaire.md` |
| `expected` | `products`, `referral` or `out of scope` |
| `expected_traits` | what a good product should respect for this profile (see below) |

**`swan_test_results_v1.csv`**, one row per recommended product (3 per profile), or one row when there is no product:

| Column | Meaning |
|---|---|
| `outcome` | what `recommend()` gave |
| `rank`, `code`, `product_name`, `score` | the recommended product |
| `R2_respects_avoid` | the product respects Q7 (automatic) |
| `texture_ok` | the texture matches the rule (automatic, see limits) |
| `R4_face_moisturizer`, `R5_texture_fits`, `comment` | to fill by hand |

## Expected traits

| Answer | Expected trait |
|---|---|
| Avoid fragrance | no parfum |
| Avoid essential oils | no essential oil |
| Reactive skin | fragrance-free first |
| Oily, combination, normal, not sure | not rich (light preferred) |
| Dry | rich |


## For Loubna

- Profiles: the 31 profiles in `swan_test_profiles_v1.csv`.
- Products: Lina's catalogue v1 is the reference. Until it is shared, use my draft `draft_for_lina_moisturizers.csv` (`in_scope == True`) to start.
- Ingredient matrix (optional): `draft_for_lina_ingredient_matrix.csv`, join on `code`.
- Columns the score can use: `has_parfum`, `has_essential_oil`, `has_acne_active`, `is_rich`, `is_light`, `is_anti_ageing`.
- Keep the same output as `recommend()`: `referral`, `out of scope`, `not enough products`, or the top 3.

## How I set the product signals

- has_parfum : parfum in the ingredient list
- has_essential_oil : if there is any essential oil from the essential oil list - created based on knowledge and based o research
- has_acne_active : based on my knowledge and some research - represent the actifs for acne : salicylic acid, niacinamide, zinc PCA, zinc gluconate or azelaic acid
- is_rich : water is not the first ingredient, or a heavy ingredient (butter, wax, oil, petrolatum, mineral oil…) in the first 3, or 2 in the first 5
- is_light : water first and no heavy ingredient in the first 5
The product name wins when it says the texture: "riche", "baume", "cold cream" = rich; "gel", "fluide", "matifiant" = light
