"""Test profiles on the recommendation model"""
import sys
from pathlib import Path

import pytest

swan_folder = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(swan_folder))

from models.baseline import ranking_data            # the products the model can recommend
from models.recommendations import recommend        # the model: recommend(profile, products)


# ========== Answers of the questionnaire (same values as questionnaire.md) ==========

SKIN_TYPES = ["oily", "combination", "normal", "dry", "not_sure"]
AVOID_ANSWERS = [[], ["fragrance"], ["essential_oils"], ["fragrance", "essential_oils"]]
Q4_ANSWERS = [[], ["prescribed_treatment"], ["unusual_lesion"], ["pregnant_or_breastfeeding"],
              ["prescribed_treatment", "unusual_lesion"], ["prescribed_treatment", "pregnant_or_breastfeeding"],
              ["unusual_lesion", "pregnant_or_breastfeeding"],
              ["prescribed_treatment", "unusual_lesion", "pregnant_or_breastfeeding"]]

# a normal profile that gets products
BASE = {"is_adult": True, "concern": "acne_prone", "blemish_level": 2, "referral_flags": [],
        "skin_type": "oily", "reactivity": False, "avoid": []}


# ========== Small helpers ==========

def change(field, value):
    """A copy of BASE with one answer changed (same as in my notebook)."""
    profile = BASE.copy()
    profile[field] = value
    return profile


def eligible_profile(skin_type, reactivity, avoid):
    """A copy of BASE with the 3 answers that change the products (Q5, Q6, Q7)."""
    profile = BASE.copy()
    profile["skin_type"] = skin_type
    profile["reactivity"] = reactivity
    profile["avoid"] = avoid
    return profile


def expected_status(profile):
    """What the model should answer, written again from questionnaire.md (not from the code)."""
    if profile["is_adult"] == False:
        return "referral"                 # Q1: under 18
    if profile["concern"] == "other":
        return "out_of_scope"             # Q2: not acne-prone skin
    if profile["blemish_level"] >= 4:
        return "referral"                 # Q3: level 4 or 5
    if len(profile["referral_flags"]) > 0:
        return "referral"                 # Q4: at least one special case
    return "ok"                           # 3 products


def every_profile():
    """Every combination of the questionnaire: 2 x 2 x 5 x 8 x 5 x 2 x 4 = 6,400 profiles."""
    profiles = []
    for is_adult in [True, False]:
        for concern in ["acne_prone", "other"]:
            for blemish_level in [1, 2, 3, 4, 5]:
                for referral_flags in Q4_ANSWERS:
                    for skin_type in SKIN_TYPES:
                        for reactivity in [True, False]:
                            for avoid in AVOID_ANSWERS:
                                profiles.append({"is_adult": is_adult, "concern": concern,
                                                 "blemish_level": blemish_level, "referral_flags": referral_flags,
                                                 "skin_type": skin_type, "reactivity": reactivity, "avoid": avoid})
    return profiles


def top3(profile):
    """The 3 recommended products, as rows of ranking_data (to read their signals)."""
    result = recommend(profile, ranking_data)
    products = []
    for recommended in result["results"]:
        row = ranking_data[ranking_data["code"] == recommended["code"]].iloc[0]
        products.append(row)
    return products


# ========== R1: the right outcome ==========

def test_every_combination_gets_the_right_status():
    wrong = []
    for profile in every_profile():
        if recommend(profile, ranking_data)["status"] != expected_status(profile):
            wrong.append(profile)
    assert len(wrong) == 0, str(len(wrong)) + " profiles with a wrong status"


def test_referral_and_out_of_scope_give_no_product_and_a_message():
    profiles = [change("is_adult", False), change("concern", "other"), change("blemish_level", 4),
                change("blemish_level", 5), change("referral_flags", ["pregnant_or_breastfeeding"])]
    for profile in profiles:
        result = recommend(profile, ranking_data)
        assert result["results"] == []          # no product
        assert result["message"] != ""          # but a message for the person


def test_eligible_profiles_get_3_products():
    for skin_type in SKIN_TYPES:
        for avoid in AVOID_ANSWERS:
            result = recommend(eligible_profile(skin_type, False, avoid), ranking_data)
            assert result["status"] == "ok"
            assert len(result["results"]) == 3


# ========== R2: avoid answers are respected ==========

def test_avoid_fragrance_gives_no_parfum():
    for skin_type in SKIN_TYPES:
        for reactivity in [True, False]:
            for product in top3(eligible_profile(skin_type, reactivity, ["fragrance"])):
                assert product["has_parfum"] == False, product["product_name"]


