from pathlib import Path
from textwrap import dedent

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from src.storage.action_storage import load_actions, save_actions

PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


st.set_page_config(
    page_title="SustainOps Control Tower",
    page_icon="🌱",
    layout="wide",
)

# -------------------------------------------------
# GREEN + WHITE SUSTAINABILITY THEME
# -------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --green-dark: #071A12;
        --green-panel: #0B2418;
        --green-primary: #22C55E;
        --green-light: #86EFAC;
        --white: #FFFFFF;
        --white-soft: #F2FFF6;
        --border: rgba(134, 239, 172, 0.24);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(34,197,94,0.16), transparent 30%),
            radial-gradient(circle at 95% 100%, rgba(34,197,94,0.10), transparent 28%),
            linear-gradient(135deg, #06150E 0%, #082117 48%, #0C2D1E 100%);
        background-attachment: fixed;
        color: var(--white);
    }

    .stApp,
    .stApp p,
    .stApp label {
        color: var(--white-soft);
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06150E 0%, #0A2A1B 100%);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(34,197,94,0.10), rgba(255,255,255,0.035));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.22);
    }

    div[data-testid="stMetricLabel"] * {
        color: #CFF7DB !important;
    }

    div[data-testid="stMetricValue"] * {
        color: #FFFFFF !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #16A34A, #22C55E) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255,255,255,0.14) !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: linear-gradient(90deg, #22C55E, #4ADE80) !important;
        color: #FFFFFF !important;
        border-color: #86EFAC !important;
        box-shadow: 0 8px 20px rgba(34,197,94,0.24);
    }

    .stTextInput input,
    .stNumberInput input,
    .stDateInput input,
    .stTextArea textarea {
        background: #F0FDF4 !important;
        color: #14532D !important;
        border: 1px solid #86EFAC !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    .stTextInput input::placeholder,
    .stNumberInput input::placeholder,
    .stDateInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #4B7A5D !important;
        opacity: 1 !important;
    }
    .stNumberInput button {
        background: #DCFCE7 !important;
        color: #14532D !important;
        border-color: #86EFAC !important;
    }

    .stNumberInput button * {
        color: #14532D !important;
    }

    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.07) !important;
        border-color: rgba(134,239,172,0.28) !important;
        color: #FFFFFF !important;
    }

    span[data-baseweb="tag"] {
        background-color: #16A34A !important;
        border-color: #4ADE80 !important;
    }

    span[data-baseweb="tag"] *,
    span[data-baseweb="tag"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #0B2418 !important;
    }

    li[role="option"] {
        color: #FFFFFF !important;
    }

    li[role="option"]:hover {
        background-color: rgba(34,197,94,0.18) !important;
    }

    input[type="radio"],
    input[type="checkbox"] {
        accent-color: #22C55E !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #22C55E !important;
        border-color: #86EFAC !important;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stPlotlyChart"] {
        background: rgba(255,255,255,0.035);
        border: 1px solid rgba(134,239,172,0.16);
        border-radius: 14px;
        padding: 8px;
    }

    div[data-testid="stAlert"] {
        background: rgba(22,163,74,0.12) !important;
        border: 1px solid rgba(74,222,128,0.35) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
    }

    div[data-testid="stAlert"] * {
        color: #F2FFF6 !important;
    }

    a {
        color: #86EFAC !important;
    }

    a:hover {
        color: #FFFFFF !important;
    }

    hr {
        border-color: rgba(134,239,172,0.18) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #06150E;
    }

    ::-webkit-scrollbar-thumb {
        background: #1F7A46;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #22C55E;
    }

    /* Home hero */
    .sustainops-hero {
        padding: 34px 36px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(34,197,94,0.18),
            rgba(255,255,255,0.035)
        );
        border: 1px solid rgba(134,239,172,0.28);
        box-shadow: 0 14px 40px rgba(0,0,0,0.20);
        margin: 6px 0 28px 0;
    }

    .sustainops-eyebrow {
        font-size: 13px;
        letter-spacing: 2.2px;
        font-weight: 700;
        color: #86EFAC !important;
        margin-bottom: 10px;
    }

    .sustainops-title {
        font-size: clamp(34px, 4vw, 52px);
        line-height: 1.08;
        font-weight: 800;
        color: #FFFFFF !important;
        margin-bottom: 14px;
    }

    .sustainops-subtitle {
        max-width: 900px;
        font-size: 18px;
        line-height: 1.6;
        color: #E9FFF0 !important;
    }

    /* Home module cards */
    .module-card {
        min-height: 190px;
        padding: 24px;
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(34,197,94,0.10),
            rgba(255,255,255,0.035)
        );
        border: 1px solid rgba(134,239,172,0.20);
        box-shadow: 0 8px 24px rgba(0,0,0,0.16);
    }

    .module-icon {
        font-size: 28px;
        margin-bottom: 14px;
    }

    .module-title {
        font-size: 19px;
        font-weight: 700;
        color: #FFFFFF !important;
        margin-bottom: 10px;
    }

    .module-text {
        font-size: 15px;
        line-height: 1.55;
        color: #DDFBE6 !important;
    }

    /* -------------------------------------------------
       DARK GREEN TABLES / DATAFRAMES
       ------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        background: #0B2418 !important;
        border: 1px solid rgba(134,239,172,0.22) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    /* Try to keep dataframe canvas/container in dark green */
    div[data-testid="stDataFrame"] > div {
        background: #0B2418 !important;
    }

    div[data-testid="stDataFrame"] [role="grid"] {
        background: #0B2418 !important;
        color: #F2FFF6 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #123A27 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border-bottom: 1px solid rgba(134,239,172,0.22) !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: #0D2B1D !important;
        color: #F2FFF6 !important;
        border-color: rgba(134,239,172,0.10) !important;
    }

    div[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
        background: #103523 !important;
    }

    /* Data editor */
    div[data-testid="stDataEditor"] {
        background: #0B2418 !important;
        border: 1px solid rgba(134,239,172,0.22) !important;
        border-radius: 14px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataEditor"] [role="columnheader"] {
        background: #123A27 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDataEditor"] [role="gridcell"] {
        background: #0D2B1D !important;
        color: #F2FFF6 !important;
    }

    /* -------------------------------------------------
       LIGHT-GREEN SLIDERS
       ------------------------------------------------- */

    div[data-baseweb="slider"] {
        --slider-track-color: #86EFAC;
    }

    div[data-baseweb="slider"] > div > div {
        background-color: rgba(134,239,172,0.26) !important;
    }

    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #86EFAC !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(134,239,172,0.20) !important;
    }

    div[data-baseweb="slider"] div[role="slider"]:hover {
        background-color: #BBF7D0 !important;
        border-color: #FFFFFF !important;
    }

    /* Streamlit slider filled track */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div:nth-child(2) {
        background-color: #86EFAC !important;
    }

    /* Slider value labels */
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #FFFFFF !important;
        background: #166534 !important;
        border: 1px solid #86EFAC !important;
    }

    /* -------------------------------------------------
       REMOVE RED ACCENTS FROM SELECTED CONTROLS
       ------------------------------------------------- */

    span[data-baseweb="tag"] {
        background-color: #4ADE80 !important;
        border-color: #86EFAC !important;
    }

    span[data-baseweb="tag"] * {
        color: #062412 !important;
        fill: #062412 !important;
        font-weight: 600 !important;
    }

    /* Radio selection */
    div[role="radiogroup"] [data-baseweb="radio"] > div:first-child {
        border-color: #86EFAC !important;
    }

    div[role="radiogroup"] [aria-checked="true"] > div:first-child,
    div[role="radiogroup"] [data-checked="true"] > div:first-child {
        background-color: #86EFAC !important;
        border-color: #86EFAC !important;
    }

    /* Checkbox selection */
    div[data-baseweb="checkbox"] [aria-checked="true"],
    div[data-baseweb="checkbox"] [data-checked="true"] {
        background-color: #86EFAC !important;
        border-color: #86EFAC !important;
    }


    /* =================================================
       STREAMLIT SLIDER — FULL LIGHT-GREEN RAIL + THUMB
       ================================================= */

    /* BaseWeb slider rail/track */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background: #86EFAC !important;
    }

    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background: #86EFAC !important;
    }

    /* Newer Streamlit/BaseWeb track pieces */
    div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
        background: #86EFAC !important;
    }

    /* Force both selected and unselected portions to same light green */
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
        background: #86EFAC !important;
        background-color: #86EFAC !important;
    }

    /* Slider thumb */
    div[data-testid="stSlider"] div[role="slider"] {
        background: #BBF7D0 !important;
        background-color: #BBF7D0 !important;
        border: 2px solid #166534 !important;
        box-shadow: 0 0 0 2px rgba(187,247,208,0.35) !important;
    }

    /* Slider value bubble */
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        background: #DCFCE7 !important;
        color: #14532D !important;
        border: 1px solid #166534 !important;
    }

    /* =================================================
       DATAFRAME OUTER FRAME — LIGHT GREEN
       ================================================= */

    div[data-testid="stDataFrame"] {
        background: #DCFCE7 !important;
        border: 1px solid #166534 !important;
        border-radius: 12px !important;
    }

    div[data-testid="stDataFrame"] > div {
        background: #DCFCE7 !important;
    }


    /* =================================================
       FINAL COLOR OVERRIDES
       Dark app background + readable white text
       ================================================= */

    /* Keep the overall app dark. Never make page backgrounds light green. */
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(34,197,94,0.16), transparent 30%),
            radial-gradient(circle at 95% 100%, rgba(34,197,94,0.10), transparent 28%),
            linear-gradient(135deg, #06150E 0%, #082117 48%, #0C2D1E 100%) !important;
        color: #FFFFFF !important;
    }

    /* Default text on dark surfaces */
    .stApp p,
    .stApp label,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #FFFFFF !important;
    }

    /* Sidebar stays dark with white text */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06150E 0%, #0A2A1B 100%) !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* =================================================
       TABLES
       Light-green body + light-green header
       Dark-green text + dark-green borders
       ================================================= */

    div[data-testid="stDataFrame"] {
        background: #DCFCE7 !important;
        border: 1px solid #166534 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataFrame"] > div,
    div[data-testid="stDataFrame"] [role="grid"] {
        background: #DCFCE7 !important;
    }

    /* Column headers */
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #BBF7D0 !important;
        color: #14532D !important;
        border: 1px solid #166534 !important;
        font-weight: 800 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] * {
        color: #14532D !important;
        font-weight: 800 !important;
    }

    /* Table cells */
    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: #DCFCE7 !important;
        color: #14532D !important;
        border-color: #166534 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] * {
        color: #14532D !important;
    }

    /* Slight alternating shade for readability */
    div[data-testid="stDataFrame"] [role="row"]:nth-child(even) [role="gridcell"] {
        background: #D1FAE5 !important;
    }

    /* Data editor gets the same look */
    div[data-testid="stDataEditor"] {
        background: #DCFCE7 !important;
        border: 1px solid #166534 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataEditor"] [role="columnheader"] {
        background: #BBF7D0 !important;
        color: #14532D !important;
        font-weight: 800 !important;
        border-color: #166534 !important;
    }

    div[data-testid="stDataEditor"] [role="columnheader"] * {
        color: #14532D !important;
        font-weight: 800 !important;
    }

    div[data-testid="stDataEditor"] [role="gridcell"] {
        background: #DCFCE7 !important;
        color: #14532D !important;
        border-color: #166534 !important;
    }

    div[data-testid="stDataEditor"] [role="gridcell"] * {
        color: #14532D !important;
    }

    /* =================================================
       SLIDERS
       Entire rail light green
       ================================================= */

    div[data-testid="stSlider"] div[data-baseweb="slider"] > div,
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div,
    div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
        background: #86EFAC !important;
        background-color: #86EFAC !important;
    }

    /* Force every visible slider track segment to light green */
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
        background: #86EFAC !important;
        background-color: #86EFAC !important;
    }

    div[data-testid="stSlider"] div[role="slider"] {
        background: #BBF7D0 !important;
        border: 2px solid #166534 !important;
        box-shadow: 0 0 0 2px rgba(187,247,208,0.35) !important;
    }

    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        background: #DCFCE7 !important;
        color: #14532D !important;
        border: 1px solid #166534 !important;
        font-weight: 700 !important;
    }

    /* Inputs on dark background should remain readable */
