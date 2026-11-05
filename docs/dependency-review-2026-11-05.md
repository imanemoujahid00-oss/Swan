# Shared dependency review — 5 November 2026

I checked Lina’s GitHub `skincare_project/requirements.txt` and imports in her three committed notebooks, her later shared Nov 3 notebooks, Loredana’s requirements/notebooks, and the ranker/API/UI imports.

- MVP runtime: existing Streamlit pin plus pandas, numpy, requests, FastAPI, uvicorn, pydantic and python-dotenv, under requirements.txt.
- Tests: pytest and httpx under requirements-dev.txt.
- Notebook/data preparation: Loredana’s existing libraries remain under requirements-notebooks.txt. Lina’s rapidfuzz and openpyxl were missing; added as verified pins 3.14.5 and 3.1.5. ipykernel was already listed. Her later shared notebooks use pandas/numpy and standard-library modules, covered by this setup.
- Python standard-library imports (pathlib, re, json, hashlib, datetime, itertools, difflib and unicodedata) require no extra package installation.

Verified on Python 3.10.6: new packages import, fuzzy-match smoke check, Excel round trip and pip check. This does not claim every optional notebook has been rerun or every teammate has reproduced the environment. Teammates should report dependencies used by any newer code not yet shared.

Loredana’s evaluation notebook and tests are already on her branch. Notebooks are evidence and reproduction tools; the deployed service uses models/*.py and the three prepared CSVs. Do not block the serving container on running an evaluation notebook.
