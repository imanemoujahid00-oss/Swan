"""Run with: python -m streamlit run app.py"""

import streamlit as st

from swan_ui.client import fetch_recommendations, RecommendationUnavailable
from swan_ui.profile import Profile, preview_route


st.set_page_config(page_title="Swan · A simpler skincare starting point", page_icon="🦢", layout="wide")

SKIN_TYPES = {"Not sure": "not_sure", "Oily": "oily", "Combination": "combination", "Normal": "normal", "Dry": "dry"}
REACTIVITY = {"Not sure": "not_sure", "Yes": "yes", "No": "no"}
CONCERNS = {
    "Acne-prone skin": "acne_prone",
    "Dryness / skin barrier": "dryness_barrier",
    "Sensitivity / irritation": "sensitivity",
}
FLAGS = {
    "I use a prescribed skin treatment": "prescribed_treatment",
    "I have a new or unusual skin concern": "unusual_lesion",
    "I am pregnant or breastfeeding": "pregnant_or_breastfeeding",
}
AVOID = {"Fragrance": "fragrance", "Essential oils": "essential_oils"}
NONE = "None of these"


def navigate(view: str) -> None:
    st.session_state.view = view


def reset_demo() -> None:
    for key in list(st.session_state):
        if key.startswith("q_") or key in {"profile", "recommendation_response"}:
            del st.session_state[key]
    st.session_state.view = "welcome"