/* ===== FORCE INPUT TEXT TO DARK GREEN ===== */

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #F0FDF4 !important;

    color: #14532D !important;
    -webkit-text-fill-color: #14532D !important;

    border-color: #86EFAC !important;

    font-weight: 600 !important;
    opacity: 1 !important;
}


/* Number input + and - buttons */
div[data-testid="stNumberInput"] button {
    background-color: #DCFCE7 !important;
    color: #14532D !important;
}

div[data-testid="stNumberInput"] button svg {
    fill: #14532D !important;
    color: #14532D !important;
}


/* Placeholder text */
div[data-testid="stNumberInput"] input::placeholder,
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stDateInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: #4B7A5D !important;
    -webkit-text-fill-color: #4B7A5D !important;
    opacity: 1 !important;
}


/* Focus state */
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stDateInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    color: #14532D !important;
    -webkit-text-fill-color: #14532D !important;
    border-color: #22C55E !important;
}

    /* Keep green information/metric cards dark enough for white text */
    div[data-testid="stMetric"],
    div[data-testid="stAlert"],
    .module-card,
    .sustainops-hero {
        color: #FFFFFF !important;
    }

    div[data-testid="stMetric"] *,
    div[data-testid="stAlert"] *,
    .module-card *,
    .sustainops-hero * {
        color: inherit;
    }

    
    /* =================================================
       FINAL FORM + DROPDOWN + SLIDER VISIBILITY FIXES
       ================================================= */

    /* ---------- INPUT FIELDS ---------- */
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background-color: #F0FDF4 !important;
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
        caret-color: #14532D !important;
        border-color: #86EFAC !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        background-color: #F0FDF4 !important;
        border-color: #86EFAC !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"] *,
    div[data-testid="stTextInput"] div[data-baseweb="input"] *,
    div[data-testid="stDateInput"] div[data-baseweb="input"] *,
    div[data-testid="stTextArea"] div[data-baseweb="textarea"] * {
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
    }

    div[data-testid="stNumberInput"] input::placeholder,
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stDateInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #4B7A5D !important;
        -webkit-text-fill-color: #4B7A5D !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }

    /* +/- buttons for number fields */
    div[data-testid="stNumberInput"] button {
        background-color: #DCFCE7 !important;
        color: #14532D !important;
        border-color: #86EFAC !important;
    }

    div[data-testid="stNumberInput"] button *,
    div[data-testid="stNumberInput"] button svg {
        color: #14532D !important;
        fill: #14532D !important;
        stroke: #14532D !important;
    }

    /* Date icon */
    div[data-testid="stDateInput"] svg {
        color: #14532D !important;
        fill: #14532D !important;
    }

    /* Focus state */
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stDateInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus,
    div[data-baseweb="input"] input:focus,
    div[data-baseweb="textarea"] textarea:focus {
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
        border-color: #22C55E !important;
        box-shadow: 0 0 0 1px #22C55E !important;
        outline: none !important;
    }

    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus {
        -webkit-text-fill-color: #14532D !important;
        -webkit-box-shadow: 0 0 0 1000px #F0FDF4 inset !important;
        transition: background-color 9999s ease-out 0s;
    }

    /* ---------- SELECTBOX / DROPDOWN ---------- */

    /* Closed select box */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #123A27 !important;
        border: 1px solid #86EFAC !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Dropdown arrow */
    div[data-testid="stSelectbox"] svg {
        color: #86EFAC !important;
        fill: #86EFAC !important;
        stroke: #86EFAC !important;
        opacity: 1 !important;
    }

    /* Open dropdown menu */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    ul[role="listbox"] {
        background-color: #DCFCE7 !important;
        border-color: #166534 !important;
    }

    /* Options */
    li[role="option"] {
        background-color: #DCFCE7 !important;
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
        font-weight: 600 !important;
    }

    li[role="option"] *,
    ul[role="listbox"] li * {
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
    }

    li[role="option"]:hover {
        background-color: #BBF7D0 !important;
        color: #14532D !important;
    }

    li[role="option"][aria-selected="true"] {
        background-color: #86EFAC !important;
        color: #14532D !important;
        font-weight: 800 !important;
    }

    /* ---------- MULTISELECT ---------- */

    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #123A27 !important;
        border: 1px solid #86EFAC !important;
    }

    div[data-testid="stMultiSelect"] svg {
        color: #86EFAC !important;
        fill: #86EFAC !important;
        stroke: #86EFAC !important;
        opacity: 1 !important;
    }

    span[data-baseweb="tag"] {
        background-color: #4ADE80 !important;
        border-color: #86EFAC !important;
    }

    span[data-baseweb="tag"] * {
        color: #062412 !important;
        -webkit-text-fill-color: #062412 !important;
        fill: #062412 !important;
        font-weight: 700 !important;
    }

    /* ---------- SLIDERS ---------- */

    /* Entire visible rail */
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div,
    div[data-testid="stSlider"] div[data-baseweb="slider"] > div > div,
    div[data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"],
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
        background: #86EFAC !important;
        background-color: #86EFAC !important;
    }

    /* Thumb */
    div[data-testid="stSlider"] div[role="slider"] {
        background: #BBF7D0 !important;
        background-color: #BBF7D0 !important;
        border: 2px solid #166534 !important;
        box-shadow: 0 0 0 2px rgba(187,247,208,0.35) !important;
    }

    /* Value bubble */
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {
        background: #DCFCE7 !important;
        color: #14532D !important;
        -webkit-text-fill-color: #14532D !important;
        border: 1px solid #166534 !important;
        font-weight: 700 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


def green_table_style(dataframe: pd.DataFrame):
    """Light-green table body and header with dark-green bold headings."""
    return (
        dataframe.style
        .set_properties(
            **{
                "background-color": "#DCFCE7",
                "color": "#14532D",
                "border": "1px solid #166534",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "thead th",
                    "props": [
                        ("background-color", "#BBF7D0"),
                        ("color", "#14532D"),
                        ("border", "1px solid #166534"),
                        ("font-weight", "800"),
                        ("text-align", "left"),
                    ],
                },
                {
                    "selector": "tbody td",
                    "props": [
                        ("background-color", "#DCFCE7"),
                        ("color", "#14532D"),
                        ("border", "1px solid #166534"),
                    ],
                },
                {
                    "selector": "tbody th",
                    "props": [
                        ("background-color", "#BBF7D0"),
                        ("color", "#14532D"),
                        ("border", "1px solid #166534"),
                        ("font-weight", "800"),
                    ],
                },
            ]
        )
    )


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    """Load all processed datasets used by the application."""

    files = {
        "smart_manufacturing": "smart_manufacturing_clean.csv",
        "steel_energy": "steel_energy_clean.csv",
        "logistics_orders": "logistics_orders_clean.csv",
        "freight_rates": "freight_rates_clean.csv",
        "warehouse_costs": "warehouse_costs_clean.csv",
        "warehouse_capacities": "warehouse_capacities_clean.csv",
        "products_per_plant": "products_per_plant_clean.csv",
        "vmi_customers": "vmi_customers_clean.csv",
        "plant_ports": "plant_ports_clean.csv",
    }

    datasets: dict[str, pd.DataFrame] = {}

    for dataset_name, filename in files.items():
        file_path = PROCESSED_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required processed file is missing: {file_path}"
            )

        datasets[dataset_name] = pd.read_csv(file_path)

    return datasets



