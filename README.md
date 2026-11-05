# Swan MVP

A Streamlit questionnaire connected to a FastAPI service and the team's agreed moisturizer baseline. Friday MVP: acne-prone skin only; dryness/barrier and sensitivity remain visible future options. Results are moisturizer alternatives, not a three-product routine.

## Shared environment — T05

Use Python 3.10.6 (the existing `.python-version`).

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python -m pip check
python scripts/download_data.py
python -m pytest -q
```

`requirements.txt` is the shared MVP runtime; it includes the existing pinned UI dependency. `requirements-dev.txt` adds the test tools. `requirements-notebooks.txt` adds Loredana's existing exploration/notebook libraries; those optional extras have not all been validated in the runtime environment. Lina’s GitHub requirements/imports were reconciled on 5 Nov: `rapidfuzz==3.14.5` and `openpyxl==3.1.5` are included in notebook extras; fuzzy matching and an Excel read/write smoke check passed. Her later shared Nov 3 notebooks only add pandas/numpy and standard-library imports, already covered. A teammate still needs to reproduce the setup. Do not commit `.venv`, `.env`, `raw_data`, caches or credentials.

## Exact runtime artifacts

[Shared runtime folder](https://drive.google.com/drive/folders/1poLgGMa7S74oOVE5eY1khSEaZl6xt4PO), inside Data and ingredient references:

- `baseline_ranking_data.csv`: 50 products, 304 columns.
- `baseline_moisturising_ingredients.csv`: 7 ingredient names.
- `baseline_scoring_table.csv`: moisturising +1, acne_active +1.

`data_manifest.json` records their Drive IDs, byte checksums, source Slack message, source commit and recovery provenance. The downloader refuses bytes that do not match. `SWAN_DATA_DIR` can point to an alternative folder; otherwise use `raw_data/` at the repository root. Raw data remains outside Git under the team's existing policy.

Loredana's finding is corrected at load time: exact INCI tokens `aroma`, `parfum`, `perfume`, `fragrance` mark fragrance presence. The original CSV bytes are preserved. Unknown avoidance flags are not treated as absence. The scoring weights and deterministic tie-breaking remain Loubna's agreed baseline.

## Run the API — T28/T30

```sh
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --no-access-log
```

- `GET /health`: process is alive.
- `GET /ready`: loaded catalogue count and content-derived version, or 503 if artifacts are missing/invalid.
- `POST /v1/recommendations`: real ranker results, scope outcome, or controlled error. No mock-product fallback.
- `/docs` and `docs/openapi.json`: implemented request/response contract. This supersedes the earlier draft for this integration branch; team review remains required.

The seven fields are `is_adult`, `concern`, `blemish_level`, `referral_flags`, `skin_type`, `reactivity`, `avoid`. API booleans and blemish integers are strict: the string `"2"` is invalid, whereas integer `2` is eligible. The UI sends numeric levels. Blemish levels 4–5 follow the existing model referral route. The UI keeps its existing under-18 outside-scope screen, while the model API uses `referral`; both show no products. Future concern routes return `coming_soon` in the API. Missing blemish level or unknown reactivity in the eligible acne path requires completion.

Statuses: `ok`, `insufficient_results`, `no_result`, `incomplete_profile`, `referral`, `out_of_scope`, `coming_soon`. Request-schema errors return 422 with a generic error, without echoing answers; unavailable model data returns 503. Response IDs remain strings; versions identify the runtime artifacts and ranker.

## Run the interface — T31

```sh
SWAN_API_URL=http://127.0.0.1:8000 python -m streamlit run app.py --browser.gatherUsageStats false
```

Set `SWAN_API_URL` to the deployed API for the hosted UI. The results path always calls the API. It renders real names, codes, reasons, insufficient/no-result responses and a retryable unavailable state. Editing answers invalidates cached results. Reset clears profile and results from the app session.

## Tests — T32

`tests/test_loredana_profiles.py` is copied from Loredana's updated branch (`e8520a0`) so her executable tests can run directly with the runtime files. It covers 6,400 answer combinations, exclusions, duplicates, invalid answers, aroma and stability. It does not require the separate 31-profile CSV. The two personalisation tests remain expected failures because skin type/reactivity do not yet alter ranking; these are documented post-MVP limits. Other tests exercise the API, absent data, strict input types, the UI flow and client failures. UI fixture tests are separate from the actual local API/browser check.

The active workflow in `.github/workflows/checks.yml` downloads pinned artifacts and runs installation checks/tests on Python 3.10. A readable copy is in `docs/ci-checks.yml`. Check the GitHub run result before merge; local test success alone is not a hosted release.

## Deployment

`Dockerfile` runs the API on `$PORT` (default 8080), downloads and verifies the three artifacts at build time, and disables request access logs. `Dockerfile.ui` runs Streamlit and reads `SWAN_API_URL`. See `docs/deployment.md` for the commands. The hosting project/region and release approval still need confirmation. No remote deployment has been claimed or completed by this branch.

No database or questionnaire-retention feature is implemented. Answers transit the API and remain in the Streamlit session; do not log request bodies. Confirm the hosting provider's logging/access settings before release. This MVP does not diagnose or establish clinical effectiveness or individual suitability.

## After Friday

The team agreed to work together on 7–8 November on further data cleaning, outstanding issues and additional outcomes. Preserve the working MVP first. At the start, name exact input/output files, owners, versions and links; use a separate improvement branch and data snapshot so the team does not lose track of which files are current. Detailed scope and time remain to agree.
