"""Exercise the handoff flow and ensure fixtures cannot look personalized."""

from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def questionnaire():
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    app.button(key="begin").click().run()
    assert not app.exception
    return app


def answer(app, adult="Yes", concern="Moisturizers for acne-prone skin", flags=None):
    app.radio(key="q_adult").set_value(adult)
    app.radio(key="q_concern").set_value(concern)
    app.multiselect(key="q_flags").set_value(flags or ["None of these"])
    app.button(key="FormSubmitter:profile_form-Preview the next step").click().run()
    assert not app.exception


def test_unanswered_required_questions_do_not_show_results():
    app = questionnaire()
    app.button(key="FormSubmitter:profile_form-Preview the next step").click().run()
    assert not app.exception
    assert app.error
    assert app.session_state["view"] == "questionnaire"
    assert not any("Example moisturizer" in h.value for h in app.subheader)


@pytest.mark.parametrize("adult,concern,flags,expected", [
    ("Yes", "Moisturizers for acne-prone skin", ["None of these"], "results"),
    ("No", "Moisturizers for acne-prone skin", ["None of these"], "outside_scope"),
    ("Yes", "Something else", ["None of these"], "outside_scope"),
    ("Yes", "Moisturizers for acne-prone skin", ["I use a prescribed skin treatment"], "professional_guidance"),
])
def test_scope_routes(adult, concern, flags, expected):
    app = questionnaire()
    answer(app, adult, concern, flags)
    assert app.session_state["view"] == expected
    names = [h.value for h in app.subheader if h.value.startswith("Example moisturizer")]
    if expected == "results":
        assert len(names) == 3
        assert any("not personalized" in w.value for w in app.warning)
    else:
        assert names == []


def test_none_and_scope_flags_cannot_be_selected_together():
    app = questionnaire()
    answer(app, flags=["None of these", "I use a prescribed skin treatment"])
    assert app.error
    assert app.session_state["view"] == "questionnaire"


def test_edit_preserves_answers_and_start_over_clears_them():
    app = questionnaire()
    app.selectbox(key="q_skin").set_value("Dry")
    app.multiselect(key="q_avoid").set_value(["Fragrance"])
    answer(app)
    app.button(key="edit").click().run()
    assert app.selectbox(key="q_skin").value == "Dry"
    assert app.multiselect(key="q_avoid").value == ["Fragrance"]
    app.button(key="reset").click().run()
    assert app.session_state["view"] == "welcome"
    assert "profile" not in app.session_state
    app.button(key="begin").click().run()
    assert app.radio(key="q_adult").value is None
    assert app.selectbox(key="q_skin").value == "Not sure"
    assert app.multiselect(key="q_avoid").value == []


def test_preferences_and_blemish_score_do_not_fabricate_personalized_results():
    app = questionnaire()
    answer(app)
    first = [h.value for h in app.subheader]
    app.button(key="edit").click().run()
    app.selectbox(key="q_skin").set_value("Oily")
    app.radio(key="q_reactivity").set_value("Yes")
    app.multiselect(key="q_avoid").set_value(["Fragrance", "Essential oils"])
    app.select_slider(key="q_blemish").set_value(5)
    app.button(key="FormSubmitter:profile_form-Preview the next step").click().run()
    assert not app.exception
    assert app.session_state["view"] == "results"
    assert [h.value for h in app.subheader] == first
    assert any("not personalized" in w.value for w in app.warning)
