# Swan files: what to use

Loredana, 02/11/2026. Branch `loredana`. Data files are never in Git (`raw_data/` is ignored): share them on the Drive.

## Documents (in Git)

| File | What it is | Who uses it |
|---|---|---|
| `questionnaire.md` | The 7 questions, profile fields and values, referral and out-of-scope messages | Imane (app), whole team |
| `test_profiles.md` | The 31 test profiles, the result files, how we judge results, product signals | Loubna (score), whole team |
| `files_guide.md` | This file | whole team |

## Notebooks (in Git)

| File | What it is | Status |
|---|---|---|
| `notebooks/loredana_questionnaire_v2_mvp.ipynb` | Main notebook: catalogue draft, signals, questionnaire, `recommend()`, test profiles | **Use this one** |
| `notebooks/loredana_data_check_questionnaire.ipynb` | First exploration (23–30/10): scope, France, categories, from the full Open Beauty Facts file | Kept as evidence only, not up to date |

## Input data (in `raw_data/`)

| File | What it is | Used by |
|---|---|---|
| `moisturizers_with_cosing.csv` | 244 moisturizer candidates (team audit 27/09 + first CosIng matching) | main notebook |
| `Swan_CosIng_Ingredient_Reference_2026-10-26.csv` | CosIng reference, 1,521 ingredients (same file as `cosing_reference_matched.csv` in the team folder) | main notebook |
| `en.openbeautyfacts.org.products.csv` | Full Open Beauty Facts export (29/10), worldwide | first exploration notebook only |

## Files created by the main notebook (in `raw_data/`, run again with Restart → Run All)

| File | One row = | For |
|---|---|---|
| `draft_for_lina_moisturizers.csv` | one product (`in_scope`, `exclusion_reason`, `possible_duplicate`, signals) | Lina, Loubna (until Lina's catalogue is ready) |
| `draft_for_lina_ingredient_matrix.csv` | one product, one column per ingredient (1 = contains it) | Loubna (model) |
| `draft_for_lina_ingredients_long.csv` | one product × one ingredient, with position and INCI name | Lina (only if she needs it) |
| `swan_test_profiles_v1.csv` | one test profile (31) | Loubna, whole team |
| `swan_test_results_v1.csv` | one recommended product, with R4 / R5 to judge by hand | whole team |

## Old files: don't use

| File | Why |
|---|---|
| `swan_moisturizers_v1.csv`, `swan_moisturizers_ingredients_long_v1.csv` | First catalogue draft (30/10), replaced by the `draft_for_lina_*` files |
| `draft_for_lina_matrix_coverage.csv` | Left from a test version, not created by the notebook anymore: can be deleted |
| `swan_basic_routine_candidates.csv` | 494 products with cleansers and sunscreens (the 244 moisturizers come from it) |
| `all_routine_candidates.csv` | 699 products with serums: for later, not the MVP |
| `eu_uv_filters_sample.csv`, `ListOfIngredienct_INCI_2026.pdf` | Early EU references, not used anymore |

## Team folder (Drive / `Swan_Project_Data`), originals: don't modify

| Folder | Content |
|---|---|
| `Full_Project/Original_Data` | Product extracts from the audit |
| `Full_Project/CosIng_Reference` | CosIng reference + official metadata |
| `Full_Project/Linked_Data` | 699 products with CosIng, product × ingredient links, unmatched names |
| `Full_Project/Documentation` | `dataset_audit.md` (still says "concern not selected": to update), matching summary |

## Coming from the team

| File | From | Then |
|---|---|---|
| `catalogue_provisional.csv` (catalogue v1) | Lina | becomes the reference product list; my notebook and Loubna's score switch to it |
| Score (T15) | Loubna | tested on the 31 profiles |
| Streamlit app, `requirements-ui.txt` | Imane (branch `streamlit-mvp-shell`) | uses the values in `questionnaire.md` |
