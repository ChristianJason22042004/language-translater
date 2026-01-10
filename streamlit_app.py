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


# ================== TRANSLATION LOGIC ==================
def translate_text(text: str, source: str, target: str) -> str:
    model_key = f"{source}-{target}"

    if model_key not in MODELS:
        return "❌ This language pair is currently not supported."

    tokenizer, model = load_translation_model(MODELS[model_key])

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    with torch.no_grad():
        outputs = model.generate(**inputs)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# ================== STREAMLIT CONFIG ==================
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)


# ================== PROFESSIONAL UI CSS ==================
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #f8fafc;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

h1, h2, h3 {
    text-align: center;
    font-weight: 600;
}

.block-container {
    max-width: 720px;
    padding-top: 2rem;
}

.stTextArea textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 14px;
    border: 1px solid #334155;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border-radius: 14px;
    font-weight: 600;
    padding: 0.7rem;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #1e40af) !important;
    transform: scale(1.02);
}

.info-card {
    background-color: #020617;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
}

@media (max-width: 600px) {
    .stTextArea textarea {
        font-size: 1.1rem;
    }
}
</style>
""", unsafe_allow_html=True)


# ================== UI ==================
st.title("🌍 AI Language Translator")
st.markdown(
    "<p style='text-align:center; opacity:0.85;'>Offline Neural Translation • Secure • Fast</p>",
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
This translator uses <b>offline neural models</b> powered by HuggingFace MarianMT.
No internet calls are made after model download.
</div>
""", unsafe_allow_html=True)

# Language mapping
languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr"
}

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("Source Language", list(languages.keys()))
with col2:
    tgt_lang = st.selectbox("Target Language", list(languages.keys()))

input_text = st.text_area(
    "Text to Translate",
    placeholder="Type or paste your text here..."
)

if st.button("Translate"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to translate.")
    elif src_lang == tgt_lang:
        st.info("ℹ️ Source and target languages are the same.")
    else:
        with st.spinner("Translating text..."):
            translation = translate_text(
                input_text,
                languages[src_lang],
                languages[tgt_lang]
            )

        st.success("✅ Translation completed successfully")
        st.text_area(
            "Translated Output",
            translation,
            height=190
        )
