"""Load and validate the agreed MVP artifacts without changing their source bytes."""
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os
import re
import pandas as pd

FILES = ("baseline_ranking_data.csv", "baseline_moisturising_ingredients.csv", "baseline_scoring_table.csv")
FRAGRANCE_ALIASES = {"aroma", "parfum", "perfume", "fragrance"}


def has_fragrance_alias(value):
    return bool(FRAGRANCE_ALIASES.intersection(
        token.strip().casefold() for token in re.split(r"[|,;]", str(value))
    ))


@dataclass
class BaselineData:
    ranking_data: pd.DataFrame
    ingredients: list[str]
    weights: dict[str, float]


def load_baseline(folder):
    folder = Path(folder)
    data = pd.read_csv(folder / FILES[0], dtype={"code": str})
    ingredients = pd.read_csv(folder / FILES[1])["ingredient"].tolist()
    scoring = pd.read_csv(folder / FILES[2])
    required = {"code", "product_name", "moisturising_flag", "has_acne_active",
                "has_parfum", "has_essential_oil", "inci_text", *ingredients}
    if not required.issubset(data.columns):
        raise ValueError("Incomplete ranking data schema")
    if data["code"].isna().any() or not data["code"].is_unique:
        raise ValueError("Product codes must be present and unique")
    if data["product_name"].isna().any():
        raise ValueError("Product names must be present")
    for column in ["moisturising_flag", "has_acne_active", "has_parfum", "has_essential_oil"]:
        known = data[column].dropna()
        if not known.isin([True, False]).all():
            raise ValueError("Invalid boolean indicator: " + column)
    for ingredient in ingredients:
        if not data[ingredient].isin([0, 1]).all():
            raise ValueError("Invalid ingredient presence")
    if scoring["criterion"].duplicated().any():
        raise ValueError("Duplicate scoring criterion")
    weights = scoring.set_index("criterion")["weight"].to_dict()
    if set(weights) != {"moisturising", "acne_active"} or not all(
        isinstance(v, (int, float)) and pd.notna(v) and abs(v) != float("inf")
        for v in weights.values()
    ):
        raise ValueError("Invalid scoring table")
    # Loredana's 4 Nov finding: aroma is a fragrance alias. Preserve source CSVs.
    data.loc[data["inci_text"].map(has_fragrance_alias), "has_parfum"] = True
    return BaselineData(data, ingredients, weights)


@lru_cache(maxsize=1)
def default_baseline():
    folder = os.environ.get("SWAN_DATA_DIR", str(Path(__file__).resolve().parents[1] / "raw_data"))
    return load_baseline(folder)
