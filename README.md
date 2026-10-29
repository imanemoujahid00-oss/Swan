# Swan

A skincare discovery project. The initial prototype explores one concern and
moisturizer recommendations through a basic Streamlit interface.

## Run the UI prototype

From the repository root, using Python 3.10.6 and the project's `Swan` environment:

```bash
python -m pip install -r requirements-ui.txt
python -m streamlit run app.py
```

The UI-only requirements are separate so this work does not replace Loredana's
shared dependency proposal for T05. Exact direct versions are pinned; transitive
dependencies are resolved by pip. Reconcile the files when the team agrees on the
shared environment.

## What is implemented

- Welcome screen, draft questionnaire, fictional moisturizer results and scope messages.
- Editable answers and a start-over action that clears questionnaire session state.
- A draft `Profile` contract and a mock-results adapter for future integration.
- No raw dataset, credentials or real user records are needed to run the app.

All products are visibly labelled fictional fixtures. Their order and contents
do not depend on questionnaire answers. There is no real ranking, ingredient
filtering, recommendation, concentration estimate or claim of suitability.
Answers are kept in the current app session; application code does not write
them to disk or send them to an API. Start over clears them.

## Questionnaire and decisions to review together

The draft follows the questionnaire in Loredana's
`notebooks/loredana_data_check_questionnaire.ipynb` on branch `loredana`
(commit `5e4a386`). It includes adult scope, acne-prone concern, self-described
blemishes, scope flags, skin type, reactivity and ingredient preferences. Texture
is excluded. The existing notebook is not modified or merged by this branch.

The interface shows three concerns: acne-prone skin, dryness / skin barrier,
and sensitivity / irritation. Only acne-prone skin reaches the fictional
moisturizer results. The other two retain distinct profile values and show a
not-available-yet screen with no product results. They are future scope, not
additional supported recommendation paths. The blemish answer is only retained
for the acne-prone profile.

This three-choice presentation extends Loredana's original acne-prone / other
question without expanding the MVP ranking scope. The acne-prone wording and
scope messages are placeholders for team confirmation.
The 1–5 blemish answer is descriptive only: no clinical severity threshold is
invented. Skin type, reactivity and avoid preferences do not personalize the
fixtures. The scope flags reproduce a proposed prototype boundary, not clinical
triage or a validated medical decision rule. Review the final questions, option
labels, referral wording and relevance rubric before integrating real products.

## Handoff to the team

`swan_ui/profile.py` owns the draft input schema. `app.py` translates visible
labels to stable values. `swan_ui/mock.py:get_mock_results(profile)` is the
integration boundary: replace it with an adapter to the reviewed moisturizer
catalogue and agreed ranker once T07/T09/T10/T15/T16 are ready. Do not enable real
results by silently relabelling the fixtures.

Keep the raw ingredient list alongside normalized ingredient identities and
unresolved matches. Proposed alias mapping belongs in a shared normalization
table; evidence and suitability weights belong in a separate reviewed table.
The source data does not provide ingredient concentrations.

This branch starts T27 (interface flow), T29 (mock Streamlit shell) and a draft of
T12 (questionnaire contract). It does not complete catalogue cleaning, real ranking,
deployment or team approval. Work on the other branches remains independent.

## Check the prototype

```bash
python -m pip install -r requirements-ui-dev.txt
python -m pytest -q
```

Tests use Streamlit's AppTest to exercise validation, scope routes, editing,
session reset and explicitly fictional results.
