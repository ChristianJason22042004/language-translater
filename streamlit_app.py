import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch

# ================== MODEL CACHE ==================
@st.cache_resource(show_spinner=False)
def load_translation_model(model_name: str):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model


# ================== SUPPORTED MODELS ==================
MODELS = {
    "en-hi": "Helsinki-NLP/opus-mt-en-hi",
    "hi-en": "Helsinki-NLP/opus-mt-hi-en",
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
}

LANGUAGE_FLAGS = {
    "English": "🇬🇧",
    "Hindi": "🇮🇳",
    "Spanish": "🇪🇸",
    "French": "🇫🇷",
}

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
}


# ================== TRANSLATION LOGIC ==================
def translate_text(text: str, source: str, target: str) -> str:
    model_key = f"{source}-{target}"
    if model_key not in MODELS:
        return None
    tokenizer, model = load_translation_model(MODELS[model_key])
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Translucent — AI Translator",
    page_icon="🌐",
    layout="centered"
)

# ================== CSS ==================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background-color: #F7F4EF !important;
    font-family: 'DM Sans', sans-serif;
    color: #1a1a18;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 700px !important;
    padding: 3rem 1.5rem 4rem !important;
}

/* ── Wordmark ── */
.wordmark {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    letter-spacing: -0.02em;
    color: #1a1a18;
    text-align: center;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.tagline {
    text-align: center;
    font-size: 0.82rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8a8070;
    margin-bottom: 2.8rem;
}

/* ── Language Selector Card ── */
.lang-card {
    background: #FFFFFF;
    border: 1px solid #E4DECE;
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.04);
}
.lang-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8a8070;
    margin-bottom: 0.5rem;
}

/* ── Selectbox override ── */
.stSelectbox > div > div {
    background: #F7F4EF !important;
    border: 1px solid #D9D0C0 !important;
    border-radius: 12px !important;
    color: #1a1a18 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}

/* ── Text areas ── */
.stTextArea label { display: none !important; }
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #E4DECE !important;
    border-radius: 16px !important;
    color: #1a1a18 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    line-height: 1.65 !important;
    padding: 1.1rem 1.2rem !important;
    resize: none !important;
    box-shadow: 0 2px 20px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus {
    border-color: #B8A890 !important;
    box-shadow: 0 0 0 3px rgba(184,168,144,0.15) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #B0A494 !important; }

/* ── Translate Button ── */
.stButton > button {
    width: 100% !important;
    background: #1a1a18 !important;
    color: #F7F4EF !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    padding: 0.85rem 1rem !important;
    cursor: pointer !important;
    transition: background 0.2s ease, transform 0.15s ease !important;
    margin-top: 0.4rem !important;
}
.stButton > button:hover {
    background: #333330 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Divider arrow ── */
.swap-arrow {
    text-align: center;
    font-size: 1.3rem;
    color: #B0A494;
    margin: -0.3rem 0 0.6rem;
    user-select: none;
}

/* ── Result card ── */
.result-card {
    background: #1a1a18;
    border-radius: 20px;
    padding: 1.8rem;
    margin-top: 1.4rem;
    box-shadow: 0 4px 30px rgba(0,0,0,0.12);
}
.result-lang-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #8a8070;
    background: #2a2a28;
    border-radius: 8px;
    padding: 0.25rem 0.65rem;
    margin-bottom: 1rem;
}
.result-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    line-height: 1.6;
    color: #F7F4EF;
    letter-spacing: -0.01em;
}

/* ── Warning / info overrides ── */
.stWarning, .stInfo {
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Spinner ── */
.stSpinner { color: #1a1a18 !important; }

/* ── Offline badge ── */
.offline-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 400;
    color: #8a8070;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2.2rem;
}
.offline-dot {
    width: 6px; height: 6px;
    background: #7DB87D;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 0 3px rgba(125,184,125,0.25);
}
</style>
""", unsafe_allow_html=True)


# ================== UI ==================

st.markdown('<div class="wordmark">Translucent</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">Offline Neural Translation</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="offline-badge"><span class="offline-dot"></span> Running locally · No data leaves your machine</div>',
    unsafe_allow_html=True
)

# Language pickers
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox(
        "From",
        list(LANGUAGES.keys()),
        format_func=lambda x: f"{LANGUAGE_FLAGS[x]}  {x}"
    )
with col2:
    tgt_lang = st.selectbox(
        "To",
        [l for l in LANGUAGES.keys() if l != src_lang],
        format_func=lambda x: f"{LANGUAGE_FLAGS[x]}  {x}"
    )

# Input
input_text = st.text_area(
    "Input",
    placeholder=f"Type something in {src_lang}…",
    height=160,
    label_visibility="collapsed"
)

translate_clicked = st.button("Translate  →")

# ── Result ──
if translate_clicked:
    if not input_text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Loading model & translating…"):
            result = translate_text(
                input_text,
                LANGUAGES[src_lang],
                LANGUAGES[tgt_lang]
            )

        if result is None:
            st.warning(
                f"The **{src_lang} → {tgt_lang}** pair isn't supported yet. "
                "Try a different combination."
            )
        else:
            flag = LANGUAGE_FLAGS[tgt_lang]
            st.markdown(f"""
            <div class="result-card">
                <div class="result-lang-badge">{flag} {tgt_lang}</div>
                <div class="result-text">{result}</div>
            </div>
            """, unsafe_allow_html=True)
