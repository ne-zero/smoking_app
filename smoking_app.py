from pathlib import Path
from textwrap import dedent

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# PAGE SETUP
# =========================================================
st.set_page_config(
    page_title="SmokeScreen",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================
st.markdown(
    """
    <style>
    :root{
        --font-serif: Georgia, "Iowan Old Style", "Palatino Linotype",
                      "Book Antiqua", serif;
        --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI",
                     Roboto, Helvetica, Arial, sans-serif;
        --font-mono: "SF Mono", "Cascadia Code", Consolas,
                     "Liberation Mono", Menlo, monospace;

        --bg:#100c09;
        --bg-deep:#0b0806;
        --bg-soft:#170f09;
        --card:#150f0a;
        --card-2:#1a130c;
        --ink:#f3ede4;
        --ink-soft:#b5aa9d;
        --ink-dim:#7d7264;
        --line:#2a2019;
        --line-soft:#1f170f;

        --ember:#ff7a3d;
        --ember-deep:#c9501a;
        --ember-soft:rgba(255,122,61,.14);
        --green:#67d695;
        --green-soft:rgba(103,214,149,.14);
        --red:#ff5967;
        --red-soft:rgba(255,89,103,.14);
        --amber:#ffbf4d;
        --amber-soft:rgba(255,191,77,.14);
    }

    html{color-scheme:dark!important}

    html,body,[class*="css"]{
        font-family:var(--font-sans);
    }

    .stApp{
        background:
            radial-gradient(circle at 12% -6%,
                rgba(255,122,61,.14), transparent 34rem),
            radial-gradient(circle at 100% 0%,
                rgba(255,89,103,.07), transparent 30rem),
            linear-gradient(180deg,var(--bg-deep) 0%,var(--bg) 100%);
        color:var(--ink)!important;
    }

    html,body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section[data-testid="stMain"],
    .main,
    [data-testid="stHeader"]{
        background:transparent!important;
    }

    body{background:var(--bg)!important}

    .block-container{
        max-width:1240px;
        padding-top:0;
        padding-bottom:3rem;
    }

    header[data-testid="stHeader"]{background:transparent}

    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"]{
        visibility:hidden!important;
        display:none!important;
    }

    ::selection{
        background:var(--ember);
        color:#160803;
    }

    /* ---------- ticker ---------- */
    .ticker{
        overflow:hidden;
        border-top:1px solid var(--line-soft);
        border-bottom:1px solid var(--line-soft);
        background:var(--bg-soft);
        padding:.55rem 0;
        white-space:nowrap;
    }

    .ticker-track{
        display:inline-flex;
        animation:ticker-scroll 28s linear infinite;
    }

    .ticker-track span{
        padding:0 1.35rem;
        font-family:var(--font-mono);
        font-size:.7rem;
        font-weight:600;
        letter-spacing:.13em;
        text-transform:uppercase;
        color:var(--ink-dim)!important;
    }

    .ticker-track span.accent{color:var(--ember)!important}

    @keyframes ticker-scroll{
        from{transform:translateX(0)}
        to{transform:translateX(-50%)}
    }

    /* ---------- hero ---------- */
    .hero{
        position:relative;
        overflow:hidden;
        padding:4.2rem 1rem 3.5rem;
        border-bottom:1px solid var(--line-soft);
    }

    .hero-grid{
        display:flex;
        justify-content:space-between;
        align-items:flex-end;
        gap:2rem;
        position:relative;
        z-index:2;
    }

    .hero-badge{
        display:inline-flex;
        align-items:center;
        gap:.5rem;
        padding:.42rem .85rem;
        border-radius:999px;
        background:var(--ember-soft);
        border:1px solid rgba(255,122,61,.35);
        font-family:var(--font-mono);
        font-size:.7rem;
        font-weight:600;
        letter-spacing:.12em;
        text-transform:uppercase;
        color:var(--ember)!important;
    }

    .hero-badge .dot{
        width:6px;
        height:6px;
        border-radius:50%;
        background:var(--ember);
        box-shadow:0 0 0 3px rgba(255,122,61,.25);
    }

    .hero h1{
        max-width:760px;
        margin:1.3rem 0 0;
        font-family:var(--font-serif);
        font-weight:600;
        font-size:clamp(2.75rem,5.6vw,5rem);
        line-height:.98;
        letter-spacing:-.035em;
        color:var(--ink)!important;
    }

    .hero h1 em{
        font-style:italic;
        font-weight:500;
        color:var(--ember)!important;
    }

    .hero p{
        max-width:560px;
        margin:1.4rem 0 0;
        line-height:1.72;
        font-size:1.02rem;
        color:var(--ink-soft)!important;
    }

    .hero-gauge-wrap{text-align:center}

    .hero-gauge{
        width:100%;
        max-width:300px;
        height:auto;
    }

    .hero-gauge-label{
        display:block;
        margin-top:-.2rem;
        text-align:center;
        font-family:var(--font-mono);
        font-size:.72rem;
        font-weight:600;
        letter-spacing:.1em;
        text-transform:uppercase;
        color:var(--ink-soft)!important;
    }

    .hero-meta{
        display:flex;
        gap:1.8rem;
        margin-top:2.3rem;
        flex-wrap:wrap;
    }

    .hero-meta div{
        border-left:2px solid var(--ember);
        padding-left:.7rem;
    }

    .hero-meta .meta-label{
        font-family:var(--font-mono);
        font-size:.65rem;
        letter-spacing:.1em;
        text-transform:uppercase;
        color:var(--ink-soft)!important;
    }

    .hero-meta .meta-value{
        margin-top:.15rem;
        font-family:var(--font-mono);
        font-size:1.05rem;
        font-weight:600;
        color:var(--ink)!important;
    }

    /* ---------- reusable cards ---------- */
    .card{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:18px;
        padding:1.2rem 1.35rem;
        min-height:125px;
    }

    .kicker{
        font-family:var(--font-mono);
        font-size:.7rem;
        font-weight:600;
        letter-spacing:.09em;
        text-transform:uppercase;
        color:var(--ember)!important;
    }

    .title{
        margin:.35rem 0;
        font-family:var(--font-serif);
        font-size:1.3rem;
        font-weight:600;
        color:var(--ink)!important;
    }

    .copy{
        font-size:.92rem;
        line-height:1.64;
        color:var(--ink-soft)!important;
    }

    .pills{
        display:flex;
        gap:.5rem;
        flex-wrap:wrap;
        margin-top:.85rem;
    }

    .pill{
        display:inline-flex;
        align-items:center;
        gap:.4rem;
        padding:.4rem .72rem .4rem .5rem;
        border-radius:999px;
        background:var(--ember-soft);
        border:1px solid rgba(255,122,61,.3);
        color:var(--ember)!important;
        font-size:.8rem;
        font-weight:600;
    }

    .pill b{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        width:1.15rem;
        height:1.15rem;
        border-radius:50%;
        background:var(--ember);
        color:#160803!important;
        font-family:var(--font-mono);
        font-size:.66rem;
    }

    /* ---------- mode selector ---------- */
    div[data-testid="stRadio"] div[role="radiogroup"]{
        gap:.55rem;
    }

    div[data-testid="stRadio"] label{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:999px;
        padding:.55rem 1.1rem!important;
        margin:0!important;
    }

    div[data-testid="stRadio"] label:has(input:checked){
        background:var(--ember-soft);
        border-color:rgba(255,122,61,.45);
    }

    div[role="radiogroup"] label,
    div[role="radiogroup"] label p{
        color:var(--ink)!important;
    }

    /* ---------- form shell ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"]{
        background:var(--card);
        border:1px solid var(--line)!important;
        border-radius:22px!important;
        padding:.35rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]
    div[data-testid="stVerticalBlock"]{
        gap:.65rem;
    }

    .section-head{
        display:flex;
        align-items:baseline;
        gap:.55rem;
        margin:.45rem 0 1rem;
    }

    .section-head .n{
        font-family:var(--font-mono);
        font-size:.75rem;
        font-weight:600;
        color:var(--ember)!important;
    }

    .section-head .t{
        font-family:var(--font-serif);
        font-size:1.08rem;
        font-weight:600;
        color:var(--ink)!important;
    }

    .section-head .r{
        flex:1;
        height:1px;
        background:var(--line);
    }

    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3,
    .stMarkdown h4{
        color:var(--ink)!important;
        font-family:var(--font-serif);
        letter-spacing:-.01em;
    }

    .stMarkdown p,
    .stCaption,
    label,
    div[data-testid="stWidgetLabel"] p{
        color:var(--ink)!important;
    }

    .stCaption{color:var(--ink-soft)!important}

    .field-note{
        margin-top:-.3rem;
        margin-bottom:.9rem;
        padding:.5rem .65rem;
        border:1px solid var(--line);
        border-radius:10px;
        background:var(--card-2);
        color:var(--ink-soft)!important;
        font-size:.76rem;
        line-height:1.42;
    }

    .info-box{
        padding:.85rem 1rem;
        border-radius:14px;
        background:var(--ember-soft);
        border:1px solid rgba(255,122,61,.3);
        color:var(--ember)!important;
        font-size:.88rem;
        line-height:1.55;
        margin-bottom:1rem;
    }

    .warn-box{
        padding:.85rem 1rem;
        border-radius:14px;
        background:var(--amber-soft);
        border:1px solid rgba(255,191,77,.35);
        color:var(--amber)!important;
        font-size:.88rem;
        line-height:1.55;
    }

    div[data-testid="stTabs"] button{
        color:var(--ink-dim)!important;
        font-weight:600!important;
    }

    div[data-testid="stTabs"] button[aria-selected="true"]{
        color:var(--ember)!important;
    }

    div[data-testid="stTabs"] div[data-baseweb="tab-highlight"]{
        background-color:var(--ember)!important;
    }

    div[data-testid="stTabs"] div[data-baseweb="tab-border"]{
        background-color:var(--line)!important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="input"]>div,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"]>div,
    div[data-baseweb="select"]>div{
        background:var(--card-2)!important;
        border-color:var(--line)!important;
        color:var(--ink)!important;
        border-radius:10px!important;
    }

    input,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input{
        color:var(--ink)!important;
        -webkit-text-fill-color:var(--ink)!important;
        opacity:1!important;
        font-family:var(--font-mono)!important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[role="option"]{
        color:var(--ink)!important;
    }

    div[role="listbox"]{
        background:var(--card-2)!important;
        border:1px solid var(--line)!important;
    }

    button[title="Increment"],
    button[title="Decrement"]{
        background:var(--card-2)!important;
        border-color:var(--line)!important;
    }

    button[title="Increment"] svg,
    button[title="Decrement"] svg{
        fill:var(--ink)!important;
    }

    .stButton>button{
        width:100%;
        min-height:3.1rem;
        border:none;
        border-radius:14px;
        background:linear-gradient(90deg,var(--ember-deep),var(--ember));
        color:#160803!important;
        font-size:.96rem;
        font-weight:700;
        box-shadow:0 13px 30px rgba(255,122,61,.18);
    }

    .stButton>button p{color:#160803!important}

    /* ---------- right prediction panel ---------- */
    .result-sticky{
        position:sticky;
        top:1rem;
    }

    .result-placeholder{
        min-height:300px;
        padding:1.5rem;
        border:1px dashed #3b2a1f;
        border-radius:22px;
        background:rgba(21,15,10,.82);
        display:flex;
        flex-direction:column;
        justify-content:center;
    }

    .result-placeholder h3{
        margin:.3rem 0 .5rem;
        font-family:var(--font-serif);
        color:var(--ink)!important;
    }

    .result-placeholder p{
        margin:0;
        line-height:1.62;
        color:var(--ink-soft)!important;
    }

    .result-card{
        min-height:300px;
        padding:1.55rem;
        border:1px solid;
        border-radius:22px;
    }

    .result-card h3{
        margin:.3rem 0 .5rem;
        font-family:var(--font-serif);
        color:var(--ink)!important;
    }

    .result-card p{
        line-height:1.62;
        color:var(--ink-soft)!important;
    }

    .result-smoker{
        background:var(--red-soft);
        border-color:rgba(255,89,103,.38);
    }

    .result-nonsmoker{
        background:var(--green-soft);
        border-color:rgba(103,214,149,.38);
    }

    .result-score{
        margin-top:1.15rem;
        font-family:var(--font-mono);
        font-size:2.85rem;
        font-weight:600;
        color:var(--ink)!important;
    }

    .result-caption{
        font-family:var(--font-mono);
        font-size:.69rem;
        letter-spacing:.08em;
        text-transform:uppercase;
        color:var(--ink-soft)!important;
    }

    .foot{
        font-size:.84rem;
        line-height:1.6;
        color:var(--ink-dim)!important;
    }

    @media(max-width:900px){
        .hero-grid{
            flex-direction:column;
            align-items:flex-start;
        }

        .hero-gauge-wrap{text-align:left}
        .hero-gauge{max-width:220px}
        .result-sticky{position:static}
    }

    @media(max-width:760px){
        .hero{padding:2.7rem 1rem 2.3rem}

        .block-container{
            padding-left:.8rem;
            padding-right:.8rem;
        }
    }
    
    /* Compact priority slider status */
    .slider-status-row{
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:.5rem;
        margin:.05rem 0 .55rem;
    }

    .slider-selected{
        font-family:var(--font-mono);
        font-size:.72rem;
        color:var(--ink-soft)!important;
    }

    .slider-status{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding:.23rem .55rem;
        border-radius:999px;
        font-family:var(--font-mono);
        font-size:.61rem;
        font-weight:700;
        letter-spacing:.05em;
        text-transform:uppercase;
    }

    .slider-good{
        color:#6bd596!important;
        background:rgba(107,213,150,.14);
        border:1px solid rgba(107,213,150,.34);
    }

    .slider-average{
        color:#ffbf4d!important;
        background:rgba(255,191,77,.14);
        border:1px solid rgba(255,191,77,.34);
    }

    .slider-bad{
        color:#ff5967!important;
        background:rgba(255,89,103,.14);
        border:1px solid rgba(255,89,103,.34);
    }

    div[data-testid="stSlider"] [data-testid*="TickBar" i]{
        display:none!important;
    }

    .st-key-quick_gtp div[data-baseweb="slider"] > div:first-child,
    .st-key-full_gtp div[data-baseweb="slider"] > div:first-child{
        background:linear-gradient(
            90deg,
            #ffbf4d 0%,
            #ffbf4d 7%,
            #6bd596 7%,
            #6bd596 18%,
            #ff5967 18%,
            #ff5967 100%
        )!important;
    }

    .st-key-quick_hemoglobin div[data-baseweb="slider"] > div:first-child,
    .st-key-full_hemoglobin div[data-baseweb="slider"] > div:first-child{
        background:linear-gradient(
            90deg,
            #ff5967 0%,
            #ff5967 32%,
            #ffbf4d 32%,
            #ffbf4d 44%,
            #6bd596 44%,
            #6bd596 78%,
            #ffbf4d 78%,
            #ffbf4d 88%,
            #ff5967 88%,
            #ff5967 100%
        )!important;
    }

    .st-key-quick_triglyceride div[data-baseweb="slider"] > div:first-child,
    .st-key-full_triglyceride div[data-baseweb="slider"] > div:first-child{
        background:linear-gradient(
            90deg,
            #6bd596 0%,
            #6bd596 15%,
            #ffbf4d 15%,
            #ffbf4d 20%,
            #ff5967 20%,
            #ff5967 100%
        )!important;
    }


</style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MODEL FILES
# =========================================================
APP_FOLDER = Path(__file__).resolve().parent
MODEL_PATH = APP_FOLDER / "smoking_random_forest_model.pkl"
FEATURE_PATH = APP_FOLDER / "smoking_feature_columns.pkl"

REFERENCE_DEFAULTS = {
    "age": 40,
    "height(cm)": 165,
    "weight(kg)": 65,
    "waist(cm)": 82.0,
    "eyesight(left)": 1.0,
    "eyesight(right)": 1.0,
    "hearing(left)": 1.0,
    "hearing(right)": 1.0,
    "systolic": 120.0,
    "relaxation": 76.0,
    "fasting blood sugar": 96.0,
    "Cholesterol": 195.0,
    "HDL": 55.0,
    "LDL": 113.0,
    "Urine protein": 1.0,
    "serum creatinine": 0.9,
    "AST": 23.0,
    "ALT": 21.0,
    "dental caries": 0,
    "tartar": "N",
}


PRIORITY_REFERENCE_BANDS = {
    "Gtp": {
        "low": 8.0,
        "high": 61.0,
        "unit": "U/L",
    },
    "hemoglobin": {
        "low": 12.0,
        "high": 17.5,
        "unit": "g/dL",
    },
    "triglyceride": {
        "low": 8.0,
        "high": 149.0,
        "unit": "mg/dL",
    },
}

PRIORITY_FEATURES = {
    "gender",
    "Gtp",
    "hemoglobin",
    "triglyceride",
    "height(cm)",
}


@st.cache_resource
def load_files():
    if not MODEL_PATH.exists() or not FEATURE_PATH.exists():
        raise FileNotFoundError(
            "Place smoking_random_forest_model.pkl and "
            "smoking_feature_columns.pkl beside this app."
        )

    loaded_model = joblib.load(MODEL_PATH)
    loaded_columns = joblib.load(FEATURE_PATH)

    expected_n = getattr(loaded_model, "n_features_in_", None)

    if expected_n is not None and expected_n != len(loaded_columns):
        raise ValueError(
            "The model and feature-column file do not match."
        )

    return loaded_model, loaded_columns


try:
    model, feature_columns = load_files()
except Exception as exc:
    st.error("The prediction system could not be loaded.")
    st.code(str(exc))
    st.stop()


# =========================================================
# HELPERS
# =========================================================
def desc(text: str) -> None:
    st.markdown(
        f'<div class="field-note">{text}</div>',
        unsafe_allow_html=True,
    )


def binary(answer: str) -> int:
    return 1 if answer == "Yes" else 0


def encode(values: dict) -> pd.DataFrame:
    frame = pd.DataFrame([values])

    frame = pd.get_dummies(
        frame,
        columns=["gender", "tartar"],
        drop_first=False,
        dtype=int,
    )

    return frame.reindex(
        columns=feature_columns,
        fill_value=0,
    )


def validate(values: dict) -> list[str]:
    errors = []

    if values["systolic"] <= values["relaxation"]:
        errors.append(
            "Systolic pressure must be higher than diastolic pressure."
        )

    if values["HDL"] > values["Cholesterol"]:
        errors.append(
            "HDL cannot be greater than total cholesterol."
        )

    return errors



def slider_input(
    feature_name: str,
    label: str,
    minimum: float,
    maximum: float,
    default: float,
    step: float,
    key: str,
    note: str,
) -> float:
    """Render a compact Good / Average / Bad status slider."""
    value = st.slider(
        label,
        min_value=minimum,
        max_value=maximum,
        value=default,
        step=step,
        key=key,
    )

    reference = PRIORITY_REFERENCE_BANDS[feature_name]
    low = reference["low"]
    high = reference["high"]
    unit = reference["unit"]

    width = max(high - low, 1.0)
    average_low = low - (0.20 * width)
    average_high = high + (0.20 * width)

    if low <= value <= high:
        status_text = "Good"
        status_class = "slider-good"
    elif average_low <= value <= average_high:
        status_text = "Average"
        status_class = "slider-average"
    else:
        status_text = "Bad"
        status_class = "slider-bad"

    st.markdown(
        (
            '<div class="slider-status-row">'
            f'<span class="slider-selected">{value:g} {unit}</span>'
            f'<span class="slider-status {status_class}">{status_text}</span>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    desc(note)
    return value


def make_prediction(values: dict) -> dict:
    model_input = encode(values)

    predicted_class = int(model.predict(model_input)[0])
    smoker_score = float(model.predict_proba(model_input)[0][1])

    return {
        "class": predicted_class,
        "score": smoker_score,
    }


def render_result_panel(result: dict | None, mode: str) -> None:
    st.markdown('<div class="result-sticky">', unsafe_allow_html=True)

    if result is None:
        st.markdown(
            """
            <div class="result-placeholder">
                <div class="kicker">Prediction panel</div>
                <h3>Your result will appear here</h3>
                <p>
                    Complete the assessment and select the prediction button.
                    On desktop, the result stays visible beside the form.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        predicted_class = result["class"]
        smoker_score = result["score"]

        if predicted_class == 1:
            st.markdown(
                f"""
                <div class="result-card result-smoker">
                    <div class="kicker">Model prediction</div>
                    <h3>Predicted class: smoker</h3>
                    <p>
                        The submitted values are more similar to records
                        classified as smokers by the trained Random Forest.
                    </p>
                    <div class="result-score">{smoker_score * 100:.1f}%</div>
                    <div class="result-caption">model smoker score</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="result-card result-nonsmoker">
                    <div class="kicker">Model prediction</div>
                    <h3>Predicted class: non-smoker</h3>
                    <p>
                        The submitted values are more similar to records
                        classified as non-smokers by the trained Random Forest.
                    </p>
                    <div class="result-score">{smoker_score * 100:.1f}%</div>
                    <div class="result-caption">model smoker score</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.progress(smoker_score)

        if mode == "Quick Assessment":
            st.warning(
                "Quick Assessment uses reference defaults for the remaining "
                "features. Use Full Assessment for the most complete result."
            )
        elif predicted_class == 1:
            st.warning(
                "A smoker prediction can still be a false positive. "
                "Confirm smoking status directly."
            )
        else:
            st.info(
                "A non-smoker prediction can still be a false negative. "
                "This result is not proof."
            )

        with st.expander("Model limitations"):
            st.markdown(
                """
- This output is not a diagnosis or verified smoking status.
- The model can produce false positives and false negatives.
- The model smoker score is not a calibrated medical probability.
- Gender was highly influential, which may create fairness concerns.
- Feature importance does not mean that a feature causes smoking.
                """
            )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================
if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "prediction_mode" not in st.session_state:
    st.session_state.prediction_mode = "Full Assessment"

if "prediction_inputs" not in st.session_state:
    st.session_state.prediction_inputs = None


# =========================================================
# IMPRESSIVE TOP SECTION
# =========================================================
components.html(
    """
    <style>
        html, body {
            margin: 0;
            background: transparent;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         Roboto, Helvetica, Arial, sans-serif;
        }

        .hero {
            padding: 62px 16px 52px;
            color: #f3ede4;
            border-bottom: 1px solid #1f170f;
        }

        .grid {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 32px;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 14px;
            border-radius: 999px;
            color: #ff7a3d;
            background: rgba(255,122,61,.14);
            border: 1px solid rgba(255,122,61,.35);
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #ff7a3d;
            box-shadow: 0 0 0 3px rgba(255,122,61,.25);
        }

        h1 {
            max-width: 760px;
            margin: 22px 0 0;
            color: #f3ede4;
            font-family: Georgia, serif;
            font-size: clamp(44px, 6vw, 76px);
            line-height: .98;
            letter-spacing: -.035em;
            font-weight: 600;
        }

        h1 em {
            color: #ff7a3d;
            font-weight: 500;
        }

        p {
            max-width: 560px;
            margin: 22px 0 0;
            color: #b5aa9d;
            font-size: 16px;
            line-height: 1.7;
        }

        .gauge {
            width: 290px;
            min-width: 250px;
            text-align: center;
        }

        .gauge svg {
            width: 100%;
        }

        .gauge-label {
            margin-top: -2px;
            color: #b5aa9d;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        .meta {
            display: flex;
            flex-wrap: wrap;
            gap: 28px;
            margin-top: 34px;
        }

        .meta-item {
            padding-left: 12px;
            border-left: 2px solid #ff7a3d;
        }

        .meta-label {
            color: #b5aa9d;
            font-family: Consolas, monospace;
            font-size: 10px;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        .meta-value {
            margin-top: 4px;
            color: #f3ede4;
            font-family: Consolas, monospace;
            font-size: 16px;
            font-weight: 700;
        }

        @media (max-width: 800px) {
            .hero {
                padding: 34px 10px 30px;
            }

            .grid {
                flex-direction: column;
                align-items: flex-start;
            }

            .gauge {
                width: 220px;
                min-width: 220px;
            }
        }
    </style>

    <section class="hero">
        <div class="grid">
            <div>
                <div class="badge">
                    <span class="dot"></span>
                    Screening-support prototype
                </div>

                <h1>
                    Read the signal<br>
                    before <em>you</em> ask.
                </h1>

                <p>
                    Start with five high-priority inputs for a fast demonstration,
                    or complete the full screening profile for the model's most
                    faithful prediction. The output supports a conversation;
                    it does not replace one.
                </p>
            </div>

            <div class="gauge">
                <svg viewBox="0 0 300 165" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20,150 A130,130 0 0,1 280,150"
                          fill="none"
                          stroke="#2a2019"
                          stroke-width="3"
                          stroke-linecap="round"/>

                    <path d="M20,150 A130,130 0 0,1 261,83"
                          fill="none"
                          stroke="#ff7a3d"
                          stroke-width="3"
                          stroke-linecap="round"/>

                    <circle cx="261" cy="83" r="8"
                            fill="#100c09"
                            stroke="#ff7a3d"
                            stroke-width="3"/>

                    <text x="150" y="122"
                          text-anchor="middle"
                          font-family="Consolas, monospace"
                          font-size="36"
                          font-weight="700"
                          fill="#f3ede4">
                        82.6%
                    </text>
                </svg>

                <div class="gauge-label">Held-out test accuracy</div>
            </div>
        </div>

        <div class="meta">
            <div class="meta-item">
                <div class="meta-label">Model</div>
                <div class="meta-value">Random Forest</div>
            </div>

            <div class="meta-item">
                <div class="meta-label">Smoker F1-score</div>
                <div class="meta-value">0.7708</div>
            </div>

            <div class="meta-item">
                <div class="meta-label">Smoker recall</div>
                <div class="meta-value">79.70%</div>
            </div>

            <div class="meta-item">
                <div class="meta-label">Validation</div>
                <div class="meta-value">5-fold CV</div>
            </div>
        </div>
    </section>
    """,
    height=560,
    scrolling=False,
)


st.write("")
st.write("")

info_left, info_right = st.columns([1.55, 1])

with info_left:
    priority_pills = "".join(
        f'<span class="pill"><b>{index + 1}</b>{name}</span>'
        for index, name in enumerate(
            [
                "Gender",
                "Gtp",
                "Haemoglobin",
                "Triglycerides",
                "Height",
            ]
        )
    )

    st.markdown(
        f"""
        <div class="card">
            <div class="kicker">Feature priority</div>
            <div class="title">
                The strongest individual model signals
            </div>
            <div class="copy">
                These five fields had the highest individual feature-importance
                scores. The complete model still relies on all available inputs,
                because the reduced-feature experiment performed worse.
            </div>
            <div class="pills">{priority_pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with info_right:
    st.markdown(
        """
        <div class="card">
            <div class="kicker">Important</div>
            <div class="title">
                Quick mode is an approximation
            </div>
            <div class="copy">
                Quick Assessment fills the remaining inputs using reference
                defaults. Full Assessment should be used whenever actual
                screening values are available.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

mode_actions, reset_actions = st.columns([4, 1])

with mode_actions:
    mode = st.radio(
        "Assessment mode",
        ["Quick Assessment", "Full Assessment"],
        horizontal=True,
    )

with reset_actions:
    st.write("")
    if st.button("Reset result", use_container_width=True):
        st.session_state.prediction_result = None
        st.session_state.prediction_inputs = None
        st.rerun()

st.write("")


# =========================================================
# FORM LEFT / RESULT RIGHT
# =========================================================
form_column, result_column = st.columns([1.75, 1], gap="large")


# ---------------------------------------------------------
# QUICK ASSESSMENT
# ---------------------------------------------------------
if mode == "Quick Assessment":
    with form_column:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Fast demonstration</div>
                <div class="title">Enter five high-priority inputs</div>
                <div class="copy">
                    The other model inputs use reference defaults. This mode is
                    faster, but less personalised than Full Assessment.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        with st.container(border=True):
            st.markdown(
                """
                <div class="section-head">
                    <span class="n">01</span>
                    <span class="t">Priority laboratory values</span>
                    <div class="r"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            lab_1, lab_2, lab_3 = st.columns(3)

            with lab_1:
                gtp = slider_input(
                    "Gtp",
                    "Gamma-glutamyl transferase (Gtp)",
                    1.0,
                    999.0,
                    25.0,
                    1.0,
                    "quick_gtp",
                    "High-priority liver-enzyme measurement.",
                )

            with lab_2:
                hemoglobin = slider_input(
                    "hemoglobin",
                    "Haemoglobin concentration (hemoglobin)",
                    4.9,
                    21.1,
                    14.8,
                    0.1,
                    "quick_hemoglobin",
                    "High-priority oxygen-carrying blood measurement.",
                )

            with lab_3:
                triglyceride = slider_input(
                    "triglyceride",
                    "Triglycerides (triglyceride)",
                    8.0,
                    999.0,
                    108.0,
                    1.0,
                    "quick_triglyceride",
                    "High-priority blood-fat measurement.",
                )

            st.markdown(
                """
                <div class="section-head">
                    <span class="n">02</span>
                    <span class="t">Personal measurements</span>
                    <div class="r"></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            personal_1, personal_2 = st.columns(2)

            with personal_1:
                gender = st.selectbox(
                    "Gender (gender)",
                    ["F", "M"],
                    format_func=lambda value: (
                        "Female" if value == "F" else "Male"
                    ),
                    key="quick_gender",
                )
                desc("Highest-ranked categorical model input.")

            with personal_2:
                height = st.number_input(
                    "Height in centimetres (height(cm))",
                    min_value=130,
                    max_value=190,
                    value=165,
                    step=5,
                    key="quick_height",
                )
                desc("Physical measurement with high model importance.")

            st.markdown(
                """
                <div class="warn-box">
                    The remaining model fields use generic reference defaults,
                    not this person's actual measurements.
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            quick_predict = st.button(
                "Generate quick prediction",
                type="primary",
                use_container_width=True,
                key="quick_predict",
            )

        if quick_predict:
            quick_values = REFERENCE_DEFAULTS.copy()

            quick_values.update(
                {
                    "gender": gender,
                    "height(cm)": height,
                    "Gtp": gtp,
                    "hemoglobin": hemoglobin,
                    "triglyceride": triglyceride,
                }
            )

            errors = validate(quick_values)

            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.prediction_result = make_prediction(
                    quick_values
                )
                st.session_state.prediction_inputs = quick_values
                st.session_state.prediction_mode = mode

    with result_column:
        render_result_panel(
            st.session_state.prediction_result,
            st.session_state.prediction_mode,
        )


# ---------------------------------------------------------
# FULL ASSESSMENT
# ---------------------------------------------------------
else:
    with form_column:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Recommended</div>
                <div class="title">
                    Complete the full screening profile
                </div>
                <div class="copy">
                    This mode supplies every raw feature required by the final
                    model and produces the most faithful result for the entered
                    screening record.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        with st.container(border=True):
            priority_tab, screening_tab, blood_tab, oral_tab = st.tabs(
                [
                    "1. Priority inputs",
                    "2. Screening checks",
                    "3. Additional blood tests",
                    "4. Oral health",
                ]
            )

            with priority_tab:
                st.markdown(
                    """
                    <div class="info-box">
                        These fields had the highest individual feature-importance
                        scores in the trained Random Forest.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                priority_1, priority_2, priority_3 = st.columns(3)

                with priority_1:
                    gender = st.selectbox(
                        "Gender (gender)",
                        ["F", "M"],
                        format_func=lambda value: (
                            "Female" if value == "F" else "Male"
                        ),
                        key="full_gender",
                    )
                    desc("Highest-ranked categorical model input.")

                    height = st.number_input(
                        "Height in centimetres (height(cm))",
                        min_value=130,
                        max_value=190,
                        value=165,
                        step=5,
                        key="full_height",
                    )
                    desc("Standing height measured in centimetres.")

                with priority_2:
                    gtp = slider_input(
                        "Gtp",
                        "Gamma-glutamyl transferase (Gtp)",
                        1.0,
                        999.0,
                        25.0,
                        1.0,
                        "full_gtp",
                        "High-priority liver-enzyme measurement.",
                    )

                    hemoglobin = slider_input(
                        "hemoglobin",
                        "Haemoglobin concentration (hemoglobin)",
                        4.9,
                        21.1,
                        14.8,
                        0.1,
                        "full_hemoglobin",
                        "High-priority oxygen-carrying blood measurement.",
                    )

                with priority_3:
                    triglyceride = slider_input(
                        "triglyceride",
                        "Triglycerides (triglyceride)",
                        8.0,
                        999.0,
                        108.0,
                        1.0,
                        "full_triglyceride",
                        "High-priority blood-fat measurement.",
                    )

                    age = st.number_input(
                        "Age in years (age)",
                        min_value=20,
                        max_value=85,
                        value=40,
                        step=5,
                        key="full_age",
                    )
                    desc("Age at the time of screening.")

            with screening_tab:
                screening_1, screening_2, screening_3 = st.columns(3)

                with screening_1:
                    weight = st.number_input(
                        "Weight in kilograms (weight(kg))",
                        min_value=30,
                        max_value=135,
                        value=65,
                        step=5,
                        key="full_weight",
                    )

                    waist = st.number_input(
                        "Waist circumference (waist(cm))",
                        min_value=51.0,
                        max_value=129.0,
                        value=82.0,
                        step=0.5,
                        key="full_waist",
                    )

                with screening_2:
                    eyesight_left = st.number_input(
                        "Left-eye eyesight score (eyesight(left))",
                        min_value=0.1,
                        max_value=9.9,
                        value=1.0,
                        step=0.1,
                        key="full_eyesight_left",
                    )

                    eyesight_right = st.number_input(
                        "Right-eye eyesight score (eyesight(right))",
                        min_value=0.1,
                        max_value=9.9,
                        value=1.0,
                        step=0.1,
                        key="full_eyesight_right",
                    )

                    hearing_left = st.selectbox(
                        "Left-ear hearing (hearing(left))",
                        [1.0, 2.0],
                        format_func=lambda value: (
                            "1 — Normal"
                            if value == 1.0
                            else "2 — Reduced"
                        ),
                        key="full_hearing_left",
                    )

                    hearing_right = st.selectbox(
                        "Right-ear hearing (hearing(right))",
                        [1.0, 2.0],
                        format_func=lambda value: (
                            "1 — Normal"
                            if value == 1.0
                            else "2 — Reduced"
                        ),
                        key="full_hearing_right",
                    )

                with screening_3:
                    systolic = st.number_input(
                        "Systolic pressure (systolic)",
                        min_value=71.0,
                        max_value=240.0,
                        value=120.0,
                        step=1.0,
                        key="full_systolic",
                    )

                    relaxation = st.number_input(
                        "Diastolic pressure (relaxation)",
                        min_value=40.0,
                        max_value=146.0,
                        value=76.0,
                        step=1.0,
                        key="full_relaxation",
                    )

            with blood_tab:
                blood_1, blood_2, blood_3 = st.columns(3)

                with blood_1:
                    fasting = st.number_input(
                        "Fasting blood glucose (fasting blood sugar)",
                        min_value=46.0,
                        max_value=505.0,
                        value=96.0,
                        step=1.0,
                        key="full_fasting",
                    )

                    cholesterol = st.number_input(
                        "Total cholesterol (Cholesterol)",
                        min_value=55.0,
                        max_value=445.0,
                        value=195.0,
                        step=1.0,
                        key="full_cholesterol",
                    )

                    hdl = st.number_input(
                        "HDL (HDL)",
                        min_value=4.0,
                        max_value=618.0,
                        value=55.0,
                        step=1.0,
                        key="full_hdl",
                    )

                    ldl = st.number_input(
                        "LDL (LDL)",
                        min_value=1.0,
                        max_value=1860.0,
                        value=113.0,
                        step=1.0,
                        key="full_ldl",
                    )

                with blood_2:
                    urine = st.selectbox(
                        "Urine protein category (Urine protein)",
                        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                        key="full_urine",
                    )

                    creatinine = st.number_input(
                        "Serum creatinine (serum creatinine)",
                        min_value=0.1,
                        max_value=11.6,
                        value=0.9,
                        step=0.1,
                        key="full_creatinine",
                    )

                    ast = st.number_input(
                        "AST (AST)",
                        min_value=6.0,
                        max_value=1311.0,
                        value=23.0,
                        step=1.0,
                        key="full_ast",
                    )

                    alt = st.number_input(
                        "ALT (ALT)",
                        min_value=1.0,
                        max_value=2914.0,
                        value=21.0,
                        step=1.0,
                        key="full_alt",
                    )

                with blood_3:
                    st.markdown(
                        """
                        <div class="warn-box">
                            Lower-ranked features were retained because the
                            reduced-feature experiment produced weaker results.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with oral_tab:
                oral_1, oral_2 = st.columns(2)

                with oral_1:
                    caries_answer = st.radio(
                        "Dental caries present? (dental caries)",
                        ["No", "Yes"],
                        horizontal=True,
                        key="full_caries",
                    )

                with oral_2:
                    tartar = st.radio(
                        "Tartar present? (tartar)",
                        ["N", "Y"],
                        format_func=lambda value: (
                            "No" if value == "N" else "Yes"
                        ),
                        horizontal=True,
                        key="full_tartar",
                    )

            st.write("")

            full_predict = st.button(
                "Generate full prediction",
                type="primary",
                use_container_width=True,
                key="full_predict",
            )

        if full_predict:
            full_values = {
                "gender": gender,
                "age": age,
                "height(cm)": height,
                "weight(kg)": weight,
                "waist(cm)": waist,
                "eyesight(left)": eyesight_left,
                "eyesight(right)": eyesight_right,
                "hearing(left)": hearing_left,
                "hearing(right)": hearing_right,
                "systolic": systolic,
                "relaxation": relaxation,
                "fasting blood sugar": fasting,
                "Cholesterol": cholesterol,
                "triglyceride": triglyceride,
                "HDL": hdl,
                "LDL": ldl,
                "hemoglobin": hemoglobin,
                "Urine protein": urine,
                "serum creatinine": creatinine,
                "AST": ast,
                "ALT": alt,
                "Gtp": gtp,
                "dental caries": binary(caries_answer),
                "tartar": tartar,
            }

            errors = validate(full_values)

            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.session_state.prediction_result = make_prediction(
                    full_values
                )
                st.session_state.prediction_inputs = full_values
                st.session_state.prediction_mode = mode

    with result_column:
        render_result_panel(
            st.session_state.prediction_result,
            st.session_state.prediction_mode,
        )


# =========================================================
# REVIEW INPUTS
# =========================================================
if st.session_state.prediction_inputs is not None:
    st.write("")

    with st.expander("Review values supplied to the model"):
        values = st.session_state.prediction_inputs

        review_table = pd.DataFrame(
            {
                "Feature": list(values.keys()),
                "Value supplied": list(values.values()),
                "Source": [
                    (
                        "User entered"
                        if (
                            st.session_state.prediction_mode
                            == "Full Assessment"
                            or feature in PRIORITY_FEATURES
                        )
                        else "Reference default"
                    )
                    for feature in values
                ],
            }
        )

        st.dataframe(
            review_table,
            use_container_width=True,
            hide_index=True,
        )


# =========================================================
# FOOTER
# =========================================================
st.write("")
st.divider()

st.markdown(
    """
    <div class="foot">
        <strong>SmokeScreen</strong> is an educational machine-learning
        prototype. It supports a follow-up screening conversation and does
        not replace direct confirmation, clinical judgement or professional
        advice. The model score is not a calibrated medical probability.
    </div>
    """,
    unsafe_allow_html=True,
)
