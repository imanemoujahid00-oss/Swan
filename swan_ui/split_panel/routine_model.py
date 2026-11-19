"""Local adapter using the ranking and catalogue preparation from Swan notebook 06."""
import os
import json
import secrets
from pathlib import Path
from urllib.parse import urlsplit
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]

SCORING_RULES = [
    ("acne_prone", "cleanser", None, 0, "Acne signal by role to be documented"),
    ("acne_prone", "moisturizer", "has_acne_active", 1, "MVP signal, used only if reviewed in the new catalogue"),
    ("acne_prone", "sunscreen", None, 0, "Declared SPF, no provisional acne bonus"),
    ("dryness_barrier", "cleanser", None, 0, "Gentleness criterion to review with Lina"),
    ("dryness_barrier", "moisturizer", "moisturizing_signal", 1, "Moisturizing or humectant function detected"),
    ("dryness_barrier", "sunscreen", "moisturizing_signal", 1, "Bonus after role and SPF verification"),
    ("sensitivity_irritation", "cleanser", None, 0, "Apply the requested exclusions"),
    ("sensitivity_irritation", "moisturizer", None, 0, "Apply the requested exclusions"),
    ("sensitivity_irritation", "sunscreen", None, 0, "Apply exclusions after role verification"),
]

rules = pd.DataFrame(SCORING_RULES, columns=["concern", "role", "signal", "weight", "condition"])

ROUTINE_ROLES = ("cleanser", "moisturizer", "sunscreen")
EXCLUSION_FIELDS = {"fragrance": "has_parfum", "essential_oils": "has_essential_oil"}

CLEANSER_MODES = {"rinse-off": "Rinse-off", "leave-on": "No-rinse"}


def as_flag(values):
    labels = values.astype("string").str.strip().str.lower()
    return labels.map({"true": True, "false": False}).astype("boolean")


