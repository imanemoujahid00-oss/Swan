# Swan — MVP demonstration brief

For Ben and teaching assistants · 6 November 2026

[Open the live Swan MVP](https://swan-mvp-ui-1083386136867.europe-west9.run.app)

## Purpose and approach

Swan helps users explore moisturizer alternatives for acne-prone skin through a short questionnaire. The deployed MVP connects a Streamlit interface to a FastAPI service and a transparent rule-based ranker using a reviewed 50-product pool.

Scope and ingredient-avoidance filters run before ranking. Products receive +1 for a moisturising indicator and +1 for a catalogue acne-related indicator; equal scores use deterministic product-code ordering. The interface returns up to three alternatives with ingredient-based explanations.

## What the demonstration shows

An eligible adult acne-prone profile with blemish level 2 returns real product names, identifiers and reasons. A scope/referral example returns no products. Fragrance avoidance changes eligibility, while dryness and sensitivity remain future options.

Technical verification: 44 local tests and 29 subtests passed, plus 51 hosted HTTP checks including 31 synthetic routing profiles. The real browser journey, editing and reset were also verified. Final independent team acceptance is still in progress.

## Limits and next steps

This is a rule-based baseline, not a trained predictive model. Skin type and reactivity do not yet personalise ranking. Ingredient concentrations are unavailable, and binary indicators do not establish clinical effectiveness or individual suitability. Results are moisturizer alternatives, not a complete routine.

Next: complete independent functional acceptance, then improve data quality and relevance evaluation before expanding outcomes. The services are hosted in Paris; the first load after inactivity may take longer.