def render_sidebar() -> str:
    """Render application navigation."""

    st.sidebar.title("SustainOps")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Data Overview",
            "Manufacturing",
            "Energy",
            "Logistics",
            "Scenario Simulator",
            "Opportunity Prioritisation",
            "Action Tracker",
        ],
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "Sustainability operations intelligence prototype"
    )

    return page


def render_home(datasets: dict[str, pd.DataFrame]) -> None:
    """Render the application landing page."""

    # Use st.html so the hero is rendered as HTML and never shown as a code block.
    st.html("""
<div class="sustainops-hero">
    <div class="sustainops-eyebrow">SUSTAINABILITY OPERATIONS INTELLIGENCE</div>
    <div class="sustainops-title">SustainOps Control Tower</div>
    <div class="sustainops-subtitle">
        Transforming manufacturing, energy and logistics data into sustainability
        insights, operational priorities and actionable decisions.
    </div>
</div>
""")

    total_rows = sum(len(dataframe) for dataframe in datasets.values())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Processed datasets", len(datasets))
    col2.metric("Total records", f"{total_rows:,}")
    col3.metric(
        "Manufacturing records",
        f"{len(datasets['smart_manufacturing']):,}",
    )
    col4.metric(
        "Energy records",
        f"{len(datasets['steel_energy']):,}",
    )

    st.markdown("### Application Modules")

    module_col1, module_col2, module_col3 = st.columns(3)

    with module_col1:
        st.html("""
<div class="module-card">
    <div class="module-icon">⚙️</div>
    <div class="module-title">Manufacturing Intelligence</div>
    <div class="module-text">
        Analyse production output, material efficiency, recycled content and defect rates.
    </div>
</div>
""")

    with module_col2:
        st.html("""
<div class="module-card">
    <div class="module-icon">⚡</div>
    <div class="module-title">Energy Intelligence</div>
    <div class="module-text">
        Analyse industrial electricity consumption, CO₂ emissions and load behaviour.
    </div>
</div>
""")

    with module_col3:
        st.html("""
<div class="module-card">
    <div class="module-icon">🚚</div>
    <div class="module-title">Logistics Intelligence</div>
    <div class="module-text">
        Analyse orders, freight rates, plants, ports and delivery performance.
    </div>
</div>
""")


def render_data_overview(
    datasets: dict[str, pd.DataFrame],
) -> None:
    """Show all loaded datasets and their dimensions."""

    st.title("Data Overview")

    summary_rows = []

    for dataset_name, dataframe in datasets.items():
        summary_rows.append(
            {
                "dataset": dataset_name,
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "missing_values": int(
                    dataframe.isna().sum().sum()
                ),
                "duplicate_rows": int(
                    dataframe.duplicated().sum()
                ),
            }
        )

    summary = pd.DataFrame(summary_rows)

    st.dataframe(
        green_table_style(summary),
        width="stretch",
        hide_index=True,
    )

    selected_dataset = st.selectbox(
        "Preview dataset",
        options=list(datasets.keys()),
    )

    selected_dataframe = datasets[selected_dataset]

    st.subheader(selected_dataset.replace("_", " ").title())

    st.dataframe(
        green_table_style(selected_dataframe.head(100)),
        width="stretch",
    )

