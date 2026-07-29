from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Dark theme, set at runtime (no .streamlit/config.toml needed).
# This uses Streamlit's internal config API -- undocumented and technically
# unsupported, so a future Streamlit release could change or drop it. If
# that ever happens, the officially-supported fallback is a
# .streamlit/config.toml with an equivalent [theme] block.
# ---------------------------------------------------------------------------
try:
    st._config.set_option("theme.base", "dark")
    st._config.set_option("theme.primaryColor", "#ff7a3d")
    st._config.set_option("theme.backgroundColor", "#100c09")
    st._config.set_option("theme.secondaryBackgroundColor", "#170f09")
    st._config.set_option("theme.textColor", "#f3ede4")
except Exception:
    pass  # falls back to the CSS overrides below if this API ever disappears

st.set_page_config(
    page_title="SmokeScreen",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# DESIGN SYSTEM
# A "lab report" identity: cool paper background, deep teal ink, a serif
# display face for authority, monospace for numbers (like a printed panel),
# and a coral/amber/teal traffic-light reserved only for the reference gauges.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,500&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root{
--bg:#100c09; --bg2:#170f09;
--ink:#f3ede4; --ink-soft:#a89b8c; --ink-dim:#5c534a;
--line:#2a2019; --line-soft:#1f170f; --card:#150f0a; --card2:#1a130c;
--ember:#ff7a3d; --ember-deep:#c9501a; --ember-soft:rgba(255,122,61,.14);
--ok:#8fae7c; --ok-deep:#5c7a4d; --ok-soft:rgba(143,174,124,.15);
--coral:#e14b3a; --coral-soft:rgba(225,75,58,.15);
--amber:#e0a94a; --amber-soft:rgba(224,169,74,.15);
}
html{color-scheme:dark!important}
html,body,[class*="css"]{font-family:'IBM Plex Sans',ui-sans-serif,system-ui,sans-serif}
.stApp{
background:
radial-gradient(circle at 12% -6%, rgba(255,122,61,.14), transparent 34rem),
radial-gradient(circle at 100% 0%, rgba(225,75,58,.07), transparent 30rem),
linear-gradient(180deg,#0b0806 0%, var(--bg) 100%);
color:var(--ink)!important}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],section[data-testid="stMain"],
.main,[data-testid="stHeader"]{background:transparent!important}
body{background:var(--bg)!important}
.block-container{max-width:1180px;padding-top:0;padding-bottom:3rem}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{
  visibility:hidden!important;display:none!important}
::selection{background:var(--ember);color:#04120e}
div[data-testid="stElementContainer"]{margin-bottom:.3rem}

/* ---- Marquee ticker ---- */
.marquee{overflow:hidden;border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft);
background:var(--bg2);margin:0 -1px 0;padding:.55rem 0;white-space:nowrap}
.marquee-track{display:inline-flex;animation:scroll-left 26s linear infinite}
.marquee-track span{font-family:'IBM Plex Mono';font-size:.72rem;font-weight:600;letter-spacing:.14em;
text-transform:uppercase;color:var(--ink-dim)!important;padding:0 1.4rem}
.marquee-track span.accent{color:var(--ember)!important}
@keyframes scroll-left{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* ---- Hero (editorial, asymmetric, oversized type) ---- */
.hero{position:relative;overflow:hidden;padding:4.2rem 1rem 3.4rem;margin-bottom:0;
border-bottom:1px solid var(--line-soft)}
.hero-grid{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;position:relative;z-index:2}
.hero-badge{display:inline-flex;align-items:center;gap:.5rem;padding:.4rem .85rem;border-radius:999px;
background:var(--ember-soft);border:1px solid rgba(255,122,61,.35);
font-family:'IBM Plex Mono';font-size:.7rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--ember)!important}
.hero-badge .dot{width:6px;height:6px;border-radius:50%;background:var(--ember);box-shadow:0 0 0 3px rgba(255,122,61,.25)}
.hero h1{max-width:760px;margin:1.3rem 0 0;font-family:'Fraunces',serif;font-weight:600;
font-size:clamp(2.6rem,5.6vw,4.9rem);line-height:.98;letter-spacing:-.03em;color:var(--ink)!important}
.hero h1 em{font-style:italic;font-weight:500;color:var(--ember)!important}
.hero p{max-width:520px;margin:1.4rem 0 0;line-height:1.7;font-size:1.02rem;color:var(--ink-soft)!important}
.hero-gauge-wrap{text-align:center}
.hero-gauge{width:100%;max-width:300px;height:auto}
.hero-ghost-tag{display:block;text-align:center;font-family:'IBM Plex Mono';font-size:.72rem;font-weight:600;
letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)!important;margin-top:-.3rem}
.hero-meta{display:flex;gap:1.8rem;margin-top:2.3rem;flex-wrap:wrap}
.hero-meta div{border-left:2px solid var(--ember);padding-left:.7rem}
.hero-meta .hm-label{font-family:'IBM Plex Mono';font-size:.65rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)!important}
.hero-meta .hm-value{font-family:'IBM Plex Mono';font-size:1.05rem;font-weight:600;color:var(--ink)!important;margin-top:.15rem}

