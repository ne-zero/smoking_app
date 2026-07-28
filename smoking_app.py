from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="SmokeScreen | Smoking Status Predictor",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------
# Global styles
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        :root {
            --navy: #10233f;
            --blue: #2563eb;
            --blue-dark: #1d4ed8;
            --teal: #0f766e;
            --green: #047857;
            --amber: #b45309;
            --ink: #172033;
            --muted: #64748b;
            --line: #dbe3ee;
            --surface: #ffffff;
            --page: #f4f7fb;
            --soft-blue: #eff6ff;
            --soft-green: #ecfdf5;
            --soft-amber: #fff7ed;
        }

        html, body, [class*="css"] {
            font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                         BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 15% 0%, rgba(37, 99, 235, 0.10), transparent 28rem),
                radial-gradient(circle at 95% 15%, rgba(15, 118, 110, 0.08), transparent 24rem),
                var(--page);
            color: var(--ink);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 1.25rem;
            padding-bottom: 3rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        .hero {
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 2.5rem 2.7rem;
            margin-bottom: 1.2rem;
            color: white;
            background:
                linear-gradient(135deg, rgba(16, 35, 63, 0.98), rgba(29, 78, 216, 0.94));
            box-shadow: 0 24px 60px rgba(15, 35, 63, 0.18);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 330px;
            height: 330px;
            border-radius: 999px;
            right: -110px;
            top: -120px;
            background: rgba(255, 255, 255, 0.10);
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.72rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.13);
            border: 1px solid rgba(255, 255, 255, 0.22);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 1rem;
        }

        .hero h1 {
            color: white !important;
            margin: 0;
            max-width: 780px;
            font-size: clamp(2.2rem, 5vw, 4.1rem);
            line-height: 1.02;
            letter-spacing: -0.045em;
        }

        .hero p {
            color: rgba(255, 255, 255, 0.88) !important;
            margin: 1rem 0 0;
            max-width: 760px;
            font-size: 1.05rem;
            line-height: 1.7;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 8px 24px rgba(30, 64, 175, 0.06);
            min-height: 118px;
        }

        .metric-label {
            color: var(--muted) !important;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .metric-value {
            color: var(--navy) !important;
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.04em;
            margin-top: 0.25rem;
        }

        .metric-note {
            color: var(--muted) !important;
            font-size: 0.83rem;
            margin-top: 0.25rem;
        }

        .panel {
            background: rgba(255, 255, 255, 0.97);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 1.35rem 1.45rem;
            box-shadow: 0 14px 38px rgba(15, 35, 63, 0.07);
        }

        .panel-title {
            color: var(--navy) !important;
            font-size: 1.2rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .panel-copy {
            color: var(--muted) !important;
            font-size: 0.94rem;
            line-height: 1.6;
        }

        .section-kicker {
            color: var(--blue) !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }

        .result-card {
            border-radius: 22px;
            padding: 1.45rem 1.6rem;
            border: 1px solid;
            box-shadow: 0 12px 32px rgba(15, 35, 63, 0.08);
        }

        .result-card h3 {
            margin: 0 0 0.45rem;
            color: var(--navy) !important;
            font-size: 1.45rem;
        }

        .result-card p {
            margin: 0;
            color: #334155 !important;
            line-height: 1.6;
        }

        .result-smoker {
            background: var(--soft-amber);
            border-color: #fed7aa;
        }

        .result-nonsmoker {
            background: var(--soft-green);
            border-color: #a7f3d0;
        }

        .confidence-box {
            background: white;
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1.25rem 1.35rem;
            height: 100%;
        }

        .confidence-number {
            color: var(--navy) !important;
            font-size: 2.45rem;
            font-weight: 850;
            letter-spacing: -0.05em;
            margin: 0.15rem 0;
        }

        .footnote {
            color: var(--muted) !important;
            font-size: 0.85rem;
            line-height: 1.6;
        }

        div[data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid var(--line);
            border-radius: 24px;
            padding: 1.35rem 1.45rem 1.15rem;
            box-shadow: 0 16px 44px rgba(15, 35, 63, 0.08);
        }

        div[data-testid="stTabs"] button {
            color: var(--muted) !important;
            font-weight: 750 !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--blue) !important;
        }

        label,
        .stMarkdown p,
        .stCaption,
        div[data-testid="stWidgetLabel"] p {
            color: var(--ink) !important;
        }

        .stCaption,
        small {
            color: var(--muted) !important;
        }

        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div {
            background: white !important;
            border-color: #cbd5e1 !important;
            color: var(--ink) !important;
            border-radius: 12px !important;
        }

        input {
            color: var(--ink) !important;
            -webkit-text-fill-color: var(--ink) !important;
        }

        div[data-baseweb="select"] span {
            color: var(--ink) !important;
        }

        div[role="radiogroup"] label p {
            color: var(--ink) !important;
        }

        .stFormSubmitButton > button {
            width: 100%;
            min-height: 3.2rem;
            border: none;
            border-radius: 14px;
            color: white !important;
            font-size: 1rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--blue), var(--blue-dark));
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24);
        }

        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(37, 99, 235, 0.30);
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


