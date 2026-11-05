"""Swan model API: python -m uvicorn api.main:app --host 0.0.0.0 --port 8000."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal
import hashlib
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt

from models.baseline import rank_moisturizers
from models.data import FILES, load_baseline
from models.recommendations import recommend

VERSION = "mvp-2026-11-05"


class ProfileRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_adult: StrictBool
    concern: Literal["acne_prone", "dryness_barrier", "sensitivity", "other"]
    blemish_level: StrictInt | None = None
    referral_flags: list[Literal["prescribed_treatment", "unusual_lesion", "pregnant_or_breastfeeding"]] = Field(default_factory=list)
    skin_type: Literal["oily", "combination", "normal", "dry", "not_sure"] = "not_sure"
    reactivity: StrictBool | None = None
    avoid: list[Literal["fragrance", "essential_oils"]] = Field(default_factory=list)


class ProductResult(BaseModel):
    code: str
    product_name: str
    moisturising_flag: bool | None
    has_acne_active: bool | None
    score: float
    reason: str


class RecommendationResponse(BaseModel):
    status: Literal["ok", "insufficient_results", "no_result", "incomplete_profile", "referral", "out_of_scope", "coming_soon"]
    message: str
    results: list[ProductResult]
    catalogue_version: str | None
    ranker_version: str


def create_app(data_dir=None):
    folder = Path(data_dir or os.environ.get("SWAN_DATA_DIR", Path(__file__).resolve().parents[1] / "raw_data"))

    @asynccontextmanager
    async def lifespan(app):
        app.state.baseline = None
        app.state.catalogue_version = None
        try:
            app.state.baseline = load_baseline(folder)
            digest = hashlib.sha256()
            for name in FILES:
                digest.update(name.encode())
                digest.update((folder / name).read_bytes())
            app.state.catalogue_version = digest.hexdigest()[:16] + "-fragrance-alias-v1"
        except (OSError, ValueError, KeyError):
            # Do not expose paths or request/profile contents in logs or errors.
            pass
        yield

    app = FastAPI(title="Swan MVP API", version=VERSION, lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def invalid_request(request, exc):
        # Default validation responses may echo submitted sensitive answers.
        return JSONResponse(status_code=422, content={
            "error": {"code": "invalid_profile", "message": "Please complete the questionnaire with valid answers."}
        })

    @app.get("/health")
    def health():
        return {"status": "ok", "version": VERSION}

    @app.get("/ready")
    def ready(request: Request):
        if request.app.state.baseline is None:
            return JSONResponse(status_code=503, content={"status": "unavailable"})
        return {"status": "ready", "products": len(request.app.state.baseline.ranking_data),
                "catalogue_version": request.app.state.catalogue_version}

    @app.post("/v1/recommendations", response_model=RecommendationResponse)
    def recommendations(profile: ProfileRequest, request: Request):
        answers = profile.model_dump()
        versions = {"catalogue_version": request.app.state.catalogue_version, "ranker_version": VERSION}
        if profile.is_adult and profile.concern in {"dryness_barrier", "sensitivity"}:
            return {"status": "coming_soon", "message": "This concern is not available in this version.", "results": [], **versions}
        # Scope/invalid-profile routes work even while product data is unavailable.
        from models.recommendations import check_scope, outcome_message
        scope = check_scope(answers)
        if scope != "eligible":
            return {"status": scope, "message": outcome_message(answers, scope), "results": [], **versions}
        if profile.reactivity is None:
            return {"status": "incomplete_profile", "message": "Please answer the skin reactivity question.", "results": [], **versions}
        baseline = request.app.state.baseline
        if baseline is None:
            return JSONResponse(status_code=503, content={"error": {
                "code": "model_unavailable", "message": "Recommendations are temporarily unavailable. Please try again later."}})
        try:
            result = recommend(answers, baseline.ranking_data,
                ranker=lambda selected: rank_moisturizers(selected, weights=baseline.weights, ingredients=baseline.ingredients))
            return {**result, **versions}
        except (ValueError, KeyError, TypeError):
            return JSONResponse(status_code=500, content={"error": {
                "code": "recommendation_failed", "message": "We could not complete this request. Please try again later."}})

    return app


app = create_app()
