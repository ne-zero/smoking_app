# SmokeScreen Streamlit App

SmokeScreen is an interactive Streamlit application that uses a tuned Random Forest model to estimate whether entered health-screening measurements are more similar to smoker or non-smoker records.

## App Purpose

The application is designed as a screening-support prototype for authorised health-screening staff.

It provides:

- a predicted smoking-status class;
- an estimated smoker likelihood;
- input validation;
- user-facing error messages;
- a review of submitted values;
- a clear non-diagnostic disclaimer.

## Files

```text
smoking_app/
├── README.md
├── smoking_app.py
├── requirements.txt
└── .streamlit/
    └── config.toml
```

The app also requires these files from the model-development folder:

```text
Anis_Suhaimi/
├── smoking_random_forest_model.pkl
└── smoking_feature_columns.pkl
```

## Run Locally

### 1. Open the app folder

```powershell
cd path\to\MLDP-C25U02-Apr2026\smoking_app
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Start Streamlit

```powershell
python -m streamlit run smoking_app.py
```

The app normally opens at:

```text
http://localhost:8501
```

## Requirements

The app uses:

- Streamlit
- pandas
- scikit-learn
- joblib

## Input Sections

The form is divided into:

1. Personal and body measurements
2. Screening checks
3. Blood-test measurements
4. Oral-health indicators

## Validation

The app checks for invalid or inconsistent values, including:

- systolic pressure not exceeding relaxation pressure;
- impossible height or weight values;
- invalid cholesterol relationships;
- missing model files.

Errors are shown directly to the user instead of causing the app to crash.

## Deployment

The app can be deployed using Streamlit Community Cloud.

Recommended main file path:

```text
smoking_app/smoking_app.py
```

Before deployment, confirm that GitHub contains:

- `smoking_app.py`
- `requirements.txt`
- `.streamlit/config.toml`
- `smoking_random_forest_model.pkl`
- `smoking_feature_columns.pkl`

## Important Notice

SmokeScreen is an educational machine learning prototype.

Its output is a model estimate and not a diagnosis or confirmation of smoking status.
