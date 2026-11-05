"""Run with: python -m streamlit run app.py"""

import base64
import time
from pathlib import Path

import streamlit as st

from swan_ui.client import fetch_recommendations, RecommendationUnavailable
from swan_ui.profile import Profile, preview_route


st.set_page_config(page_title="Swan · A simpler skincare starting point", page_icon="🦢", layout="wide")

SKIN_TYPES = {"Not sure": "not_sure", "Oily": "oily", "Combination": "combination", "Normal": "normal", "Dry": "dry"}
REACTIVITY = {"Yes": "yes", "No": "no"}
CONCERNS = {
    "Acne-prone skin": "acne_prone",
    "Dryness / skin barrier": "dryness_barrier",
    "Sensitivity / irritation": "sensitivity",
}
FLAGS = {
    "I use a skin treatment prescribed by a doctor": "prescribed_treatment",
    "I have a sudden, painful flare-up or a skin change that worries me": "unusual_lesion",
    "I am pregnant or breastfeeding": "pregnant_or_breastfeeding",
}
AVOID = {"Fragrance": "fragrance", "Essential oils": "essential_oils"}
NONE = "None of these"


def navigate(view: str) -> None:
    st.session_state.view = view


def reset_demo() -> None:
    for key in list(st.session_state):
        if key.startswith("q_") or key in {"profile", "recommendation_response", "answers", "question_step", "reset_pending", "slide_direction"}:
            del st.session_state[key]
    st.session_state.view = "welcome"