/* ---- Stat / info cards ---- */
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:1.15rem 1.3rem;min-height:120px}
.label{font-family:'IBM Plex Mono';font-size:.7rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ink-soft)!important}
.value{font-family:'IBM Plex Mono';font-size:1.7rem;font-weight:600;letter-spacing:-.01em;color:var(--ember)!important;margin-top:.3rem}
.note{font-size:.82rem;line-height:1.45;color:var(--ink-soft)!important;margin-top:.3rem}

.kicker{font-family:'IBM Plex Mono';font-size:.7rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;color:var(--ember)!important}
.title{font-family:'Fraunces',serif;font-size:1.28rem;font-weight:600;color:var(--ink)!important;margin:.3rem 0}
.copy{font-size:.92rem;line-height:1.62;color:var(--ink-soft)!important}

/* ---- Ranked priority chips ---- */
.pills{display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.85rem}
.pill{display:inline-flex;align-items:center;gap:.4rem;padding:.4rem .72rem .4rem .5rem;border-radius:999px;
background:var(--ember-soft);border:1px solid rgba(255,122,61,.3);color:var(--ember)!important;font-size:.8rem;font-weight:600}
.pill b{display:inline-flex;align-items:center;justify-content:center;width:1.15rem;height:1.15rem;border-radius:50%;
background:var(--ember);color:#04120e!important;font-family:'IBM Plex Mono';font-size:.66rem}

/* ---- Bordered containers (st.container(border=True)) act as our form cards ---- */
div[data-testid="stVerticalBlockBorderWrapper"]{background:var(--card);border:1px solid var(--line)!important;
border-radius:22px!important;padding:.3rem}
div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"]{gap:.6rem}

.section-head{display:flex;align-items:baseline;gap:.55rem;margin:.4rem 0 1rem}
.section-head .n{font-family:'IBM Plex Mono';font-size:.75rem;font-weight:600;color:var(--ember)!important}
.section-head .t{font-family:'Fraunces',serif;font-size:1.05rem;font-weight:600;color:var(--ink)!important}
.section-head .r{flex:1;height:1px;background:var(--line)}

.stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4{color:var(--ink)!important;font-family:'Fraunces',serif;letter-spacing:-.01em}
.stMarkdown p,.stCaption,label,div[data-testid="stWidgetLabel"] p{color:var(--ink)!important}
.stCaption{color:var(--ink-soft)!important}
.field-note{margin-top:-.3rem;margin-bottom:.9rem;padding:.5rem .65rem;border:1px solid var(--line);border-radius:10px;
background:var(--card2);color:var(--ink-soft)!important;font-size:.76rem;line-height:1.4}
.info-box{padding:.85rem 1rem;border-radius:14px;background:var(--ember-soft);border:1px solid rgba(255,122,61,.3);
color:var(--ember)!important;font-size:.9rem;line-height:1.55;margin-bottom:1rem}
.warn-box{padding:.85rem 1rem;border-radius:14px;background:var(--amber-soft);border:1px solid rgba(224,169,74,.35);
color:var(--amber)!important;font-size:.9rem;line-height:1.55}

div[data-testid="stTabs"] button{color:var(--ink-dim)!important;font-weight:600!important}
div[data-testid="stTabs"] button[aria-selected="true"]{color:var(--ember)!important}
div[data-testid="stTabs"] div[data-baseweb="tab-highlight"]{background-color:var(--ember)!important}
div[data-testid="stTabs"] div[data-baseweb="tab-border"]{background-color:var(--line)!important}
div[data-baseweb="input"],div[data-baseweb="input"]>div,div[data-baseweb="base-input"],div[data-baseweb="base-input"]>div,
div[data-baseweb="select"]>div{background:var(--card2)!important;border-color:var(--line)!important;color:var(--ink)!important;border-radius:10px!important}
input,div[data-baseweb="input"] input,div[data-baseweb="base-input"] input{
color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important;opacity:1!important;font-family:'IBM Plex Mono'!important}
div[data-baseweb="select"] span,div[data-baseweb="select"] div,div[role="option"]{color:var(--ink)!important}
div[role="listbox"]{background:var(--card2)!important;border:1px solid var(--line)!important}
div[role="radiogroup"] label,div[role="radiogroup"] label p{color:var(--ink)!important}
button[title="Increment"],button[title="Decrement"]{background:var(--card2)!important;border-color:var(--line)!important}
button[title="Increment"] svg,button[title="Decrement"] svg{fill:var(--ink)!important}

/* ---- Mode selector as pill tabs ---- */
div[data-testid="stRadio"] div[role="radiogroup"]{gap:.5rem}
div[data-testid="stRadio"] label{background:var(--card);border:1px solid var(--line);border-radius:999px;
padding:.5rem 1.1rem!important;margin:0!important}
div[data-testid="stRadio"] label:has(input:checked){background:var(--ember-soft);border-color:rgba(255,122,61,.4)}

.stButton>button,.stFormSubmitButton>button{width:100%;min-height:3.3rem;border:none;border-radius:14px;
background:linear-gradient(90deg,var(--ember-deep),var(--ember));
color:#04120e!important;font-size:1rem;font-weight:700;box-shadow:0 13px 30px rgba(255,122,61,.18)}
.stButton>button p,.stFormSubmitButton>button p{color:#04120e!important}

.result{min-height:185px;padding:1.5rem 1.6rem;border:1px solid;border-radius:22px}
.result h3{color:var(--ink)!important;font-family:'Fraunces',serif;margin:.25rem 0 .5rem}
.result p{color:var(--ink-soft)!important;line-height:1.62}
.smoker{background:var(--coral-soft);border-color:rgba(225,75,58,.35)}
.nonsmoker{background:var(--ok-soft);border-color:rgba(143,174,124,.35)}
.confidence{min-height:185px;padding:1.4rem 1.5rem;border:1px solid var(--line);border-radius:22px;background:var(--card)}
.confidence-value{font-family:'IBM Plex Mono';font-size:2.5rem;font-weight:600;letter-spacing:-.02em;color:var(--ink)!important}
.foot{font-size:.84rem;line-height:1.6;color:var(--ink-dim)!important}

/* ---- Reference-range gauge (the signature element) ---- */
.gauge-wrap{margin:-.15rem 0 .2rem}
.gauge-field-label{font-family:'IBM Plex Sans';font-size:.9rem;font-weight:600;color:var(--ink)!important;
margin-bottom:.35rem;min-height:2.4rem;line-height:1.2;display:flex;align-items:flex-end}
.gauge-val{font-family:'IBM Plex Mono';font-size:.86rem;font-weight:600;color:var(--ink)!important}
.gauge-tag{font-family:'IBM Plex Mono';font-size:.66rem;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
padding:.1rem .5rem;border-radius:999px;white-space:nowrap}
.tag-normal{background:var(--ok-soft);color:var(--ok)!important}
.tag-low{background:var(--amber-soft);color:var(--amber)!important}
.tag-high{background:var(--coral-soft);color:var(--coral)!important}
.gauge-scale{display:flex;justify-content:space-between;align-items:center;margin-top:.25rem;margin-bottom:.9rem}
.gauge-scale span:first-child,.gauge-scale span:last-child{font-family:'IBM Plex Mono';font-size:.68rem;color:var(--ink-soft)!important}

/* ---- Native slider taken over as the interactive gauge ---- */
div[data-testid="stSlider"]{padding-top:.3rem!important;padding-bottom:0!important}
div[data-baseweb="slider"]{padding-top:0!important;padding-bottom:0!important}
div[data-testid*="TickBar" i]{display:none!important}
div[data-baseweb="slider"] [role="slider"] div{display:none!important}
div[data-baseweb="slider"] div[style*="background"]{background:transparent!important}
div[data-baseweb="slider"] > div:first-child{
  height:8px!important;border-radius:999px!important;background:var(--line)!important;
  box-shadow:inset 0 1px 3px rgba(0,0,0,.35)!important}
div[data-baseweb="slider"] [role="slider"]{
  background:var(--ink)!important;border:3px solid var(--bg)!important;
  box-shadow:0 0 0 2.5px var(--ember), 0 2px 8px rgba(0,0,0,.4)!important;
  width:19px!important;height:19px!important;top:-6px!important;cursor:grab!important;
  transition:transform .12s ease, box-shadow .12s ease!important}
div[data-baseweb="slider"] [role="slider"]:hover{
  transform:scale(1.15)!important;box-shadow:0 0 0 5px var(--ember-soft),0 2px 10px rgba(0,0,0,.45)!important}
div[data-baseweb="slider"] [role="slider"]:active,
div[data-baseweb="slider"] [role="slider"][aria-valuenow]:focus{
  cursor:grabbing!important;transform:scale(1.2)!important}
div[data-testid="stNumberInput"] input{font-family:'IBM Plex Mono'!important;font-size:.85rem!important;
padding:.4rem .5rem!important;text-align:center!important}

/* ---- Field spacing (keeps grouped rows of same-type fields aligned) ---- */
.plain-field{margin-bottom:.85rem}

@media(max-width:760px){.hero{padding:2.6rem 1rem 2.2rem}.hero-grid{flex-direction:column;align-items:flex-start}
.hero-gauge-wrap,.hero-ghost-tag{text-align:left}.hero-gauge{max-width:220px}.block-container{padding-left:.8rem;padding-right:.8rem}}
</style>
""", unsafe_allow_html=True)

APP_FOLDER = Path(__file__).resolve().parent
MODEL_PATH = APP_FOLDER / "smoking_random_forest_model.pkl"
FEATURE_PATH = APP_FOLDER / "smoking_feature_columns.pkl"

REFERENCE_DEFAULTS = {
    "age": 40, "height(cm)": 165, "weight(kg)": 65, "waist(cm)": 82.0,
    "eyesight(left)": 1.0, "eyesight(right)": 1.0,
    "hearing(left)": 1.0, "hearing(right)": 1.0,
    "systolic": 120.0, "relaxation": 76.0,
    "fasting blood sugar": 96.0, "Cholesterol": 195.0,
    "HDL": 55.0, "LDL": 113.0, "Urine protein": 1.0,
    "serum creatinine": 0.9, "AST": 23.0, "ALT": 21.0,
    "dental caries": 0, "tartar": "N",
}

# Ordered by Random Forest feature-importance rank (highest signal first).
PRIORITY_ORDER = ["gender", "Gtp", "hemoglobin", "triglyceride", "height(cm)"]
PRIORITY_FEATURES = set(PRIORITY_ORDER)

# General adult reference bands used purely to help someone read a raw lab
# number at a glance. These are widely-published population reference
# ranges, not a diagnosis -- always shown with that caveat in the UI.
# Format: low, high, unit, reverse (True = below `low` is the flagged zone,
# and there is no penalised upper zone -- e.g. HDL, where higher is better).
LAB_RANGES = {
    "waist(cm)":           (70.0, 94.0, "cm", False),
    "systolic":            (90.0, 129.0, "mmHg", False),
    "relaxation":          (60.0, 84.0, "mmHg", False),
    "fasting blood sugar": (70.0, 99.0, "mg/dL", False),
    "Cholesterol":         (100.0, 199.0, "mg/dL", False),
    "HDL":                 (40.0, 200.0, "mg/dL", True),
    "LDL":                 (0.0, 129.0, "mg/dL", False),
    "triglyceride":        (0.0, 149.0, "mg/dL", False),
    "hemoglobin":          (12.0, 17.5, "g/dL", False),
    "serum creatinine":    (0.6, 1.3, "mg/dL", False),
    "AST":                 (8.0, 40.0, "U/L", False),
    "ALT":                 (7.0, 56.0, "U/L", False),
    "Gtp":                 (8.0, 61.0, "U/L", False),
}

# UI metadata for every interactive_gauge() field, kept in one place so call
# sites just say interactive_gauge("Gtp", key="...") instead of repeating
# labels/notes/bounds inline at every call site.
# Format: label, note, default, step, num_min, num_max (num_min/num_max are
# the hard limits on the paired number box; the slider's own range is
# derived from LAB_RANGES inside interactive_gauge()).
GAUGE_FIELDS = {
    "Gtp": dict(
        label="Gamma-glutamyl transferase (Gtp) · #2 priority",
        note="High-priority liver-enzyme measurement.",
        default=25.0, step=1.0, num_min=1.0, num_max=999.0,
    ),
    "hemoglobin": dict(
        label="Haemoglobin (hemoglobin) · #3 priority",
        note="High-priority oxygen-carrying blood measurement.",
        default=14.8, step=0.1, num_min=4.9, num_max=21.1,
    ),
    "triglyceride": dict(
        label="Triglycerides (triglyceride) · #4 priority",
        note="High-priority blood-fat measurement.",
        default=108.0, step=1.0, num_min=8.0, num_max=999.0,
    ),
    "waist(cm)": dict(
        label="Waist circumference (waist(cm))", note="",
        default=82.0, step=0.5, num_min=51.0, num_max=129.0,
    ),
    "systolic": dict(
        label="Systolic pressure (systolic)", note="",
        default=120.0, step=1.0, num_min=71.0, num_max=240.0,
    ),
    "relaxation": dict(
        label="Diastolic pressure (relaxation)", note="",
        default=76.0, step=1.0, num_min=40.0, num_max=146.0,
    ),
    "fasting blood sugar": dict(
        label="Fasting blood glucose (fasting blood sugar)", note="",
        default=96.0, step=1.0, num_min=46.0, num_max=505.0,
    ),
    "Cholesterol": dict(
        label="Total cholesterol (Cholesterol)", note="",
        default=195.0, step=1.0, num_min=55.0, num_max=445.0,
    ),
    "HDL": dict(
        label="HDL (HDL)", note="",
        default=55.0, step=1.0, num_min=4.0, num_max=618.0,
    ),
    "LDL": dict(
        label="LDL (LDL)", note="",
        default=113.0, step=1.0, num_min=1.0, num_max=1860.0,
    ),
    "serum creatinine": dict(
        label="Serum creatinine (serum creatinine)", note="",
        default=0.9, step=0.1, num_min=0.1, num_max=11.6,
    ),
    "AST": dict(
        label="AST (AST)", note="",
        default=23.0, step=1.0, num_min=6.0, num_max=1311.0,
    ),
    "ALT": dict(
        label="ALT (ALT)", note="",
        default=21.0, step=1.0, num_min=1.0, num_max=2914.0,
    ),
}

@st.cache_resource
def load_files():
    if not MODEL_PATH.exists() or not FEATURE_PATH.exists():
        raise FileNotFoundError(
            "Place smoking_random_forest_model.pkl and "
            "smoking_feature_columns.pkl beside this app."
        )
    model = joblib.load(MODEL_PATH)
    columns = joblib.load(FEATURE_PATH)
    return model, columns

try:
    model, feature_columns = load_files()
except Exception as exc:
    st.error("The prediction system could not be loaded.")
    st.code(str(exc))
    st.stop()

def desc(text):
    st.markdown(f'<div class="field-note">{text}</div>', unsafe_allow_html=True)

def _sync_from_slider(key):
    st.session_state[f"{key}__num"] = st.session_state[f"{key}__sld"]

def _sync_from_number(key):
    lo, hi = st.session_state[f"{key}__bounds"]
    st.session_state[f"{key}__sld"] = max(lo, min(hi, st.session_state[f"{key}__num"]))

def interactive_gauge(feature_key, key):
    """Draggable, colour-zoned reference gauge for one lab field. Doubles as
    the value input -- slide the thumb or type the exact number in the box
    beside it; the two stay in sync via session_state.

    feature_key : key into LAB_RANGES / GAUGE_FIELDS (e.g. "Gtp")
    key         : unique widget key for this occurrence of the field
                  (the same feature_key can appear in both Quick and Full
                  assessment, so each needs its own session_state slot)
    """
    low, high, unit, reverse = LAB_RANGES[feature_key]
    field = GAUGE_FIELDS[feature_key]
    label, note = field["label"], field["note"]
    default, step = field["default"], field["step"]
    num_min, num_max = field["num_min"], field["num_max"]

    span = max(high - low, 1e-6)
    lo_bound = round(max(low - span * 0.7, num_min), 4)
    hi_bound = round(min(high + span * 0.7, num_max), 4)
    if hi_bound <= lo_bound:
        lo_bound, hi_bound = num_min, num_max

    sld_key, num_key, bnd_key = f"{key}__sld", f"{key}__num", f"{key}__bounds"
    st.session_state[bnd_key] = (lo_bound, hi_bound)
    if sld_key not in st.session_state:
        clamped = max(lo_bound, min(hi_bound, default))
        st.session_state[sld_key] = clamped
        st.session_state[num_key] = default

    def pct(v):
        return max(0.0, min(100.0, (v - lo_bound) / (hi_bound - lo_bound) * 100))

    low_pct, high_pct = pct(low), pct(high)
    if reverse:
        grad = (f"linear-gradient(to right, var(--amber) 0%, var(--amber) {low_pct:.1f}%, "
                f"var(--ok) {low_pct:.1f}%, var(--ok) 100%)")
    else:
        grad = (f"linear-gradient(to right, var(--amber) 0%, var(--amber) {low_pct:.1f}%, "
                f"var(--ok) {low_pct:.1f}%, var(--ok) {high_pct:.1f}%, "
                f"var(--coral) {high_pct:.1f}%, var(--coral) 100%)")

    with st.container(key=f"gauge_{key}"):
        st.markdown(f"""
        <div class="gauge-field-label">{label}</div>
        <style>
        div.st-key-gauge_{key} div[data-baseweb="slider"] div[style*="background"] {{
            background: transparent !important;
        }}
        div.st-key-gauge_{key} div[data-baseweb="slider"] > div:first-child {{
            background: {grad} !important;
            height: 8px !important;
            border-radius: 999px !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        col_s, col_n = st.columns([3.3, 1])
        with col_s:
            st.slider("", lo_bound, hi_bound, step=step, key=sld_key,
                       on_change=_sync_from_slider, args=(key,), label_visibility="collapsed")
        with col_n:
            st.number_input("", num_min, num_max, step=step, key=num_key,
                             on_change=_sync_from_number, args=(key,), label_visibility="collapsed")

        value = st.session_state[num_key]
        if reverse:
            tag_label, tag_class = ("Low", "tag-low") if value < low else ("Normal", "tag-normal")
        else:
            if value < low:
                tag_label, tag_class = "Low", "tag-low"
            elif value > high:
                tag_label, tag_class = "High", "tag-high"
            else:
                tag_label, tag_class = "Normal", "tag-normal"

        st.markdown(f"""
        <div class="gauge-scale">
          <span>{lo_bound:g} {unit}</span>
          <span class="gauge-tag {tag_class}">{tag_label} · ref {low:g}–{high:g}</span>
          <span>{hi_bound:g} {unit}</span>
        </div>
        """, unsafe_allow_html=True)
        if note:
            desc(note)
    return value

def encode(values):
    frame = pd.DataFrame([values])
    frame = pd.get_dummies(
        frame,
        columns=["gender", "tartar"],
        drop_first=False,
        dtype=int,
    )
    return frame.reindex(columns=feature_columns, fill_value=0)

def validate(values):
    errors = []
    if values["systolic"] <= values["relaxation"]:
        errors.append("Systolic pressure must be higher than diastolic pressure.")
    if values["HDL"] > values["Cholesterol"]:
        errors.append("HDL cannot be greater than total cholesterol.")
    return errors

def binary(answer):
    return 1 if answer == "Yes" else 0

st.markdown("""
<div class="marquee"><div class="marquee-track">
<span>QUICK&nbsp;OR&nbsp;FULL&nbsp;ASSESSMENT</span><span class="accent">·</span><span>LIVE&nbsp;REFERENCE&nbsp;GAUGES</span><span class="accent">·</span>
<span>RANDOM&nbsp;FOREST&nbsp;MODEL</span><span class="accent">·</span><span>SCREENING&nbsp;SUPPORT,&nbsp;NOT&nbsp;A&nbsp;DIAGNOSIS</span><span class="accent">·</span>
<span>QUICK&nbsp;OR&nbsp;FULL&nbsp;ASSESSMENT</span><span class="accent">·</span><span>LIVE&nbsp;REFERENCE&nbsp;GAUGES</span><span class="accent">·</span>
<span>RANDOM&nbsp;FOREST&nbsp;MODEL</span><span class="accent">·</span><span>SCREENING&nbsp;SUPPORT,&nbsp;NOT&nbsp;A&nbsp;DIAGNOSIS</span><span class="accent">·</span>
</div></div>
<section class="hero">
  <div class="hero-grid">
    <div>
      <div class="hero-badge"><span class="dot"></span>Screening-support prototype</div>
      <h1>Read the signal<br>before <em>you</em> ask.</h1>
      <p>Five inputs, ranked by what the model actually leans on, turn into a
      probability in seconds — or go deeper with a full twenty-three field
      screening profile. Every lab value sits on a live reference gauge as you move it.</p>
    </div>
    <div class="hero-gauge-wrap">
      <svg viewBox="0 0 300 165" class="hero-gauge" xmlns="http://www.w3.org/2000/svg">
        <path d="M20,150 A130,130 0 0,1 280,150" fill="none" stroke="var(--line)" stroke-width="3" stroke-linecap="round"/>
        <path d="M20,150 A130,130 0 0,1 261,83" fill="none" stroke="var(--ember)" stroke-width="3" stroke-linecap="round"/>
        <circle cx="261" cy="83" r="8" fill="var(--bg)" stroke="var(--ember)" stroke-width="3"/>
        <text x="150" y="122" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="36" font-weight="600" fill="var(--ink)">82.6%</text>
      </svg>
      <div class="hero-ghost-tag">Held-out test accuracy</div>
    </div>
  </div>
  <div class="hero-meta">
    <div><div class="hm-label">Model</div><div class="hm-value">Random Forest</div></div>
    <div><div class="hm-label">F1-score</div><div class="hm-value">0.7708</div></div>
    <div><div class="hm-label">Smoker recall</div><div class="hm-value">79.70%</div></div>
    <div><div class="hm-label">Validation</div><div class="hm-value">5-fold CV</div></div>
  </div>
</section>
""", unsafe_allow_html=True)

st.write("")
st.write("")
left, right = st.columns([1.55, 1])
with left:
    priority_pills = "".join(
        f'<span class="pill"><b>{i+1}</b>{name}</span>'
        for i, name in enumerate(["Gender", "Gtp", "Haemoglobin", "Triglycerides", "Height"])
    )
    st.markdown(f"""
    <div class="card">
    <div class="kicker">Feature priority</div>
    <div class="title">The strongest model signals appear first</div>
    <div class="copy">
    These five fields are ranked by the trained Random Forest's feature-importance
    scores, highest first. They're the fields most worth getting right; everything
    else is optional detail for a fuller picture.
    </div>
    <div class="pills">{priority_pills}</div></div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="card">
    <div class="kicker">Important</div>
    <div class="title">Quick mode uses reference defaults</div>
    <div class="copy">
    The final model still expects all trained features. Quick mode fills the
    remaining fields with representative reference values. Full mode is recommended.
    </div></div>
    """, unsafe_allow_html=True)

st.write("")
mode = st.radio(
    "Assessment mode",
    ["Quick Assessment", "Full Assessment"],
    horizontal=True,
)

input_values = None
source_text = ""

if mode == "Quick Assessment":
    st.markdown("""
    <div class="card">
    <div class="kicker">Fast demonstration</div>
    <div class="title">Enter five high-priority inputs</div>
    <div class="copy">
    Other model inputs use representative reference defaults. This makes the
    experience faster, but less personalised than the full assessment.
    </div></div>
    """, unsafe_allow_html=True)
    st.write("")

    with st.container(border=True):
        st.markdown('<div class="section-head"><span class="n">01</span><span class="t">Reference-gauge fields</span><div class="r"></div></div>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns(3)
        with g1:
            gtp = interactive_gauge("Gtp", key="quick_gtp")
        with g2:
            hemoglobin = interactive_gauge("hemoglobin", key="quick_hemoglobin")
        with g3:
            triglyceride = interactive_gauge("triglyceride", key="quick_triglyceride")

        st.markdown('<div class="section-head"><span class="n">02</span><span class="t">Other priority fields</span><div class="r"></div></div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1:
            gender = st.selectbox(
                "Gender (gender) · #1 priority", ["F", "M"],
                format_func=lambda x: "Female" if x == "F" else "Male",
            )
            desc("Highest-ranked categorical input after encoding.")
        with p2:
            height = st.number_input(
                "Height in centimetres (height(cm)) · #5 priority",
                130, 190, 165, 5,
            )
            desc("Physical measurement that ranked strongly in the model.")
        with p3:
            st.markdown(
                '<div class="warn-box">Remaining inputs will use reference defaults.</div>',
                unsafe_allow_html=True,
            )

        st.write("")
        submitted = st.button(
            "Generate quick prediction",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        input_values = REFERENCE_DEFAULTS.copy()
        input_values.update({
            "gender": gender,
            "height(cm)": height,
            "Gtp": gtp,
            "hemoglobin": hemoglobin,
            "triglyceride": triglyceride,
        })
        source_text = "Quick Assessment using reference defaults"

else:
    st.markdown("""
    <div class="card">
    <div class="kicker">Recommended</div>
    <div class="title">Complete the full screening profile</div>
    <div class="copy">
    This mode uses every raw feature required by the final model and provides
    the most faithful prediction for the submitted screening record.
    </div></div>
    """, unsafe_allow_html=True)
    st.write("")

    with st.container(border=True):
        t1, t2, t3, t4 = st.tabs([
            "1. Priority inputs",
            "2. Screening checks",
            "3. Additional blood tests",
            "4. Oral health",
        ])
        with t1:
            st.markdown('<div class="info-box">These fields appeared among the strongest signals in the model ranking. Gauges show where each value sits against a general adult reference range.</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-head"><span class="n">01</span><span class="t">Reference-gauge fields</span><div class="r"></div></div>', unsafe_allow_html=True)
            g1, g2, g3 = st.columns(3)
            with g1:
                gtp = interactive_gauge("Gtp", key="full_gtp")
            with g2:
                hemoglobin = interactive_gauge("hemoglobin", key="full_hemoglobin")
            with g3:
                triglyceride = interactive_gauge("triglyceride", key="full_triglyceride")
            st.markdown('<div class="section-head"><span class="n">02</span><span class="t">Other priority fields</span><div class="r"></div></div>', unsafe_allow_html=True)
            p1, p2, p3 = st.columns(3)
            with p1:
                gender = st.selectbox(
                    "Gender (gender) · #1 priority", ["F", "M"],
                    format_func=lambda x: "Female" if x == "F" else "Male",
                )
                desc("Recorded sex category used after one-hot encoding.")
            with p2:
                height = st.number_input(
                    "Height in centimetres (height(cm)) · #5 priority",
                    130, 190, 165, 5,
                )
                desc("Standing height measured in centimetres.")
            with p3:
                age = st.number_input("Age in years (age)", 20, 85, 40, 5)
                desc("Age at the time of screening.")

        with t2:
            st.markdown('<div class="section-head"><span class="n">01</span><span class="t">Reference-gauge fields</span><div class="r"></div></div>', unsafe_allow_html=True)
            g1, g2, g3 = st.columns(3)
            with g1:
                waist = interactive_gauge("waist(cm)", key="waist")
            with g2:
                systolic = interactive_gauge("systolic", key="systolic")
            with g3:
                relaxation = interactive_gauge("relaxation", key="relaxation")
            st.markdown('<div class="section-head"><span class="n">02</span><span class="t">Other screening fields</span><div class="r"></div></div>', unsafe_allow_html=True)
            p1, p2, p3 = st.columns(3)
            with p1:
                weight = st.number_input(
                    "Weight in kilograms (weight(kg))",
                    30, 135, 65, 5,
                )
            with p2:
                eyesight_left = st.number_input(
                    "Left-eye eyesight score (eyesight(left))",
                    0.1, 9.9, 1.0, 0.1,
                )
                eyesight_right = st.number_input(
                    "Right-eye eyesight score (eyesight(right))",
                    0.1, 9.9, 1.0, 0.1,
                )
            with p3:
                hearing_left = st.selectbox(
                    "Left-ear hearing (hearing(left))",
                    [1.0, 2.0],
                    format_func=lambda x: "1 — Normal" if x == 1.0 else "2 — Reduced",
                )
                hearing_right = st.selectbox(
                    "Right-ear hearing (hearing(right))",
                    [1.0, 2.0],
                    format_func=lambda x: "1 — Normal" if x == 1.0 else "2 — Reduced",
                )

        with t3:
            st.markdown('<div class="section-head"><span class="n">01</span><span class="t">Reference-gauge fields</span><div class="r"></div></div>', unsafe_allow_html=True)
            g1, g2, g3, g4 = st.columns(4)
            with g1:
                fasting = interactive_gauge("fasting blood sugar", key="fasting")
            with g2:
                cholesterol = interactive_gauge("Cholesterol", key="cholesterol")
            with g3:
                hdl = interactive_gauge("HDL", key="hdl")
            with g4:
                ldl = interactive_gauge("LDL", key="ldl")
            g5, g6, g7, g8 = st.columns(4)
            with g5:
                creatinine = interactive_gauge("serum creatinine", key="creatinine")
            with g6:
                ast = interactive_gauge("AST", key="ast")
            with g7:
                alt = interactive_gauge("ALT", key="alt")
            with g8:
                urine = st.selectbox(
                    "Urine protein category (Urine protein)",
                    [1.0,2.0,3.0,4.0,5.0,6.0],
                )
            st.markdown(
                '<div class="warn-box">These lower-ranked features were retained because the reduced-feature model performed worse. Reference bands are general adult population ranges, shown for context only — not a diagnosis.</div>',
                unsafe_allow_html=True,
            )

        with t4:
            c1, c2 = st.columns(2)
            with c1:
                caries_answer = st.radio(
                    "Dental caries present? (dental caries)",
                    ["No", "Yes"], horizontal=True,
                )
            with c2:
                tartar = st.radio(
                    "Tartar present? (tartar)",
                    ["N", "Y"],
                    format_func=lambda x: "No" if x == "N" else "Yes",
                    horizontal=True,
                )

        st.write("")
        submitted = st.button(
            "Generate full prediction",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        input_values = {
            "gender": gender, "age": age, "height(cm)": height,
            "weight(kg)": weight, "waist(cm)": waist,
            "eyesight(left)": eyesight_left, "eyesight(right)": eyesight_right,
            "hearing(left)": hearing_left, "hearing(right)": hearing_right,
            "systolic": systolic, "relaxation": relaxation,
            "fasting blood sugar": fasting, "Cholesterol": cholesterol,
            "triglyceride": triglyceride, "HDL": hdl, "LDL": ldl,
            "hemoglobin": hemoglobin, "Urine protein": urine,
            "serum creatinine": creatinine, "AST": ast, "ALT": alt,
            "Gtp": gtp, "dental caries": binary(caries_answer), "tartar": tartar,
        }
        source_text = "Full Assessment using all model inputs"

if input_values is not None:
    errors = validate(input_values)
    if errors:
        st.error("Please correct the following:")
        for error in errors:
            st.write(f"- {error}")
    else:
        try:
            model_input = encode(input_values)
            prediction = int(model.predict(model_input)[0])
            probability = float(model.predict_proba(model_input)[0][1])

            st.write("")
            st.markdown("## Prediction result")
            left, right = st.columns([1.55, 1])

            with left:
                if prediction == 1:
                    st.markdown("""
                    <div class="result smoker">
                    <div class="kicker">Model classification</div>
                    <h3>Smoker pattern detected</h3>
                    <p>The submitted values are more similar to records classified as smokers.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="result nonsmoker">
                    <div class="kicker">Model classification</div>
                    <h3>Non-smoker pattern detected</h3>
                    <p>The submitted values are more similar to records classified as non-smokers.</p>
                    </div>
                    """, unsafe_allow_html=True)

            with right:
                st.markdown(
                    f'<div class="confidence"><div class="label">Estimated smoker likelihood</div>'
                    f'<div class="confidence-value">{probability*100:.1f}%</div>'
                    f'<div class="note">{source_text}</div></div>',
                    unsafe_allow_html=True,
                )

            st.progress(probability)

            if mode == "Quick Assessment":
                st.warning(
                    "Quick Assessment used reference defaults for the remaining features. "
                    "Use Full Assessment for the most complete result."
                )
            elif prediction == 1:
                st.warning("Confirm smoking status directly before taking action.")
            else:
                st.info("A non-smoker prediction is not proof. Direct confirmation is still required.")

            with st.expander("Review model inputs"):
                table = pd.DataFrame({
                    "Feature": list(input_values.keys()),
                    "Value supplied": list(input_values.values()),
                    "Source": [
                        "User entered"
                        if mode == "Full Assessment" or feature in PRIORITY_FEATURES
                        else "Reference default"
                        for feature in input_values
                    ],
                })
                st.dataframe(table, use_container_width=True, hide_index=True)

            st.success("Prediction completed successfully.")
        except Exception as exc:
            st.error("The prediction could not be completed.")
            with st.expander("Technical details"):
                st.code(str(exc))

st.write("")
st.divider()
st.markdown("""
<div class="foot">
<strong>SmokeScreen</strong> is an educational machine-learning prototype.
It supports screening conversations and does not replace direct confirmation,
clinical judgement or professional advice. Reference ranges shown on lab
values are general adult population bands for orientation only.
</div>
""", unsafe_allow_html=True)