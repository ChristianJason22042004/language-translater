import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch

# ══════════════════════════════════════════════
#  MODEL CACHE
# ══════════════════════════════════════════════
@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model     = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model


# ══════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════
MODELS = {
    "en-hi": "Helsinki-NLP/opus-mt-en-hi",
    "hi-en": "Helsinki-NLP/opus-mt-hi-en",
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
}

LANGUAGES = {
    "English": {"code": "en", "flag": "🇬🇧", "native": "English"},
    "Hindi":   {"code": "hi", "flag": "🇮🇳", "native": "हिन्दी"},
    "Spanish": {"code": "es", "flag": "🇪🇸", "native": "Español"},
    "French":  {"code": "fr", "flag": "🇫🇷", "native": "Français"},
}


# ══════════════════════════════════════════════
#  TRANSLATION
# ══════════════════════════════════════════════
def translate(text: str, src_code: str, tgt_code: str) -> str | None:
    key = f"{src_code}-{tgt_code}"
    if key not in MODELS:
        return None
    tokenizer, model = load_model(MODELS[key])
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        tokens = model.generate(**inputs, num_beams=4, early_stopping=True)
    return tokenizer.decode(tokens[0], skip_special_tokens=True)


# ══════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════
st.set_page_config(page_title="Vernā", page_icon="🗣️", layout="centered")


# ══════════════════════════════════════════════
#  CSS  — Warm paper · editorial · minimal
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Outfit:wght@300;400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #FAFAF7 !important;
    font-family: 'Outfit', sans-serif;
    color: #18181A;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    max-width: 680px !important;
    padding: 3.5rem 1.8rem 5rem !important;
}

/* ── Header ── */
.verna-header {
    text-align: center;
    margin-bottom: 3rem;
}

.verna-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.8rem;
    font-weight: 600;
    letter-spacing: -0.03em;
    color: #18181A;
    line-height: 1;
    display: block;
}

.verna-logo em {
    font-style: italic;
    color: #5C6BC0;
}

.verna-tagline {
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #9E9E9E;
    margin-top: 0.5rem;
    display: block;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: #F0F4FF;
    border: 1px solid #C5CAE9;
    border-radius: 99px;
    padding: 0.3rem 0.9rem;
    font-size: 0.72rem;
    font-weight: 400;
    color: #5C6BC0;
    letter-spacing: 0.06em;
    margin-top: 1rem;
}

.status-dot {
    width: 5px; height: 5px;
    background: #66BB6A;
    border-radius: 50%;
    box-shadow: 0 0 0 2.5px rgba(102,187,106,0.3);
    flex-shrink: 0;
}

/* ── Language panel ── */
.lang-panel {
    background: #FFFFFF;
    border: 1px solid #EBEBEA;
    border-radius: 20px;
    padding: 0.2rem 0.2rem 0.8rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #FAFAF7 !important;
    border: 1px solid #E8E8E6 !important;
    border-radius: 12px !important;
    color: #18181A !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 400 !important;
}
.stSelectbox label {
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #AEAEAD !important;
    font-family: 'Outfit', sans-serif !important;
}

/* ── Divider with arrow ── */
.arrow-divider {
    text-align: center;
    padding: 0.6rem 0;
    font-size: 0.85rem;
    color: #CFCFCC;
    letter-spacing: 0.08em;
    user-select: none;
    font-family: 'Outfit', sans-serif;
}

/* ── Textarea ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #EBEBEA !important;
    border-radius: 16px !important;
    color: #18181A !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 300 !important;
    line-height: 1.75 !important;
    padding: 1.2rem 1.4rem !important;
    resize: none !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}
.stTextArea textarea:focus {
    border-color: #9FA8DA !important;
    box-shadow: 0 0 0 3px rgba(92,107,192,0.08) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #C8C8C4 !important; font-weight: 300 !important; }

/* ── Char counter ── */
.char-count {
    text-align: right;
    font-size: 0.68rem;
    color: #C8C8C4;
    margin-top: -0.6rem;
    margin-bottom: 0.8rem;
    font-family: 'Outfit', sans-serif;
}

/* ── Translate button ── */
.stButton > button {
    width: 100% !important;
    background: #18181A !important;
    color: #FAFAF7 !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.9rem !important;
    transition: background 0.18s ease, transform 0.12s ease !important;
    margin-top: 0.2rem !important;
}
.stButton > button:hover {
    background: #2C2C30 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: scale(0.99) !important; }

/* ── Result card ── */
.result-outer {
    margin-top: 1.4rem;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06), 0 8px 32px rgba(0,0,0,0.05);
}

.result-header {
    background: #18181A;
    padding: 0.75rem 1.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.result-lang-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #6B6B72;
}

.result-flag-name {
    font-size: 0.82rem;
    font-weight: 400;
    color: #F0EEE8;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.result-body {
    background: #1E1E22;
    padding: 1.6rem 1.4rem 1.8rem;
}

