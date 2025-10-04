import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
from gtts import gTTS
import speech_recognition as sr
import tempfile

# ---------------- Models ----------------
models = {
    "en-hi": "Helsinki-NLP/opus-mt-en-hi",
    "hi-en": "Helsinki-NLP/opus-mt-hi-en",
    "en-es": "Helsinki-NLP/opus-mt-en-es",
    "es-en": "Helsinki-NLP/opus-mt-es-en",
    "en-fr": "Helsinki-NLP/opus-mt-en-fr",
    "fr-en": "Helsinki-NLP/opus-mt-fr-en",
}


def translate(text, src, tgt):
    key = f"{src}-{tgt}"
    if key not in models:
        return "❌ Translation not available for this pair"
    model_name = models[key]
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer([text], return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs)
    return tokenizer.decode(translated_tokens[0], skip_special_tokens=True)


# ---------------- UI Setup ----------------
st.set_page_config(
    page_title="🌍 Smart Voice Translator", page_icon="🎙️", layout="centered"
)

# Custom CSS
st.markdown(
    """
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3 {
    color: #f1f1f1;
    text-align: center;
}

.stTextArea textarea {
    background-color: #1e2a32;
    color: white;
    border-radius: 12px;
}

.stSelectbox, .stButton > button {
    border-radius: 12px;
}

.stButton > button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px 20px;
    border-radius: 12px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    transform: scale(1.05);
}

.voice-badge {
    padding: 5px 10px;
    border-radius: 12px;
    font-weight: bold;
    display: inline-block;
}

.available {
    background-color: #28a745;
    color: white;
}

.disabled {
    background-color: #dc3545;
    color: white;
}

@media (max-width: 768px) {
    h1, h2, h3 { font-size: 1.3rem; }
    .stTextArea textarea { font-size: 0.95rem; padding: 8px; }
    .stButton>button { font-size: 0.9rem; padding: 8px 12px; }
    .voice-badge { font-size: 0.8rem; padding: 4px 8px; }
}

</style>
""",
    unsafe_allow_html=True,
)

st.title("🎙️ Smart Voice Translator")
st.markdown(
    "#### Speak, translate, and listen in **English, Hindi, Spanish, and French**"
)

# ---------------- Voice Badge ----------------
try:
    sr.Microphone()  # Test if mic is available
    voice_available = True
except Exception:
    voice_available = False

if voice_available:
    st.markdown(
        '<span class="voice-badge available">Voice input: Available</span>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        '<span class="voice-badge disabled">Voice input: Disabled on cloud</span>',
        unsafe_allow_html=True,
    )

# ---------------- Language Selection ----------------
languages = {"English": "en", "Hindi": "hi", "Spanish": "es", "French": "fr"}
col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("🎤 From:", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("🔊 To:", list(languages.keys()), index=1)

# ---------------- Text Translation ----------------
text = st.text_area("✍️ Or type text to translate:", placeholder="Type here...")
if st.button("🔄 Translate Text"):
    if text.strip():
        src = languages[src_lang]
        tgt = languages[tgt_lang]
        if src == tgt:
            st.info("ℹ️ Source and target languages are same.")
        else:
            with st.spinner("✨ Translating..."):
                result = translate(text, src, tgt)
            st.success("✅ Translation Complete")
            st.text_area("Output:", result, height=100)

            # TTS
            try:
                tts = gTTS(result, lang=tgt)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_file.name)
                st.audio(temp_file.name, format="audio/mp3")
            except Exception as e:
                st.error(f"⚠️ Could not generate speech: {e}")
    else:
        st.warning("⚠️ Please enter some text.")

# ---------------- Voice Input (Local Only) ----------------
if voice_available:
    if st.button("🎙️ Speak & Translate"):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        st.info("🎤 Listening... please speak now")
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
        try:
            spoken_text = recognizer.recognize_google(
                audio, language=languages[src_lang]
            )
            st.write(f"🗣️ You said: `{spoken_text}`")
            with st.spinner("✨ Translating..."):
                src = languages[src_lang]
                tgt = languages[tgt_lang]
                result = translate(spoken_text, src, tgt)
            st.success("✅ Translation Complete")
            st.text_area("Output:", result, height=100)

            # TTS output
            try:
                tts = gTTS(result, lang=tgt)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(temp_file.name)
                st.audio(temp_file.name, format="audio/mp3")
            except Exception as e:
                st.error(f"⚠️ Could not generate speech: {e}")
        except Exception as e:
            st.error(f"⚠️ Could not recognize speech: {e}")
