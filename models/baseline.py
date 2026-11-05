"""Agreed +1/+1 baseline. Data loading is explicit/lazy for API readiness."""
from models.data import default_baseline


def __getattr__(name):
    if name not in {"ranking_data", "moisturising_ingredients", "weights"}:
        raise AttributeError(name)
    baseline = default_baseline()
    if name == "ranking_data":
        return baseline.ranking_data
    if name == "moisturising_ingredients":
        return baseline.ingredients
    if name == "weights":
        return baseline.weights
    raise AttributeError(name)


def calculate_score(data, weights=None):
    if weights is None:
        weights = default_baseline().weights
    return (
        data["moisturising_flag"].astype(int) * weights["moisturising"]
        + data["has_acne_active"].astype(int) * weights["acne_active"]
    )


def explain_score(row, ingredients=None):
    if ingredients is None:
        ingredients = default_baseline().ingredients
    reasons = []
    detected_ingredients = []

    for ingredient in ingredients:
        if row[ingredient] == 1:
            detected_ingredients.append(ingredient)

    if detected_ingredients:
        reasons.append(
            "MOISTURISING ingredients detected: "
            + ", ".join(detected_ingredients)
        )

    if row["has_acne_active"] == True:
        reasons.append(
            "Positive acne-related ingredient flag in the catalogue"
        )

    if not reasons:
        return "No positive indicator detected for the baseline score."

    return ". ".join(reasons)


def rank_moisturizers(eligible_data, *, weights=None, ingredients=None):
    ranked = eligible_data.copy()
    ranked["score"] = calculate_score(ranked, weights)

    ranked = ranked.sort_values(
        by=["score", "code"],
        ascending=[False, True]
    )

    results = ranked.head(3).copy()

    if results.empty:
        return {
            "status": "no_result",
            "message": "No eligible products available.",
            "results": []
        }

    results["reason"] = results.apply(lambda row: explain_score(row, ingredients), axis=1)

    if len(results) < 3:
        status = "insufficient_results"
        message = "Fewer than three eligible products available."
    else:
        status = "ok"
        message = "Three moisturizer alternatives available."

    return {
        "status": status,
        "message": message,
        "results": results[
            [
                "code",
                "product_name",
                "moisturising_flag",
                "has_acne_active",
                "score",
                "reason"
            ]
        ].to_dict(orient="records")
    }