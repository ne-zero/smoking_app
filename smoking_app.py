from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# =========================================================
# Page setup
# =========================================================
st.set_page_config(
    page_title="SmokeScreen | Smoking Status Support",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Styling — all design stays inside this .py file
# =========================================================
st.markdown(
    """
    <style>
        :root {
            --navy-950: #071829;
            --navy-900: #0B1F33;
            --navy-800: #12375E;
            --blue-600: #2563EB;
            --blue-500: #3B82F6;
            --blue-100: #DBEAFE;
            --blue-50: #EFF6FF;
            --teal-700: #0F766E;
            --green-700: #047857;
            --green-100: #D1FAE5;
            --green-50: #ECFDF5;
            --amber-700: #B45309;
            --amber-100: #FDE7BF;
            --amber-50: #FFF7ED;
            --slate-950: #0F172A;
            --slate-900: #172033;
            --slate-700: #334155;
            --slate-600: #475569;
            --slate-500: #64748B;
            --slate-400: #94A3B8;
            --slate-300: #CBD5E1;
            --slate-200: #E2E8F0;
            --slate-100: #F1F5F9;
            --slate-50: #F8FAFC;
            --white: #FFFFFF;
        }

        html {
            color-scheme: light !important;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        body, .stApp {
            background:
                radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.11), transparent 27rem),
                radial-gradient(circle at 95% 8%, rgba(15, 118, 110, 0.08), transparent 22rem),
                linear-gradient(180deg, #FAFCFF 0%, #F3F6FA 100%);
            color: var(--slate-900) !important;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1rem;
            padding-bottom: 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        /* ---------- Hero ---------- */
        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 30px;
            padding: 2.35rem 2.55rem;
            margin-bottom: 1rem;
            background:
                linear-gradient(135deg, #071829 0%, #10345A 55%, #2563EB 100%);
            box-shadow: 0 24px 58px rgba(11, 31, 51, 0.20);
        }

        .hero::before {
            content: "";
            position: absolute;
            top: -120px;
            right: 12%;
            width: 260px;
            height: 260px;
            border-radius: 999px;
            background: rgba(255,255,255,0.07);
        }

        .hero::after {
            content: "";
            position: absolute;
            right: -80px;
            bottom: -150px;
            width: 380px;
            height: 380px;
            border-radius: 999px;
            background: rgba(255,255,255,0.09);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.78rem;
            margin-bottom: 1rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.22);
            color: #FFFFFF !important;
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0.07em;
            text-transform: uppercase;
        }

        .hero h1,
        .hero h2,
        .hero h3,
        .hero p,
        .hero span,
        .hero div {
            color: #FFFFFF !important;
        }

        .hero h1 {
            position: relative;
            z-index: 2;
            margin: 0;
            max-width: 760px;
            font-size: clamp(2.4rem, 5vw, 4.15rem);
            line-height: 1.03;
            letter-spacing: -0.055em;
            font-weight: 900;
        }

        .hero p {
            position: relative;
            z-index: 2;
            margin: 1rem 0 0;
            max-width: 760px;
            font-size: 1.03rem;
            line-height: 1.72;
            opacity: 0.92;
        }

        /* ---------- Summary cards ---------- */
        .metric-card {
            min-height: 112px;
            padding: 1.05rem 1.1rem;
            border: 1px solid var(--slate-200);
            border-radius: 18px;
            background: rgba(255,255,255,0.98);
            box-shadow: 0 10px 28px rgba(15, 35, 63, 0.06);
        }

        .metric-label {
            color: var(--slate-500) !important;
            font-size: 0.75rem;
            font-weight: 850;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .metric-value {
            margin-top: 0.24rem;
            color: var(--navy-900) !important;
            font-size: 1.78rem;
            font-weight: 900;
            letter-spacing: -0.045em;
        }

        .metric-note {
            margin-top: 0.25rem;
            color: var(--slate-500) !important;
            font-size: 0.81rem;
            line-height: 1.42;
        }

        .intro-card {
            min-height: 135px;
            padding: 1.2rem 1.3rem;
            border: 1px solid var(--slate-200);
            border-radius: 20px;
            background: rgba(255,255,255,0.98);
            box-shadow: 0 12px 34px rgba(15, 35, 63, 0.06);
        }

        .eyebrow {
            margin-bottom: 0.38rem;
            color: var(--blue-600) !important;
            font-size: 0.74rem;
            font-weight: 850;
            letter-spacing: 0.085em;
            text-transform: uppercase;
        }

        .intro-title {
            margin-bottom: 0.3rem;
            color: var(--navy-900) !important;
            font-size: 1.16rem;
            font-weight: 850;
        }

        .intro-copy {
            color: var(--slate-500) !important;
            font-size: 0.92rem;
            line-height: 1.62;
        }

        /* ---------- Form ---------- */
        div[data-testid="stForm"] {
            padding: 1.45rem 1.5rem 1.2rem;
            border: 1px solid var(--slate-200);
            border-radius: 26px;
            background: rgba(255,255,255,0.99);
            box-shadow: 0 18px 48px rgba(15, 35, 63, 0.08);
        }

        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4 {
            color: var(--navy-900) !important;
            letter-spacing: -0.025em;
        }

        .stMarkdown p,
        .stCaption,
        label,
        div[data-testid="stWidgetLabel"] p {
            color: var(--slate-900) !important;
        }

        .stCaption {
            color: var(--slate-500) !important;
        }

        .section-note {
            margin-bottom: 1rem;
            padding: 0.82rem 0.95rem;
            border: 1px solid #CFE0FF;
            border-radius: 14px;
            background: var(--blue-50);
            color: #244B7A !important;
            font-size: 0.9rem;
            line-height: 1.55;
        }

        .field-note {
            margin-top: -0.45rem;
            margin-bottom: 0.72rem;
            padding: 0.58rem 0.68rem;
            border: 1px solid #E6EBF2;
            border-radius: 10px;
            background: var(--slate-50);
            color: var(--slate-500) !important;
            font-size: 0.79rem;
            line-height: 1.43;
        }

        /* ---------- Tabs ---------- */
        div[data-testid="stTabs"] button {
            color: var(--slate-500) !important;
            font-weight: 760 !important;
            padding-top: 0.7rem !important;
            padding-bottom: 0.7rem !important;
        }

        div[data-testid="stTabs"] button p,
        div[data-testid="stTabs"] button span {
            color: inherit !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--blue-600) !important;
        }

        div[data-testid="stTabs"] button[aria-selected="false"] {
            color: var(--slate-500) !important;
            opacity: 1 !important;
        }

        /* ---------- Inputs: force readable light mode ---------- */
        div[data-baseweb="input"],
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="textarea"] > div {
            background: #FFFFFF !important;
            border-color: var(--slate-300) !important;
            color: var(--slate-950) !important;
            border-radius: 12px !important;
        }

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--blue-500) !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
        }

        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input,
        textarea,
        input {
            background: transparent !important;
            color: var(--slate-950) !important;
            -webkit-text-fill-color: var(--slate-950) !important;
            caret-color: var(--blue-600) !important;
            opacity: 1 !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        div[role="listbox"] span,
        div[role="option"] {
            color: var(--slate-950) !important;
        }

        div[role="listbox"] {
            background: #FFFFFF !important;
        }

        div[data-baseweb="input"] button,
        div[data-baseweb="base-input"] button {
            background: var(--slate-50) !important;
            color: var(--slate-600) !important;
            border-left: 1px solid var(--slate-200) !important;
        }

        div[data-baseweb="input"] button svg,
        div[data-baseweb="base-input"] button svg,
        div[data-baseweb="select"] svg {
            fill: var(--slate-600) !important;
            color: var(--slate-600) !important;
        }

        div[role="radiogroup"] label,
        div[role="radiogroup"] label p,
        div[role="radiogroup"] label span {
            color: var(--slate-900) !important;
        }

        /* ---------- Submit button ---------- */
        .stFormSubmitButton > button {
            width: 100%;
            min-height: 3.25rem;
            border: none;
            border-radius: 14px;
            background: linear-gradient(90deg, #2563EB, #1D4ED8);
            color: #FFFFFF !important;
            font-size: 1rem;
            font-weight: 850;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.25);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(37, 99, 235, 0.30);
        }

        .stFormSubmitButton > button p {
            color: #FFFFFF !important;
        }

        /* ---------- Results ---------- */
        .result-card {
            min-height: 185px;
            padding: 1.45rem 1.55rem;
            border: 1px solid;
            border-radius: 22px;
            box-shadow: 0 12px 32px rgba(15, 35, 63, 0.07);
        }

        .result-card h3 {
            margin: 0.25rem 0 0.45rem;
            color: var(--navy-900) !important;
            font-size: 1.46rem;
            letter-spacing: -0.025em;
        }

        .result-card p {
            margin: 0;
            color: var(--slate-700) !important;
            line-height: 1.6;
        }

        .result-smoker {
            background: var(--amber-50);
            border-color: #F4D7A8;
        }

        .result-nonsmoker {
            background: var(--green-50);
            border-color: #B8EBD9;
        }

        .confidence-card {
            min-height: 185px;
            padding: 1.3rem 1.4rem;
            border: 1px solid var(--slate-200);
            border-radius: 22px;
            background: #FFFFFF;
            box-shadow: 0 12px 32px rgba(15, 35, 63, 0.06);
        }

        .confidence-value {
            margin: 0.15rem 0;
            color: var(--navy-900) !important;
            font-size: 2.58rem;
            font-weight: 900;
            letter-spacing: -0.055em;
        }

        .status-pill {
            display: inline-flex;
            margin-top: 0.72rem;
            padding: 0.36rem 0.7rem;
            border-radius: 999px;
            font-size: 0.77rem;
            font-weight: 800;
        }

        .status-pill.amber {
            background: var(--amber-100);
            color: #8A4B05 !important;
        }

        .status-pill.green {
            background: var(--green-100);
            color: #056B4C !important;
        }

        .footnote {
            color: var(--slate-500) !important;
            font-size: 0.84rem;
            line-height: 1.6;
        }

        .stAlert {
            border-radius: 14px;
        }

        div[data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid var(--slate-200);
            border-radius: 14px;
        }

        @media (max-width: 760px) {
            .hero {
                padding: 1.8rem 1.35rem;
                border-radius: 22px;
            }

            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Model loading
# =========================================================
APP_FOLDER = Path(__file__).resolve().parent
MODEL_PATH = APP_FOLDER / "smoking_random_forest_model.pkl"
FEATURE_PATH = APP_FOLDER / "smoking_feature_columns.pkl"


@st.cache_resource
def load_model_files():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing model file: {MODEL_PATH.name}. "
            "Place it in the same folder as this app."
        )

    if not FEATURE_PATH.exists():
        raise FileNotFoundError(
            f"Missing feature file: {FEATURE_PATH.name}. "
            "Place it in the same folder as this app."
        )

    loaded_model = joblib.load(MODEL_PATH)
    loaded_columns = joblib.load(FEATURE_PATH)

    if not hasattr(loaded_model, "predict"):
        raise TypeError("The saved file is not a fitted prediction model.")

    if not hasattr(loaded_model, "predict_proba"):
        raise TypeError("The saved model does not support probability estimates.")

    if not isinstance(loaded_columns, list) or not loaded_columns:
        raise TypeError("The saved feature-column file is invalid.")

    return loaded_model, loaded_columns


try:
    model, feature_columns = load_model_files()
except Exception as error:
    st.error("The prediction system could not be loaded.")
    st.code(str(error))
    st.info(
        "Place both .pkl files in the same folder as smoking_app.py, "
        "then restart the app."
    )
    st.stop()


# =========================================================
# Helpers
# =========================================================
def build_model_input(values: dict) -> pd.DataFrame:
    raw_input = pd.DataFrame([values])

    encoded_input = pd.get_dummies(
        raw_input,
        columns=["gender", "tartar"],
        drop_first=False,
        dtype=int,
    )

    return encoded_input.reindex(
        columns=feature_columns,
        fill_value=0,
    )


def validate_inputs(values: dict) -> list[str]:
    errors = []

    if values["systolic"] <= values["relaxation"]:
        errors.append(
            "Systolic blood pressure must be higher than "
            "relaxation (diastolic) blood pressure."
        )

    if values["HDL"] > values["Cholesterol"]:
        errors.append(
            "HDL cannot be greater than total cholesterol. "
            "Please review both values."
        )

    if values["height(cm)"] <= 0 or values["weight(kg)"] <= 0:
        errors.append("Height and weight must be greater than zero.")

    return errors


def binary_value(answer: str) -> int:
    return 1 if answer == "Yes" else 0


def add_description(text: str) -> None:
    st.markdown(
        f'<div class="field-note">{text}</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# Header
# =========================================================
st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">🫁 Screening-support prototype</div>
        <h1>Clearer smoking-status insights from routine screening data.</h1>
        <p>
            Enter one person's screening measurements to receive a transparent
            Random Forest classification, an estimated smoker likelihood and
            practical follow-up guidance.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_columns = st.columns(4)
metric_cards = [
    ("Final model", "Random Forest", "Tuned with 5-fold cross-validation"),
    ("F1-score", "0.7708", "Balance of smoker precision and recall"),
    ("Smoker recall", "79.70%", "Actual smokers identified"),
    ("Test accuracy", "82.60%", "Held-out test-set performance"),
]

for column, (label, value, note) in zip(metric_columns, metric_cards):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")

intro_left, intro_right = st.columns([1.55, 1])

with intro_left:
    st.markdown(
        """
        <div class="intro-card">
            <div class="eyebrow">How it works</div>
            <div class="intro-title">Complete four focused sections</div>
            <div class="intro-copy">
                Enter measurements from the same screening session where possible.
                Every field maps to a feature used by the trained model.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with intro_right:
    st.markdown(
        """
        <div class="intro-card">
            <div class="eyebrow">Important</div>
            <div class="intro-title">Support tool, not a diagnosis</div>
            <div class="intro-copy">
                The result identifies statistical patterns only.
                Direct confirmation and professional judgement remain necessary.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")


# =========================================================
# Prediction form
# =========================================================
with st.form("smoking_prediction_form", clear_on_submit=False):
    st.markdown("### Enter screening details")
    st.caption(
        "Typical values are pre-filled so the form can be tested immediately. "
        "Replace them with actual screening values for a real demonstration."
    )

    personal_tab, screening_tab, blood_tab, oral_tab = st.tabs(
        [
            "1. Personal & body",
            "2. Screening checks",
            "3. Blood tests",
            "4. Oral health",
        ]
    )

    with personal_tab:
        st.markdown("#### Personal and body measurements")
        st.markdown(
            '<div class="section-note">'
            "These fields describe the person's basic demographic and physical measurements."
            "</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox(
                "Gender (gender)",
                ["F", "M"],
                format_func=lambda value: "Female" if value == "F" else "Male",
                help="Sex category recorded in the original dataset.",
            )
            add_description(
                "Recorded sex category used by the model after one-hot encoding."
            )

            age = st.number_input(
                "Age in years (age)",
                min_value=20,
                max_value=85,
                value=40,
                step=5,
            )
            add_description("Age at the time of screening, recorded in years.")

        with col2:
            height = st.number_input(
                "Height in centimetres (height(cm))",
                min_value=130,
                max_value=190,
                value=165,
                step=5,
            )
            add_description("Standing height measured in centimetres.")

            weight = st.number_input(
                "Weight in kilograms (weight(kg))",
                min_value=30,
                max_value=135,
                value=65,
                step=5,
            )
            add_description("Body weight measured in kilograms.")

        with col3:
            waist = st.number_input(
                "Waist circumference in centimetres (waist(cm))",
                min_value=51.0,
                max_value=129.0,
                value=82.0,
                step=0.5,
            )
            add_description(
                "Waist measurement taken around the abdomen in centimetres."
            )

            st.info("Use measurements from the same screening session where possible.")

    with screening_tab:
        st.markdown("#### Vision, hearing and blood pressure")
        st.markdown(
            '<div class="section-note">'
            "These fields capture eyesight, hearing and blood-pressure measurements."
            "</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            eyesight_left = st.number_input(
                "Left-eye eyesight score (eyesight(left))",
                min_value=0.1,
                max_value=9.9,
                value=1.0,
                step=0.1,
            )
            add_description("Visual-acuity score recorded for the left eye.")

            eyesight_right = st.number_input(
                "Right-eye eyesight score (eyesight(right))",
                min_value=0.1,
                max_value=9.9,
                value=1.0,
                step=0.1,
            )
            add_description("Visual-acuity score recorded for the right eye.")

        with col2:
            hearing_left = st.selectbox(
                "Left-ear hearing category (hearing(left))",
                [1.0, 2.0],
                format_func=lambda value: (
                    "1 — Normal hearing category"
                    if value == 1.0
                    else "2 — Reduced hearing category"
                ),
            )
            add_description(
                "Dataset category for the left ear: 1 is normal and 2 indicates reduced hearing."
            )

            hearing_right = st.selectbox(
                "Right-ear hearing category (hearing(right))",
                [1.0, 2.0],
                format_func=lambda value: (
                    "1 — Normal hearing category"
                    if value == 1.0
                    else "2 — Reduced hearing category"
                ),
            )
            add_description(
                "Dataset category for the right ear: 1 is normal and 2 indicates reduced hearing."
            )

        with col3:
            systolic = st.number_input(
                "Systolic blood pressure (systolic)",
                min_value=71.0,
                max_value=240.0,
                value=120.0,
                step=1.0,
            )
            add_description(
                "Upper blood-pressure reading measured when the heart contracts."
            )

            relaxation = st.number_input(
                "Diastolic / relaxation blood pressure (relaxation)",
                min_value=40.0,
                max_value=146.0,
                value=76.0,
                step=1.0,
            )
            add_description(
                "Lower blood-pressure reading measured when the heart relaxes."
            )

    with blood_tab:
        st.markdown("#### Blood and laboratory measurements")
        st.markdown(
            '<div class="section-note">'
            "Enter the laboratory values exactly as shown on the health-screening record."
            "</div>",
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            fasting_blood_sugar = st.number_input(
                "Fasting blood glucose (fasting blood sugar)",
                min_value=46.0,
                max_value=505.0,
                value=96.0,
                step=1.0,
            )
            add_description("Blood glucose level measured after fasting.")

            cholesterol = st.number_input(
                "Total cholesterol (Cholesterol)",
                min_value=55.0,
                max_value=445.0,
                value=195.0,
                step=1.0,
            )
            add_description("Overall cholesterol level recorded in the blood test.")

            triglyceride = st.number_input(
                "Triglycerides (triglyceride)",
                min_value=8.0,
                max_value=999.0,
                value=108.0,
                step=1.0,
            )
            add_description("Blood-fat measurement associated with energy storage.")

            hdl = st.number_input(
                "High-density lipoprotein cholesterol (HDL)",
                min_value=4.0,
                max_value=618.0,
                value=55.0,
                step=1.0,
            )
            add_description(
                "HDL is commonly described as the protective or 'good' cholesterol fraction."
            )

        with col2:
            ldl = st.number_input(
                "Low-density lipoprotein cholesterol (LDL)",
                min_value=1.0,
                max_value=1860.0,
                value=113.0,
                step=1.0,
            )
            add_description(
                "LDL is commonly described as the 'bad' cholesterol fraction."
            )

            hemoglobin = st.number_input(
                "Haemoglobin concentration (hemoglobin)",
                min_value=4.9,
                max_value=21.1,
                value=14.8,
                step=0.1,
            )
            add_description(
                "Protein concentration in red blood cells that carries oxygen."
            )

            urine_protein = st.selectbox(
                "Urine protein category (Urine protein)",
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                index=0,
            )
            add_description(
                "Ordinal category indicating the recorded urine-protein level."
            )

            serum_creatinine = st.number_input(
                "Serum creatinine (serum creatinine)",
                min_value=0.1,
                max_value=11.6,
                value=0.9,
                step=0.1,
            )
            add_description(
                "Waste-product measurement commonly used in kidney-function screening."
            )

        with col3:
            ast = st.number_input(
                "Aspartate aminotransferase (AST)",
                min_value=6.0,
                max_value=1311.0,
                value=23.0,
                step=1.0,
            )
            add_description("Enzyme measurement included in liver-function testing.")

            alt = st.number_input(
                "Alanine aminotransferase (ALT)",
                min_value=1.0,
                max_value=2914.0,
                value=21.0,
                step=1.0,
            )
            add_description("Liver-enzyme measurement used in routine blood testing.")

            gtp = st.number_input(
                "Gamma-glutamyl transferase (Gtp)",
                min_value=1.0,
                max_value=999.0,
                value=25.0,
                step=1.0,
            )
            add_description(
                "Enzyme measurement often associated with liver and bile-duct activity."
            )

    with oral_tab:
        st.markdown("#### Oral-health indicators")
        st.markdown(
            '<div class="section-note">'
            "The constant oral column was removed during modelling, so only the two variable oral-health features are required."
            "</div>",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            dental_caries_answer = st.radio(
                "Dental caries present? (dental caries)",
                ["No", "Yes"],
                horizontal=True,
            )
            add_description(
                "Indicates whether tooth decay was recorded during screening."
            )

        with col2:
            tartar = st.radio(
                "Tartar present? (tartar)",
                ["N", "Y"],
                format_func=lambda value: "No" if value == "N" else "Yes",
                horizontal=True,
            )
            add_description(
                "Indicates whether hardened dental plaque was recorded."
            )

        st.info("Review each section before generating the prediction.")

    submitted = st.form_submit_button(
        "Generate smoking-status prediction",
        type="primary",
        use_container_width=True,
    )


# =========================================================
# Prediction results
# =========================================================
if submitted:
    input_values = {
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
        "fasting blood sugar": fasting_blood_sugar,
        "Cholesterol": cholesterol,
        "triglyceride": triglyceride,
        "HDL": hdl,
        "LDL": ldl,
        "hemoglobin": hemoglobin,
        "Urine protein": urine_protein,
        "serum creatinine": serum_creatinine,
        "AST": ast,
        "ALT": alt,
        "Gtp": gtp,
        "dental caries": binary_value(dental_caries_answer),
        "tartar": tartar,
    }

    errors = validate_inputs(input_values)

    if errors:
        st.error("Please correct the following input issue(s):")
        for error in errors:
            st.write(f"- {error}")
    else:
        try:
            model_input = build_model_input(input_values)

            prediction = int(model.predict(model_input)[0])
            smoker_probability = float(model.predict_proba(model_input)[0][1])

            st.write("")
            st.markdown("## Prediction result")

            result_col, probability_col = st.columns([1.55, 1])

            with result_col:
                if prediction == 1:
                    st.markdown(
                        """
                        <div class="result-card result-smoker">
                            <div class="eyebrow">Model classification</div>
                            <h3>Smoker pattern detected</h3>
                            <p>
                                The submitted measurements are more similar to records
                                classified as smokers by the trained Random Forest.
                            </p>
                            <span class="status-pill amber">Follow-up recommended</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="result-card result-nonsmoker">
                            <div class="eyebrow">Model classification</div>
                            <h3>Non-smoker pattern detected</h3>
                            <p>
                                The submitted measurements are more similar to records
                                classified as non-smokers by the trained Random Forest.
                            </p>
                            <span class="status-pill green">Lower smoker-pattern score</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with probability_col:
                st.markdown(
                    f"""
                    <div class="confidence-card">
                        <div class="metric-label">Estimated smoker likelihood</div>
                        <div class="confidence-value">{smoker_probability * 100:.1f}%</div>
                        <div class="metric-note">
                            Model estimate based on the submitted screening values
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.progress(smoker_probability)

            if prediction == 1:
                st.warning(
                    "Suggested next step: confirm smoking status directly and "
                    "consider an appropriate follow-up conversation."
                )
            else:
                st.info(
                    "A non-smoker prediction does not prove that the person does not smoke. "
                    "Direct confirmation remains necessary."
                )

            with st.expander("Review submitted inputs"):
                review_table = pd.DataFrame(
                    {
                        "Feature": list(input_values.keys()),
                        "Entered value": list(input_values.values()),
                    }
                )

                st.dataframe(
                    review_table,
                    use_container_width=True,
                    hide_index=True,
                )

            st.success("Prediction completed successfully.")

        except Exception as error:
            st.error(
                "The prediction could not be completed. "
                "Please review the values and try again."
            )

            with st.expander("Technical details"):
                st.code(str(error))


# =========================================================
# Footer
# =========================================================
st.write("")
st.divider()

footer_left, footer_right = st.columns([1.65, 1])

with footer_left:
    st.markdown(
        """
        <div class="footnote">
            <strong>SmokeScreen</strong> is an educational machine-learning prototype.
            It supports screening conversations and does not replace direct confirmation,
            clinical judgement or professional advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

with footer_right:
    st.markdown(
        """
        <div class="footnote" style="text-align:right;">
            Built with Streamlit · Tuned Random Forest
        </div>
        """,
        unsafe_allow_html=True,
    )