# Swan brand-v2 — local visual review

Base commit: 3bdb9db. Branch: brand-v2. This change is local only: no push, merge or deployment.

## Diff summary

The only changed application file is swan_ui/split_panel/index.html. It now has an inline SWAN wordmark with red dot, the requested SVG data favicon, Google Fonts for Bebas Neue and Barlow 500/600/700, the exact new palette, uppercase display headings, purple small labels and pale-blue secondary highlights. All old theme colour literals were replaced, including obsolete theme layers and gradients. The desktop split and mobile stacked layouts are retained.

Existing additional theme variables --coral and --lime are retained as aliases of --accent-red. The actual photographic welcome image, all three skin guide PNG files and all product photo URLs are unchanged. Header image styling and the embedded old logo were removed. The header wordmark is 30px, nowrap and has no overlap at 390px.

The inline JavaScript is byte-identical to the base. API, model, data, source-review JSON and image files are byte-identical to the base. Existing test files are unchanged. See source-checks.json for hashes and protected-file checks.

## Colour replacement list

[Every replaced hex value, named colours and variable assignment details](COLOUR_REPLACEMENTS.md).

## Contrast and typography decisions

White on #d9402c is 4.449:1, slightly below the 4.5:1 AA requirement for small text. Primary buttons therefore use Barlow 700 at 20px, meeting the large-text AA threshold of 3:1. Hover white/#b9331f is 5.905:1. Small secondary shopping links use purple, whose contrast against white is 11.464:1. Errors use the darker hover colour; supporting text uses --muted. Photo credits were increased from 10px to 12px for readability. These are presentation changes only.

No unreviewed functional changes or uncertain product decisions are included. Remaining limits: Google Fonts require a network connection (specified fallbacks remain), external product images remain dependent on their hosts, and the full legacy pytest suite cannot collect in this checkout for the environment/data reasons below. Different tied sunscreen choices between screenshots are expected existing model behaviour; the model was not changed.

## Browser checks

Real Chromium checks at 1440 × 1000 and 390 × 844, with full-page screenshots. Google font faces were confirmed loaded. Reduced-motion preference was used for the final captures so the screenshots show stable end states without changing the app's animation code.

Checks cover the real buttons and answers through all three concerns, the first question, the final cleanser preference, review, results, required-answer validation, under-18 referral, prescribed-treatment referral, pregnancy/breastfeeding referral, unusual skin-change referral, known-allergy referral, editing retained answers, wordmark containment, horizontal overflow and AA primary-button contrast. Browser-checks.json records the results; browser-check.cjs is the read-only UI automation runner. No browser JavaScript or failed network requests were reported in the successful run.

| Screen | Desktop 1440px | Phone 390px |
| --- | --- | --- |
| Welcome | [Screenshot](screenshots/welcome-1440.png) | [Screenshot](screenshots/welcome-390.png) |
| Your profile — first question | [Screenshot](screenshots/profile-first-1440.png) | [Screenshot](screenshots/profile-first-390.png) |
| Your profile — last question | [Screenshot](screenshots/profile-last-1440.png) | [Screenshot](screenshots/profile-last-390.png) |
| Your routine | [Screenshot](screenshots/routine-1440.png) | [Screenshot](screenshots/routine-390.png) |
| Referral | [Screenshot](screenshots/referral-1440.png) | [Screenshot](screenshots/referral-390.png) |

## Pytest results

`python3 -m pytest -q` stopped with three collection errors:

- tests/test_api.py: FastAPI is not installed in the existing Swan environment.
- tests/test_app.py: Streamlit is not installed in the existing Swan environment.
- tests/test_loredana_profiles.py: the old raw_data/baseline_ranking_data.csv file is missing from this checkout.

These are unrelated dependency/legacy-data blockers, not colour or old-logo assertions. No test file or source data was edited to hide them. Full output: [pytest-full.txt](pytest-full.txt).

Running all collectable tests with those three files explicitly ignored passed: **17 tests and 29 subtests**. Output: [pytest-available.txt](pytest-available.txt).

## Local preview

http://127.0.0.1:8080/

Launch from the repository root with SWAN_HOST=127.0.0.1 PORT=8080 python -m swan_ui.split_panel.server using the existing Swan Python environment. The server itself is unchanged.
