# Final Catalogue Report & FUP

The catalogue is built by notebooks/loredana_catalogue_v2.ipynb

## Where we are

Cleansers (189): done. Rules C01 to C10, 25 products checked by hand.
Sunscreens (61): done. Rules S01 to S06, 10 checked by hand, 2 moved to the moisturizers.
Moisturizers (246): done. 183 agreed by Lina and me, 63 checked by hand.
Cleaning and signals: done. catalogue_v2.csv has 494 products and 88 columns, ingredient_matrix_v2.csv 494 products and 363 ingredients.
Still to do: 4 fixes found in the review (below), price level by brand, data tests with pytest.

## Questions

Final decisions: cleansers 115 kept / 73 excluded / 1 to verify, moisturizers 176 / 64 / 6, sunscreens 50 / 9 / 0.
"All countries" includes 123 products outside the EU. They are cleaned but the app never shows them.

In France, for sensitive skin (is_gentle): 15 cleansers, 7 moisturizers, 1 sunscreen. Sunscreens are the weak point. With the EU we have 19 sunscreens, 5 of them gentle.

Other figures: 91.2 % of ingredient names found in CosIng, 32 incomplete ingredient lists, 17 products with Lilial (banned in the EU since 2022), 8 duplicates removed.

## Columns for the model and the app:

is_recommendable: always filter on it first. It already removes duplicates, Lilial and incomplete lists.
role: cleanser, moisturizer or sunscreen.
france, eu: where the product was scanned (not proof it is sold there). eu includes France.
Avoid fragrance: has_parfum == False (and has_fragrance_allergen if we decide so). Avoid essential oils: has_essential_oil == False. Avoid animal ingredients: is_vegan == True. Pregnancy: is_pregnancy_ok == True.
Acne: has_acne_active, has_salicylic_acid, has_betaine_salicylate, is_light.
Dry skin: has_dry_skin_active, has_ceramides, has_petrolatum, has_panthenol, is_rich.
Sensitive skin: is_gentle first. sensitive_claim is only what the pack says.
Sunscreens: has_uv_filter, has_oxybenzone. There is no column for mineral filters yet.
Cleansers: rinse_mode, rinse-off (gel, foam) or leave-on (micellar water, milk). It comes from the name, so check it before showing it. In France only 11 recommendable cleansers are rinse-off.
Why a product is not gentle: has_retinoid, has_strong_acid, has_alcohol_denat, has_parfum, has_essential_oil.
To show: product_name, brands, inci_text.

Limits: texture (is_rich, is_light) was made for moisturizers. We don't know ingredient amounts, so 2 % salicylic acid and a peeling look the same. has_glycerin is too common to rank. is_gentle, is_vegan and is_pregnancy_ok are read from the ingredient list only, they are not a medical or label claim.

## Problems found in the review of 11/11
A toilet cleaner (EcoClean nordic "WC Reiniger") was kept as a cleanser, because "reinig" is a cleanser word. Fix: add "wc" (whole word) to NOT_COSMETIC.
Florucci "Makeup removers cleaning cloths" was kept. Fix: add "cloth" to WIPES.
10 recommendable products have an ingredient field that is not a real INCI list (less than 50 % of names found in CosIng), for example Novexpert La Crème au Caramel, Bottega Verde Bakuchiol, Cancer Council sunscreen. La Roche-Posay Nutric Intense uses "⚫" between ingredients. Fix: add coverage >= 0.5 to is_recommendable and "⚫" as a separator.
Two pairs look like the same product and are both recommendable: Bioderma Atoderm Cream / Creme Ultra, and the two caremare creams (same list).

## Check against Sephora

Sephora product_info.csv (Kaggle, US products, 2023) is only used to check our rules.

Our name rules compared with Sephora's categories: cleansers 85 % precision and 62 % recall, moisturizers 82 % and 54 %, sunscreens 54 % and 99 %. Names are reliable but miss products. "SPF" in a name also catches moisturizers with SPF and BB creams, which is why we have rules S03 and S04.
Only 79 products are in both sources (45 brands, matched on brand and close name). About 1 in 5 matches is another variant, so we can't import Sephora prices or ratings.
For the matched products, Open Beauty Facts categories give the right step only 5 times out of 43, because most products have no category. That is why we don't use them.
"Fragrance Free" on Sephora agrees with our parfum rule 105 times out of 105.
"Vegan" agrees with our animal rule 186 times out of 193 (the 7 cases are in sephora_vegan_disagreements.csv).
"Good for: Acne": only 26 out of 52 have one of our acne actives. So has_acne_active should be a bonus, not a filter.

## Decisions
04/11. "aroma" counts as parfum.
04/11. A product needs at least 5 ingredients to be recommended.
10/11 (team). Full routine: cleanser, moisturizer, sunscreen, for 3 concerns: acne_prone, dryness_barrier, sensitive_irritated.
10/11. We clean the data from all countries. The app filters the country with france and eu. in_scope only means the step decision is Include.
10/11. We keep is_anti_ageing in case we add a question on anti-ageing actives.
10/11. is_vegan means no animal and no uncertain ingredient (squalane, cholesterol...) in the list.
10/11. Cleansers: rules C01 to C10. Scrubs are excluded (C05). Soaps are kept only if made for the face (C07).
10/11. Sunscreens: rules S01 to S06, at least SPF 30 (NHS, AAD). BB / CC creams and lip products are excluded.
10/11. A moisturizer with SPF stays a moisturizer, and Swan always shows a separate sunscreen. Nivea Q10 Power and Mixa anti-taches were moved from sunscreens to moisturizers.
10/11. Duplicates: we keep one record per name and brand (France first, then the longest list).
10/11. Products with Lilial are not recommendable - forbidden in Europe.
10/11. Glycerin is not a dry-skin active (it is in 88 % of moisturizers). It has its own column, has_glycerin.
10/11 (to validate with the team). Pregnancy: no referral any more. We show products without retinoids, hydroquinone or essential oils, with the message "this is only a suggestion, ask your doctor or pharmacist". The essential oils part is my own precaution, the sources only talk about retinoids and hydroquinone.
11/11. Moisturizers: The 63 other ones were decided by hand. "Not France" products are kept since we now work on all countries.
11/11. Status columns show the latest status. Lina's history stays in her own file.
11/11. Open Prices has no price for cosmetics (0 for 8 well-known products).
11/11. No pictures from brand or shop websites. Open Beauty Facts pictures are allowed with a credit (CC BY-SA).