def render_manufacturing(
    dataframe: pd.DataFrame,
) -> None:
    """Render the manufacturing intelligence module."""

    st.title("Manufacturing Intelligence")

    manufacturing = dataframe.copy()

    manufacturing["timestamp"] = pd.to_datetime(
        manufacturing["timestamp"],
        errors="coerce",
    )

    st.sidebar.subheader("Manufacturing Filters")

    machine_options = sorted(
        manufacturing["machine_id"].dropna().unique()
    )

    selected_machines = st.sidebar.multiselect(
        "Machine",
        options=machine_options,
        default=machine_options,
    )

    material_options = sorted(
        manufacturing["material_category"].dropna().unique()
    )

    selected_materials = st.sidebar.multiselect(
        "Material category",
        options=material_options,
        default=material_options,
    )

    minimum_date = manufacturing["timestamp"].min().date()
    maximum_date = manufacturing["timestamp"].max().date()

    selected_dates = st.sidebar.date_input(
        "Date range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
    )

    filtered = manufacturing[
        manufacturing["machine_id"].isin(selected_machines)
        & manufacturing["material_category"].isin(selected_materials)
    ].copy()

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered = filtered[
            filtered["timestamp"].dt.date.between(
                start_date,
                end_date,
            )
        ]

    if filtered.empty:
        st.warning("No manufacturing records match the selected filters.")
        return

    total_output = filtered["production_output_units"].sum()
    total_energy = filtered["energy_consumption_kwh"].sum()
    average_defect_rate = filtered["defect_rate"].mean()
    average_recycled_content = filtered["recycled_material"].mean()

    overall_energy_intensity = (
        total_energy / total_output
        if total_output > 0
        else 0
    )

    total_material = filtered["quantity_used_kg"].sum()

    overall_material_efficiency = (
        total_output / total_material
        if total_material > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Production output",
        f"{total_output:,.0f} units",
    )

    col2.metric(
        "Energy consumed",
        f"{total_energy:,.0f} kWh",
    )

    col3.metric(
        "Energy intensity",
        f"{overall_energy_intensity:.3f} kWh/unit",
    )
    
    col4.metric(
        "Average defect rate",
        f"{average_defect_rate:.2f}%",
    )

    col5, col6, col7 = st.columns(3)

    col5.metric(
        "Material used",
        f"{total_material:,.0f} kg",
    )

    col6.metric(
        "Material efficiency",
        f"{overall_material_efficiency:.2f} units/kg",
    )

    col7.metric(
        "Average recycled content",
        f"{average_recycled_content:.2f}%",
    )

    st.divider()

    machine_summary = (
        filtered.groupby("machine_id", as_index=False)
        .agg(
            production_output_units=(
                "production_output_units",
                "sum",
            ),
            energy_consumption_kwh=(
                "energy_consumption_kwh",
                "sum",
            ),
            average_defect_rate=(
                "defect_rate",
                "mean",
            ),
            average_recycled_content=(
                "recycled_material",
                "mean",
            ),
            material_used_kg=(
                "quantity_used_kg",
                "sum",
            ),
        )
    )
    machine_summary["energy_intensity_kwh_per_unit"] = (
        machine_summary["energy_consumption_kwh"]
        / machine_summary["production_output_units"].replace(0, pd.NA)
    )

    machine_summary["material_efficiency_units_per_kg"] = (
        machine_summary["production_output_units"]
        / machine_summary["material_used_kg"].replace(0, pd.NA)
    )

    energy_median = machine_summary[
        "energy_intensity_kwh_per_unit"
    ].median()

    defect_median = machine_summary[
        "average_defect_rate"
    ].median()

    material_efficiency_median = machine_summary[
        "material_efficiency_units_per_kg"
    ].median()

    recycled_content_median = machine_summary[
        "average_recycled_content"
    ].median()

    machine_summary["energy_deviation_pct"] = (
        (
            machine_summary["energy_intensity_kwh_per_unit"]
            - energy_median
        )
        / energy_median
        * 100
    )

    machine_summary["defect_deviation_pct"] = (
        (
            machine_summary["average_defect_rate"]
            - defect_median
        )
        / defect_median
        * 100
    )

    machine_summary["material_efficiency_deviation_pct"] = (
        (
            machine_summary["material_efficiency_units_per_kg"]
            - material_efficiency_median
        )
        / material_efficiency_median
        * 100
    )

    machine_summary["recycled_content_deviation_pct"] = (
        (
            machine_summary["average_recycled_content"]
            - recycled_content_median
        )
        / recycled_content_median
        * 100
    )

    machine_summary["risk_points"] = 0

    machine_summary.loc[
        machine_summary["energy_deviation_pct"] > 1,
        "risk_points",
    ] += 30

    machine_summary.loc[
        machine_summary["defect_deviation_pct"] > 1,
        "risk_points",
    ] += 30

    machine_summary.loc[
        machine_summary["material_efficiency_deviation_pct"] < -1,
        "risk_points",
    ] += 25

    machine_summary.loc[
        machine_summary["recycled_content_deviation_pct"] < -5,
        "risk_points",
    ] += 15

    machine_summary["performance_score"] = (
        100 - machine_summary["risk_points"]
    )

    machine_summary["status"] = "Healthy"

    machine_summary.loc[
        machine_summary["performance_score"] < 80,
        "status",
    ] = "Watch"

    machine_summary.loc[
        machine_summary["performance_score"] < 60,
        "status",
    ] = "Critical"
    st.subheader("Machine Health and Priority Queue")

    priority_table = machine_summary[
        [
            "machine_id",
            "performance_score",
            "status",
            "energy_deviation_pct",
            "defect_deviation_pct",
            "material_efficiency_deviation_pct",
            "recycled_content_deviation_pct",
        ]
    ].sort_values(
        "performance_score",
        ascending=True,
    )

    st.dataframe(
        green_table_style(priority_table),
        width="stretch",
        hide_index=True,
    )

    critical_count = (
        priority_table["status"]
        .eq("Critical")
        .sum()
    )

    watch_count = (
        priority_table["status"]
        .eq("Watch")
        .sum()
    )

    healthy_count = (
        priority_table["status"]
        .eq("Healthy")
        .sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Critical machines", int(critical_count))
    col2.metric("Machines to watch", int(watch_count))
    col3.metric("Healthy machines", int(healthy_count))

    st.subheader("Recommended Actions")

    machines_requiring_attention = priority_table[
        priority_table["status"] != "Healthy"
    ]

    if machines_requiring_attention.empty:
        st.success(
            "No machines currently require immediate attention."
        )
    else:
        for _, machine in machines_requiring_attention.iterrows():
            reasons = []

            if machine["energy_deviation_pct"] > 1:
                reasons.append(
                    f"Energy intensity is "
                    f"{machine['energy_deviation_pct']:.2f}% "
                    f"above the fleet median."
                )

            if machine["defect_deviation_pct"] > 1:
                reasons.append(
                    f"Defect rate is "
                    f"{machine['defect_deviation_pct']:.2f}% "
                    f"above the fleet median."
                )

            if (
                machine["material_efficiency_deviation_pct"]
                < -1
            ):
                reasons.append(
                    f"Material efficiency is "
                    f"{abs(machine['material_efficiency_deviation_pct']):.2f}% "
                    f"below the fleet median."
                )

            if (
                machine["recycled_content_deviation_pct"]
                < -5
            ):
                reasons.append(
                    f"Recycled-material usage is "
                    f"{abs(machine['recycled_content_deviation_pct']):.2f}% "
                    f"below the fleet median."
                )

            reason_text = " ".join(reasons)

            if machine["status"] == "Critical":
                st.error(
                    f"""
                    **Machine {machine['machine_id']} — Critical**

                    Performance score:
                    `{machine['performance_score']:.0f}/100`

                    {reason_text}

                    **Recommended action:** Inspect machine calibration,
                    review recent material batches, and compare the
                    machine's recent operating conditions with normal
                    performance.
                    """
                )

            elif machine["status"] == "Watch":
                st.warning(
                    f"""
                    **Machine {machine['machine_id']} — Watch**

                    Performance score:
                    `{machine['performance_score']:.0f}/100`

                    {reason_text}

                    **Recommended action:** Monitor the next production
                    cycle and review energy consumption, defect rate,
                    and material efficiency.
                    """
                )
    
def render_energy(
    dataframe: pd.DataFrame,
) -> None:
    """Render the industrial energy intelligence module."""

    st.title("Energy Intelligence")

    energy = dataframe.copy()

    energy["date"] = pd.to_datetime(
        energy["date"],
        errors="coerce",
    )

    energy = energy.dropna(
        subset=[
            "date",
            "energy_usage_kwh",
            "co2_emissions_tco2",
        ]
    )

    st.sidebar.subheader("Energy Filters")

    load_types = sorted(energy["load_type"].dropna().unique())
    selected_load_types = st.sidebar.multiselect(
        "Load type",
        options=load_types,
        default=load_types,
    )

    day_options = sorted(energy["day_of_week"].dropna().unique())
    selected_days = st.sidebar.multiselect(
        "Day of week",
        options=day_options,
        default=day_options,
    )

    minimum_date = energy["date"].min().date()
    maximum_date = energy["date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Energy date range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
    )

    filtered = energy[
        energy["load_type"].isin(selected_load_types)
        & energy["day_of_week"].isin(selected_days)
    ].copy()

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = filtered[
            filtered["date"].dt.date.between(start_date, end_date)
        ]

    if filtered.empty:
        st.warning("No energy records match the selected filters.")
        return

    total_energy = filtered["energy_usage_kwh"].sum()
    total_co2 = filtered["co2_emissions_tco2"].sum()
    average_energy = filtered["energy_usage_kwh"].mean()
    peak_energy = filtered["energy_usage_kwh"].max()
    overall_co2_intensity = total_co2 / total_energy if total_energy > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total energy use", f"{total_energy:,.0f} kWh")
    col2.metric("Total CO₂ emissions", f"{total_co2:,.2f} tCO₂")
    col3.metric("Average interval use", f"{average_energy:,.2f} kWh")
    col4.metric("Peak interval use", f"{peak_energy:,.2f} kWh")
    st.metric("CO₂ intensity", f"{overall_co2_intensity:.6f} tCO₂/kWh")

    st.divider()

    hourly_summary = (
        filtered.groupby("hour", as_index=False)
        .agg(
            average_energy_usage_kwh=("energy_usage_kwh", "mean"),
            average_co2_emissions_tco2=("co2_emissions_tco2", "mean"),
        )
    )

    chart_col1, chart_col2 = st.columns(2)

    # ENERGY CHART
    with chart_col1:
        energy_fig = go.Figure()

        energy_fig.add_trace(
            go.Scatter(
                x=hourly_summary["hour"],
                y=hourly_summary["average_energy_usage_kwh"],
                mode="lines+markers",
                name="Energy Use",
                line=dict(color="#22C55E", width=4, shape="spline"),
                marker=dict(
                    size=7,
                    color="#86EFAC",
                    line=dict(width=2, color="#14532D"),
                ),
                fill="tozeroy",
                fillcolor="rgba(34, 197, 94, 0.12)",
                hovertemplate=(
                    "<b>Hour %{x}:00</b><br>"
                    "Energy: %{y:.2f} kWh"
                    "<extra></extra>"
                ),
            )
        )

        energy_fig.update_layout(
            title={
                "text": "⚡ Average Energy Use by Hour",
                "x": 0.02,
                "xanchor": "left",
                "font": {"color": "#FFFFFF", "size": 20},
            },
            height=430,
            margin=dict(l=20, r=20, t=65, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.025)",
            font=dict(color="#FFFFFF", size=13),
            hovermode="x unified",
            showlegend=False,
            xaxis=dict(
                title="Hour of Day",
                showgrid=False,
                tickmode="linear",
                dtick=2,
                color="#FFFFFF",
            ),
            yaxis=dict(
                title="Energy Use (kWh)",
                gridcolor="rgba(255,255,255,0.10)",
                zeroline=False,
                color="#FFFFFF",
            ),
        )

        st.plotly_chart(
            energy_fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    # CO2 CHART
    with chart_col2:
        co2_fig = go.Figure()

        co2_fig.add_trace(
            go.Scatter(
                x=hourly_summary["hour"],
                y=hourly_summary["average_co2_emissions_tco2"],
                mode="lines+markers",
                name="CO₂ Emissions",
                line=dict(color="#4ADE80", width=4, shape="spline"),
                marker=dict(
                    size=7,
                    color="#FFFFFF",
                    line=dict(width=2, color="#22C55E"),
                ),
                fill="tozeroy",
                fillcolor="rgba(74, 222, 128, 0.10)",
                hovertemplate=(
                    "<b>Hour %{x}:00</b><br>"
                    "CO₂: %{y:.4f} tCO₂"
                    "<extra></extra>"
                ),
            )
        )

        co2_fig.update_layout(
            title={
                "text": "🌱 Average CO₂ Emissions by Hour",
                "x": 0.02,
                "xanchor": "left",
                "font": {"color": "#FFFFFF", "size": 20},
            },
            height=430,
            margin=dict(l=20, r=20, t=65, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.025)",
            font=dict(color="#FFFFFF", size=13),
            hovermode="x unified",
            showlegend=False,
            xaxis=dict(
                title="Hour of Day",
                showgrid=False,
                tickmode="linear",
                dtick=2,
                color="#FFFFFF",
            ),
            yaxis=dict(
                title="CO₂ Emissions (tCO₂)",
                gridcolor="rgba(255,255,255,0.10)",
                zeroline=False,
                color="#FFFFFF",
            ),
        )

        st.plotly_chart(
            co2_fig,
            width="stretch",
            config={"displayModeBar": False},
        )

    st.subheader("Energy anomaly detection")

    sensitivity = st.slider(
        "Anomaly sensitivity",
        min_value=1.0,
        max_value=6.0,
        value=4.0,
        step=0.1,
        help=(
            "Higher values detect fewer anomalies. The model compares each "
            "record with observations from the same load type, day type and hour."
        ),
    )

    anomaly_data = filtered.sort_values("date").copy()
    anomaly_data["day_type"] = anomaly_data["week_status"].fillna("Unknown")
    anomaly_data["minute_slot"] = (
        anomaly_data["date"].dt.hour * 4
        + anomaly_data["date"].dt.minute // 15
    )

    baseline_group_columns = ["load_type", "day_type", "minute_slot"]

    anomaly_data["expected_energy_kwh"] = (
        anomaly_data.groupby(baseline_group_columns)["energy_usage_kwh"]
        .transform("median")
    )

    anomaly_data["absolute_deviation"] = (
        anomaly_data["energy_usage_kwh"]
        - anomaly_data["expected_energy_kwh"]
    ).abs()

    anomaly_data["mad"] = (
        anomaly_data.groupby(baseline_group_columns)["absolute_deviation"]
        .transform("median")
        .replace(0, pd.NA)
    )

    anomaly_data["robust_anomaly_score"] = (
        0.6745
        * (
            anomaly_data["energy_usage_kwh"]
            - anomaly_data["expected_energy_kwh"]
        ).abs()
        / anomaly_data["mad"]
    )

    anomaly_data["deviation_pct"] = (
        (
            anomaly_data["energy_usage_kwh"]
            - anomaly_data["expected_energy_kwh"]
        )
        / anomaly_data["expected_energy_kwh"].replace(0, pd.NA)
        * 100
    )

    anomaly_data["absolute_difference_kwh"] = (
        anomaly_data["energy_usage_kwh"]
        - anomaly_data["expected_energy_kwh"]
    ).abs()

    anomaly_data["is_anomaly"] = (
        (anomaly_data["robust_anomaly_score"] > sensitivity)
        & (anomaly_data["absolute_difference_kwh"] >= 15)
        & (anomaly_data["expected_energy_kwh"] >= 10)
    )

    anomalies = anomaly_data[anomaly_data["is_anomaly"]].copy()

    anomaly_rate = (
        len(anomalies) / len(anomaly_data) * 100
        if len(anomaly_data) > 0
        else 0
    )

    anomaly_col1, anomaly_col2, anomaly_col3 = st.columns(3)
    anomaly_col1.metric("Detected anomalies", f"{len(anomalies):,}")
    anomaly_col2.metric("Anomaly rate", f"{anomaly_rate:.2f}%")

    maximum_deviation = (
        anomalies["deviation_pct"].abs().max()
        if not anomalies.empty
        else 0
    )

    anomaly_col3.metric("Largest deviation", f"{maximum_deviation:.2f}%")
    st.subheader("Detected anomaly records")

    if anomalies.empty:
        st.success("No significant energy anomalies were detected.")
        return

    anomaly_display = anomalies[
        [
            "date",
            "energy_usage_kwh",
            "expected_energy_kwh",
            "deviation_pct",
            "robust_anomaly_score",
            "co2_emissions_tco2",
            "load_type",
            "day_type",
            "day_of_week",
            "hour",
        ]
    ].sort_values("robust_anomaly_score", ascending=False)

    st.dataframe(
        green_table_style(anomaly_display.head(100)),
        width="stretch",
        hide_index=True,
    )

    most_severe = anomaly_display.iloc[0]

    st.error(
        f"""
        **Most severe anomaly**

        Date: `{most_severe['date']}`

        Actual energy use: `{most_severe['energy_usage_kwh']:.2f} kWh`

        Expected consumption for similar conditions:
        `{most_severe['expected_energy_kwh']:.2f} kWh`

        Deviation: `{most_severe['deviation_pct']:.2f}%`

        Robust anomaly score: `{most_severe['robust_anomaly_score']:.2f}`

        Load type: `{most_severe['load_type']}`

        **Recommended investigation:** Check production load, equipment
        operating status, shutdown schedules and unusual reactive-power
        behaviour during this interval.
        """
    )

def render_logistics(
    orders: pd.DataFrame,
    freight_rates: pd.DataFrame,
    warehouse_costs: pd.DataFrame,
    warehouse_capacities: pd.DataFrame,
) -> None:
    """Render the logistics intelligence module."""

    st.title("Logistics Intelligence")

    logistics = orders.copy()

    logistics["order_date"] = pd.to_datetime(
        logistics["order_date"],
        errors="coerce",
    )

    logistics = logistics.dropna(
        subset=[
            "order_date",
            "order_id",
            "carrier",
            "plant_code",
            "origin_port",
            "destination_port",
        ]
    )

    st.sidebar.subheader("Logistics Filters")

    carrier_options = sorted(
        logistics["carrier"].dropna().unique()
    )

    selected_carriers = st.sidebar.multiselect(
        "Carrier",
        options=carrier_options,
        default=carrier_options,
    )

    plant_options = sorted(
        logistics["plant_code"].dropna().unique()
    )

    selected_plants = st.sidebar.multiselect(
        "Plant",
        options=plant_options,
        default=plant_options,
    )

    service_options = sorted(
        logistics["service_level"].dropna().unique()
    )

    selected_services = st.sidebar.multiselect(
        "Service level",
        options=service_options,
        default=service_options,
    )

    filtered = logistics[
        logistics["carrier"].isin(selected_carriers)
        & logistics["plant_code"].isin(selected_plants)
        & logistics["service_level"].isin(selected_services)
    ].copy()

    if filtered.empty:
        st.warning(
            "No logistics records match the selected filters."
        )
        return

    total_orders = len(filtered)

    late_orders = int(
        filtered["is_late"].fillna(False).sum()
    )

    late_rate = (
        late_orders / total_orders * 100
        if total_orders > 0
        else 0
    )

    total_units = filtered["unit_quantity"].sum()
    total_weight = filtered["total_weight"].sum()

    average_transport_time = filtered["tpt"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total orders",
        f"{total_orders:,}",
    )

    col2.metric(
        "Late orders",
        f"{late_orders:,}",
    )

    col3.metric(
        "Late-delivery rate",
        f"{late_rate:.2f}%",
    )

    col4.metric(
        "Average transport time",
        f"{average_transport_time:.2f} days",
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "Total units",
        f"{total_units:,.0f}",
    )

    col6.metric(
        "Total shipment weight",
        f"{total_weight:,.0f}",
    )

    st.divider()

    carrier_summary = (
        filtered.groupby("carrier", as_index=False)
        .agg(
            total_orders=("order_id", "count"),
            late_orders=("is_late", "sum"),
            average_transport_time=("tpt", "mean"),
            total_units=("unit_quantity", "sum"),
            total_weight=("total_weight", "sum"),
        )
    )

    carrier_summary["late_delivery_rate_pct"] = (
        carrier_summary["late_orders"]
        / carrier_summary["total_orders"]
        * 100
    )

    st.subheader("Carrier Performance")

    st.dataframe(
        green_table_style(
            carrier_summary.sort_values(
                "late_delivery_rate_pct",
                ascending=False,
            )
        ),
        width="stretch",
        hide_index=True,
    )

    st.divider()

    st.subheader("Shipment Intervention Queue")

    carrier_risk = carrier_summary[
        [
            "carrier",
            "late_delivery_rate_pct",
        ]
    ].copy()

    intervention = filtered.merge(
        carrier_risk,
        on="carrier",
        how="left",
    )

    intervention["priority_score"] = 0

    intervention.loc[
        intervention["ship_late_day_count"] > 0,
        "priority_score",
    ] += 40

    intervention.loc[
        intervention["ship_late_day_count"] >= 2,
        "priority_score",
    ] += 20

    intervention.loc[
        intervention["late_delivery_rate_pct"] > 2,
        "priority_score",
    ] += 20

    intervention.loc[
        intervention["tpt"] > filtered["tpt"].median(),
        "priority_score",
    ] += 10

    intervention.loc[
        intervention["weight"] > filtered["weight"].quantile(0.75),
        "priority_score",
    ] += 10

    intervention["risk_level"] = "Low"

    intervention.loc[
        intervention["priority_score"] >= 30,
        "risk_level",
    ] = "Medium"

    intervention.loc[
        intervention["priority_score"] >= 60,
        "risk_level",
    ] = "High"

    intervention.loc[
        intervention["priority_score"] >= 80,
        "risk_level",
    ] = "Critical"

    priority_orders = intervention[
        intervention["priority_score"] > 0
    ][
        [
            "order_id",
            "order_date",
            "carrier",
            "plant_code",
            "origin_port",
            "destination_port",
            "service_level",
            "ship_late_day_count",
            "tpt",
            "weight",
            "late_delivery_rate_pct",
            "priority_score",
            "risk_level",
        ]
    ].sort_values(
        "priority_score",
        ascending=False,
    )
    critical_shipments = int(
        priority_orders["risk_level"].eq("Critical").sum()
    )

    high_risk_shipments = int(
        priority_orders["risk_level"].eq("High").sum()
    )

    medium_risk_shipments = int(
        priority_orders["risk_level"].eq("Medium").sum()
    )

    queue_col1, queue_col2, queue_col3 = st.columns(3)

    queue_col1.metric(
        "Critical shipments",
        critical_shipments,
    )

    queue_col2.metric(
        "High-risk shipments",
        high_risk_shipments,
    )

    queue_col3.metric(
        "Medium-risk shipments",
        medium_risk_shipments,
    )
    selected_risk_levels = st.multiselect(
        "Show risk levels",
        options=["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium"],
    )

    displayed_orders = priority_orders[
        priority_orders["risk_level"].isin(
            selected_risk_levels
        )
    ]
    st.dataframe(
        green_table_style(displayed_orders.head(100)),
        width="stretch",
        hide_index=True,
    )

    if not priority_orders.empty:
        top_shipment = priority_orders.iloc[0]

        route_options = freight_rates[
            (
                freight_rates["orig_port_cd"]
                == top_shipment["origin_port"]
            )
            & (
                freight_rates["dest_port_cd"]
                == top_shipment["destination_port"]
            )
            & (
                freight_rates["carrier"]
                != top_shipment["carrier"]
            )
        ].copy()

        if route_options.empty:
            alternative_carrier = "No route-specific alternative available"
            alternative_rate = None
            alternative_transit_days = None
        else:
            route_options = route_options.merge(
                carrier_summary[
                    [
                        "carrier",
                        "late_delivery_rate_pct",
                        "average_transport_time",
                    ]
                ],
                on="carrier",
                how="left",
            )

            route_options = route_options.sort_values(
                [
                    "late_delivery_rate_pct",
                    "rate",
                    "tpt_day_cnt",
                ],
                ascending=[True, True, True],
            )

            best_alternative = route_options.iloc[0]

            alternative_carrier = best_alternative["carrier"]
            alternative_rate = best_alternative["rate"]
            alternative_transit_days = best_alternative["tpt_day_cnt"]

        st.warning(
            f"""
            **Highest-priority shipment**

            Order: `{top_shipment['order_id']}`

            Current carrier:
            `{top_shipment['carrier']}`

            Route:
            `{top_shipment['origin_port']} → {top_shipment['destination_port']}`

            Delay:
            `{top_shipment['ship_late_day_count']:.0f} days`

            Priority score:
            `{top_shipment['priority_score']:.0f}/100`

            Risk level:
            `{top_shipment['risk_level']}`
            """
        )

        if alternative_rate is None or alternative_transit_days is None:
            st.info(
                "No route-specific alternative carrier was found in the "
                "freight-rate table for this shipment."
            )
        else:
            estimated_alternative_cost = (
                alternative_rate * top_shipment["weight"]
            )
            time_reduction = (
                top_shipment["tpt"] - alternative_transit_days
            )

            st.info(
                f"""
                **Recommended route-specific alternative**

                Carrier: `{alternative_carrier}`

                Freight rate: `${alternative_rate:,.2f}`

                Transit time: `{alternative_transit_days:.0f} days`

                Estimated time reduction: `{time_reduction:.0f} day(s)`

                Estimated transport cost:
                `${estimated_alternative_cost:,.2f}`

                Confirm route availability and obtain a final quotation
                before changing the carrier.
                """
            )


def render_scenario_simulator(
    energy_data: pd.DataFrame,
) -> None:
    """Simulate energy, emissions and cost reduction scenarios."""

    st.title("Scenario Simulator")

    st.write(
        """
        Test how operational energy-efficiency measures could affect
        electricity use, CO₂ emissions and annual operating costs.
        """
    )

    energy = energy_data.copy()

    total_energy = energy["energy_usage_kwh"].sum()
    total_co2 = energy["co2_emissions_tco2"].sum()

    current_energy_cost = st.number_input(
        "Electricity price ($/kWh)",
        min_value=0.01,
        max_value=2.00,
        value=0.18,
        step=0.01,
    )

    reduction_percentage = st.slider(
        "Expected energy reduction",
        min_value=0,
        max_value=40,
        value=10,
        step=1,
        format="%d%%",
    )

    implementation_cost = st.number_input(
        "Implementation cost ($)",
        min_value=0.0,
        value=50000.0,
        step=5000.0,
    )

    current_cost = total_energy * current_energy_cost

    energy_saving = (
        total_energy
        * reduction_percentage
        / 100
    )

    projected_energy = (
        total_energy - energy_saving
    )

    co2_reduction = (
        total_co2
        * reduction_percentage
        / 100
    )

    projected_co2 = (
        total_co2 - co2_reduction
    )

    annual_cost_saving = (
        energy_saving
        * current_energy_cost
    )

    payback_period = (
        implementation_cost / annual_cost_saving
        if annual_cost_saving > 0
        else None
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Energy reduction",
        f"{energy_saving:,.0f} kWh",
    )

    col2.metric(
        "CO₂ reduction",
        f"{co2_reduction:,.2f} tCO₂",
    )

    col3.metric(
        "Annual cost saving",
        f"${annual_cost_saving:,.2f}",
    )

    col4, col5, col6 = st.columns(3)

    col4.metric(
        "Projected energy use",
        f"{projected_energy:,.0f} kWh",
    )

    col5.metric(
        "Projected CO₂ emissions",
        f"{projected_co2:,.2f} tCO₂",
    )

    col6.metric(
        "Payback period",
        (
            f"{payback_period:.2f} years"
            if payback_period is not None
            else "N/A"
        ),
    )

    st.subheader("Scenario comparison")

    comparison = pd.DataFrame(
        {
            "Metric": [
                "Energy use (kWh)",
                "CO₂ emissions (tCO₂)",
                "Energy cost ($)",
            ],
            "Current": [
                total_energy,
                total_co2,
                current_cost,
            ],
            "Scenario": [
                projected_energy,
                projected_co2,
                current_cost - annual_cost_saving,
            ],
            "Improvement": [
                energy_saving,
                co2_reduction,
                annual_cost_saving,
            ],
        }
    )

    st.dataframe(
        green_table_style(comparison),
        width="stretch",
        hide_index=True,
    )
    net_five_year_benefit = (
        annual_cost_saving * 5
        - implementation_cost
    )

    if reduction_percentage == 0:
        decision_rating = "No change"
        decision_message = (
            "Increase the expected reduction percentage to test "
            "an improvement scenario."
        )

    elif (
        payback_period is not None
        and payback_period <= 3
        and net_five_year_benefit > 0
    ):
        decision_rating = "Recommended"
        decision_message = (
            "The scenario has a payback period of three years or less "
            "and creates a positive estimated five-year financial benefit."
        )

    elif (
        payback_period is not None
        and payback_period <= 5
        and net_five_year_benefit > 0
    ):
        decision_rating = "Review"
        decision_message = (
            "The scenario creates a positive five-year benefit, but the "
            "payback period is longer than three years."
        )

    else:
        decision_rating = "Not attractive"
        decision_message = (
            "The estimated savings do not justify the implementation "
            "cost under the current assumptions."
        )

    st.subheader("Decision Assessment")

    assessment_col1, assessment_col2 = st.columns(2)

    assessment_col1.metric(
        "Scenario rating",
        decision_rating,
    )

    assessment_col2.metric(
        "Five-year net benefit",
        f"${net_five_year_benefit:,.2f}",
    )

    st.info(decision_message)

    if (
        payback_period is not None
        and payback_period <= 3
        and reduction_percentage > 0
    ):
        st.success(
            """
            This scenario appears financially attractive because the
            estimated payback period is three years or less.
            """
        )

    elif reduction_percentage > 0:
        st.warning(
            """
            This scenario reduces energy use and emissions, but the
            estimated payback period is longer than three years.
            Review implementation cost or identify additional savings.
            """
        )

def render_opportunity_prioritisation() -> None:
    """Rank sustainability improvement opportunities."""

    st.title("Opportunity Prioritisation")

    opportunities = pd.DataFrame(
        [
            {
                "opportunity": "Compressed-air leak repair",
                "co2_reduction_tco2": 84,
                "annual_saving_usd": 31000,
                "implementation_cost_usd": 12000,
                "difficulty": 1,
                "strategic_relevance": 5,
            },
            {
                "opportunity": "High-efficiency motor replacement",
                "co2_reduction_tco2": 145,
                "annual_saving_usd": 42000,
                "implementation_cost_usd": 95000,
                "difficulty": 3,
                "strategic_relevance": 5,
            },
            {
                "opportunity": "Renewable electricity contract",
                "co2_reduction_tco2": 240,
                "annual_saving_usd": 18000,
                "implementation_cost_usd": 40000,
                "difficulty": 2,
                "strategic_relevance": 5,
            },
            {
                "opportunity": "Waste reduction on production line",
                "co2_reduction_tco2": 110,
                "annual_saving_usd": 27000,
                "implementation_cost_usd": 35000,
                "difficulty": 2,
                "strategic_relevance": 4,
            },
            {
                "opportunity": "Switch selected truck routes to rail",
                "co2_reduction_tco2": 92,
                "annual_saving_usd": 9000,
                "implementation_cost_usd": 25000,
                "difficulty": 4,
                "strategic_relevance": 4,
            },
        ]
    )

    opportunities["payback_years"] = (
        opportunities["implementation_cost_usd"]
        / opportunities["annual_saving_usd"]
    )

    opportunities["priority_score"] = (
        opportunities["co2_reduction_tco2"].rank(pct=True) * 35
        + opportunities["annual_saving_usd"].rank(pct=True) * 30
        + opportunities["strategic_relevance"] / 5 * 20
        + (6 - opportunities["difficulty"]) / 5 * 15
    ).round(1)

    opportunities["priority_level"] = "Low"

    opportunities.loc[
        opportunities["priority_score"] >= 60,
        "priority_level",
    ] = "Medium"

    opportunities.loc[
        opportunities["priority_score"] >= 75,
        "priority_level",
    ] = "High"

    opportunities.loc[
        opportunities["priority_score"] >= 90,
        "priority_level",
    ] = "Critical"

    ranked = opportunities.sort_values(
        "priority_score",
        ascending=False,
    ).reset_index(drop=True)

    st.dataframe(
        green_table_style(ranked),
        width="stretch",
        hide_index=True,
    )
    
    top_opportunity = ranked.iloc[0]

    st.subheader("Top Recommended Opportunity")

    recommendation_box = st.container(border=True)

    with recommendation_box:
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Priority score",
            f"{top_opportunity['priority_score']:.1f}/100",
        )

        col2.metric(
            "CO₂ reduction",
            f"{top_opportunity['co2_reduction_tco2']:.0f} tCO₂",
        )

        col3.metric(
            "Payback period",
            f"{top_opportunity['payback_years']:.2f} years",
        )

        st.markdown(
            f"### {top_opportunity['opportunity']}"
        )

        st.write(
            f"**Annual saving:** "
            f"${top_opportunity['annual_saving_usd']:,.2f}"
        )

        st.write(
            f"**Implementation cost:** "
            f"${top_opportunity['implementation_cost_usd']:,.2f}"
        )

        st.write(
            f"**Priority level:** "
            f"{top_opportunity['priority_level']}"
        )

        st.info(
            """
            Recommended action: validate the operational assumptions,
            confirm the implementation cost, assign an owner and move
            the opportunity into the action plan.
            """
        )
        if st.button("Add top opportunity to Action Tracker"):
            st.session_state.pending_opportunity = {
                "action_title": top_opportunity["opportunity"],
                "expected_co2_reduction_tco2": float(
                    top_opportunity["co2_reduction_tco2"]
                ),
                "expected_annual_cost_saving_usd": float(
                    top_opportunity["annual_saving_usd"]
                ),
                "priority": top_opportunity["priority_level"],
            }

            st.success(
                "Opportunity prepared for the Action Tracker."
            )


def render_action_tracker() -> None:
    """Create and track sustainability improvement actions."""

    st.title("Action Tracker")

    st.write(
        """
        Create corrective actions, assign ownership, set deadlines,
        and monitor implementation progress.
        """
    )

    if "actions" not in st.session_state:
        st.session_state.actions = load_actions()

    pending_opportunity = st.session_state.get("pending_opportunity")

    opportunity_options = [
        "Compressed-air leak repair",
        "High-efficiency motor replacement",
        "Renewable electricity contract",
        "Waste reduction on production line",
        "Switch selected truck routes to rail",
        "Custom action",
    ]

    opportunity_defaults = {
        "Compressed-air leak repair": {
            "co2": 84.0,
            "saving": 31000.0,
        },
        "High-efficiency motor replacement": {
            "co2": 145.0,
            "saving": 42000.0,
        },
        "Renewable electricity contract": {
            "co2": 240.0,
            "saving": 18000.0,
        },
        "Waste reduction on production line": {
            "co2": 110.0,
            "saving": 27000.0,
        },
        "Switch selected truck routes to rail": {
            "co2": 92.0,
            "saving": 9000.0,
        },
    }

    default_opportunity_index = 0

    if pending_opportunity:
        pending_title = pending_opportunity.get("action_title")

        if pending_title in opportunity_options:
            default_opportunity_index = opportunity_options.index(
                pending_title
            )

    selected_opportunity = st.radio(
        "Select opportunity",
        opportunity_options,
        index=default_opportunity_index,
    )

    if selected_opportunity == "Custom action":
        action_title = st.text_input("Custom action title")
        default_co2 = 0.0
        default_saving = 0.0

    else:
        action_title = selected_opportunity

        if (
            pending_opportunity
            and pending_opportunity.get("action_title")
            == selected_opportunity
        ):
            default_co2 = float(
                pending_opportunity.get(
                    "expected_co2_reduction_tco2",
                    0.0,
                )
            )

            default_saving = float(
                pending_opportunity.get(
                    "expected_annual_cost_saving_usd",
                    0.0,
                )
            )

        else:
            default_co2 = opportunity_defaults[
                selected_opportunity
            ]["co2"]

            default_saving = opportunity_defaults[
                selected_opportunity
            ]["saving"]

    priority_options = ["Low", "Medium", "High", "Critical"]
    default_priority_index = 0

    if pending_opportunity:
        pending_priority = pending_opportunity.get("priority")

        if pending_priority in priority_options:
            default_priority_index = priority_options.index(
                pending_priority
            )

    with st.form("action_form"):
        owner = st.radio(
            "Owner",
            [
                "Operations Manager",
                "Energy Manager",
                "Sustainability Manager",
                "Maintenance Team",
                "Supply Chain Manager",
                "Procurement Manager",
            ],
        )

        priority = st.radio(
            "Priority",
            priority_options,
            index=default_priority_index,
        )

        status = st.radio(
            "Status",
            ["Not started", "In progress", "Completed", "Blocked"],
        )

        deadline = st.date_input("Deadline")

        expected_co2_reduction = st.number_input(
            "Expected CO₂ reduction (tCO₂)",
            min_value=0.0,
            value=float(default_co2),
            step=1.0,
            key=f"co2_{selected_opportunity}",
        )

        expected_cost_saving = st.number_input(
            "Expected annual cost saving ($)",
            min_value=0.0,
            value=float(default_saving),
            step=1000.0,
            key=f"saving_{selected_opportunity}",
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button("Create action")

    if submitted:
        cleaned_title = action_title.strip()

        if not cleaned_title:
            st.error("Action title is required.")

        else:
            duplicate_exists = any(
                action.get("action_title", "").strip().lower()
                == cleaned_title.lower()
                and action.get("status") != "Completed"
                for action in st.session_state.actions
            )

            if duplicate_exists:
                st.warning(
                    "An open action with this title already exists."
                )

            else:
                st.session_state.actions.append(
                    {
                        "action_title": cleaned_title,
                        "owner": owner.strip(),
                        "priority": priority,
                        "status": status,
                        "deadline": deadline,
                        "expected_co2_reduction_tco2": (
                            expected_co2_reduction
                        ),
                        "expected_annual_cost_saving_usd": (
                            expected_cost_saving
                        ),
                        "notes": notes.strip(),
                    }
                )

                save_actions(st.session_state.actions)
                st.session_state.pop("pending_opportunity", None)

                st.success("Action created successfully.")

    st.subheader("Current Actions")

    if not st.session_state.actions:
        st.info("No actions have been created yet.")
        return

    actions_dataframe = pd.DataFrame(st.session_state.actions)

    total_actions = len(actions_dataframe)

    completed_actions = int(
        actions_dataframe["status"].eq("Completed").sum()
    )

    open_actions = int(
        (~actions_dataframe["status"].eq("Completed")).sum()
    )

    total_co2_reduction = actions_dataframe[
        "expected_co2_reduction_tco2"
    ].sum()

    total_cost_saving = actions_dataframe[
        "expected_annual_cost_saving_usd"
    ].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total actions", total_actions)
    col2.metric("Completed actions", completed_actions)
    col3.metric("Open actions", open_actions)
    col4.metric(
        "Expected CO₂ reduction",
        f"{total_co2_reduction:,.1f} tCO₂",
    )

    st.metric(
        "Expected annual cost saving",
        f"${total_cost_saving:,.2f}",
    )

    edited_actions = st.data_editor(
        actions_dataframe,
        width="stretch",
        hide_index=True,
        num_rows="dynamic",
        column_config={
            "priority": st.column_config.SelectboxColumn(
                "Priority",
                options=priority_options,
            ),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=[
                    "Not started",
                    "In progress",
                    "Completed",
                    "Blocked",
                ],
            ),
            "deadline": st.column_config.DateColumn("Deadline"),
            "expected_co2_reduction_tco2": (
                st.column_config.NumberColumn(
                    "Expected CO₂ reduction",
                    min_value=0.0,
                    format="%.1f tCO₂",
                )
            ),
            "expected_annual_cost_saving_usd": (
                st.column_config.NumberColumn(
                    "Expected annual saving",
                    min_value=0.0,
                    format="$%.2f",
                )
            ),
        },
        key="actions_editor",
    )

    if st.button("Save action changes"):
        cleaned_actions = edited_actions.copy()

        cleaned_actions["action_title"] = (
            cleaned_actions["action_title"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        cleaned_actions = cleaned_actions[
            ~cleaned_actions["action_title"]
            .str.lower()
            .isin(["", "none", "nan"])
        ]

        st.session_state.actions = cleaned_actions.to_dict(
            orient="records"
        )

        save_actions(st.session_state.actions)

        st.success("Action changes saved permanently.")
        st.rerun()

def render_placeholder(page_name: str) -> None:
    """Render a temporary module page."""

    st.title(page_name)
    st.info(
        f"The {page_name.lower()} module will be built next."
    )


def main() -> None:
    """Run the Streamlit application."""

    try:
        datasets = load_data()
    except FileNotFoundError as error:
        st.error(str(error))
        st.stop()

    selected_page = render_sidebar()

    if selected_page == "Home":
        render_home(datasets)

    elif selected_page == "Data Overview":
        render_data_overview(datasets)

    elif selected_page == "Manufacturing":
        render_manufacturing(
            datasets["smart_manufacturing"]
    )

    elif selected_page == "Energy":
        render_energy(
            datasets["steel_energy"]
    )
    
    elif selected_page == "Logistics":
        render_logistics(
            datasets["logistics_orders"],
            datasets["freight_rates"],
            datasets["warehouse_costs"],
            datasets["warehouse_capacities"], 
    )

    elif selected_page == "Scenario Simulator":
        render_scenario_simulator(
            datasets["steel_energy"]
    )

    elif selected_page == "Opportunity Prioritisation":
        render_opportunity_prioritisation()

    elif selected_page == "Action Tracker":
        render_action_tracker()


if __name__ == "__main__":
    main()  