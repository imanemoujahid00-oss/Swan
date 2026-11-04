from pathlib import Path

import pandas as pd


# locate the raw_data folder from this Python file.
project_folder = Path(__file__).resolve().parent.parent
data_folder = project_folder / 'raw_data'


# load the prepared baseline inputs.
ranking_data = pd.read_csv(
    data_folder / 'baseline_ranking_data.csv',
    dtype={
        'code': str,
        'moisturising_flag': bool,
        'has_acne_active': bool
    }
)

ingredient_table = pd.read_csv(
    data_folder / "baseline_moisturising_ingredients.csv"
)

moisturising_ingredients = ingredient_table["ingredient"].tolist()

scoring_table = pd.read_csv(
    data_folder / 'baseline_scoring_table.csv'
)

weights = scoring_table.set_index('criterion')['weight'].to_dict()


def calculate_score(data):
    return (
        data["moisturising_flag"].astype(int) * weights["moisturising"]
        + data["has_acne_active"].astype(int) * weights["acne_active"]
    )


def explain_score(row):
    reasons = []
    detected_ingredients = []

    for ingredient in moisturising_ingredients:
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


def rank_moisturizers(eligible_data):
    ranked = eligible_data.copy()
    ranked["score"] = calculate_score(ranked)

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

    results["reason"] = results.apply(explain_score, axis=1)

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