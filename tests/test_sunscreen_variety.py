from unittest.mock import patch
from swan_ui.split_panel.routine_model import load_products,rank_by_role


def test_equal_matches_vary_without_immediately_repeating():
    products=load_products()
    with patch('swan_ui.split_panel.routine_model.secrets.choice',side_effect=lambda choices:choices[0]):
        first=rank_by_role(products,'sensitivity_irritation',skin_type='normal',reactivity='yes')['sunscreen'].iloc[0]
        second=rank_by_role(products,'sensitivity_irritation',skin_type='normal',reactivity='yes',previous_sunscreen=first['code'])['sunscreen'].iloc[0]
    assert first['code'] != second['code']
    for field in ['score','gentleness_priority','texture_priority','availability_priority']:
        assert first[field] == second[field]
    assert first.fragrance_free_verified and second.fragrance_free_verified


def test_single_best_match_is_not_replaced_by_weaker_product():
    products=load_products()
    first=rank_by_role(products,'sensitivity_irritation',skin_type='dry',reactivity='yes')['sunscreen'].iloc[0]
    again=rank_by_role(products,'sensitivity_irritation',skin_type='dry',reactivity='yes',previous_sunscreen=first['code'])['sunscreen'].iloc[0]
    assert first['code']==again['code']