def header() -> None:
    logo = base64.b64encode((Path(__file__).parent / "swan_ui/assets/swan-logo.png").read_bytes()).decode()
    st.markdown("""
    <style>
    .stApp {background: radial-gradient(ellipse at 90% 0%, #f8e7df 0, transparent 45%), #fcf8f5; color:#402c3b;}
    .block-container {max-width:1080px; padding-top:2rem; padding-bottom:4rem;}
    h1,h2,h3 {letter-spacing:-.035em; color:#503047;}
    [data-testid="stAppViewContainer"] h1 {font-family:Georgia,serif; font-weight:400; font-size:clamp(2.4rem,5vw,4rem); line-height:1.13;}
    .swan-brand {display:flex;align-items:center;gap:10px;margin-bottom:24px;}
    .swan-brand img {width:92px;height:92px;object-fit:contain;}
    .swan-wordmark {font-family:Georgia,serif;font-size:3.45rem;letter-spacing:.04em;color:#59324e;}
    .swan-kicker {color:#7b5b6b;font-size:.76rem;text-transform:uppercase;letter-spacing:.16em;margin:1rem 0;}
    .swan-lead {font-size:1.13rem;line-height:1.7;color:#685762;max-width:43rem;}
    [data-testid="stSidebar"] {background:#f2e9e8;border-right:1px solid #e5d6dc;}
    [data-testid="stVerticalBlockBorderWrapper"] > div {border-radius:20px;}
    [data-testid="stBaseButton-primary"] {background:#60394f;border-color:#60394f;border-radius:24px;padding:.55rem 1.4rem;}
    [data-testid="stBaseButton-secondary"] {border-radius:24px;border-color:#d9c6cf;}
    [data-testid="stProgressBar"] {margin-bottom:1.5rem;}
    [class*="st-key-question_slide_"] h1 {font-size:clamp(2rem,3.4vw,3rem) !important;}
    [class*="st-key-question_slide_"] [data-testid="stWidgetLabel"] p,
    [class*="st-key-question_slide_"] [data-testid="stRadio"] label p {font-size:1.2rem;line-height:1.6;}
    [class*="st-key-question_slide_"] [data-testid="stRadio"] label {padding:.4rem .2rem;}
    [class*="st-key-question_slide_"] button {min-height:3.2rem;padding:.65rem 1.6rem;}
    [class*="st-key-question_slide_"] button p {font-size:1.1rem;}
    @media(max-width:640px){[class*="st-key-question_slide_"] h1{font-size:2rem !important;}}

    @media(max-width:640px){.block-container{padding-top:1rem;} .swan-brand{margin-bottom:12px;} .swan-brand img{width:76px;height:76px;} .swan-wordmark{font-size:2.85rem;}}
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f'<div class="swan-brand"><img src="data:image/png;base64,{logo}" alt="Swan logo"><span class="swan-wordmark">Swan</span></div>', unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("### Your skincare starting point")
        view = st.session_state.get("view", "welcome")
        for key, label in [("welcome","01 · Welcome"),("questionnaire","02 · Your profile"),("results","03 · Your alternatives")]:
            st.markdown(f"**{label}**" if key == view else label)
        st.divider()
        st.caption("OUR FIRST CHAPTER")
        st.write("Moisturizer alternatives for acne-prone skin.")
        st.caption("Dryness, sensitivity and a complete routine are planned for a later version.")
        with st.expander("About your answers"):
            st.caption("Answers are sent to the Swan API to return results. Swan does not intentionally store questionnaire answers. No name or photo is needed.")
        if st.button("Start over", key="reset", use_container_width=True):
            st.session_state.reset_pending = True
        if st.session_state.get("reset_pending"):
            st.warning("Clear your answers and start again?")
            st.button("Yes, start again", key="confirm_reset", on_click=reset_demo)
            if st.button("Keep my answers", key="cancel_reset"):
                st.session_state.reset_pending = False
                st.rerun()


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


QUESTIONS = [
    ("q_adult", "First, a quick age check.", "Are you 18 or older?"),
    ("q_concern", "What brings you here?", "Which concern would you like to explore?"),
    ("q_blemish", "One more detail.", "How would you describe your blemishes?"),
    ("q_flags", "A few boundaries first.", "Do any of these apply to you?"),
    ("q_skin", "Tell us about your skin.", "How would you describe your skin?"),
    ("q_reactivity", "How does your skin feel?", "Does your skin react easily, such as stinging or redness?"),
    ("q_avoid", "Your preferences matter.", "Ingredients you prefer to avoid (optional)"),
]
DEFAULTS = {"q_adult":None,"q_concern":None,"q_flags":[],"q_skin":"Not sure","q_reactivity":None,"q_blemish":"Prefer not to say","q_avoid":[]}


def save_answer(key):
    st.session_state.answers[key] = st.session_state[key]


def profile_from_answers(a):
    return Profile(
        is_adult=a["q_adult"] == "Yes", concern=CONCERNS[a["q_concern"]],
        blemish_level=a["q_blemish"] if a["q_concern"] == "Acne-prone skin" and isinstance(a["q_blemish"], int) else None,
        referral_flags=tuple(FLAGS[x] for x in a["q_flags"] if x != NONE),
        skin_type=SKIN_TYPES[a["q_skin"]], reactivity=REACTIVITY.get(a["q_reactivity"], "not_sure"),
        avoid=tuple(AVOID[x] for x in a["q_avoid"]),
    )


def slide_to(step: int) -> None:
    current = st.session_state.get("question_step", 0)
    direction = 1 if step > current else -1
    # Animate the existing card before the rerun replaces it with the next card.
    st.markdown(f"""<style>
    @keyframes swan-exit-{current} {{to {{opacity:0;transform:translateX({-direction * 48}px);}}}}
    .st-key-question_slide_{current} {{animation:swan-exit-{current} 180ms ease-in forwards !important;pointer-events:none;}}
    @media(prefers-reduced-motion:reduce){{.st-key-question_slide_{current}{{animation:none !important;}}}}
    </style>""", unsafe_allow_html=True)
    time.sleep(.20)
    st.session_state.slide_direction = direction
    st.session_state.question_step = step
    st.rerun()


def questionnaire() -> None:
    # Permanent answers survive Streamlit's cleanup of widgets on hidden steps.
    st.session_state.setdefault("answers", DEFAULTS.copy())
    st.session_state.setdefault("question_step", 0)
    a = st.session_state.answers
    step = st.session_state.question_step
    st.markdown('<div class="swan-kicker">Your profile · A little clarity, one question at a time</div>', unsafe_allow_html=True)
    st.progress(min(step / 7, 1), text=f"Question {step + 1} of 7" if step < 7 else "Your profile is ready to review")
    direction = st.session_state.get("slide_direction", 1)
    st.markdown(f"""<style>
    @keyframes swan-enter-{step} {{from {{opacity:0;transform:translateX({direction * 48}px);}} to {{opacity:1;transform:translateX(0);}}}}
    .st-key-question_slide_{step} {{animation:swan-enter-{step} 280ms ease-out both;}}
    @media(prefers-reduced-motion:reduce){{.st-key-question_slide_{step}{{animation:none;}}}}
    </style>""", unsafe_allow_html=True)
    with st.container(key=f"question_slide_{step}"):
        if step == 7:
            st.title("Does this look like you?")
            st.write("Review your answers before exploring the available route.")
            for i, (key, _, label) in enumerate(QUESTIONS):
                with st.container(border=True):
                    left, right = st.columns([5,1])
                    value = a[key]
                    left.markdown(f"**{label}**")
                    left.write(", ".join(value) if isinstance(value,list) and value else "No exclusions" if key == "q_avoid" else str(value))
                    if right.button("Edit", key=f"review_{i}"):
                        slide_to(i)
            st.caption("Skin type and reactivity are collected but do not yet change baseline ranking. Exclusions filter the available products.")
            if st.button("See my results", key="submit_profile", type="primary"):
                profile = profile_from_answers(a)
                st.session_state.profile = profile
                st.session_state.pop("recommendation_response", None)
                st.session_state.view = preview_route(profile)
                st.rerun()
            return
        key, title, label = QUESTIONS[step]
        st.title(title)
        st.session_state.setdefault(key, a[key])
        kwargs = dict(key=key, on_change=save_answer, args=(key,))
        with st.container(border=True):
            if key == "q_adult":
                st.radio(label, ["Yes","No"], index=None, horizontal=True, **kwargs)
                st.caption("This first version is intended for adults.")
            elif key == "q_concern":
                st.radio(label, list(CONCERNS), index=None, **kwargs)
                st.caption("Acne-prone moisturizer suggestions are available. Dryness and sensitivity will show a not-available-yet message.")
            elif key == "q_flags":
                st.multiselect(label, [NONE,*FLAGS], **kwargs)
                st.caption("Choose None of these if none apply. These scope rules are not a clinical assessment.")
            elif key == "q_skin":
                st.selectbox(label, list(SKIN_TYPES), **kwargs)
                st.caption("We’re collecting this for the wider experience; it does not yet change ranking.")
            elif key == "q_reactivity":
                st.radio(label, list(REACTIVITY), index=None, **kwargs)
                st.caption("This answer does not automatically exclude fragrance or essential oils. Choose those exclusions in the preferences step.")
            elif key == "q_blemish":
                st.select_slider(label, ["Prefer not to say","No current blemishes",1,2,3,4,5], **kwargs)
                st.caption("Choose No current blemishes if none of the descriptions apply to you.")
                st.markdown("1 · A few blackheads or small spots now and then\n\n2 · Some small spots, often in the same area\n\n3 · Small spots in several areas, not painful\n\n4 · Lots of red or swollen spots\n\n5 · Deep, painful lumps, or spots that leave scars")
                st.caption("Levels 4–5 lead to guidance rather than product suggestions. This is not a diagnosis.")
            else:
                st.multiselect(label, list(AVOID), **kwargs)
                st.caption("Ingredient lists can be incomplete. If you have an allergy, check the packaging or ask a pharmacist.")
                st.caption("Leave blank for no exclusions. Fragrance avoidance does not automatically exclude every fragrance allergen.")
        left, right = st.columns([1,2])
        if left.button("Back", key="previous_question"):
            a[key] = st.session_state[key]
            if step:
                slide_to(step - 1)
            else:
                navigate("welcome")
            st.rerun()
        if right.button("Review my answers" if step == 6 else "Continue", key="next_question", type="primary"):
            a[key] = st.session_state[key]
            value = a[key]
            error = None
            if key in {"q_adult","q_concern"} and value is None:
                error = "Please select an answer to continue."
            elif key == "q_flags" and (not value or NONE in value and len(value)>1):
                error = "Choose either None of these or the options that apply."
            elif key in {"q_reactivity","q_blemish"}:
                p = profile_from_answers(a)
                if preview_route(p) == "results" and (key == "q_reactivity" and value is None or key == "q_blemish" and value != "No current blemishes" and not isinstance(value,int)):
                    error = "Please answer Yes or No to the skin reactivity question." if key == "q_reactivity" else "Please choose a blemish level from 1 to 5."
            if error:
                st.error(error)
            else:
                profile = profile_from_answers(a) if a["q_concern"] else None
                route = preview_route(profile) if profile else "results"
                if key in {"q_adult", "q_concern", "q_blemish", "q_flags"}:
                    # Respect early scope exits; later answers are not required.
                    if key == "q_adult" and value == "No":
                        profile = Profile(False, "acne_prone", None, (), "not_sure", "not_sure", ())
                        route = "outside_scope"
                    if profile and ((key == "q_adult" and value == "No") or (key == "q_concern" and profile.concern != "acne_prone") or (key == "q_blemish" and (value == "No current blemishes" or isinstance(value, int) and value >= 4)) or (key == "q_flags" and profile.referral_flags)):
                        st.session_state.profile = profile
                        st.session_state.pop("recommendation_response", None)
                        st.session_state.view = "outside_scope" if key == "q_blemish" and value == "No current blemishes" else route
                        st.rerun()
                slide_to(step + 1)


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
                        st.caption("YOUR MOISTURIZER ALTERNATIVE")
                        st.subheader(product["product_name"])
                        st.write(product["reason"])
                        st.caption("Product code: " + product["code"])
                        st.caption("Baseline indicator score: " + str(product["score"]))
        with st.expander("Why might the same products appear?"):
            st.write("This baseline uses two product indicators. Skin type and reactivity do not yet change the score. With the same exclusions, the same alternatives can appear; this is not a fully personalised ranking.")
        with st.expander("About these results"):
            st.write("Products are ranked using the agreed moisturising and acne-related indicators. Ties use product codes for a reproducible order. Ingredient concentration and clinical effectiveness are not assessed.")
    else:
        st.error("We could not read this recommendation response. Please try again later.")
    st.button("Edit my answers", key="edit", on_click=navigate, args=("questionnaire",))


def outside_scope(professional: bool = False) -> None:
    st.markdown('<div class="swan-kicker">A useful boundary</div>', unsafe_allow_html=True)
    st.title("Let's pause here.")
    profile = st.session_state.get("profile")
    if profile and not profile.is_adult:
        st.write("Swan is made for adults. Please ask a specialized doctor if needed.")
    elif st.session_state.get("answers", {}).get("q_blemish") == "No current blemishes":
        st.write("You selected no current blemishes. This first version focuses on acne-prone skin with mild blemishes, so no product suggestions are shown for this path. Our broader skincare experience is planned for a later version.")
    elif profile and profile.blemish_level is not None and profile.blemish_level >= 4:
        st.write("Lots of red, painful or deep spots, or scars, are worth showing to a doctor or dermatologist.")
    elif professional and profile:
        messages = {
            "prescribed_treatment": "Check with the person who prescribed your treatment before adding new products.",
            "unusual_lesion": "A sudden or unusual change in your skin should be checked by a doctor.",
            "pregnant_or_breastfeeding": "This MVP does not suggest products during pregnancy or breastfeeding. Please ask a pharmacist or your healthcare professional for advice.",
        }
        for flag in profile.referral_flags:
            st.write(messages[flag])
    else:
        st.write("Swan only covers acne-prone skin for now.")
    st.caption("No product suggestions are shown for this route. These are prototype scope rules, not a diagnosis or a medical safety assessment.")
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
