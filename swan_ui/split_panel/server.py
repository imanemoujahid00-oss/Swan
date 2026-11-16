"""Serve the Swan Split panel and its recommendation API locally or in a container."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import sys

import pandas as pd

from .routine_model import assemble_routine, load_products, rank_by_role

CONCERNS = {
    "Acne-prone skin and blemishes": "acne_prone",
    "Dryness and skin barrier": "dryness_barrier",
    "Sensitive or easily irritated skin": "sensitivity_irritation",
}
ROLES = {"cleanser": "Cleanser", "moisturizer": "Moisturizer", "sunscreen": "Facial sunscreen"}
PRODUCTS = load_products()
BY_CODE = PRODUCTS.set_index("code")
PAGE = Path(__file__).with_name("index.html").read_bytes()


def build_routine(profile):
    focus = profile["focus"]
    skin = profile["skin"]
    reactivity = profile["reactivity"]
    if skin not in ("Oily", "Dry", "Combination", "Normal", "Not sure") or reactivity not in ("Yes", "No", "Not sure"):
        raise ValueError("Incomplete profile")
    ranked = rank_by_role(
        PRODUCTS, CONCERNS[focus], skin_type=skin.lower().replace(" ", "_"),
        reactivity=reactivity.lower().replace(" ", "_"),
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
        signals = match["applied_signals"]
        if role == "sunscreen":
            description = "Verified SPF."
            if "moisturizing_signal" in signals:
                description = "Verified SPF with moisturizing ingredients."
        elif "has_acne_active" in signals:
            description = "Swan found an ingredient associated with blemish-prone skincare."
        elif "moisturizing_signal" in signals:
            description = "Includes ingredients that help skin retain moisture."
        else:
            description = {
                "cleanser": "Washes away surface oil and impurities.",
                "moisturizer": "Adds moisture after cleansing.",
            }[role]
        if match["texture_priority"]:
            description += " Light texture." if skin == "Oily" else " Rich texture."
        brand = row.get("brands")
        card.update(name=str(row["product_name"]), brand=str(brand).strip() if pd.notna(brand) else "",
                    description=description, ingredients=[
                        label for flag, label in (("has_parfum", "fragrance"), ("has_essential_oil", "essential oils"))
                        if pd.notna(row[flag]) and bool(row[flag])
                    ])
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
