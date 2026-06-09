import streamlit as st
from google import genai
import json
import re

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JobGenius AI Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --navy: #0f1f3d;
    --navy-light: #1b3a6b;
    --accent: #4f8ef7;
    --accent2: #00e5a0;
    --bg: #07111f;
    --surface: #0d1f35;
    --surface2: #132840;
    --text: #e8edf5;
    --muted: #7a92b0;
    --border: rgba(79,142,247,0.15);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #0d2a4a 0%, var(--bg) 60%) !important;
}
h1,h2,h3 { font-family: 'Syne', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

.hero { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.hero-badge {
    display: inline-block;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.3);
    color: var(--accent);
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase;
    padding: 0.35rem 1rem; border-radius: 100px; margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800; line-height: 1.1;
    background: linear-gradient(135deg, #e8edf5 30%, var(--accent) 70%, var(--accent2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 0.8rem;
}
.hero-sub {
    color: var(--muted); font-size: 1rem; font-weight: 300;
    max-width: 520px; margin: 0 auto 2rem; line-height: 1.6;
}
.steps-row { display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2.5rem; }
.step-pill {
    display: flex; align-items: center; gap: 0.5rem;
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 100px; padding: 0.4rem 1rem;
    font-size: 0.78rem; color: var(--muted);
    font-family: 'Syne', sans-serif; font-weight: 600;
}
.step-num {
    width: 20px; height: 20px; background: var(--accent); color: white;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 0.65rem; font-weight: 800;
}
.card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.6rem; margin-bottom: 1.2rem; }
.card-title {
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.85rem;
    text-transform: uppercase; letter-spacing: 0.1em; color: var(--accent);
    margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;
}
.score-container { text-align: center; padding: 1.5rem 0; }
.score-ring {
    width: 130px; height: 130px; border-radius: 50%; margin: 0 auto 1rem;
    display: flex; align-items: center; justify-content: center;
    flex-direction: column; position: relative; font-family: 'Syne', sans-serif;
}
.score-value { font-size: 2.4rem; font-weight: 800; line-height: 1; }
.score-label { font-size: 0.65rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; }
.tag-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.tag { padding: 0.3rem 0.75rem; border-radius: 100px; font-size: 0.75rem; font-weight: 500; font-family: 'Syne', sans-serif; }
.tag-match { background: rgba(0,229,160,0.12); color: var(--accent2); border: 1px solid rgba(0,229,160,0.25); }
.tag-miss  { background: rgba(247,79,79,0.1);  color: #f77; border: 1px solid rgba(247,79,79,0.2); }
.tag-kw    { background: rgba(79,142,247,0.1); color: var(--accent); border: 1px solid var(--border); }
.q-card {
    background: var(--surface2); border-left: 3px solid var(--accent);
    border-radius: 0 10px 10px 0; padding: 0.9rem 1.1rem; margin-bottom: 0.7rem;
    font-size: 0.9rem; line-height: 1.5;
}
.q-num { font-family: 'Syne', sans-serif; font-weight: 800; color: var(--accent); font-size: 0.75rem; margin-bottom: 0.3rem; }
.stTextArea textarea, .stTextInput input {
    background: var(--surface2) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.88rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #2563eb) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.9rem !important; letter-spacing: 0.05em !important;
    padding: 0.65rem 2rem !important; width: 100% !important; transition: all 0.2s !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 8px 25px rgba(79,142,247,0.35) !important; }
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important; border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important; border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--muted) !important;
    border-radius: 8px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
}
.stTabs [aria-selected="true"] { background: var(--accent) !important; color: white !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.2rem !important; }
.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }
.result-header {
    font-family: 'Syne', sans-serif; font-size: 1.4rem; font-weight: 800;
    color: var(--text); margin: 2rem 0 1.2rem; display: flex; align-items: center; gap: 0.6rem;
}
.copy-box {
    background: var(--surface2); border: 1px solid var(--border); border-radius: 10px;
    padding: 1.2rem; font-size: 0.85rem; line-height: 1.7; color: var(--text);
    white-space: pre-wrap; font-family: 'DM Sans', sans-serif;
}
label { color: var(--muted) !important; font-size: 0.82rem !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
.stAlert { background: var(--surface2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)


# ── Gemini client ──────────────────────────────────────────────────────────────
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


# ── Prompt ─────────────────────────────────────────────────────────────────────
def build_prompt(jd: str, resume: str) -> str:
    return f"""
You are an expert ATS system and career coach. Analyse the resume against the job description below.

Respond ONLY with a valid JSON object — no markdown, no backticks, no extra text whatsoever.

Use this exact structure:
{{
  "ats_score": <integer 0-100>,
  "score_reason": "<2-sentence explanation of the score>",
  "matched_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "jd_keywords": ["keyword1", "keyword2"],
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2", "weakness3"],
  "rewritten_summary": "<A powerful 3-sentence professional summary rewritten specifically for this JD, using JD language and keywords>",
  "interview_questions": [
    {{"q": "<question 1>", "hint": "<one-line answer hint>"}},
    {{"q": "<question 2>", "hint": "<one-line answer hint>"}},
    {{"q": "<question 3>", "hint": "<one-line answer hint>"}},
    {{"q": "<question 4>", "hint": "<one-line answer hint>"}},
    {{"q": "<question 5>", "hint": "<one-line answer hint>"}}
  ],
  "cover_letter": "<A professional 3-paragraph cover letter tailored to this role. Start with 'Dear Hiring Manager,' and end with 'Sincerely,\\n[Your Name]'>"
}}

JOB DESCRIPTION:
{jd}

RESUME:
{resume}
"""


def safe_parse(raw: str) -> dict:
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    return json.loads(cleaned)


def score_color(score: int) -> str:
    if score >= 75: return "#00e5a0"
    if score >= 50: return "#4f8ef7"
    return "#f77"


def score_ring_css(score: int) -> str:
    color = score_color(score)
    return f"border: 5px solid {color}; background: rgba(0,0,0,0.2);"


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">⚡ AI-Powered Career Agent</div>
  <div class="hero-title">JobGenius</div>
  <div class="hero-sub">Paste any job description + your resume. Get your ATS score, skill gaps, a rewritten summary, interview questions, and a cover letter — in seconds.</div>
  <div class="steps-row">
    <div class="step-pill"><div class="step-num">1</div> Enter API Key</div>
    <div class="step-pill"><div class="step-num">2</div> Paste JD + Resume</div>
    <div class="step-pill"><div class="step-num">3</div> Run Agent</div>
    <div class="step-pill"><div class="step-num">4</div> Get Results</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ─────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="card-title">🔑 Gemini API Key</div>', unsafe_allow_html=True)
    api_key = st.text_input(
        "API Key", type="password",
        placeholder="Paste your Gemini API key here...",
        help="Get your free key at aistudio.google.com → Get API Key",
        label_visibility="collapsed"
    )
    st.markdown(
        '<div style="font-size:0.75rem;color:#4f8ef7;margin-top:0.3rem;">'
        '🔗 Get free key → <a href="https://aistudio.google.com" target="_blank" style="color:#4f8ef7;">aistudio.google.com</a>'
        '</div>', unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
    jd_input = st.text_area(
        "JD", height=260,
        placeholder="Paste the full job description here...\n\nInclude: role title, responsibilities, required skills, qualifications etc.",
        label_visibility="collapsed"
    )

with col_right:
    st.markdown('<div class="card-title">📄 Your Resume</div>', unsafe_allow_html=True)
    resume_input = st.text_area(
        "Resume", height=360,
        placeholder="Paste your resume text here...\n\nInclude: summary, skills, experience, education, projects etc.",
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
run_col, _ = st.columns([1, 2])
with run_col:
    run_btn = st.button("🚀  Analyse My Application", use_container_width=True)

# ── Run agent ──────────────────────────────────────────────────────────────────
if run_btn:
    if not api_key:
        st.error("Please enter your Gemini API key.")
    elif not jd_input.strip():
        st.error("Please paste a job description.")
    elif not resume_input.strip():
        st.error("Please paste your resume.")
    else:
        with st.spinner("Agent is analysing your application..."):
            try:
                client   = get_client(api_key)
                prompt   = build_prompt(jd_input, resume_input)
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=prompt
                )
                data = safe_parse(response.text)
                st.session_state["result"] = data
                st.session_state["ran"]    = True

            except json.JSONDecodeError as e:
                st.error(f"JSON parsing error: {e}\n\nRaw response preview:\n{response.text[:500]}")
            except Exception as e:
                err = str(e)
                if "429" in err or "RESOURCE_EXHAUSTED" in err:
                    st.error(
                        "⚠️ Gemini free tier quota exceeded.\n\n"
                        "**Fix:** Go to aistudio.google.com → sign in with a different Google account → "
                        "create a new API key → paste it above and try again.\n\n"
                        "The free tier resets every 24 hours."
                    )
                elif "API_KEY_INVALID" in err or "400" in err:
                    st.error("❌ Invalid API key. Please check your key at aistudio.google.com and try again.")
                else:
                    st.error(f"Error: {err}")

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.get("ran") and "result" in st.session_state:
    data  = st.session_state["result"]
    score = data.get("ats_score", 0)
    color = score_color(score)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">📊 Analysis Results</div>', unsafe_allow_html=True)

    # ── Score + Strengths + Weaknesses
    s1, s2, s3 = st.columns([1, 1.5, 1.5], gap="large")

    with s1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
          <div class="card-title" style="justify-content:center;">ATS Match Score</div>
          <div class="score-ring" style="{score_ring_css(score)}">
            <div class="score-value" style="color:{color};">{score}</div>
            <div class="score-label">out of 100</div>
          </div>
          <div style="font-size:0.8rem;color:var(--muted);line-height:1.5;margin-top:0.5rem;">{data.get('score_reason','')}</div>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="card"><div class="card-title">✅ Strengths</div>', unsafe_allow_html=True)
        for s in data.get("strengths", []):
            st.markdown(f'<div style="font-size:0.85rem;padding:0.4rem 0;border-bottom:1px solid var(--border);color:var(--text);">💚 {s}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s3:
        st.markdown('<div class="card"><div class="card-title">⚠️ Gaps to Fix</div>', unsafe_allow_html=True)
        for w in data.get("weaknesses", []):
            st.markdown(f'<div style="font-size:0.85rem;padding:0.4rem 0;border-bottom:1px solid var(--border);color:var(--text);">🔴 {w}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Skills
    sk1, sk2, sk3 = st.columns(3, gap="medium")

    with sk1:
        matched = data.get("matched_skills", [])
        st.markdown(f'<div class="card"><div class="card-title">✅ Matched Skills ({len(matched)})</div><div class="tag-row">', unsafe_allow_html=True)
        for t in matched:
            st.markdown(f'<span class="tag tag-match">{t}</span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with sk2:
        missing = data.get("missing_skills", [])
        st.markdown(f'<div class="card"><div class="card-title">❌ Missing Skills ({len(missing)})</div><div class="tag-row">', unsafe_allow_html=True)
        for t in missing:
            st.markdown(f'<span class="tag tag-miss">{t}</span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    with sk3:
        keywords = data.get("jd_keywords", [])
        st.markdown(f'<div class="card"><div class="card-title">🔑 JD Keywords ({len(keywords)})</div><div class="tag-row">', unsafe_allow_html=True)
        for t in keywords:
            st.markdown(f'<span class="tag tag-kw">{t}</span>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

    # ── Tabs
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["✍️  Rewritten Summary", "🎤  Interview Questions", "📩  Cover Letter"])

    with tab1:
        st.markdown('<div class="card-title">✍️ Rewritten Professional Summary</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="copy-box">{data.get("rewritten_summary", "")}</div>', unsafe_allow_html=True)
        st.info("💡 Copy this and paste it at the top of your resume when applying for this specific role.")

    with tab2:
        st.markdown('<div class="card-title">🎤 Likely Interview Questions</div>', unsafe_allow_html=True)
        for i, q in enumerate(data.get("interview_questions", []), 1):
            st.markdown(f"""
            <div class="q-card">
              <div class="q-num">QUESTION {i}</div>
              <div style="font-weight:500;margin-bottom:0.4rem;">{q.get('q','')}</div>
              <div style="font-size:0.78rem;color:var(--muted);">💡 Hint: {q.get('hint','')}</div>
            </div>
            """, unsafe_allow_html=True)
        st.info("💡 Prepare answers using STAR method: Situation → Task → Action → Result.")

    with tab3:
        st.markdown('<div class="card-title">📩 Tailored Cover Letter</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="copy-box">{data.get("cover_letter", "")}</div>', unsafe_allow_html=True)
        st.info("💡 Replace [Your Name] with your name before sending.")
