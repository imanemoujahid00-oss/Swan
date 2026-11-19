import pandas as pd
from swan_ui.split_panel.routine_model import load_products, rank_by_role


def test_spf_gate_still_blocks_unverified_products():
    products = load_products()
    products.loc[products.role.eq('sunscreen'), 'sun_protection_verified'] = pd.NA
    assert rank_by_role(products, 'acne_prone')['sunscreen'].empty


def test_sensitive_and_reactive_profiles_require_verified_fragrance_free_claim():
    products = load_products()
    for concern, reactivity in [('sensitivity_irritation', 'no'), ('acne_prone', 'yes'), ('dryness_barrier', 'yes')]:
        sunscreen = rank_by_role(products, concern, reactivity=reactivity)['sunscreen']
        assert len(sunscreen) >= 2
        assert sunscreen['fragrance_free_verified'].all()
        assert sunscreen['has_parfum'].eq(False).all()


def test_missing_or_contradictory_evidence_does_not_pass_sensitivity_filter():
    products = load_products()
    products.loc[products.role.eq('sunscreen'), 'fragrance_free_verified'] = False
    assert rank_by_role(products, 'sensitivity_irritation')['sunscreen'].empty
    products.loc[products.role.eq('sunscreen'), 'fragrance_free_verified'] = True
    products.loc[products.role.eq('sunscreen'), 'has_parfum'] = True
    assert rank_by_role(products, 'sensitivity_irritation')['sunscreen'].empty


def test_oily_skin_texture_and_availability_break_real_ties():
    products = load_products()
    sunscreen = rank_by_role(products, 'acne_prone', skin_type='oily')['sunscreen']
    assert sunscreen.iloc[0].texture_priority
    sensitive = rank_by_role(products, 'sensitivity_irritation')['sunscreen']
    assert sensitive.iloc[0]['code'] != '4067796256239'
    assert sensitive.iloc[0]['fragrance_free_verified']
