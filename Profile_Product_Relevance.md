# Swan — Profile–Product Relevance Examples (catalogue_v2)

## 1. Catalogue audit and eligibility

- **494** catalogue records: **189** cleansers, **246** moisturizers, **59** sunscreens.
- `final_decision`: Include **341**, Exclude **146**, Verify **7**.
- `is_recommendable=True`: **318** records. We restrict candidate recommendations to **Include AND is_recommendable=True AND in_scope=True**, with a supported category and reviewed attributes.
- Existing `catalogue_review_complete=True` is a catalogue workflow field, **not** a medical-validation certificate. `is_gentle`, `has_acne_active`, `has_dry_skin_active`, texture and fragrance indicators are catalogue flags; verify provenance before treating them as stronger claims.
- Ingredient coverage and classification can be incomplete or contradictory, even on included products. Unknown or inconsistent information must be visible, not silently treated as negative.
- A `has_uv_filter=True` flag is **not sufficient by itself** to establish a regulatory SPF/UVA protection claim.

**Audit provenance:** Counts and attributes in this report were taken from `catalogue_v2.csv` (494 rows; SHA-256 `5c0ee454e3b6981edc86040a23020f8814df25835f498417ed1eaa597d362875`). This is an input-file fingerprint, **not** the original catalogue publication date or independent validation. Recalculate counts and annotations if the catalogue changes.

## 2. Applied labeling rules

1. Check profile eligibility and completion first; if blocked, use `NE_blocked` and do not recommend anything.
2. Check that the product is included, in scope, recommendable, and of the *correct category*; when category fields conflict, require review (`NE_insufficient_evidence`).
3. Label the profile–product match using only supported field values. Here the 0–3 labels are **reviewer proposals** based on catalogue-derived attributes, not empirical user outcomes or the production model's concern scores.
4. For sensitivity/reactivity, the gentleness flag supports a **tie-break only** in production; it cannot guarantee tolerance. A `3_high` human label is not proof a product is safe.
5. Fragrance/essential-oil flags are disclosed when supported; user avoidance questions were removed. Never infer product absence or allergy safety from unchecked fields.
6. Reviewer approval is required before calling any of these **final** labels. Verify SPF/UVA separately for sunscreen where the ranking/display requires claims.

## 3. Real profile–product example pairs

| Profile | Product (brand; catalogue code) | Step | Proposed label | Evidence-backed rationale / qualification |
|---|---|---|---|---|
| AC-01 | Cerave — CeraVe (`3606000537750`) | cleanser | `3_high` | Acne-primary cleanser; source flags acne-active=True and gentle=True. **Review required:** Catalogue product name is nonspecific. Source review notes suggest CeraVe Foaming Facial Cleanser, but confirm the exact identity/code independently before approving `3_high`. |
| SI-02 | Bioderma — Sensibioh2o (`3401396991779`) | cleanser | `2_moderate` | Sensitive-primary cleanser; source gentleness flag=True; no further validated sensitive-skin suitability criterion is provided. **Limit:** Gentleness is a catalogue-derived feature, not a tolerance guarantee. |
| DR-01 | Dewytree — Dewytree Hi Amino All Cleansing Milk (`8809517475460`) | cleanser | `2_moderate` | Dryness-primary cleanser; source dry-skin-active=True, but gentle=False and INCI coverage is 0.84. **Limit:** Essential-oil presence is flagged; disclosed, not treated as a categorical safety exclusion. |
| MC-01 | Thalia Natural Beauty — Thalia Salisilik Asit Yüz Temizleme Jeli (`8684225891937`) | cleanser | `3_high` | Acne-primary cleanser with dryness secondary; acne-active=True, dry-skin-active=True, gentle=True. **Limit:** No independent clinical suitability evaluation. |
| DR-01 | M.Asam — M.Asam Aqua Intense Supreme Hyaluron Yüz Kremi (`4049639451803`) | moisturizer | `3_high` | Dryness-primary moisturizer; dry-skin-active=True, gentle=True; the catalogue marks the texture as light. **Limit:** Rich texture is a tie-break preference for dry skin, not a minimum eligibility criterion. |
| MC-01 | Isntree — Isntree Onion Newpair Gel Cream (`8809783322635`) | moisturizer | `3_high` | Acne-primary moisturizer with dryness secondary; both concern flags=True, gentle=True and light=True. **Limit:** Assumes catalogue feature flags accurately represent formulation properties. |
| ST-02 | M.Asam — M.Asam Vinolift Sıkılaştırıcı Yüz Kremi (`4049639419728`) | moisturizer | `2_moderate` | **Acne is primary; dry is skin type only.** Catalogue acne-active=True, dry-skin-active=True, rich=True, gentle=False, parfum=True. **Review required:** Reassess primary acne relevance; rich texture is a moisturizer tie-break, not independent proof of fit. |
| AC-01 | Neutrogena — Hydro Boost (`7891010255725`) | moisturizer | `NE_insufficient_evidence` | Moisturizer classification is Needs manual review; do not assert reliable category/concern fit. **Limit:** Despite Include and is_recommendable=True, category evidence is contradictory. |
| AC-01 | Nivea — Nivea Derma Skin Clear UV Fluid 50+SPF Akne Karşıtı Yüz Güneş Kremi 40 ml (`4006000174686`) | sunscreen | `3_high` | Acne-primary sunscreen; dedicated facial sunscreen, UV-filter=True and acne-active=True. **Limit:** SPF is in product name; UVA protection needs independent verification. |
| MC-07 | Cerave — Facial Moisturizing Lotion AM Lightweight SPF 50 (`3606000612655`) | sunscreen | `3_high` | Acne-primary sunscreen with dryness and sensitivity selected; acne-active=True, dry-skin-active=True, gentle=True and UV-filter=True. **Limit:** Catalogue gentleness flag is not medical assurance; UVA protection not independently verified. |
| SI-02 | Derma — Face sun lotion 30 High spf (`5709954020564`) | sunscreen | `2_moderate` | Sensitivity-primary sunscreen; gentle=True, dedicated facial sunscreen and UV-filter=True; specific sensitive-skin suitability not independently assessed. **Limit:** UV-filter flag does not verify UVA rating or label compliance. |
| ST-02 | Neutrogena — Ultra Sheer Dry-Touch Sunscreen (`0086800078487`) | sunscreen | `2_moderate` | **Acne is primary; dry is skin type only.** Catalogue facial sunscreen; UV-filter=True, gentle=True, acne-active=False. **Review required:** Richness does not justify a sunscreen match; reassess acne-primary fit and independently verify any displayed SPF/UVA claims. |
| RF-07 | Isntree — Isntree Onion Newpair Gel Cream (`8809783322635`) | moisturizer | `NE_blocked` | Secondary acne is level 5; T13 safety gate stops ranking regardless of product. **Limit:** Not a negative product judgment. |

