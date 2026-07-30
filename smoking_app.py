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

        --bg:#0F172A;
        --bg-deep:#0B1120;
        --bg-soft:#131D33;
        --card:#1E293B;
        --card-2:#1E293B;
        --card-border:#334155;
        --ink:#F1F5F9;
        --ink-soft:#94A3B8;
        --ink-dim:#64748B;
        --line:#334155;
        --line-soft:#243044;

        /* single consistent accent for active controls / tab headers */
        --accent:#F97316;
        --accent-deep:#C2570A;
        --accent-soft:rgba(249,115,22,.14);

        /* semantic red — reserved strictly for critical/BAD states */
        --red:#EF4444;
        --red-soft:rgba(239,68,68,.14);
        --green:#22C55E;
        --green-soft:rgba(34,197,94,.14);
        --amber:#F59E0B;
        --amber-soft:rgba(245,158,11,.14);

        /* kept as aliases so existing rules below don't need renaming */
        --ember:var(--accent);
        --ember-deep:var(--accent-deep);
        --ember-soft:var(--accent-soft);
    }

    html{color-scheme:dark!important}

    html,body,[class*="css"]{
        font-family:var(--font-sans);
    }

    .stApp{
        background:var(--bg);
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

    /* NOTE: .hero-gauge*/.hero-meta below are unused (real hero is in the components.html iframe, see IMPRESSIVE TOP SECTION). Safe to delete. */
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
        border:1px solid var(--card-border);
        border-radius:12px;
        padding:1.25rem 1.4rem;
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
    /* Plain text label — the field label lives in stWidgetLabel, not one of the option <label> elements below. */
    div[data-testid="stRadio"] div[data-testid="stWidgetLabel"]{
        margin-bottom:.5rem;
    }

    div[data-testid="stRadio"] div[data-testid="stWidgetLabel"] p{
        color:var(--ink-soft)!important;
        font-size:.85rem!important;
        font-weight:600!important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"]{
        gap:.55rem;
    }

    /* Segmented-control pills — selection shown via fill/border, so the native radio dot is hidden below to avoid a doubled-up indicator. */
    div[data-testid="stRadio"] div[role="radiogroup"] label{
        background:var(--card);
        border:1px solid var(--line);
        border-radius:999px;
        padding:.55rem 1.1rem!important;
        margin:0!important;
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked){
        background:var(--ember-soft);
        border-color:rgba(255,122,61,.45);
    }

    div[data-testid="stRadio"] div[role="radiogroup"] label div[data-baseweb="radio"]{
        display:none;
    }

    div[role="radiogroup"] label,
    div[role="radiogroup"] label p{
        color:var(--ink)!important;
    }

    /* ---------- form shell ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"]{
        background:var(--bg-soft);
        border:1px solid var(--card-border)!important;
        border-radius:12px!important;
        padding:.45rem;
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

    /* Small muted caption line under a field card (rendered by desc()). */
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

    /* Accent-colored callout box (feature-priority / Quick-mode cards). */
    .info-box{
        padding:.85rem 1rem;
        border-radius:14px;
        background:var(--ember-soft);
        border:1px solid rgba(249,115,22,.3);
        color:var(--ember)!important;
        font-size:.88rem;
        line-height:1.55;
        margin-bottom:1rem;
    }

    /* Amber callout variant — currently unused, kept for future reuse. */
    .warn-box{
        padding:.85rem 1rem;
        border-radius:14px;
        background:var(--amber-soft);
        border:1px solid rgba(245,158,11,.35);
        color:var(--amber)!important;
        font-size:.88rem;
        line-height:1.55;
    }

    /* st.tabs() styling — accent color for the active tab + underline. */
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

    /* BaseWeb = the component library behind Streamlit's inputs/selects. */
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
        border:1px dashed var(--card-border);
        border-radius:12px;
        background:var(--card);
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
        border:1px solid var(--card-border);
        border-radius:12px;
        background:var(--card);
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

    /* Status pill (not a full-card color) so red stays reserved for critical states. */
    .result-status-pill{
        display:inline-flex;
        align-items:center;
        gap:.4rem;
        padding:.3rem .7rem;
        border-radius:999px;
        font-family:var(--font-mono);
        font-size:.68rem;
        font-weight:700;
        letter-spacing:.05em;
        text-transform:uppercase;
        margin-bottom:.6rem;
    }

    .result-status-pill.is-smoker{
        color:var(--red)!important;
        background:var(--red-soft);
        border:1px solid rgba(239,68,68,.35);
    }

    .result-status-pill.is-nonsmoker{
        color:var(--green)!important;
        background:var(--green-soft);
        border:1px solid rgba(34,197,94,.35);
    }

    /* Whole-card theme that dynamically reflects the predicted risk level */
    .result-card.is-smoker-card{
        border-color:rgba(239,68,68,.55)!important;
        box-shadow:0 0 0 1px rgba(239,68,68,.12),0 0 32px rgba(239,68,68,.18);
    }

    .result-card.is-nonsmoker-card{
        border-color:rgba(34,197,94,.55)!important;
        box-shadow:0 0 0 1px rgba(34,197,94,.12),0 0 32px rgba(34,197,94,.18);
    }

    .result-score{
        margin-top:1.15rem;
        font-family:var(--font-mono);
        font-size:2.85rem;
        font-weight:600;
        color:var(--ink)!important;
    }

    .result-score.is-smoker{color:var(--red)!important}
    .result-score.is-nonsmoker{color:var(--green)!important}

    /* ---------- linear risk bar: 0% (non-smoker) to 100% (smoker) ---------- */
    .risk-bar-wrap{
        margin-top:1.3rem;
    }

    .risk-bar-track{
        position:relative;
        height:10px;
        border-radius:999px;
        background:linear-gradient(90deg,
            var(--green) 0%, var(--amber) 50%, var(--red) 100%);
    }

    .risk-bar-tick{
        position:absolute;
        top:-4px;
        bottom:-4px;
        left:50%;
        width:2px;
        background:rgba(241,245,249,.55);
    }

    .risk-bar-tick-label{
        position:absolute;
        top:14px;
        left:50%;
        transform:translateX(-50%);
        font-family:var(--font-mono);
        font-size:.6rem;
        color:var(--ink-dim)!important;
    }

    .risk-bar-thumb{
        position:absolute;
        top:50%;
        width:16px;
        height:16px;
        border-radius:50%;
        background:#0F172A;
        border:3px solid var(--ink);
        transform:translate(-50%,-50%);
        box-shadow:0 0 0 4px rgba(0,0,0,.28);
    }

    .risk-bar-thumb.is-smoker{border-color:var(--red)}
    .risk-bar-thumb.is-nonsmoker{border-color:var(--green)}

    .risk-bar-labels{
        display:flex;
        justify-content:space-between;
        margin-top:1.4rem;
        font-family:var(--font-mono);
        font-size:.66rem;
        letter-spacing:.03em;
        color:var(--ink-soft)!important;
    }

    /* Small "MODEL SMOKER SCORE" label under the result percentage. */
    .result-caption{
        font-family:var(--font-mono);
        font-size:.69rem;
        letter-spacing:.08em;
        text-transform:uppercase;
        color:var(--ink-soft)!important;
    }

    /* Page footer disclaimer text. */
    .foot{
        font-size:.84rem;
        line-height:1.6;
        color:var(--ink-dim)!important;
    }

    @media(max-width:900px){
        /* .hero-grid/.hero-gauge* are unused; .result-sticky is the real rule. */
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
        color:var(--green)!important;
        background:var(--green-soft);
        border:1px solid rgba(34,197,94,.34);
    }

    .slider-average{
        color:var(--amber)!important;
        background:var(--amber-soft);
        border:1px solid rgba(245,158,11,.34);
    }

    .slider-bad{
        color:var(--red)!important;
        background:var(--red-soft);
        border:1px solid rgba(239,68,68,.34);
    }

    div[data-testid="stSlider"] [data-testid*="TickBar" i]{
        display:none!important;
    }

    /* One accent color for every slider — status comes from the pill badge, not track color. */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child{
        background:var(--line)!important;
    }

    div[data-testid="stSlider"] div[data-baseweb="slider"] > div:nth-child(2){
        background:var(--accent)!important;
    }

    div[data-testid="stSlider"] div[role="slider"]{
        background:var(--accent)!important;
        border-color:var(--accent)!important;
        box-shadow:0 0 0 4px var(--accent-soft)!important;
    }



    /* SINGLE NUMBER INPUT — the one editable value per card. */
    div[data-testid="stNumberInput"]{
        min-width:0!important;
    }

    div[data-testid="stNumberInput"] > div{
        width:100%!important;
    }

    div[data-testid="stNumberInput"] input{
        min-height:2.3rem!important;
        padding:.45rem .4rem!important;
        text-align:center!important;
        font-family:var(--font-mono)!important;
        font-size:.86rem!important;
        font-weight:700!important;
        color:var(--ink)!important;
        -webkit-text-fill-color:var(--ink)!important;
        background:var(--bg-deep)!important;
        border:1px solid var(--card-border)!important;
        border-radius:8px!important;
    }

    div[data-testid="stNumberInput"] button{
        min-width:2rem!important;
        width:2rem!important;
        background:var(--bg-deep)!important;
        border-color:var(--card-border)!important;
    }

    div[data-testid="stNumberInput"] button svg{
        fill:var(--ink)!important;
        color:var(--ink)!important;
    }

    /* Make field descriptions less bulky. */
    .field-note{
        margin-top:-.1rem!important;
        margin-bottom:.75rem!important;
        padding:.46rem .6rem!important;
        font-size:.73rem!important;
    }

    /* Slightly tighten the quick form section. */
    .section-head{
        margin:.25rem 0 .8rem!important;
    }

    /* FIELD CARDS — targets every st.container(key="card_x"/"fc_x") via its auto-added "st-key-<key>" class. */
    div[class*="st-key-card_"],
    div[class*="st-key-fc_"]{
        background:#1E293B!important;
        border:1px solid #334155!important;
        border-radius:8px!important;
        padding:16px!important;
        box-shadow:none!important;
    }

    div[class*="st-key-card_"] div[data-testid="stVerticalBlock"],
    div[class*="st-key-fc_"] div[data-testid="stVerticalBlock"]{
        gap:.5rem;
    }

    .field-card-title{
        font-size:14px;
        font-weight:700;
        color:#ffffff!important;
        line-height:1.3;
        padding-top:.35rem;
    }

    .field-card-title-simple{
        font-size:14px;
        font-weight:700;
        color:#ffffff!important;
        line-height:1.3;
        margin-bottom:.35rem;
    }

    /* Abbreviation in subtle parens next to the full name, e.g. HDL. */
    .field-card-abbr{
        font-size:12px;
        font-weight:500;
        color:var(--ink-soft)!important;
    }

    /* Status & reference row */
    .slider-status-row{
        display:flex;
        align-items:center;
        justify-content:space-between;
        gap:.5rem;
        margin:.3rem 0 0;
    }

    .slider-selected{
        font-family:var(--font-mono);
        font-size:12px;
        color:var(--ink-soft)!important;
    }

    /* Footer note inside a field card */
    div[class*="st-key-card_"] .field-note,
    div[class*="st-key-fc_"] .field-note{
        margin-top:.4rem!important;
        margin-bottom:0!important;
        padding:8px 0 0!important;
        border:none!important;
        background:transparent!important;
        font-size:12px!important;
    }

</style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# MODEL FILES
# =========================================================
# The trained model + the exact column order it was trained on.
APP_FOLDER = Path(__file__).resolve().parent
MODEL_PATH = APP_FOLDER / "smoking_random_forest_model.pkl"
FEATURE_PATH = APP_FOLDER / "smoking_feature_columns.pkl"

# Fallback values for model features Quick Assessment doesn't ask about.
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


# Reference bands for the 3 top-priority lab features (always visible).
PRIORITY_REFERENCE_BANDS = {
    "Gtp": {
        "low": 8.0,
        "high": 61.0,
        "unit": "U/L",
        "direction": "within",
    },
    "hemoglobin": {
        "low": 12.0,
        "high": 17.5,
        "unit": "g/dL",
        "direction": "within",
    },
    "triglyceride": {
        "low": 8.0,
        "high": 149.0,
        "unit": "mg/dL",
        "direction": "within",
    },
}

# Reference bands for the remaining numeric cards ("higher_better"=HDL, "lower_better"=LDL, else within-range).
CLINICAL_BANDS = {
    "fasting": {"low": 70.0, "high": 99.0, "unit": "mg/dL", "direction": "within"},
    "cholesterol": {"low": 125.0, "high": 199.0, "unit": "mg/dL", "direction": "within"},
    "hdl": {"low": 40.0, "high": 60.0, "unit": "mg/dL", "direction": "higher_better"},
    "ldl": {"low": 99.0, "high": 159.0, "unit": "mg/dL", "direction": "lower_better"},
    "creatinine": {"low": 0.6, "high": 1.3, "unit": "mg/dL", "direction": "within"},
    "ast": {"low": 8.0, "high": 40.0, "unit": "U/L", "direction": "within"},
    "alt": {"low": 7.0, "high": 56.0, "unit": "U/L", "direction": "within"},
    "systolic": {"low": 90.0, "high": 119.0, "unit": "mmHg", "direction": "within"},
    "relaxation": {"low": 60.0, "high": 79.0, "unit": "mmHg", "direction": "within"},
}


def bmi_weight_band(height_cm: float) -> dict:
    """Healthy-weight range (BMI 18.5-24.9) for the given height."""
    height_m = height_cm / 100.0
    return {
        "low": round(18.5 * height_m ** 2, 1),
        "high": round(24.9 * height_m ** 2, 1),
        "unit": "kg",
        "direction": "within",
    }


def waist_band(gender: str) -> dict:
    """Standard gender-specific waist circumference thresholds."""
    if gender == "M":
        return {"low": 93.9, "high": 101.9, "unit": "cm", "direction": "lower_better"}
    return {"low": 79.9, "high": 87.9, "unit": "cm", "direction": "lower_better"}


# The 5 highest-importance features — the only inputs in Quick Assessment.
PRIORITY_FEATURES = {
    "gender",
    "Gtp",
    "hemoglobin",
    "triglyceride",
    "height(cm)",
}


@st.cache_resource
def load_files():
    """Load the model + feature-column list once per session (cached)."""
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


# Fail fast and visibly if the model can't load.
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
    """Small muted helper-text line under a field card."""
    st.markdown(
        f'<div class="field-note">{text}</div>',
        unsafe_allow_html=True,
    )


def binary(answer: str) -> int:
    """Convert a Yes/No radio answer into the 0/1 the model expects."""
    return 1 if answer == "Yes" else 0


def clean_label(label: str) -> tuple[str, str]:
    """Split 'Field Name (dataset_var)' into name + trailing parens."""
    if "(" in label and label.endswith(")"):
        head, _, tail = label.rpartition("(")
        return head.strip(), tail[:-1].strip()
    return label, ""


def _is_real_abbreviation(paren: str) -> bool:
    """True only for genuine abbreviations (HDL), not raw dataset vars."""
    return (
        bool(paren)
        and " " not in paren
        and paren[0].isupper()
        and len(paren) <= 6
    )


def field_title_html(label: str, css_class: str) -> str:
    """Card header: full name, with a real abbreviation in subtle parens."""
    clean_name, paren = clean_label(label)

    if _is_real_abbreviation(paren):
        return (
            f'<div class="{css_class}">{clean_name} '
            f'<span class="field-card-abbr">({paren})</span></div>'
        )

    return f'<div class="{css_class}">{clean_name}</div>'


def classify_status(value: float, band: dict) -> tuple[str, str]:
    """Classify a value as Good/Average/Bad per the band's direction."""
    low = band["low"]
    high = band["high"]
    direction = band.get("direction", "within")

    if direction == "higher_better":
        if value >= high:
            return "Good", "slider-good"
        if value >= low:
            return "Average", "slider-average"
        return "Bad", "slider-bad"

    if direction == "lower_better":
        if value <= low:
            return "Good", "slider-good"
        if value <= high:
            return "Average", "slider-average"
        return "Bad", "slider-bad"

    width = max(high - low, 1.0)
    average_low = low - (0.20 * width)
    average_high = high + (0.20 * width)

    if low <= value <= high:
        return "Good", "slider-good"
    if average_low <= value <= average_high:
        return "Average", "slider-average"
    return "Bad", "slider-bad"


def format_value(value: float) -> str:
    """Render a number without a trailing decimal point (999, not 999.00)."""
    text = f"{value:g}"
    return text


def step_format(step, value):
    """Pick a number_input format from the step size (avoids 999.00/999.)."""
    if isinstance(value, int) and isinstance(step, int):
        return None
    return "%.0f" if float(step).is_integer() else "%.1f"


def encode(values: dict) -> pd.DataFrame:
    """Turn the form's values dict into the one-hot-encoded model input."""
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
    """Flag physiologically-odd input combos as warnings (non-blocking)."""
    warnings = []

    if values["systolic"] <= values["relaxation"]:
        warnings.append(
            "Systolic pressure must be higher than diastolic pressure."
        )

    if values["HDL"] > values["Cholesterol"]:
        warnings.append(
            "HDL cannot be greater than total cholesterol."
        )

    return warnings


# Keep each field's slider and number box synced to the same value.
def _sync_slider_to_number(widget_key: str) -> None:
    st.session_state[f"{widget_key}_number"] = st.session_state[
        f"{widget_key}_slider"
    ]


def _sync_number_to_slider(
    widget_key: str,
    minimum: float,
    maximum: float,
) -> None:
    typed_value = st.session_state[f"{widget_key}_number"]
    # Clamp so an out-of-range typed value can't break the slider.
    st.session_state[f"{widget_key}_slider"] = max(
        minimum,
        min(maximum, typed_value),
    )


def clinical_field(
    label: str,
    minimum: float,
    maximum: float,
    default: float,
    step: float,
    key: str,
    note: str,
    band: dict,
) -> float:
    """One field card: title + number input, slider, status row, note."""
    slider_key = f"{key}_slider"
    number_key = f"{key}_number"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default

    if number_key not in st.session_state:
        st.session_state[number_key] = default

    low = band["low"]
    high = band["high"]
    unit = band["unit"]

    with st.container(border=True, key=f"card_{key}"):
        # ---- Header row: full name + abbreviation (left) + single value input (right)
        header_label, header_input = st.columns([2, 1.1], gap="small")

        with header_label:
            st.markdown(
                field_title_html(label, "field-card-title"),
                unsafe_allow_html=True,
            )

        with header_input:
            st.number_input(
                f"{label} exact value",
                min_value=minimum,
                max_value=maximum,
                value=st.session_state[number_key],
                step=step,
                key=number_key,
                format=step_format(step, st.session_state[number_key]),
                label_visibility="collapsed",
                on_change=_sync_number_to_slider,
                args=(key, minimum, maximum),
            )

        # ---- Slider row: full width, no overlaid text
        st.slider(
            label,
            min_value=minimum,
            max_value=maximum,
            value=st.session_state[slider_key],
            step=step,
            key=slider_key,
            label_visibility="collapsed",
            on_change=_sync_slider_to_number,
            args=(key,),
        )

        value = st.session_state[number_key]
        status_text, status_class = classify_status(value, band)

        # Status & reference row (≥X = higher-better, ≤X = lower-better, else a range)
        ref_text = (
            f"Ref: ≥{format_value(high)} {unit}"
            if band.get("direction") == "higher_better"
            else f"Ref: ≤{format_value(high)} {unit}"
            if band.get("direction") == "lower_better"
            else f"Ref: {format_value(low)}–{format_value(high)} {unit}"
        )

        st.markdown(
            (
                '<div class="slider-status-row">'
                f'<span class="slider-selected">{ref_text}</span>'
                f'<span class="slider-status {status_class}">{status_text}</span>'
                '</div>'
            ),
            unsafe_allow_html=True,
        )

        # ---- Footer: secondary description
        desc(note)

    return value


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
    """Backward-compatible wrapper for the 3 top-priority feature cards."""
    return clinical_field(
        label,
        minimum,
        maximum,
        default,
        step,
        key,
        note,
        PRIORITY_REFERENCE_BANDS[feature_name],
    )


def number_field(
    label: str,
    minimum,
    maximum,
    value,
    step,
    key: str,
    note: str | None = None,
):
    """A single number input wrapped in its own field card."""
    with st.container(border=True, key=f"fc_{key}"):
        st.markdown(
            field_title_html(label, "field-card-title-simple"),
            unsafe_allow_html=True,
        )

        result = st.number_input(
            label,
            min_value=minimum,
            max_value=maximum,
            value=value,
            step=step,
            key=key,
            format=step_format(step, value),
            label_visibility="collapsed",
        )

        if note:
            desc(note)

    return result


def select_field(
    label: str,
    options,
    key: str,
    format_func=None,
    note: str | None = None,
):
    """A single selectbox wrapped in its own field card."""
    with st.container(border=True, key=f"fc_{key}"):
        st.markdown(
            field_title_html(label, "field-card-title-simple"),
            unsafe_allow_html=True,
        )

        kwargs = {} if format_func is None else {"format_func": format_func}
        result = st.selectbox(
            label,
            options,
            key=key,
            label_visibility="collapsed",
            **kwargs,
        )

        if note:
            desc(note)

    return result


def radio_field(
    label: str,
    options,
    key: str,
    format_func=None,
    note: str | None = None,
    horizontal: bool = True,
):
    """A single radio control wrapped in its own field card."""
    with st.container(border=True, key=f"fc_{key}"):
        st.markdown(
            field_title_html(label, "field-card-title-simple"),
            unsafe_allow_html=True,
        )

        kwargs = {} if format_func is None else {"format_func": format_func}
        result = st.radio(
            label,
            options,
            key=key,
            horizontal=horizontal,
            label_visibility="collapsed",
            **kwargs,
        )

        if note:
            desc(note)

    return result


def make_prediction(values: dict) -> dict:
    """Run inputs through the model; return predicted class + smoker score."""
    model_input = encode(values)

    predicted_class = int(model.predict(model_input)[0])
    smoker_score = float(model.predict_proba(model_input)[0][1])

    return {
        "class": predicted_class,
        "score": smoker_score,
    }


def render_result_panel(result: dict | None, mode: str) -> None:
    """Draw the sticky result card (placeholder, or themed score + risk bar)."""
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
        score_pct = smoker_score * 100

        if predicted_class == 1:
            st.markdown(
                f'<div class="result-card is-smoker-card">'
                f'<div class="result-status-pill is-smoker">Smoker — High Risk</div>'
                f'<div class="kicker">Model prediction</div>'
                f'<h3>Predicted class: smoker</h3>'
                f'<p>The submitted values are more similar to records '
                f'classified as smokers by the trained Random Forest.</p>'
                f'<div class="result-score is-smoker">{score_pct:.1f}%</div>'
                f'<div class="result-caption">model smoker score</div>'
                f'<div class="risk-bar-wrap">'
                f'<div class="risk-bar-track">'
                f'<div class="risk-bar-tick"></div>'
                f'<div class="risk-bar-tick-label">50%</div>'
                f'<div class="risk-bar-thumb is-smoker" '
                f'style="left:{score_pct:.1f}%;"></div>'
                f'</div>'
                f'<div class="risk-bar-labels">'
                f'<span>0% · Non-smoker</span>'
                f'<span>100% · Smoker</span>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="result-card is-nonsmoker-card">'
                f'<div class="result-status-pill is-nonsmoker">Non-smoker — Low Risk</div>'
                f'<div class="kicker">Model prediction</div>'
                f'<h3>Predicted class: non-smoker</h3>'
                f'<p>The submitted values are more similar to records '
                f'classified as non-smokers by the trained Random Forest.</p>'
                f'<div class="result-score is-nonsmoker">{score_pct:.1f}%</div>'
                f'<div class="result-caption">model smoker score</div>'
                f'<div class="risk-bar-wrap">'
                f'<div class="risk-bar-track">'
                f'<div class="risk-bar-tick"></div>'
                f'<div class="risk-bar-tick-label">50%</div>'
                f'<div class="risk-bar-thumb is-nonsmoker" '
                f'style="left:{score_pct:.1f}%;"></div>'
                f'</div>'
                f'<div class="risk-bar-labels">'
                f'<span>0% · Non-smoker</span>'
                f'<span>100% · Smoker</span>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.write("")

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
def _build_signal_path(period_width: int = 140, periods: int = 8, baseline: int = 34) -> str:
    """Repeating signal-pulse path; drawn 2x wide so -50% translate loops."""
    segments = [f"M0,{baseline}"]
    for i in range(periods):
        x0 = i * period_width
        segments.append(
            f"L{x0+30},{baseline} "
            f"L{x0+42},{baseline-20} "
            f"L{x0+54},{baseline+26} "
            f"L{x0+66},{baseline-6} "
            f"L{x0+78},{baseline} "
            f"L{x0+period_width},{baseline}"
        )
    return " ".join(segments)


_hero_html = """
    <style>
        html, body {
            margin: 0;
            background: transparent;
            overflow: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         Roboto, Helvetica, Arial, sans-serif;
        }

        .hero {
            padding: 42px 16px 36px;
            color: #F1F5F9;
            border-bottom: 1px solid #334155;
        }

        .grid {
            display: flex;
            justify-content: space-between;
            align-items: stretch;
            gap: 32px;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 7px 14px;
            border-radius: 999px;
            color: #F97316;
            background: rgba(249,115,22,.14);
            border: 1px solid rgba(249,115,22,.35);
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
            background: #F97316;
            box-shadow: 0 0 0 3px rgba(249,115,22,.25);
        }

        h1 {
            max-width: 760px;
            margin: 16px 0 0;
            color: #F1F5F9;
            font-family: Georgia, serif;
            font-size: clamp(40px, 5.2vw, 68px);
            line-height: .98;
            letter-spacing: -.035em;
            font-weight: 600;
        }

        h1 em {
            color: #F97316;
            font-weight: 500;
        }

        p {
            max-width: 560px;
            margin: 16px 0 0;
            color: #94A3B8;
            font-size: 16px;
            line-height: 1.7;
        }

        .accuracy-card {
            width: 300px;
            min-width: 260px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 6px;
            padding: 28px 22px;
            border-radius: 20px;
            background: #1E293B;
            border: 1px solid #334155;
            height: 100%;
            box-sizing: border-box;
            text-align: center;
        }

        .accuracy-eyebrow {
            color: #F97316;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .14em;
            text-transform: uppercase;
        }

        .signal-strip {
            width: 100%;
            height: 46px;
            margin: 12px 0 2px;
            overflow: hidden;
            -webkit-mask-image: linear-gradient(90deg,
                transparent 0%, black 14%, black 86%, transparent 100%);
            mask-image: linear-gradient(90deg,
                transparent 0%, black 14%, black 86%, transparent 100%);
        }

        .signal-strip svg {
            display: block;
            width: 100%;
            height: 100%;
        }

        .signal-path {
            fill: none;
            stroke: #F97316;
            stroke-width: 3;
            stroke-linecap: round;
            stroke-linejoin: round;
            filter: drop-shadow(0 0 7px rgba(249,115,22,.8));
            animation: signal-scroll 3.2s linear infinite;
        }

        @keyframes signal-scroll {
            from { transform: translateX(0); }
            to   { transform: translateX(-50%); }
        }

        .stat-value {
            font-family: Consolas, monospace;
            font-size: 76px;
            font-weight: 700;
            line-height: 1;
            color: #F1F5F9;
            letter-spacing: -.02em;
            text-shadow: 0 0 30px rgba(249,115,22,.4);
        }

        .stat-percent {
            font-size: 34px;
            font-weight: 700;
            color: #F97316;
        }

        .stat-caption {
            margin-top: 10px;
            color: #94A3B8;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .14em;
            text-transform: uppercase;
        }

        .accuracy-sub {
            max-width: 240px;
            margin-top: 6px;
            color: #94A3B8;
            font-size: 12.5px;
            line-height: 1.55;
        }

        .meta {
            display: flex;
            flex-wrap: wrap;
            gap: 28px;
            margin-top: 24px;
        }

        .meta-item {
            padding-left: 12px;
            border-left: 2px solid #F97316;
        }

        .meta-label {
            color: #94A3B8;
            font-family: Consolas, monospace;
            font-size: 10px;
            letter-spacing: .1em;
            text-transform: uppercase;
        }

        .meta-value {
            margin-top: 4px;
            color: #F1F5F9;
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

            .accuracy-card {
                width: 100%;
                min-width: 0;
                height: auto;
            }

            .stat-value {
                font-size: 56px;
            }

            .stat-percent {
                font-size: 26px;
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

            <div class="accuracy-card">
                <div class="accuracy-eyebrow">Primary Metric</div>

                <div class="signal-strip">
                    <svg viewBox="0 0 560 60" preserveAspectRatio="none"
                         xmlns="http://www.w3.org/2000/svg">
                        <path class="signal-path" d="__SIGNAL_PATH__"/>
                    </svg>
                </div>

                <div class="stat-value" id="heroStatValue">0<span class="stat-percent">%</span></div>
                <div class="stat-caption">Model accuracy</div>

                <div class="accuracy-sub">
                    Tested on held-out validation data across 5-fold CV.
                </div>
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

    <script>
        (function () {
            var el = document.getElementById('heroStatValue');
            var target = 82.6;
            var duration = 1600;
            var start = null;

            function step(timestamp) {
                if (!start) { start = timestamp; }
                var progress = Math.min((timestamp - start) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                var value = (target * eased).toFixed(1);
                el.innerHTML = value + '<span class="stat-percent">%</span>';
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                }
            }

            window.requestAnimationFrame(step);
        })();
    </script>
    """.replace("__SIGNAL_PATH__", _build_signal_path())

components.html(
    _hero_html,
    height=520,
    scrolling=False,
)


st.write("")
st.write("")

# =========================================================
# INFO CARDS + ASSESSMENT MODE SELECTOR
# =========================================================
# Two explanatory cards + the mode selector radio that picks the form below.
info_left, info_right = st.columns([1.55, 1])

with info_left:
    # Numbered pills listing the 5 PRIORITY_FEATURES, purely for display.
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
    # Drives the if/else below that swaps between Quick and Full Assessment.
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
# Quick Assessment: only the 5 PRIORITY_FEATURES come from the user (rest = REFERENCE_DEFAULTS).
if mode == "Quick Assessment":
    with form_column:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Fast demonstration</div>
                <div class="title">Enter five high-priority inputs</div>
                <div class="copy">
                    This mode asks for the five strongest individual inputs.
                    Remaining features still use reference defaults, so Full
                    Assessment gives the most complete result.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "Quick mode is for demonstration. Full Assessment is recommended "
            "when actual screening values are available."
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
                    300.0,
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
                    500.0,
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
                gender = select_field(
                    "Gender (gender)",
                    ["F", "M"],
                    format_func=lambda value: (
                        "Female" if value == "F" else "Male"
                    ),
                    key="quick_gender",
                    note="Highest-ranked categorical model input.",
                )

            with personal_2:
                height = number_field(
                    "Height in Centimetres",
                    130,
                    190,
                    165,
                    5,
                    key="quick_height",
                    note="Physical measurement with high model importance.",
                )

        # Start from the defaults, then overwrite the 5 user-entered fields.
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

        # No "Predict" button — reruns live on every widget change (validate() only warns, never blocks).
        warnings = validate(quick_values)

        for warning_text in warnings:
            st.warning(warning_text)

        st.session_state.prediction_result = make_prediction(quick_values)
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
# Every model feature is collected directly from the user across 4 tabs.
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
            # All 4 tabs' widgets run every rerun regardless of active tab, so full_values below can safely read every tab's variables.
            priority_tab, screening_tab, blood_tab, oral_tab = st.tabs(
                [
                    "1. Priority inputs",
                    "2. Screening checks",
                    "3. Additional blood tests",
                    "4. Oral health",
                ]
            )

            # Tab 1: the same 5 PRIORITY_FEATURES shown in Quick Assessment.
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
                    gender = select_field(
                        "Gender (gender)",
                        ["F", "M"],
                        format_func=lambda value: (
                            "Female" if value == "F" else "Male"
                        ),
                        key="full_gender",
                        note="Highest-ranked categorical model input.",
                    )

                    height = number_field(
                        "Height in Centimetres",
                        130,
                        190,
                        165,
                        5,
                        key="full_height",
                        note="Standing height measured in centimetres.",
                    )

                with priority_2:
                    gtp = slider_input(
                        "Gtp",
                        "Gamma-glutamyl transferase (Gtp)",
                        1.0,
                        300.0,
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
                        500.0,
                        108.0,
                        1.0,
                        "full_triglyceride",
                        "High-priority blood-fat measurement.",
                    )

                    age = number_field(
                        "Age in years (age)",
                        20,
                        85,
                        40,
                        5,
                        key="full_age",
                        note="Age at the time of screening.",
                    )

            # Tab 2: basic vitals. weight/waist reuse height/gender from priority_tab (safe, see comment above).
            with screening_tab:
                screening_1, screening_2, screening_3 = st.columns(3)

                with screening_1:
                    weight = clinical_field(
                        "Weight in Kilograms",
                        30.0,
                        135.0,
                        65.0,
                        5.0,
                        "full_weight",
                        "Healthy range shown is based on your entered height.",
                        bmi_weight_band(height),
                    )

                    waist = clinical_field(
                        "Waist Circumference",
                        51.0,
                        129.0,
                        82.0,
                        0.5,
                        "full_waist",
                        "Threshold shown reflects standard cardiometabolic "
                        "risk guidance for your selected gender.",
                        waist_band(gender),
                    )

                with screening_2:
                    eyesight_left = number_field(
                        "Left-Eye Eyesight Score",
                        0.1,
                        9.9,
                        1.0,
                        0.1,
                        key="full_eyesight_left",
                    )

                    eyesight_right = number_field(
                        "Right-Eye Eyesight Score",
                        0.1,
                        9.9,
                        1.0,
                        0.1,
                        key="full_eyesight_right",
                    )

                with screening_3:
                    systolic = clinical_field(
                        "Systolic Pressure (systolic)",
                        71.0,
                        240.0,
                        120.0,
                        1.0,
                        "full_systolic",
                        "Pressure in the arteries during a heartbeat.",
                        CLINICAL_BANDS["systolic"],
                    )

                    relaxation = clinical_field(
                        "Diastolic Pressure (relaxation)",
                        40.0,
                        130.0,
                        76.0,
                        1.0,
                        "full_relaxation",
                        "Pressure in the arteries between heartbeats.",
                        CLINICAL_BANDS["relaxation"],
                    )

                st.write("")

                # Own full-width row so L/R hearing sit side by side.
                hearing_left_col, hearing_right_col = st.columns(2)

                with hearing_left_col:
                    hearing_left = select_field(
                        "Left-Ear Hearing",
                        [1.0, 2.0],
                        format_func=lambda value: (
                            "1 — Normal"
                            if value == 1.0
                            else "2 — Reduced"
                        ),
                        key="full_hearing_left",
                    )

                with hearing_right_col:
                    hearing_right = select_field(
                        "Right-Ear Hearing",
                        [1.0, 2.0],
                        format_func=lambda value: (
                            "1 — Normal"
                            if value == 1.0
                            else "2 — Reduced"
                        ),
                        key="full_hearing_right",
                    )

            # Tab 3: remaining lab values, each with a slider + status badge.
            with blood_tab:
                blood_1, blood_2 = st.columns(2)

                with blood_1:
                    fasting = clinical_field(
                        "Fasting Blood Glucose",
                        46.0,
                        505.0,
                        96.0,
                        1.0,
                        "full_fasting",
                        "Blood sugar level after a period without eating.",
                        CLINICAL_BANDS["fasting"],
                    )

                    cholesterol = clinical_field(
                        "Total Cholesterol",
                        55.0,
                        445.0,
                        195.0,
                        1.0,
                        "full_cholesterol",
                        "Combined measurement of blood cholesterol.",
                        CLINICAL_BANDS["cholesterol"],
                    )

                    hdl = clinical_field(
                        "High-Density Lipoprotein (HDL)",
                        4.0,
                        150.0,
                        55.0,
                        1.0,
                        "full_hdl",
                        "\"Good\" cholesterol — higher values are better.",
                        CLINICAL_BANDS["hdl"],
                    )

                    ldl = clinical_field(
                        "Low-Density Lipoprotein (LDL)",
                        1.0,
                        400.0,
                        113.0,
                        1.0,
                        "full_ldl",
                        "\"Bad\" cholesterol — lower values are better.",
                        CLINICAL_BANDS["ldl"],
                    )

                with blood_2:
                    urine = select_field(
                        "Urine Protein Category",
                        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                        key="full_urine",
                    )

                    creatinine = clinical_field(
                        "Serum Creatinine",
                        0.1,
                        11.6,
                        0.9,
                        0.1,
                        "full_creatinine",
                        "Waste product filtered by the kidneys.",
                        CLINICAL_BANDS["creatinine"],
                    )

                    ast = clinical_field(
                        "Aspartate Aminotransferase (AST)",
                        6.0,
                        500.0,
                        23.0,
                        1.0,
                        "full_ast",
                        "Liver enzyme released when liver cells are damaged.",
                        CLINICAL_BANDS["ast"],
                    )

                    alt = clinical_field(
                        "Alanine Aminotransferase (ALT)",
                        1.0,
                        500.0,
                        21.0,
                        1.0,
                        "full_alt",
                        "Liver enzyme used to screen for liver damage.",
                        CLINICAL_BANDS["alt"],
                    )

            # Tab 4: the two remaining binary/categorical model features.
            with oral_tab:
                oral_1, oral_2 = st.columns(2)

                with oral_1:
                    caries_answer = radio_field(
                        "Dental caries present? (dental caries)",
                        ["No", "Yes"],
                        key="full_caries",
                    )

                with oral_2:
                    tartar = radio_field(
                        "Tartar present? (tartar)",
                        ["N", "Y"],
                        format_func=lambda value: (
                            "No" if value == "N" else "Yes"
                        ),
                        key="full_tartar",
                    )

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

        # Same live-prediction pattern as Quick Assessment (see above).
        warnings = validate(full_values)

        for warning_text in warnings:
            st.warning(warning_text)

        st.session_state.prediction_result = make_prediction(full_values)
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

        # Full Assessment: everything is user-entered. Quick Assessment: only the 5 PRIORITY_FEATURES are (rest = REFERENCE_DEFAULTS).
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