def test_avoid_essential_oils_gives_no_essential_oil():
    for skin_type in SKIN_TYPES:
        for product in top3(eligible_profile(skin_type, False, ["essential_oils"])):
            assert product["has_essential_oil"] == False, product["product_name"]


# ========== R3: no duplicate, only products we can recommend ==========

def test_no_product_twice_in_a_top_3():
    for skin_type in SKIN_TYPES:
        for avoid in AVOID_ANSWERS:
            names = []
            for product in top3(eligible_profile(skin_type, False, avoid)):
                names.append(product["product_name"])
            assert len(set(names)) == 3, names      # set() keeps each name once: 3 = no duplicate


def test_only_french_products_with_a_complete_ingredient_list():
    # negative controls: products not sold in France or with a broken list are never shown
    for skin_type in SKIN_TYPES:
        for avoid in AVOID_ANSWERS:
            for product in top3(eligible_profile(skin_type, False, avoid)):
                assert product["france"] == True, product["product_name"]
                assert product["nb_ingredients"] >= 5, product["product_name"]


def test_aroma_is_counted_as_parfum():
    # decision 04/11: 'aroma' = fragrance. Fails until Lina's file and 04 are updated (Soin essentiel)
    for index, product in ranking_data.iterrows():
        if "aroma" in str(product["inci_text"]):
            assert product["has_parfum"] == True, product["product_name"]


# ========== Wrong or missing answers ==========

def test_q7_not_answered_is_the_same_as_nothing_to_avoid():
    no_q7 = BASE.copy()
    no_q7.pop("avoid")                          # Q7 is optional: remove the answer
    assert recommend(no_q7, ranking_data) == recommend(BASE, ranking_data)


def test_wrong_answers_give_incomplete_profile():
    wrong_answers = [
        change("is_adult", None),                                  # age empty
        change("concern", "acne"),                                 # not a value of the questionnaire
        change("blemish_level", 0),                                # outside 1 to 5
        change("blemish_level", 6),
        change("blemish_level", "2"),                              # text instead of a number
        change("referral_flags", "pregnant_or_breastfeeding"),     # text instead of a list
        change("referral_flags", ["allergy"]),                     # unknown answer
        change("skin_type", None),
        change("skin_type", "Oily"),                               # capital letter
        change("skin_type", ["dry"]),                              # list instead of text
        change("reactivity", "yes"),                               # text instead of True / False
        change("avoid", "fragrance"),                              # text instead of a list
        change("avoid", ["perfume"]),                              # unknown answer
        change("avoid", [""]),                                     # empty text in the list
    ]
    problems = []
    for profile in wrong_answers:
        # try / except: if the model crashes, we write it down instead of stopping the test
        try:
            result = recommend(profile, ranking_data)
        except Exception as error:
            problems.append(str(profile) + " -> crash: " + type(error).__name__)
            continue                            # go to the next wrong answer
        if result["status"] != "incomplete_profile" or result["results"] != []:
            problems.append(str(profile) + " -> " + result["status"])
    assert problems == [], "\n".join(problems)   # one problem per line in the pytest message


# ========== Personalisation (questionnaire decisions of 01/11) ==========
# xfail = expected to fail today: skin type and reactivity don't change the score yet until Loubna is changing it.
# When pytest shows XPASS, the model does it: remove the @pytest.mark.xfail line.

@pytest.mark.xfail(reason="skin type not in the score yet")
def test_dry_skin_and_oily_skin_get_a_different_top_3():
    dry = []
    for product in top3(change("skin_type", "dry")):
        dry.append(product["code"])
    oily = []
    for product in top3(change("skin_type", "oily")):
        oily.append(product["code"])
    assert dry != oily


@pytest.mark.xfail(reason="reactivity not in the score yet")
def test_reactive_skin_gets_fewer_parfum_products():
    parfum_reactive = 0
    for product in top3(change("reactivity", True)):
        if product["has_parfum"] == True:
            parfum_reactive = parfum_reactive + 1
    parfum_not_reactive = 0
    for product in top3(change("reactivity", False)):
        if product["has_parfum"] == True:
            parfum_not_reactive = parfum_not_reactive + 1
    assert parfum_reactive < parfum_not_reactive


# ========== Stability ==========

def test_same_result_when_the_products_are_shuffled():
    shuffled = ranking_data.sample(frac=1, random_state=42)      # same products, other order
    for skin_type in SKIN_TYPES:
        profile = change("skin_type", skin_type)
        assert recommend(profile, ranking_data) == recommend(profile, shuffled)
