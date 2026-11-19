# Refined local brand exploration

Local branch: brand-v2. No push or deployment.

- Equal pale lavender backgrounds for every product and concern guide card; removed positional card styling. White photo blocks, 01–03 step markers, smaller product headings, tinted badges, solid purple shopping buttons and quieter photo credits.
- Deeper red actions, purple welcome title and labels, softer blue surrounding layout, restrained borders and shadows.
- New candid editorial portrait generated with the built-in image generation tool. Original PNG retained; JPEG encoded for browser compatibility without changing server routes. See PORTRAIT.md for the prompt.
- App behavior, visible copy, API, model, catalogue, product photos and skin guide images unchanged. Only the welcome portrait accessibility description updated to describe the new image.
- 85 browser checks passed at 1440px and 390px, including all three concerns, referral routes, equal card backgrounds, contrast, fonts and overflow. Twelve screenshots saved in screenshots/.
- Available pytest suite: 17 passed, 29 subtests passed. Full-suite collection remains blocked by pre-existing missing fastapi, streamlit and raw_data/baseline_ranking_data.csv; see ../pytest-full.txt.

Palette values: see palette.json. Previous colour replacement inventory remains in ../COLOUR_REPLACEMENTS.md.