def rank_by_role(products, concern, *, avoid=(), skin_type=None, reactivity=None, cleanser_mode=None, previous_sunscreen=None, rules=rules):
    if concern not in rules["concern"].unique():
        raise ValueError("Unknown skin concern.")
    if isinstance(avoid, str) or any(item not in EXCLUSION_FIELDS for item in avoid):
        raise ValueError("Unknown exclusion.")

    if cleanser_mode is not None and cleanser_mode not in CLEANSER_MODES:
        raise ValueError("Unknown cleanser preference.")

    candidates = products.copy()
    candidates["code"] = candidates["code"].astype("string").str.strip()
    invalid_code = candidates["code"].fillna("").eq("")
    if invalid_code.any() or candidates.duplicated(["role", "code"]).any():
        raise ValueError("The catalogue must have one code per product within each role.")

    texture_field = {"oily": "is_light", "dry": "is_rich"}.get(skin_type)
    prefers_gentle = reactivity is True or reactivity == "yes"

    results = {}
    for role in ROUTINE_ROLES:
        eligible = candidates.loc[candidates["role"].eq(role)].copy()
        eligible = eligible.loc[as_flag(eligible["role_verified"]).eq(True).fillna(False)]
        if role == "sunscreen":
            eligible = eligible.loc[as_flag(eligible["sun_protection_verified"]).eq(True).fillna(False)]
        if role == "sunscreen" and (concern == "sensitivity_irritation" or prefers_gentle):
            # Local review policy: no forced fragranced or unverified fallback.
            fragrance_free = as_flag(eligible.get("fragrance_free_verified", pd.Series(False, index=eligible.index))).fillna(False)
            eligible = eligible.loc[fragrance_free & as_flag(eligible["has_parfum"]).eq(False).fillna(False)].copy()
        for item in avoid:
            field = EXCLUSION_FIELDS[item]
            if field not in eligible:
                eligible = eligible.iloc[0:0]
            else:
                eligible = eligible.loc[as_flag(eligible[field]).eq(False).fillna(False)]

        eligible["score"] = 0
        eligible["applied_signals"] = [[] for _ in range(len(eligible))]
        matching_rules = rules.loc[rules["concern"].eq(concern) & rules["role"].eq(role)]
        for rule in matching_rules.itertuples(index=False):
            if rule.weight and rule.signal in eligible:
                earns_points = as_flag(eligible[rule.signal]).eq(True).fillna(False)
                eligible.loc[earns_points, "score"] += rule.weight
                eligible.loc[earns_points, "applied_signals"] = (
                    eligible.loc[earns_points, "applied_signals"].map(lambda signals: signals + [rule.signal])
                )

        # Profile answers break ties after the concern score and eligibility checks.
        eligible["gentleness_priority"] = False
        if prefers_gentle and "is_gentle" in eligible:
            eligible["gentleness_priority"] = as_flag(eligible["is_gentle"]).fillna(False)
        eligible["texture_priority"] = False
        if role in ("moisturizer", "sunscreen") and texture_field in eligible:
            eligible["texture_priority"] = as_flag(eligible[texture_field]).fillna(False)

        # Prefer the requested cleanser type within the verified pool.
        eligible["cleanser_mode_match"] = False
        if role == "cleanser" and cleanser_mode is not None and "rinse_mode" in eligible:
            modes = eligible["rinse_mode"].astype("string").str.strip().str.lower()
            eligible["cleanser_mode_match"] = modes.eq(cleanser_mode).fillna(False)

        eligible["availability_priority"] = 1
        if role == "sunscreen" and "online_availability_reviewed" in eligible:
            eligible["availability_priority"] = eligible["online_availability_reviewed"].map({"available": 1, "unavailable": 0}).fillna(1)
        results[role] = eligible.sort_values(
            ["cleanser_mode_match", "score", "gentleness_priority", "texture_priority", "availability_priority", "code"],
            ascending=[False, False, False, False, False, True],
        )
    # Vary only equally ranked sunscreens. Profile/quality priorities remain
    # stronger than variety; the prior suggestion never lowers the match.
    sunscreen = results["sunscreen"]
    if len(sunscreen) > 1:
        priorities = ["score", "gentleness_priority", "texture_priority", "availability_priority"]
        top = sunscreen.iloc[0]
        tied = sunscreen[priorities].eq(top[priorities]).all(axis=1)
        options = sunscreen.loc[tied, "code"].tolist()
        if len(options) > 1:
            choices = [code for code in options if code != previous_sunscreen] or options
            chosen = secrets.choice(choices)
            results["sunscreen"] = pd.concat([
                sunscreen.loc[sunscreen["code"].eq(chosen)],
                sunscreen.loc[~sunscreen["code"].eq(chosen)],
            ])
            results["sunscreen"]["variety_selected"] = results["sunscreen"]["code"].eq(chosen)
    return results

from itertools import product


def choose_products(ranked):
    options = []
    max_choices = len(ROUTINE_ROLES)
    for role in ROUTINE_ROLES:
        rows = ranked[role].head(max_choices).to_dict(orient="records")
        options.append(list(enumerate(rows, start=1)) + [(max_choices + 1, None)])

    best_key = None
    best_selection = None
    for selection in product(*options):
        codes = [row["code"] for _, row in selection if row is not None]
        if len(codes) != len(set(codes)):
            continue

        positions = tuple(position for position, _ in selection)
        rank_sum = sum(position for position, row in selection if row is not None)
        key = (-len(codes), rank_sum, positions)
        if best_key is None or key < best_key:
            best_key = key
            best_selection = selection

    return best_selection

SIGNAL_LABELS = {
    "moisturizing_signal": "moisturizing or humectant function detected",
    "has_acne_active": "acne signal recorded in catalogue v2",
}