.result-translation {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.6rem;
    font-weight: 400;
    line-height: 1.6;
    color: #F5F3EE;
    letter-spacing: -0.01em;
}

.result-native {
    font-size: 0.7rem;
    font-weight: 300;
    color: #5C6BC0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 1.1rem;
    opacity: 0.9;
}

/* ── Unsupported pair banner ── */
.unsupported-banner {
    background: #FFF8F0;
    border: 1px solid #FFD49A;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    font-size: 0.88rem;
    color: #8A5A00;
    margin-top: 1rem;
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
}

/* ── Supported pairs hint ── */
.pairs-hint {
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1.8rem;
    border-top: 1px solid #EBEBEA;
}
.pairs-hint-title {
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #C8C8C4;
    margin-bottom: 0.7rem;
}
.pairs-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    justify-content: center;
}
.pair-chip {
    font-size: 0.72rem;
    font-weight: 400;
    color: #8A8A86;
    background: #F4F4F2;
    border: 1px solid #EBEBEA;
    border-radius: 99px;
    padding: 0.22rem 0.75rem;
    font-family: 'Outfit', sans-serif;
}

/* ── Warning ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════
st.markdown("""
<div class="verna-header">
    <span class="verna-logo">Vern<em>ā</em></span>
    <span class="verna-tagline">Offline Neural Translation</span>
    <br>
    <span class="status-pill">
        <span class="status-dot"></span>
        Private &nbsp;·&nbsp; Runs locally &nbsp;·&nbsp; No data transmitted
    </span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  LANGUAGE SELECTORS
# ══════════════════════════════════════════════
lang_names = list(LANGUAGES.keys())

col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    src_name = st.selectbox(
        "From",
        lang_names,
        index=0,
        format_func=lambda x: f"{LANGUAGES[x]['flag']}  {x}"
    )

with col2:
    tgt_options = [l for l in lang_names if l != src_name]
    tgt_name = st.selectbox(
        "To",
        tgt_options,
        index=0,
        format_func=lambda x: f"{LANGUAGES[x]['flag']}  {x}"
    )

src_code = LANGUAGES[src_name]["code"]
tgt_code = LANGUAGES[tgt_name]["code"]
pair_supported = f"{src_code}-{tgt_code}" in MODELS


# ══════════════════════════════════════════════
#  INPUT
# ══════════════════════════════════════════════
input_text = st.text_area(
    "input",
    placeholder=f"Write in {src_name}…",
    height=168,
    max_chars=600,
    label_visibility="collapsed",
    key="input_area"
)

char_count = len(input_text)
st.markdown(
    f'<div class="char-count">{char_count} / 600</div>',
    unsafe_allow_html=True
)

# Unsupported pair inline warning (before button press)
if not pair_supported:
    st.markdown(f"""
    <div class="unsupported-banner">
        <span>⚠️</span>
        <span>
            <strong>{src_name} → {tgt_name}</strong> is not yet supported.
            Supported pairs: English ↔ Hindi, English ↔ Spanish, English ↔ French.
        </span>
    </div>
    """, unsafe_allow_html=True)

btn_label = "Translate" if pair_supported else "Pair Not Supported"
clicked = st.button(btn_label, disabled=(not pair_supported), use_container_width=True)


# ══════════════════════════════════════════════
#  RESULT
# ══════════════════════════════════════════════
if clicked:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Loading model…"):
            output = translate(input_text, src_code, tgt_code)

        if output:
            tgt_flag   = LANGUAGES[tgt_name]["flag"]
            tgt_native = LANGUAGES[tgt_name]["native"]
            st.markdown(f"""
            <div class="result-outer">
                <div class="result-header">
                    <span class="result-lang-label">Translation</span>
                    <span class="result-flag-name">{tgt_flag} &nbsp;{tgt_name}</span>
                </div>
                <div class="result-body">
                    <div class="result-translation">{output}</div>
                    <div class="result-native">{tgt_native}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Translation failed. Please try again.")


# ══════════════════════════════════════════════
#  SUPPORTED PAIRS FOOTER
# ══════════════════════════════════════════════
pairs_display = [
    "🇬🇧 EN → 🇮🇳 HI", "🇮🇳 HI → 🇬🇧 EN",
    "🇬🇧 EN → 🇪🇸 ES", "🇪🇸 ES → 🇬🇧 EN",
    "🇬🇧 EN → 🇫🇷 FR", "🇫🇷 FR → 🇬🇧 EN",
]
chips = "".join(f'<span class="pair-chip">{p}</span>' for p in pairs_display)
st.markdown(f"""
<div class="pairs-hint">
    <div class="pairs-hint-title">Supported Language Pairs</div>
    <div class="pairs-grid">{chips}</div>
</div>
""", unsafe_allow_html=True)
