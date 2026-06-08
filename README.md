# 🎯 JobGenius — AI Job Application Assistant Agent

> An intelligent AI agent that analyses your resume against any job description and gives you everything you need to get shortlisted.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ What It Does

Paste any job description + your resume and JobGenius instantly gives you:

| Feature | Description |
|---|---|
| 🎯 **ATS Score** | 0–100 match score with explanation |
| ✅ **Matched Skills** | Skills you already have that match the JD |
| ❌ **Missing Skills** | Skills gaps you need to address |
| 🔑 **JD Keywords** | High-value keywords to add to your resume |
| 💪 **Strengths & Gaps** | Honest analysis of your application |
| ✍️ **Rewritten Summary** | Your resume summary rewritten in the JD's language |
| 🎤 **Interview Questions** | 5 likely interview questions with answer hints |
| 📩 **Cover Letter** | A tailored cover letter written from scratch |

---

## 🚀 Quick Start

### 1. Get a Free Gemini API Key
Go to [aistudio.google.com](https://aistudio.google.com) → Sign in → **Get API Key** → **Create API Key**

Free tier: **1,500 requests/day** — more than enough.

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

Opens at → `http://localhost:8501`

---

## 🌐 Live Demo

> 🔗 [**jobgenius-ai.streamlit.app**](https://jobgenius-ai.streamlit.app) *(deploy your own below)*

---

## ☁️ Deploy for Free (Get a Shareable Link)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → **New app** → select this repo → select `app.py`
4. Click **Deploy** — you get a free public URL in minutes

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit |
| AI / LLM | Google Gemini 2.0 Flash (via `google-genai` SDK) |
| Backend Logic | Python |
| Prompt Engineering | JSON-schema-constrained structured output |
| Deployment | Streamlit Cloud (free) |

---

## 🧠 How It Works

```
User Input (JD + Resume)
        ↓
Prompt Engineering (role + schema + chain-of-thought)
        ↓
Google Gemini 2.0 Flash API
        ↓
Structured JSON Output (8 fields)
        ↓
Streamlit Dashboard (Score, Skills, Summary, Questions, Cover Letter)
```

---

## 📁 Project Structure

```
jobgenius/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── .gitignore
└── README.md
```

---

## 💬 How to Talk About This in Interviews

**"What did you build?"**
> "I built an AI agent that acts as a personal ATS system. It takes a job description and resume, analyses the match score, identifies skill gaps, rewrites the resume summary using the JD's language, generates likely interview questions, and creates a tailored cover letter — all powered by Google Gemini's API with structured prompt engineering."

**"What's the tech stack?"**
> "Python and Streamlit for the app, Google Gemini 2.0 Flash for LLM inference, and JSON-schema-constrained prompting for reliable structured output parsing. Deployed free on Streamlit Cloud."

**"Why did you build this?"**
> "I was facing rejection in my own job applications and realised most freshers don't understand how ATS systems work or how to tailor resumes per role. I built this to solve that exact problem for myself and others."

---

## 🔧 Possible Extensions

- [ ] PDF resume upload (instead of pasting text)
- [ ] LangChain integration for multi-step agent reasoning
- [ ] Vector store (Chroma) for job history tracking
- [ ] FastAPI backend for scalable deployment
- [ ] Email results to yourself
- [ ] Job board scraping (auto-fetch JDs)

---

## 👤 Author

**Revanth S K**
- LinkedIn: [linkedin.com/in/revanth-s-k](https://www.linkedin.com/in/revanth-s-k-b45933251/)
- Email: revanthsk6@gmail.com

---

## 📄 License

MIT License — free to use, modify, and distribute.
