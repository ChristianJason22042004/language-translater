## 🎙️ Smart Voice Translator 🌍
A modern multilingual **AI-powered voice translator** built with **Streamlit**, **Hugging Face Transformers**, **Speech Recognition**, and **Google TTS**.  

It allows you to:
- 🎤 Speak in one language and hear the translation in another.  
- ✍️ Type text and get instant translations.  
- 🔊 Listen to the translated speech output.

Live Demo: https://nlp-language-translater.streamlit.app/
  
---

## 🚀 Why This Project?
In a world of increasing global communication, **language should not be a barrier**.  
This project demonstrates how **AI + NLP (Natural Language Processing)** can be used to build a **real-time voice translation assistant** that is:  
- ✅ Easy to use  
- ✅ Lightweight  
- ✅ Covers multiple languages (English, Hindi, Spanish, French)  

---

## 🧠 AI / NLP Behind the Scenes
- **Helsinki-NLP MarianMT Models** (via Hugging Face)  
  - Pretrained translation models for dozens of language pairs.  
  - Example: `Helsinki-NLP/opus-mt-en-hi` for **English → Hindi**.  
- **Speech Recognition AI**  
  - Converts spoken words into text using Google’s Speech-to-Text API.  
- **Text-to-Speech AI (gTTS)**  
  - Converts translated text into natural-sounding speech.  

Pipeline:  
`🎤 Voice Input → 📝 Text → 🌐 NLP Translation → 🔊 Speech Output`  

---

## ⚡ Features
- 🌍 Translate between **English, Hindi, Spanish, French**.  
- 🎙️ Speak directly using microphone.  
- ✍️ Type text and translate instantly.  
- 🔊 Get spoken audio output for translations.  
- 🎨 Modern UI with custom CSS & animations.  

---

## 🛠️ Tech Stack
- **Python** 🐍  
- **Streamlit** → Web UI  
- **Hugging Face Transformers** → MarianMT models for translation  
- **SpeechRecognition** → Speech-to-text  
- **gTTS** → Text-to-speech  

---

## 📦 Installation

1. Clone the repo:
```bash
git clone https://github.com/your-username/smart-voice-translator.git
cd smart-voice-translator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run streamlit_app.py
```

4. Open your browser
By default, Streamlit will open the app at:
```bash
http://localhost:8501
```

---

## 💡 Voice Input: Local vs Cloud
Local machine: 🎤 Voice input works! Click Speak & Translate to use your microphone.

Streamlit Cloud: 🎤 Voice input is disabled, because remote servers cannot access your local microphone.

You can always type text and get translations with TTS audio output.

---

## 📝 Troubleshooting Files: requirements.txt & packages.txt
requirements.txt
Lists all Python packages required by the project (e.g., transformers, speechrecognition, gTTS, streamlit).
Use it with pip install -r requirements.txt to quickly install Python dependencies.

packages.txt
Lists system-level dependencies needed for some Python packages to work (e.g., portaudio19-dev, python3-dev).
Install these using your system’s package manager (like apt) before running Python scripts.

---

## Why Streamlit?
Provides a fast and easy way to build interactive web apps in Python

Allows real-time updates for voice input/output

Minimal setup compared to full-stack frameworks, perfect for AI demos

Works perfectly with cloud deployments for sharing, even if voice input is limited
