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
# Styling — kept fully inside this .py file
# =========================================================
st.markdown(
    """
    <style>
        :root {
            --navy: #0B1F33;
            --blue: #2563EB;
            --blue-2: #3B82F6;
            --teal: #0F766E;
            --mint: #DFF8F2;
            --sky: #EAF2FF;
            --amber: #F59E0B;
            --amber-soft: #FFF7E8;
            --green: #0F9D72;
            --green-soft: #EAFBF5;
            --danger: #C2410C;
            --ink: #172033;
            --muted: #667085;
            --line: #DCE3EC;
            --surface: #FFFFFF;
            --surface-soft: #F8FAFC;
            --page: #F3F6FA;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 2%, rgba(37, 99, 235, 0.12), transparent 26rem),
                radial-gradient(circle at 92% 10%, rgba(15, 118, 110, 0.10), transparent 23rem),
                linear-gradient(180deg, #F8FAFD 0%, var(--page) 100%);
            color: var(--ink);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 1.1rem;
            padding-bottom: 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu, footer {
            visibility: hidden;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 30px;
            padding: 2.7rem 2.8rem;
            margin-bottom: 1.2rem;
            color: white;
            background:
                linear-gradient(135deg, #0B1F33 0%, #183B63 54%, #2563EB 100%);
            box-shadow: 0 24px 62px rgba(15, 35, 63, 0.19);
        }

        .hero::before {
            content: "";
            position: absolute;
            inset: auto -120px -170px auto;
            width: 430px;
            height: 430px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.08);
        }

        .hero::after {
            content: "";
            position: absolute;
            inset: -120px auto auto 58%;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.05);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.45rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.22);
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .hero h1 {
            color: white !important;
            margin: 0;
            max-width: 790px;
            font-size: clamp(2.35rem, 5vw, 4.35rem);
            line-height: 1.02;
            letter-spacing: -0.055em;
        }

        .hero p {
            color: rgba(255,255,255,0.88) !important;
            max-width: 760px;
            margin: 1rem 0 0;
            font-size: 1.07rem;
            line-height: 1.72;
        }

        .metric-card {
            background: rgba(255,255,255,0.98);
            border: 1px solid var(--line);
            border-radius: 19px;
            padding: 1.12rem 1.2rem;
            min-height: 118px;
            box-shadow: 0 10px 28px rgba(15, 35, 63, 0.06);
        }

        .metric-label {
            color: var(--muted) !important;
            font-size: 0.77rem;
            font-weight: 800;
            letter-spacing: 0.075em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--navy) !important;
            margin-top: 0.25rem;
            font-size: 1.85rem;
            font-weight: 850;
            letter-spacing: -0.045em;
        }

        .metric-note {
            color: var(--muted) !important;
            margin-top: 0.25rem;
            font-size: 0.82rem;
            line-height: 1.4;
        }

        .intro-card {
            background: rgba(255,255,255,0.98);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1.25rem 1.35rem;
            box-shadow: 0 12px 34px rgba(15, 35, 63, 0.06);
            min-height: 145px;
        }

        .eyebrow {
            color: var(--blue) !important;
            font-size: 0.75rem;
            font-weight: 850;
            letter-spacing: 0.085em;
            text-transform: uppercase;
            margin-bottom: 0.42rem;
        }

        .intro-title {
            color: var(--navy) !important;
            font-size: 1.2rem;
            font-weight: 850;
            margin-bottom: 0.3rem;
        }

        .intro-copy {
            color: var(--muted) !important;
            line-height: 1.62;
            font-size: 0.93rem;
        }

        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.985);
            border: 1px solid var(--line);
            border-radius: 26px;
            padding: 1.45rem 1.5rem 1.2rem;
            box-shadow: 0 18px 48px rgba(15, 35, 63, 0.08);
        }

        div[data-testid="stTabs"] button {
            color: var(--muted) !important;
            font-weight: 780 !important;
            padding-top: 0.7rem !important;
            padding-bottom: 0.7rem !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--blue) !important;
        }

        label,
        div[data-testid="stWidgetLabel"] p,
        .stMarkdown p,
        .stCaption {
            color: var(--ink) !important;
        }

        .stCaption {
            color: var(--muted) !important;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            background: white !important;
            border-color: #C9D3E0 !important;
            color: var(--ink) !important;
            border-radius: 12px !important;
        }

        input {
            color: var(--ink) !important;
            -webkit-text-fill-color: var(--ink) !important;
        }

        div[data-baseweb="select"] span,
        div[role="radiogroup"] label p {
            color: var(--ink) !important;
        }

        .field-note {
            margin-top: -0.5rem;
            margin-bottom: 0.7rem;
            padding: 0.62rem 0.72rem;
            background: var(--surface-soft);
            border: 1px solid #E6EBF2;
            border-radius: 10px;
            color: var(--muted) !important;
            font-size: 0.80rem;
            line-height: 1.45;
        }

        .section-note {
            background: var(--sky);
            border: 1px solid #CFE0FF;
            color: #244B7A !important;
            border-radius: 14px;
            padding: 0.85rem 1rem;
            font-size: 0.9rem;
            line-height: 1.55;
            margin-bottom: 0.9rem;
        }

        .stFormSubmitButton > button {
            width: 100%;
            min-height: 3.25rem;
            border: none;
            border-radius: 14px;
            color: white !important;
            font-size: 1rem;
            font-weight: 850;
            background: linear-gradient(90deg, #2563EB, #1D4ED8);
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.25);
            transition: 0.18s ease;
        }

        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 16px 34px rgba(37, 99, 235, 0.30);
        }

        .result-card {
            border-radius: 22px;
            padding: 1.45rem 1.55rem;
            border: 1px solid;
            box-shadow: 0 12px 32px rgba(15, 35, 63, 0.07);
            min-height: 188px;
        }

        .result-card h3 {
            margin: 0.25rem 0 0.45rem;
            color: var(--navy) !important;
            font-size: 1.5rem;
            letter-spacing: -0.025em;
        }

        .result-card p {
            color: #3F4E62 !important;
            line-height: 1.6;
            margin: 0;
        }

        .result-smoker {
            background: var(--amber-soft);
            border-color: #F4D7A8;
        }

        .result-nonsmoker {
            background: var(--green-soft);
            border-color: #B8EBD9;
        }

        .confidence-card {
            background: white;
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 1.3rem 1.4rem;
            min-height: 188px;
            box-shadow: 0 12px 32px rgba(15, 35, 63, 0.06);
        }

        .confidence-value {
            color: var(--navy) !important;
            font-size: 2.65rem;
            font-weight: 900;
            letter-spacing: -0.055em;
            margin: 0.15rem 0;
        }

        .status-pill {
            display: inline-flex;
            padding: 0.36rem 0.7rem;
            border-radius: 999px;
            font-size: 0.77rem;
            font-weight: 800;
            margin-top: 0.7rem;
        }

        .status-pill.amber {
            color: #8A4B05;
            background: #FDE7BF;
        }

        .status-pill.green {
            color: #056B4C;
            background: #D7F5E9;
        }

        .footnote {
            color: var(--muted) !important;
            font-size: 0.84rem;
            line-height: 1.6;
        }

        .stAlert {
            border-radius: 14px;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 14px;
            overflow: hidden;
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

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_cards = [
    ("Final model", "Random Forest", "Tuned with 5-fold cross-validation"),
    ("F1-score", "0.7708", "Balance of smoker precision and recall"),
    ("Smoker recall", "79.70%", "Actual smokers identified"),
    ("Test accuracy", "82.60%", "Held-out test-set performance"),
]

for column, (label, value, note) in zip(
    [metric_1, metric_2, metric_3, metric_4],
    metric_cards,
):
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
            'These fields describe the person’s basic demographic and physical measurements.'
            '</div>',
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
            add_description(
                "Age at the time of screening, recorded in years."
            )

        with col2:
            height = st.number_input(
                "Height in centimetres (height(cm))",
                min_value=130,
                max_value=190,
                value=165,
                step=5,
            )
            add_description(
                "Standing height measured in centimetres."
            )

            weight = st.number_input(
                "Weight in kilograms (weight(kg))",
                min_value=30,
                max_value=135,
                value=65,
                step=5,
            )
            add_description(
                "Body weight measured in kilograms."
            )

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

            st.info(
                "Use measurements from the same screening session where possible."
            )

    with screening_tab:
        st.markdown("#### Vision, hearing and blood pressure")
        st.markdown(
            '<div class="section-note">'
            'These fields capture general screening measurements for eyesight, hearing and blood pressure.'
            '</div>',
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
            add_description(
                "Visual-acuity score recorded for the left eye."
            )

            eyesight_right = st.number_input(
                "Right-eye eyesight score (eyesight(right))",
                min_value=0.1,
                max_value=9.9,
                value=1.0,
                step=0.1,
            )
            add_description(
                "Visual-acuity score recorded for the right eye."
            )

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
            'Enter the laboratory values exactly as shown on the health-screening record.'
            '</div>',
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
            add_description(
                "Blood glucose level measured after fasting."
            )

            cholesterol = st.number_input(
                "Total cholesterol (Cholesterol)",
                min_value=55.0,
                max_value=445.0,
                value=195.0,
                step=1.0,
            )
            add_description(
                "Overall cholesterol level recorded in the blood test."
            )

            triglyceride = st.number_input(
                "Triglycerides (triglyceride)",
                min_value=8.0,
                max_value=999.0,
                value=108.0,
                step=1.0,
            )
            add_description(
                "Blood-fat measurement associated with energy storage."
            )

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
            add_description(
                "Enzyme measurement included in liver-function testing."
            )

            alt = st.number_input(
                "Alanine aminotransferase (ALT)",
                min_value=1.0,
                max_value=2914.0,
                value=21.0,
                step=1.0,
            )
            add_description(
                "Liver-enzyme measurement used in routine blood testing."
            )

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
            'The constant oral column was removed during modelling, so only the two variable oral-health features are required.'
            '</div>',
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

        st.info(
            "Review each section before generating the prediction."
        )

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