# ---------------------------------------------------------
# Model loading
# ---------------------------------------------------------
MODEL_FILENAME = "smoking_random_forest_model.pkl"
FEATURE_FILENAME = "smoking_feature_columns.pkl"


def find_model_file(filename: str) -> Path | None:
    app_folder = Path(__file__).resolve().parent
    repository_folder = app_folder.parent

    possible_locations = [
        app_folder / filename,
        repository_folder / "Anis_Suhaimi" / filename,
        repository_folder / "anis" / filename,
        repository_folder / "Anis" / filename,
    ]

    for path in possible_locations:
        if path.exists():
            return path

    return None


@st.cache_resource
def load_model_files():
    model_path = find_model_file(MODEL_FILENAME)
    feature_path = find_model_file(FEATURE_FILENAME)

    if model_path is None or feature_path is None:
        missing = []

        if model_path is None:
            missing.append(MODEL_FILENAME)

        if feature_path is None:
            missing.append(FEATURE_FILENAME)

        raise FileNotFoundError(
            "Missing required file(s): "
            + ", ".join(missing)
            + ". Place them beside this app or inside the Anis_Suhaimi folder."
        )

    loaded_model = joblib.load(model_path)
    loaded_columns = joblib.load(feature_path)

    if not hasattr(loaded_model, "predict"):
        raise TypeError("The saved model is not a valid fitted classifier.")

    if not hasattr(loaded_model, "predict_proba"):
        raise TypeError("The saved model does not support probability estimates.")

    if not isinstance(loaded_columns, list) or not loaded_columns:
        raise TypeError("The feature-column file is invalid.")

    return loaded_model, loaded_columns


try:
    model, feature_columns = load_model_files()
except Exception as error:
    st.error("The prediction model could not be loaded.")
    st.code(str(error))
    st.info(
        "Run the final notebook cells to create the model and feature-column files, "
        "then place both .pkl files in the app folder or Anis_Suhaimi folder."
    )
    st.stop()


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
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
            "Systolic blood pressure must be higher than relaxation "
            "(diastolic) blood pressure."
        )

    if values["HDL"] > values["Cholesterol"]:
        errors.append(
            "HDL cannot be greater than total cholesterol. "
            "Please check the laboratory values."
        )

    if values["height(cm)"] <= 0 or values["weight(kg)"] <= 0:
        errors.append("Height and weight must be greater than zero.")

    return errors


def binary_value(answer: str) -> int:
    return 1 if answer == "Yes" else 0