def assemble_routine(ranked):
    selection = choose_products(ranked)
    steps = []
    for role, (position, row) in zip(ROUTINE_ROLES, selection):
        if row is None:
            reason = (
                "No eligible product for this step."
                if ranked[role].empty
                else "The available product is already used in this routine."
            )
            steps.append({"role": role, "code": None, "rank": None, "score": None, "reason": reason})
            continue

        labels = [SIGNAL_LABELS.get(signal, signal) for signal in row["applied_signals"]]
        reason = ", ".join(labels) if labels else "Eligible product with no score bonus for this profile."
        candidates = ranked[role]
        if row["cleanser_mode_match"]:
            reason += " I prioritized the requested cleanser type."
            candidates = candidates.loc[candidates["cleanser_mode_match"]]
        tied = candidates.loc[candidates["score"].eq(row["score"])]
        if position == 1 and len(tied) > 1:
            if row.get("gentleness_priority", False) and not tied["gentleness_priority"].all():
                reason += " I prioritized the catalogue gentleness flag for this reactive profile."
                tied = tied.loc[tied["gentleness_priority"]]
            if row.get("texture_priority", False) and not tied["texture_priority"].all():
                reason += " I prioritized the texture flag matching this skin type."
                tied = tied.loc[tied["texture_priority"]]
            if len(tied) > 1 and "availability_priority" in tied:
                if row["availability_priority"] > tied["availability_priority"].min():
                    reason += " I deprioritized an option reported unavailable online at review."
                    tied = tied.loc[tied["availability_priority"].eq(row["availability_priority"])]
            if len(tied) > 1:
                if row.get("variety_selected", False):
                    reason += " Selected among equally ranked sunscreens, avoiding the previous suggestion when possible."
                else:
                    reason += f" Product code broke the tie among {len(tied)} remaining candidates."
        if position > 1:
            reason += f" Ranked {position} for this step and selected to avoid a duplicate product."
        steps.append({
            "role": role,
            "code": row["code"],
            "rank": position,
            "score": int(row["score"]),
            "reason": reason,
        })

    filled = sum(step["code"] is not None for step in steps)
    status = {0: "no_result", len(ROUTINE_ROLES): "ok"}.get(filled, "partial")
    return {"status": status, "steps": steps}

import re
import unicodedata

ALIASES = {
    "WATER": "AQUA",
    "EAU": "AQUA",
    "AQUA/WATER/EAU": "AQUA",
    "AQUA/WATER": "AQUA",
    "WATER/AQUA": "AQUA",
    "WATER (AQUA)": "AQUA",
    "AQUA (WATER)": "AQUA",
    "AQUA (WATER/EAU)": "AQUA",
    "WATER/AQUA/EAU": "AQUA",
    "AQUA (WATER, EAU)": "AQUA",
    "FRAGRANCE": "PARFUM",
    "FRAGRANCE (PARFUM)": "PARFUM",
    "PARFUM (FRAGRANCE)": "PARFUM",
}
FRAGRANCE_MARKERS = {"PARFUM", "PERFUME", "AROMA"}
SEPARATORS = re.compile(r"(?<!\d),|,(?!\d)|[;\n•]")


def inci_key(name):
    normalized = unicodedata.normalize("NFKC", name)
    return " ".join(normalized.upper().strip().strip("•·").split())


def ingredient_keys(text):
    if pd.isna(text):
        return []
    text = re.sub(r"^\s*(?:ingredients|ingrédients|inci)\s*:\s*", "", text, flags=re.I)
    parts = []
    depth = 0
    start = 0
    for index, char in enumerate(text):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and SEPARATORS.match(text, index):
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])

    keys = [inci_key(part) for part in parts]
    return [ALIASES.get(key, key) for key in keys if key]


