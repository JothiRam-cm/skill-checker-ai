# 🔥 AI Resume Analyzer + HTML Resume Rewriter

<p align="center">
  <img src="assets/banner.svg" width="100%" />
</p>

<p align="center">
  <img src="assets/logo.svg" width="160" />
</p>

---

<img src="https://img.shields.io/badge/AI%20Resume%20Analyzer-Llama3%20%7C%20Gemini-blueviolet?style=for-the-badge" />
<img src="https://img.shields.io/github/languages/top/JothiRam-cm/skill-checker-ai?style=for-the-badge" />
<img src="https://img.shields.io/badge/Streamlit-Deployed-brightgreen?style=for-the-badge&logo=streamlit" />

# AI Resume Analyzer + HTML Resume Rewriter
### **ATS-Optimized • LLM-Powered • Streamlit App**

> A complete AI system that analyzes resumes, extracts skills, computes ATS & Fit scores, and rewrites your resume into a clean, ATS-optimized HTML template. Supports Groq, Gemini, and Ollama models.

---

## 📚 Table of Contents
- [✨ Features](#-features)
- [🏗 Architecture](#-architecture)
- [📂 Folder Structure](#-folder-structure)
- [⚙️ Tech Stack](#️-tech-stack)
- [🔧 Installation](#-installation)
- [🔑 Environment Variables](#-environment-variables)
- [▶️ Run Locally](#️-run-locally)
- [☁️ Deploy on Streamlit Cloud](#-deploy-on-streamlit-cloud)
- [📸 Screenshots](#-screenshots)
- [🛠 Future Enhancements](#-future-enhancements)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

---

## ✨ Features

### 🧠 **1. LLM-Powered ATS Analyzer**
- Accurate ATS & Fit scoring
- JD-to-resume alignment analysis
- Skill extraction using LLM (RAPTOR prompting)
- Highlights:
  - Summary alignment
  - Experience alignment
  - Missing skills
  - Red flags

### ✍️ **2. AI Resume Rewriter (HTML-Based)**
- Generates a full, modern HTML resume
- Editable inside Streamlit
- Live HTML preview
- Inline CSS for ATS compatibility
- Export:
  - **HTML**
  - **PDF (pure Python, ReportLab)**

### 🤖 **3. Multi-Model LLM Support**
- **Groq** → LLaMA 3.3 (70B Versatile)
- **Gemini** → Gemini 2.0 Flash
- **Ollama** → Local models (mistral, llama3, qwen2, etc.)

### 📄 **4. Resume Parsing**
Supports:
- PDF
- DOCX
- TXT

### 🎨 **5. Modular Template System**
- Minimal
- Professional
- Modern

---

## 🏗 Architecture

```
          Resume (PDF/DOCX/TXT)          JD (PDF/DOCX/TXT)
                    │                           │
             parse_resume()                parse_jd()
                    └──────────────┬──────────────┘
                                   ▼
                           LLM ATS Analyzer
                     (Fit Score, Skills, Review)
                                   │
                                   ▼
                         HTML Resume Generator
                                   │
                 ┌───────────Templates────────────┐
                 │ minimal | professional | modern │
                 └───────────────┬────────────────┘
                                 ▼
                         Editable HTML Resume
                                   │
                                   ▼
                           Export to PDF (Python)
```

---

## 📂 Folder Structure

```
skill_check_app/
│
├── app.py
├── requirements.txt
│
├── modules/
│   ├── parser.py
│   ├── analyzer.py
│   ├── llm_switcher.py
│   ├── rewriter.py
│   └── exporter.py
│
├── templates/
│   ├── minimal.html
│   ├── professional.html
│   └── modern.html
│
└── outputs/
```

---

## ⚙️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Models | Groq, Gemini, Ollama |
| Resume Parsing | PyPDF2, Python-docx |
| HTML → PDF | ReportLab |
| Deployment | Streamlit Cloud |

---

## 🔧 Installation

```bash
git clone https://github.com/JothiRam-cm/skill-checker-ai.git
cd skill-checker-ai

python -m venv .venv
.venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create `.env` file:

```
GROQ_API_KEY="your_groq_key"
GEMINI_API_KEY="your_gemini_key"
```

Ollama requires no key.

---

## ▶️ Run Locally

```bash
streamlit run skill_check_app/app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push repo to GitHub
2. Open https://share.streamlit.io
3. Add new app
4. Set:
   ```
   Repository: JothiRam-cm/skill-checker-ai
   Branch: main
   File: skill_check_app/app.py
   ```
5. Add secrets:

```
GROQ_API_KEY="gsk_xxxxx"
GEMINI_API_KEY="AIza_xxxxx"
```

6. Deploy 🚀

---

## 📸 Screenshots

To be added:
```
assets/analyzer.png
assets/rewriter.png
assets/pdf_export.png
```

---

## 🛠 Future Enhancements
- AI Cover Letter Generator
- AI Portfolio Website Generator
- Job Match Ranking Engine
- Multi-section Resume Editor
- Drag-and-drop Resume Blocks
- More Templates
- Cloud Resume Versioning

---

## 🤝 Contributing
Pull requests are welcome.

Steps:
1. Fork the repo
2. Create a branch
3. Add features or fixes
4. Submit PR

---

## 📜 License
MIT License

---

<p align="center">Built with ❤️ using Streamlit + Groq + Gemini + Ollama</p>

