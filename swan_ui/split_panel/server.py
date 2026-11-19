"""Serve the Swan Split panel and its recommendation API locally or in a container."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import sys

import pandas as pd

from .routine_model import CLEANSER_MODES, assemble_routine, load_products, product_photo, shopping_links, rank_by_role

CONCERNS = {
    "Acne-prone skin and blemishes": "acne_prone",
    "Dryness and skin barrier": "dryness_barrier",
    "Sensitive or easily irritated skin": "sensitivity_irritation",
}
ROLES = {"cleanser": "Cleanser", "moisturizer": "Moisturizer", "sunscreen": "Facial sunscreen"}
CLEANSER_PREFERENCES = {label: mode for mode, label in CLEANSER_MODES.items()}
CLEANSER_PREFERENCES["No preference"] = None
PRODUCTS = load_products()
BY_CODE = PRODUCTS.set_index("code")
PAGE = Path(__file__).with_name("index.html").read_bytes()


def build_routine(profile):
    focus = profile["focus"]
    skin = profile["skin"]
    reactivity = profile["reactivity"]
    if skin not in ("Oily", "Dry", "Combination", "Normal", "Not sure") or reactivity not in ("Yes", "No", "Not sure"):
        raise ValueError("Incomplete profile")
    cleanser_mode = CLEANSER_PREFERENCES[profile.get("cleanser", "No preference")]
    ranked = rank_by_role(
        PRODUCTS, CONCERNS[focus], skin_type=skin.lower().replace(" ", "_"),
        reactivity=reactivity.lower().replace(" ", "_"), cleanser_mode=cleanser_mode,
    )
    routine = assemble_routine(ranked)
    cards = []
    for step in routine["steps"]:
        role, code = step["role"], step["code"]
        card = {"role": ROLES[role]}
        cards.append(card)
        if code is None:
            continue
        row = BY_CODE.loc[code]
        match = ranked[role].loc[lambda table: table["code"].eq(code)].iloc[0]
        source_description = row.get("description")
        description = str(source_description).strip() if pd.notna(source_description) else ""
        if role == "cleanser":
            rinse_mode = str(row.get("rinse_mode", "")).strip().lower()
            if rinse_mode in CLEANSER_MODES:
                card["cleanser_type"] = CLEANSER_MODES[rinse_mode]
            if cleanser_mode is not None:
                card["matches_preference"] = bool(match["cleanser_mode_match"])
        brand = row.get("brand_display")
        if pd.isna(brand):
            brand = row.get("brands")
        badge_text = row.get("badges")
        badges = [badge.strip() for badge in str(badge_text).split("·") if badge.strip()] if pd.notna(badge_text) else []
        if pd.notna(row["has_parfum"]) and bool(row["has_parfum"]):
            badges = [badge for badge in badges if badge.lower() != "fragrance-free"]
        card.update(name=str(row["product_name"]), brand=str(brand).strip() if pd.notna(brand) else "",
                    description=description, ingredients=[
                        label for flag, label in (("has_parfum", "fragrance"), ("has_essential_oil", "essential oils"))
                        if pd.notna(row[flag]) and bool(row[flag])
                    ])
        photo = product_photo(row)
        if photo:
            card["photo"] = photo
        card["badges"] = badges
        card["shopping_links"] = shopping_links(row)
    return {"status": routine["status"], "steps": cards}


class SwanHandler(BaseHTTPRequestHandler):
    def respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in {"/assets/skin-blemishes.png", "/assets/skin-dryness.png", "/assets/skin-sensitivity.png"}:
            asset = Path(__file__).parent / self.path.lstrip("/")
            self.respond(200, "image/png", asset.read_bytes())
            return
        if self.path != "/":
            self.send_error(404)
            return
        self.respond(200, "text/html; charset=utf-8", PAGE)

    def do_POST(self):
        if self.path != "/api/routine":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            if not 0 < length <= 4096:
                raise ValueError("Invalid request size")
            profile = json.loads(self.rfile.read(length))
            if not isinstance(profile, dict):
                raise ValueError("Invalid profile")
            body = json.dumps(build_routine(profile)).encode()
        except (ValueError, KeyError, TypeError):
            self.send_error(400, "Invalid routine profile")
            return
        self.respond(200, "application/json", body)


if __name__ == "__main__":
    host = os.environ.get("SWAN_HOST", "127.0.0.1")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8514"))
    HTTPServer((host, port), SwanHandler).serve_forever()
