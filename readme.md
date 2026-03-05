<div align="center">

# 🗣️ Vernā

**Offline Neural Machine Translation**

*Runs entirely on your machine · No API keys · No data transmitted*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/MarianMT-Helsinki--NLP-FFD21E?style=flat-square&logo=huggingface&logoColor=black)](https://huggingface.co/Helsinki-NLP)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## Overview

**Vernā** (from *vernacular* — one's native tongue) is a clean, privacy-first neural machine translation app built with Streamlit and HuggingFace MarianMT models. After the one-time model download, it runs with zero internet connection and zero data leaving your device.

---

## Features

- 🔒 **100% offline** after first model download
- ⚡ **Model caching** — loads once per session, instant on repeat use
- 🎯 **Beam search decoding** (`num_beams=4`) for higher translation quality
- ⚠️ **Pre-flight pair validation** — unsupported pairs shown before you translate
- 📏 **600-character input limit** with live counter
- 🌐 **Native script display** — results labelled in the target language's own script

---

## Supported Language Pairs

| From | To |
|---|---|
| 🇬🇧 English | 🇮🇳 Hindi |
| 🇮🇳 Hindi | 🇬🇧 English |
| 🇬🇧 English | 🇪🇸 Spanish |
| 🇪🇸 Spanish | 🇬🇧 English |
| 🇬🇧 English | 🇫🇷 French |
| 🇫🇷 French | 🇬🇧 English |

> Models are auto-downloaded from HuggingFace Hub on first use (~300 MB each) and cached locally.

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-username/verna.git
cd verna

# 2. Install
pip install -r requirements.txt

# 3. Run
streamlit run verna.py
```

Open **http://localhost:8501** in your browser.

---

## Requirements

```txt
streamlit>=1.28.0
transformers>=4.35.0
torch>=2.0.0
sentencepiece
sacremoses
```

Install all at once:

```bash
pip install streamlit transformers torch sentencepiece sacremoses
```

### Why `sentencepiece` and `sacremoses`?

These are not called directly in code — `MarianTokenizer` depends on them internally:

| Package | Role |
|---|---|
| `sentencepiece` | Subword tokenization — splits rare words into known fragments so the model handles any vocabulary |
| `sacremoses` | Moses-style text normalization — matches the preprocessing format the models were trained on |

---

## How It Works

```
Input text
    │
    ▼
MarianTokenizer          ← text → token ID tensors
    │  truncate to 512 tokens, pad, return PyTorch tensors
    ▼
MarianMTModel.generate()
    │  Beam Search (num_beams=4) — explores 4 candidate
    │  translations simultaneously, keeps highest-scored
    ▼
tokenizer.decode()       ← token IDs → human-readable string
    │  skip_special_tokens=True strips [PAD], </s>
    ▼
Result displayed in UI
```

**Why beam search over greedy?** Greedy decoding picks the single highest-probability token at every step. Beam search keeps `n` candidates alive in parallel — it can recover from early low-probability choices that lead to a better overall sequence. `num_beams=4` is a good quality/speed tradeoff.

**Why `torch.no_grad()`?** Gradients are only needed during *training* to update model weights. During inference (prediction), computing them wastes memory and time. Wrapping generation in `torch.no_grad()` disables this entirely.

---

## Project Structure

```
verna/
├── verna.py          # Entire app — model, translation logic, UI
├── requirements.txt
└── README.md
```

Vernā is intentionally a single file. Sections are separated by double-rule comments for easy navigation:

```
MODEL CACHE       @st.cache_resource wrapper
CONFIG            MODELS dict + LANGUAGES registry
TRANSLATION       tokenize → generate → decode pipeline
PAGE CONFIG       Streamlit metadata
CSS               ~20 lines — result card only, rest is native Streamlit
HEADER            Wordmark + tagline + privacy status
LANGUAGE SELECT   Two-column dropdowns with auto-filter
INPUT             Textarea + live char counter + pair validation
RESULT            Dark result card with native script label
FOOTER            Supported pair reference
```

---

## Adding a New Language Pair

Two edits, nothing else changes:

**1. Add the model to `MODELS`:**

```python
MODELS = {
    ...
    "en-de": "Helsinki-NLP/opus-mt-en-de",
    "de-en": "Helsinki-NLP/opus-mt-de-en",
}
```

**2. Register the language in `LANGUAGES`:**

```python
LANGUAGES = {
    ...
    "German": {"code": "de", "flag": "🇩🇪", "native": "Deutsch"},
}
```

The dropdowns, pair validation, result card, and footer all update automatically. Browse 1,000+ available Helsinki-NLP models at [huggingface.co/Helsinki-NLP](https://huggingface.co/Helsinki-NLP).

---

## Privacy

Vernā makes **zero network calls during translation**. After the initial model download from HuggingFace Hub, the app is fully air-gapped. There is no logging, no analytics, and no telemetry of any kind. Your text never leaves your machine.

---

## Contributing

1. Fork the repo
2. Create your branch — `git checkout -b feat/your-feature`
3. Commit — `git commit -m "feat: your change"`
4. Push — `git push origin feat/your-feature`
5. Open a Pull Request

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">
<sub>Built with MarianMT · HuggingFace Transformers · Streamlit</sub>
</div>