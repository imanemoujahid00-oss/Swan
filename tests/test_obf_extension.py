import json
from pathlib import Path
import pandas as pd
from swan_ui.split_panel.routine_model import load_products, rank_by_role
ROOT=Path(__file__).resolve().parents[1]


def test_extension_preserves_baseline_and_keeps_matrix_aligned():
    baseline=pd.read_csv(ROOT/'local_review/baseline_catalogue_v2.csv',dtype='string')
    cat=pd.read_csv(ROOT/'raw_data/catalogue_v2.csv',dtype='string')
    matrix=pd.read_csv(ROOT/'raw_data/ingredient_matrix_v2.csv',dtype='string')
    assert cat.code.is_unique and matrix.code.is_unique
    assert set(cat.code)==set(matrix.code)
    pd.testing.assert_frame_equal(cat.set_index('code').loc[baseline.code,baseline.columns.drop('code')].reset_index()[baseline.columns],baseline,check_dtype=False)


def test_new_products_have_reviewed_evidence_and_quality_signals():
    extra=pd.read_csv(ROOT/'local_review/obf_sunscreen_additions.csv',dtype='string')
    assert len(extra)==5
    assert extra.france.eq('True').all()
    assert pd.to_numeric(extra.coverage).ge(.5).all()
    assert pd.to_numeric(extra.nb_ingredients).ge(5).all()
    assert extra.has_uv_filter.eq('True').all()
    assert extra.sun_protection_verified.eq('True').all()
    assert extra.review_evidence_notes.str.startswith('https://').all()
    assert extra.description.str.len().gt(0).all()


def test_held_svr_is_not_imported_and_verified_pool_has_twelve():
    products=load_products()
    assert '3662361003204' not in set(products.code)
    assert len(rank_by_role(products,'acne_prone')['sunscreen'])==12