def model_label(value: int) -> str:
    return "Smoker" if value == 1 else "Non-smoker"


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    """
    <section class="hero">
        <div class="hero-badge">🫁 HEALTH-SCREENING SUPPORT</div>
        <h1>Smoking status insights, built for clearer follow-up.</h1>
        <p>
            Enter health-screening measurements to receive a transparent
            Random Forest prediction, confidence estimate and clear next-step guidance.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

with metric_1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Final model</div>
            <div class="metric-value">Random Forest</div>
            <div class="metric-note">Tuned using 5-fold validation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric_2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">F1-score</div>
            <div class="metric-value">0.7708</div>
            <div class="metric-note">Balance of precision and recall</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric_3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Smoker recall</div>
            <div class="metric-value">79.70%</div>
            <div class="metric-note">Actual smokers identified</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with metric_4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-label">Test accuracy</div>
            <div class="metric-value">82.60%</div>
            <div class="metric-note">Held-out test performance</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

intro_left, intro_right = st.columns([1.6, 1])

with intro_left:
    st.markdown(
        """
        <div class="panel">
            <div class="section-kicker">How it works</div>
            <div class="panel-title">Complete four short screening sections</div>
            <div class="panel-copy">
                Use values from the same screening session where possible.
                The app applies the same encoding and feature order used during model training.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with intro_right:
    st.markdown(
        """
        <div class="panel">
            <div class="section-kicker">Important</div>
            <div class="panel-title">Support tool, not a diagnosis</div>
            <div class="panel-copy">
                Results should guide follow-up questions only.
                Direct confirmation and professional judgement remain necessary.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")


# ---------------------------------------------------------
# Prediction form
# ---------------------------------------------------------
with st.form("smoking_prediction_form", clear_on_submit=False):
    st.markdown("### Enter screening details")
    st.caption("All fields are required. Typical dataset values are filled in to help you begin.")

    personal_tab, screening_tab, blood_tab, oral_tab = st.tabs(
        [
            "Personal & body",
            "Screening checks",
            "Blood test",
            "Oral health",
        ]
    )

    with personal_tab:
        st.markdown("#### Personal and body measurements")

        col1, col2, col3 = st.columns(3)

        with col1:
            gender = st.selectbox(
                "Gender",
                ["F", "M"],
                format_func=lambda value: "Female" if value == "F" else "Male",
            )

            age = st.number_input(
                "Age",
                min_value=20,
                max_value=85,
                value=40,
                step=5,
            )

        with col2:
            height = st.number_input(
                "Height (cm)",
                min_value=130,
                max_value=190,
                value=165,
                step=5,
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=30,
                max_value=135,
                value=65,
                step=5,
            )

        with col3:
            waist = st.number_input(
                "Waist measurement (cm)",
                min_value=51.0,
                max_value=129.0,
                value=82.0,
                step=0.5,
            )

            st.info("Use measurements from the same screening session.")

    with screening_tab:
        st.markdown("#### Vision, hearing and blood pressure")

        col1, col2, col3 = st.columns(3)

        with col1:
            eyesight_left = st.number_input(
                "Eyesight — left",
                min_value=0.1,
                max_value=9.9,
                value=1.0,
                step=0.1,
            )

            eyesight_right = st.number_input(
                "Eyesight — right",
                min_value=0.1,
                max_value=9.9,
                value=1.0,
                step=0.1,
            )

        with col2:
            hearing_left = st.selectbox(
                "Hearing — left",
                [1.0, 2.0],
                format_func=lambda value: (
                    "1 — Normal category"
                    if value == 1.0
                    else "2 — Reduced hearing category"
                ),
            )

            hearing_right = st.selectbox(
                "Hearing — right",
                [1.0, 2.0],
                format_func=lambda value: (
                    "1 — Normal category"
                    if value == 1.0
                    else "2 — Reduced hearing category"
                ),
            )

        with col3:
            systolic = st.number_input(
                "Systolic blood pressure",
                min_value=71.0,
                max_value=240.0,
                value=120.0,
                step=1.0,
            )

            relaxation = st.number_input(
                "Relaxation blood pressure",
                min_value=40.0,
                max_value=146.0,
                value=76.0,
                step=1.0,
                help="The dataset's diastolic blood-pressure reading.",
            )

    with blood_tab:
        st.markdown("#### Blood and laboratory measurements")

        col1, col2, col3 = st.columns(3)

        with col1:
            fasting_blood_sugar = st.number_input(
                "Fasting blood sugar",
                min_value=46.0,
                max_value=505.0,
                value=96.0,
                step=1.0,
            )

            cholesterol = st.number_input(
                "Total cholesterol",
                min_value=55.0,
                max_value=445.0,
                value=195.0,
                step=1.0,
            )

            triglyceride = st.number_input(
                "Triglyceride",
                min_value=8.0,
                max_value=999.0,
                value=108.0,
                step=1.0,
            )

            hdl = st.number_input(
                "HDL",
                min_value=4.0,
                max_value=618.0,
                value=55.0,
                step=1.0,
            )

        with col2:
            ldl = st.number_input(
                "LDL",
                min_value=1.0,
                max_value=1860.0,
                value=113.0,
                step=1.0,
            )

            hemoglobin = st.number_input(
                "Haemoglobin",
                min_value=4.9,
                max_value=21.1,
                value=14.8,
                step=0.1,
            )

            urine_protein = st.selectbox(
                "Urine protein category",
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                index=0,
            )

            serum_creatinine = st.number_input(
                "Serum creatinine",
                min_value=0.1,
                max_value=11.6,
                value=0.9,
                step=0.1,
            )

        with col3:
            ast = st.number_input(
                "AST",
                min_value=6.0,
                max_value=1311.0,
                value=23.0,
                step=1.0,
            )

            alt = st.number_input(
                "ALT",
                min_value=1.0,
                max_value=2914.0,
                value=21.0,
                step=1.0,
            )

            gtp = st.number_input(
                "Gtp",
                min_value=1.0,
                max_value=999.0,
                value=25.0,
                step=1.0,
            )

            st.caption("Enter the exact values from the screening record.")

    with oral_tab:
        st.markdown("#### Oral-health indicators")

        col1, col2 = st.columns(2)

        with col1:
            dental_caries_answer = st.radio(
                "Dental caries present?",
                ["No", "Yes"],
                horizontal=True,
            )

        with col2:
            tartar = st.radio(
                "Tartar present?",
                ["N", "Y"],
                format_func=lambda value: "No" if value == "N" else "Yes",
                horizontal=True,
            )

        st.info(
            "The constant oral column was removed during modelling, "
            "so only dental caries and tartar are needed."
        )

    submitted = st.form_submit_button(
        "Generate prediction",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------
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
        st.error("Please correct the following before predicting:")

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
                            <div class="section-kicker">Model classification</div>
                            <h3>Smoker pattern detected</h3>
                            <p>
                                The entered measurements are more similar to records
                                classified as smokers by the trained model.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="result-card result-nonsmoker">
                            <div class="section-kicker">Model classification</div>
                            <h3>Non-smoker pattern detected</h3>
                            <p>
                                The entered measurements are more similar to records
                                classified as non-smokers by the trained model.
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with probability_col:
                st.markdown(
                    f"""
                    <div class="confidence-box">
                        <div class="metric-label">Estimated smoker likelihood</div>
                        <div class="confidence-number">{smoker_probability * 100:.1f}%</div>
                        <div class="metric-note">
                            Model estimate based on the entered measurements
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.progress(smoker_probability)

            if prediction == 1:
                st.warning(
                    "Suggested action: confirm smoking status directly and consider "
                    "an appropriate follow-up conversation."
                )
            else:
                st.info(
                    "A non-smoker prediction does not confirm that the person does not smoke. "
                    "Direct confirmation remains necessary."
                )

            with st.expander("Review submitted inputs"):
                review_table = pd.DataFrame(
                    {
                        "Input": list(input_values.keys()),
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


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.write("")
st.divider()

footer_left, footer_right = st.columns([1.6, 1])

with footer_left:
    st.markdown(
        """
        <div class="footnote">
            <strong>SmokeScreen</strong> is an educational machine-learning prototype.
            It supports screening conversations and does not replace direct confirmation
            or professional judgement.
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