def header() -> None:
    st.markdown("""
    <style>
    .block-container {max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem;}
    h1, h2, h3 {letter-spacing: -0.035em;}
    [data-testid="stAppViewContainer"] h1 {font-family: Georgia, serif; font-weight: 400; font-size: clamp(2.5rem, 5vw, 4.3rem); line-height: 1.1;}
    .swan-wordmark {font-family: Georgia, serif; font-size: 2rem; color: #274b42; letter-spacing: .08em;}
    .swan-kicker {color: #587368; font-size: .76rem; text-transform: uppercase; letter-spacing: .15em; margin: 1rem 0;}
    .swan-lead {font-size: 1.13rem; line-height: 1.7; color: #4e6059; max-width: 43rem;}
    .swan-bottle {background: #e7ede6; border-radius: 12px; padding: 22px; margin-bottom: 16px; text-align: center; color: #456358; font-size: 2rem; font-family: Georgia, serif;}
    [data-testid="stSidebar"] {background: #eef2eb;}
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="swan-wordmark">swan</div>', unsafe_allow_html=True)
    st.caption("A simpler skincare starting point")
    st.caption("MVP · Moisturizer alternatives for acne-prone skin, with ingredient-based explanations.")
    with st.sidebar:
        st.markdown("### Your starting point")
        steps = [("welcome", "01  Welcome"), ("questionnaire", "02  Your profile"), ("results", "03  Your results")]
        view = st.session_state.get("view", "welcome")
        for key, label in steps:
            if key == view:
                st.markdown(f"**{label}**")
            else:
                st.caption(label)
        st.divider()
        st.caption("Explore three concerns. The acne-prone moisturizer path is available; dryness and sensitivity are not available yet. Skin type and reactivity do not yet change the baseline ranking.")
        st.caption("Answers are sent to the Swan API to return results. Swan does not intentionally store questionnaire answers; please avoid entering identifying information.")
        st.button("Start over", key="reset", on_click=reset_demo, use_container_width=True)


def welcome() -> None:
    st.markdown('<div class="swan-kicker">Less guesswork. A clearer starting point.</div>', unsafe_allow_html=True)
    st.title("Skincare, one step at a time.")
    st.markdown('<p class="swan-lead">Answer a short questionnaire to compare moisturizer alternatives and see which ingredient indicators contributed to their ranking.</p>', unsafe_allow_html=True)
    st.button("Get started", key="begin", type="primary", on_click=navigate, args=("questionnaire",))
    st.write("")
    columns = st.columns(3)
    for column, title, text in zip(columns, ["Tell us a little", "Compare alternatives", "Understand the limits"], [
        "A few questions about your concerns and preferences. No name or photo needed.",
        "See up to three alternatives from our reviewed MVP product pool.",
        "Understand the ingredient indicators and the limits of this first version.",
    ]):
        with column:
            with st.container(border=True):
                st.subheader(title)
                st.write(text)
    st.caption("Swan is a cosmetic product discovery project. This prototype does not diagnose conditions or provide medical advice.")


def questionnaire() -> None:
    previous = st.session_state.get("profile")
    if previous is not None:
        saved = {
            "q_adult": "Yes" if previous.is_adult else "No",
            "q_concern": next((label for label, code in CONCERNS.items() if code == previous.concern), None),
            "q_flags": [label for label, code in FLAGS.items() if code in previous.referral_flags] or [NONE],
            "q_skin": next(label for label, code in SKIN_TYPES.items() if code == previous.skin_type),
            "q_reactivity": next(label for label, code in REACTIVITY.items() if code == previous.reactivity),
            "q_blemish": previous.blemish_level if previous.blemish_level is not None else "Prefer not to say",
            "q_avoid": [label for label, code in AVOID.items() if code in previous.avoid],
        }
        for key, value in saved.items():
            st.session_state.setdefault(key, value)
    st.markdown('<div class="swan-kicker">02 / Your profile</div>', unsafe_allow_html=True)
    st.title("Let's start with you.")
    st.write("Your answers determine the available route and your selected ingredient exclusions. Skin type and reactivity are recorded but do not yet change the baseline ranking.")
    with st.form("profile_form"):
        st.subheader("A few boundaries first")
        adult = st.radio("Are you 18 or older?", ["Yes", "No"], index=None, key="q_adult", horizontal=True)
        concern = st.radio("Which concern would you like to explore?", list(CONCERNS), index=None, key="q_concern")
        st.caption("Current MVP: acne-prone skin, with moisturizer results only. Dryness and sensitivity are future options and will show a not-available-yet message.")
        flags = st.multiselect("Do any of these apply to you?", [NONE, *FLAGS], key="q_flags", help="Choose None of these if none apply. This draft scope check is not a clinical assessment.")
        st.subheader("Your preferences")
        left, right = st.columns(2)
        with left:
            skin_type = st.selectbox("How would you describe your skin?", list(SKIN_TYPES), key="q_skin")
        with right:
            reactivity = st.radio("Does your skin react easily, such as stinging or redness?", list(REACTIVITY), key="q_reactivity")
        blemish = st.select_slider("For acne-prone skin: how noticeable do your blemishes feel?", ["Prefer not to say", 1, 2, 3, 4, 5], key="q_blemish", help="Required for the acne-prone path. 1 means less noticeable and 5 more noticeable to you. Levels 4–5 are outside this MVP recommendation path; this is not a diagnosis.")
        avoid = st.multiselect("Ingredients you prefer to avoid (optional)", list(AVOID), key="q_avoid")
        st.caption("Fragrance and essential-oil exclusions filter products before ranking. Texture-based personalisation is planned for a later version.")
        submitted = st.form_submit_button("See my results", type="primary")
    if submitted:
        if adult is None or concern is None or not flags:
            st.error("Please answer the age and concern questions, and select an option for the scope check.")
            return
        if NONE in flags and len(flags) > 1:
            st.error("Choose either None of these or the options that apply, not both.")
            return
        profile = Profile(
            is_adult=adult == "Yes",
            concern=CONCERNS[concern],
            blemish_level=blemish if concern == "Acne-prone skin" and isinstance(blemish, int) else None,
            referral_flags=tuple(FLAGS[x] for x in flags if x != NONE),
            skin_type=SKIN_TYPES[skin_type],
            reactivity=REACTIVITY[reactivity],
            avoid=tuple(AVOID[x] for x in avoid),
        )
        route = preview_route(profile)
        if route == "results" and (profile.blemish_level is None or profile.reactivity == "not_sure"):
            st.error("Please choose a blemish level and answer the reactivity question for this recommendation path.")
            return
        st.session_state.pop("recommendation_response", None)
        st.session_state.profile = profile
        st.session_state.view = preview_route(profile)
        st.rerun()


def results() -> None:
    profile = st.session_state.get("profile")
    if profile is None:
        navigate("questionnaire")
        st.rerun()
    st.markdown('<div class="swan-kicker">03 / Your results</div>', unsafe_allow_html=True)
    st.title("A clearer way to compare.")
    st.caption("These are moisturizer alternatives, not a three-product routine. The baseline uses ingredient indicators; it does not establish efficacy or personal suitability.")
    st.caption("Skin type and reactivity do not currently change ranking. Your selected ingredient exclusions are applied.")
    try:
        if "recommendation_response" not in st.session_state:
            with st.spinner("Finding available alternatives…"):
                st.session_state.recommendation_response = fetch_recommendations(profile)
        result = st.session_state.recommendation_response
    except RecommendationUnavailable as exc:
        st.error(str(exc))
        st.button("Try again", key="retry")
        st.button("Edit my answers", key="edit", on_click=navigate, args=("questionnaire",))
        return
    status = result.get("status")
    if status == "coming_soon":
        coming_soon()
        return
    if status in {"referral", "out_of_scope", "incomplete_profile"}:
        st.info(result.get("message", "Please review your answers."))
    elif status in {"ok", "insufficient_results", "no_result"}:
        if status != "ok":
            st.info(result.get("message", "No eligible alternatives are available."))
        products = result["results"]
        if products:
            for column, product in zip(st.columns(len(products)), products):
                with column:
                    with st.container(border=True):
                        st.caption("MOISTURIZER")
                        st.subheader(product["product_name"])
                        st.write(product["reason"])
                        st.caption("Product code: " + product["code"])
                        st.caption("Baseline indicator score: " + str(product["score"]))
        with st.expander("About these results"):
            st.write("Products are ranked using the agreed moisturising and acne-related indicators. Ties use product codes for a reproducible order. Ingredient concentration and clinical effectiveness are not assessed.")
            st.caption("Catalogue: " + str(result.get("catalogue_version", "unavailable")))
            st.caption("Ranker: " + str(result.get("ranker_version", "unavailable")))
    else:
        st.error("We could not read this recommendation response. Please try again later.")
    st.button("Edit my answers", key="edit", on_click=navigate, args=("questionnaire",))


def outside_scope(professional: bool = False) -> None:
    st.markdown('<div class="swan-kicker">A useful boundary</div>', unsafe_allow_html=True)
    st.title("Let's pause here.")
    if professional:
        st.write("You selected a situation outside this draft prototype's scope. Product recommendations are not available for this route. A qualified healthcare professional can help with your individual questions.")
    else:
        st.write("This draft experience covers adults exploring moisturizers for acne-prone skin. Your answers fall outside that scope, so no product results are shown.")
    st.caption("These are prototype scope rules for team review, not a diagnosis or a medical safety assessment.")
    st.button("Edit my answers", key="edit", on_click=navigate, args=("questionnaire",))


def coming_soon() -> None:
    profile = st.session_state.get("profile")
    label = next((label for label, code in CONCERNS.items() if profile and code == profile.concern), "This concern")
    st.markdown('<div class="swan-kicker">A future Swan experience</div>', unsafe_allow_html=True)
    st.title("Not available in this version.")
    st.write(f"You selected: {label}.")
    st.write("Swan's first MVP focuses on moisturizers for acne-prone skin. This concern is shown to reflect the wider project, but its recommendation path is not available yet.")
    st.info("No product results are shown for this concern. You can return to the questionnaire or start over.")
    st.button("Edit my answers", key="edit", on_click=navigate, args=("questionnaire",))


def main() -> None:
    st.session_state.setdefault("view", "welcome")
    header()
    view = st.session_state.view
    if view == "welcome":
        welcome()
    elif view == "questionnaire":
        questionnaire()
    elif view == "results":
        results()
    elif view == "professional_guidance":
        outside_scope(professional=True)
    elif view == "coming_soon":
        coming_soon()
    else:
        outside_scope()


main()