def load_products():
    data_dir = Path(os.environ.get("SWAN_DATA_DIR", REPO_ROOT / "raw_data"))
    catalogue = pd.read_csv(data_dir / "catalogue_v2.csv", dtype="string")
    matrix = pd.read_csv(data_dir / "ingredient_matrix_v2.csv", dtype="string")

    required_fields = {
        "code", "role", "product_name", "france", "eu", "is_recommendable",
        "catalogue_review_complete", "has_parfum", "has_essential_oil",
        "ingredients_text", "inci_text", "has_acne_active", "is_gentle",
    }
    missing_fields = required_fields - set(catalogue.columns)
    if missing_fields or "code" not in matrix:
        raise ValueError(f"Check the input columns. Missing catalogue columns: {sorted(missing_fields)}.")

    for name, table in (("catalogue", catalogue), ("ingredient matrix", matrix)):
        codes = table["code"].str.strip()
        if codes.fillna("").eq("").any() or codes.duplicated().any():
            raise ValueError(f"Missing or duplicate product codes in {name}.")
        table["code"] = codes

    if set(catalogue["code"]) != set(matrix["code"]):
        raise ValueError("Both files must cover the same product codes.")

    # EcoClean WC REINIGER is a household toilet cleaner misclassified in v2.
    catalogue = catalogue.loc[~catalogue["code"].eq("5708048047029")].copy()

    matrix_by_code = matrix.set_index("code").reindex(catalogue["code"])

    # I record the declared SPF and keep each source link for review.
    spf_review = pd.DataFrame([
        ("3468080009332", "50", "https://www.corinedefarme.fr/p/creme-protectrice-visage-et-corps-spf50/", "https://www.ezam.cz/pece-o-plet-a-pokozku/75210-opalovaci-krem-na-telo-a-oblicej-corine-de-farme-spf-50-50-ml-3468080009332.html", False),
        ("4743318143293", "30", "https://organicshop.co.uk/products/organic-shop-sunscreen-day-face-cream-30-spf-oily-skin-50ml", "https://www.pandashop.md/ru/product/sunscreen-day-face-cream-peach-spf30-50ml-00804499/", False),
        ("4005900458773", "50", "https://www.nivea.fr/produits/cr%C3%A8me-uv-visage-anti-%C3%A2ge-q10-spf-50-40060002197210040.html", "https://www.farmaline.be/fr/beaute/BE09802538/nivea-sun-uv-gezicht-anti-age-spf50.htm", False),
        ("42449010", pd.NA, pd.NA, pd.NA, False),
        ("3282770202120", "50+", "https://www.vidal.fr/parapharmacie/aderma-protect-spf-50-creme-sans-parfum-195613.html", pd.NA, True),
        ("4005900328946", "50+", "https://swiss-tablets.com/202394-nivea-sun-alpin-sun-cream-face-spf-50-50-ml/", pd.NA, False),
        ("3506770501008", "50", "https://www.bol.com/nl/nl/p/lovea-bio-anti-ageing-spf-50-50-ml-zonnebrand-creme/9200000005932746/", pd.NA, False),
    ], columns=["code", "declared_spf", "spf_source", "code_source", "reported_discontinued"])

    reviewed = as_flag(catalogue["catalogue_review_complete"]).fillna(False)
    recommended = as_flag(catalogue["is_recommendable"]).fillna(False)
    france = as_flag(catalogue["france"]).fillna(False)

    products = catalogue.copy()
    products["role_verified"] = (reviewed & recommended).loc[products.index]
    products["sun_protection_verified"] = pd.Series(pd.NA, index=products.index, dtype="boolean")
    if "sun_protection_verified" in catalogue:
        products["sun_protection_verified"] = as_flag(catalogue.loc[products.index, "sun_protection_verified"])

    solaires = products.loc[france & products["role"].eq("sunscreen") & products["role_verified"]]
    spf_audit = solaires[["code", "product_name"]].merge(
        spf_review, on="code", how="left", validate="one_to_one"
    )
    verified_codes = spf_audit.loc[spf_audit["declared_spf"].notna(), "code"]
    discontinued_codes = spf_audit.loc[spf_audit["reported_discontinued"].eq(True), "code"]

    # I give reviewed flags in a new export priority.
    missing_spf = products["sun_protection_verified"].isna()
    products.loc[missing_spf & products["code"].isin(verified_codes), "sun_protection_verified"] = True
    products = products.loc[~products["code"].isin(discontinued_codes)].copy()

    cosing = pd.read_csv(data_dir / "Swan_CosIng_reference_2026-10-26.csv", dtype="string")
    reference = cosing.assign(key=cosing["inci_name"].dropna().map(inci_key))
    unique_names = reference.loc[reference["key"].notna() & ~reference["key"].duplicated(keep=False)]
    functions_by_name = {
        row.key: {part.strip().upper() for part in row.functions.split("|") if part.strip()}
        for row in unique_names[["key", "functions"]].dropna().itertuples(index=False)
    }
    FUNCTION_GROUPS = {
        "moisturizing_signal": {"MOISTURISING", "HUMECTANT", "SKIN CONDITIONING - HUMECTANT"},
        "detected_uv_filter": {"UV FILTER"},
    }


    def detect_evidence(keys):
        found = {
            signal: sorted({key for key in keys if functions_by_name.get(key, set()) & functions})
            for signal, functions in FUNCTION_GROUPS.items()
        }
        found["detected_fragrance"] = sorted(set(keys) & FRAGRANCE_MARKERS)
        return found



    evidence = products["ingredients_text"].map(ingredient_keys).map(detect_evidence)
    products["moisturizing_signal"] = evidence.map(lambda row: bool(row["moisturizing_signal"]))
    products["has_acne_active"] = as_flag(products["has_acne_active"])
    signals = pd.DataFrame(index=catalogue.index)
    for field in EXCLUSION_FIELDS.values():
        signals[field + "_source"] = as_flag(catalogue[field])
        signals[field] = signals[field + "_source"].where(signals[field + "_source"].eq(True))

    # I also check for fragrance terms followed by punctuation or a reference.
    fragrance_pattern = r"\b(?:PARFUM|FRAGRANCE|PERFUME|AROMA)\b"
    fragrance_in_raw = catalogue["ingredients_text"].str.contains(
        fragrance_pattern, case=False, regex=True, na=False
    )
    signals.loc[fragrance_in_raw, "has_parfum"] = True
    signals["is_gentle_source"] = as_flag(catalogue["is_gentle"])
    signals["is_gentle"] = signals["is_gentle_source"].mask(signals["has_parfum"].eq(True).fillna(False), False)
    products = products.drop(columns=[*EXCLUSION_FIELDS.values(), "is_gentle"]).join(signals)

    disagreements = fragrance_in_raw & signals["has_parfum_source"].eq(False).fillna(False)

    # The shared European pool includes France-tagged products.
    market = as_flag(products["eu"]).fillna(False) | as_flag(products["france"]).fillna(False)
    products = products.loc[market].copy()
    if "fragrance_free_verified" in products:
        products["fragrance_free_verified"] = as_flag(products["fragrance_free_verified"]).fillna(False)
    else:
        products["fragrance_free_verified"] = False
    # Retain explicit reviewed claims from the extension without clearing a
    # detected contradiction in the ingredient list.
    reviewed_fragrance_free = products["fragrance_free_verified"] & ~products["has_parfum"].eq(True).fillna(False)
    products.loc[reviewed_fragrance_free, "has_parfum"] = False
    products.loc[~reviewed_fragrance_free, "fragrance_free_verified"] = False
    # Local evidence overlay keeps Loredana's source CSV untouched.
    review_path = Path(__file__).with_name("sunscreen_review_local.json")
    if review_path.exists() and os.environ.get("SWAN_LOCAL_SUNSCREEN_REVIEW", "1") == "1":
        for review in json.loads(review_path.read_text()):
            matched = products["code"].eq(review["code"]) & products["role"].eq("sunscreen")
            if matched.sum() != 1:
                raise ValueError("Sunscreen review must match exactly one existing product.")
            products.loc[matched, "sun_protection_verified"] = True
            products.loc[matched, "declared_spf_reviewed"] = review["declared_spf"]
            products.loc[matched, "fragrance_free_verified"] = review["fragrance_free_verified"]
            products.loc[matched, "has_parfum"] = False
            products.loc[matched, "is_light"] = str(review["is_light"])
            products.loc[matched, "product_name"] = review["display_name"]
            products.loc[matched, "description"] = review["description"]
            products.loc[matched, "sunscreen_review_source"] = review["source_url"]
            products.loc[matched, "sunscreen_review_note"] = review["note"]
            products.loc[matched, "online_availability_reviewed"] = review["online_availability_reviewed"]
    return products


def https_url(value):
    if pd.isna(value):
        return None
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if parsed.scheme == "https" and parsed.hostname and parsed.username is None:
        return value
    return None


def shopping_links(product):
    url = https_url(product.get("shopping_url"))
    return [{"url": url, "label": "Search on Google Shopping"}] if url else []


def product_photo(product):
    url = https_url(product.get("image_url"))
    if not url:
        return None
    return {
        "url": url,
        "credit_url": https_url(product.get("product_url")),
        "credit": str(product.get("image_credit", "Photo: Open Beauty Facts contributors, CC BY-SA")),
    }
