import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import torch

# ---------------- MODEL CACHE ----------------
@st.cache_resource
def load_model(model_name):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# ---------------- SUPPORTED MODELS ----------------
MODELS = {
    "en-hi": "Helsinki-NLP/opus-mt-en-hi",
    "hi-en": "Helsinki-NLP/opus-mt-hi-en",
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
}

# ---------------- TRANSLATION FUNCTION ----------------
def translate_text(text, src, tgt):
    key = f"{src}-{tgt}"
    if key not in MODELS:
        return "❌ Translation not supported"

    tokenizer, model = load_model(MODELS[key])

    inputs = tokenizer(text, return_tensors="pt", padding=True)
    with torch.no_grad():
        output_tokens = model.generate(**inputs)

    return tokenizer.decode(output_tokens[0], skip_special_tokens=True)

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    text-align: center;
    color: #ffffff;
}

textarea {
    background-color: #1e2a32 !important;
    color: white !important;
    border-radius: 12px;
}

button {
    background: linear-gradient(90deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}

button:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.title("🌍 AI Language Translator")
st.markdown("### Fast • Secure • Offline Models")

languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr"
}

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("From", list(languages.keys()))
with col2:
    tgt_lang = st.selectbox("To", list(languages.keys()))

text = st.text_area("Enter text to translate")

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text")
    elif src_lang == tgt_lang:
        st.info("Source and target language are same")
    else:
        with st.spinner("Translating..."):
            result = translate_text(
                text,
                languages[src_lang],
                languages[tgt_lang]
            )
        st.success("Translation Complete")
        st.text_area("Output", result, height=120)