### Label review notes

- These labels illustrate a **draft application** of the rubric. The relative ordering among real products has **not been validated** against actual production model outputs.
- `ST-02` has **acne as its primary concern**, while dry is its skin type; dryness is not a selected concern. Evaluate product relevance primarily against acne evidence. Richness may only be used as a documented **moisturizer** tie-break, not as sunscreen ranking evidence.
- In `RF-07`, a product cannot receive a positive suitability recommendation, regardless of ingredient flags.
- `NE_insufficient_evidence` on a class-ambiguous record is deliberate: `Include` alone does not resolve inconsistent category metadata.

### Review priorities and label coverage

The sample includes **13 provisional pairs covering 12 unique products**. Current proposed-label distribution: **6 `3_high`, 5 `2_moderate`, 1 `NE_insufficient_evidence`, 1 `NE_blocked`; 0 `1_low` and 0 `0_not_relevant`**. The latter two are **coverage gaps**, not evidence to invent labels. Add representative pairs in these classes only after finding catalogue products with documented weak fit or verified mismatch and obtaining reviewer agreement.

**Priority rechecks:**

- **AC-01 / `3606000537750` (`3_high`):** Confirm the generic CeraVe product name against code, INCI and supplier evidence before approval.
- **ST-02 / `4049639419728` (`2_moderate`):** Evaluate acne-primary fit separately from rich texture and dry-skin suitability.
- **ST-02 / `0086800078487` (`2_moderate`):** Evaluate acne-primary sunscreen fit; a rich-texture flag does not establish a sunscreen ranking preference.

These labels remain unchanged **provisionally**. Per-row `manual_review_priority`, `manual_review_reason`, `unknown_fields`, and `independent_verification_status` are recorded in the updated CSV. The class-ambiguous Hydro Boost example also requires category resolution before any relevance score is assigned.

## 4. Audit trace and evidence fields

These fields are copied from the supplied `catalogue_v2.csv` snapshot, not checked against independent supplier pages. Preserve `code` as a **string** (including leading zeros). The updated annotation CSV stores the catalogue-derived evidence fields and source-file fingerprint for every pair. It does **not** establish independent product verification; the source catalogue and its provenance are still needed to audit the underlying flags.

| Product code | Role | Decision | Recommendable | Category field | Gentle | Acne flag | Dry flag | Light | Rich | Parfum | Essential oil | UV filter | INCI coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3606000537750 | cleanser | Include | True | Face cleansers | True | True | True | True | False | False | False | False | 1.0 |
| 3401396991779 | cleanser | Include | True | Face cleansers | True | False | False | True | False | False | False | False | 1.0 |
| 8809517475460 | cleanser | Include | True | Face cleansers | False | False | True | False | True | False | True | False | 0.84 |
| 8684225891937 | cleanser | Include | True | Face cleansers | True | True | True | True | False | False | False | False | 1.0 |
| 4049639451803 | moisturizer | Include | True | Facial moisturizer candidate | True | False | True | True | False | False | False | False | 1.0 |
| 8809783322635 | moisturizer | Include | True | Facial moisturizer candidate | True | True | True | True | False | False | False | False | 1.0 |
| 4049639419728 | moisturizer | Include | True | Facial moisturizer candidate | False | True | True | False | True | True | False | False | 1.0 |
| 7891010255725 | moisturizer | Include | True | Needs manual review | False | False | False | True | False | True | False | False | 0.89 |
| 4006000174686 | sunscreen | Include | True | Dedicated facial sunscreen | False | True | False | True | False | True | False | True | 1.0 |
| 3606000612655 | sunscreen | Include | True | Dedicated facial sunscreen | True | True | True | True | False | False | False | True | 0.92 |
| 5709954020564 | sunscreen | Include | True | Dedicated facial sunscreen | True | False | False | True | False | False | False | True | 1.0 |
| 0086800078487 | sunscreen | Include | True | Dedicated facial sunscreen | True | False | False | False | True | False | False | True | 0.83 |
