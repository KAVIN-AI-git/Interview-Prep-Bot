import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import json
import re

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="InterviewIQ · AI Mock Interview",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Clash+Display:wght@400;500;600;700&family=Cabinet+Grotesk:wght@400;500;700;800&family=Instrument+Sans:wght@400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

:root {
  --ink: #0a0a0f;
  --paper: #f5f3ee;
  --cream: #ede9e0;
  --gold: #c9a84c;
  --gold-bright: #e8b84b;
  --gold-light: #e8d5a3;
  --gold-dim: rgba(201,168,76,.15);
  --teal: #0d9488;
  --teal-light: #99f6e4;
  --rose: #e11d48;
  --rose-light: #fecdd3;
  --amber: #d97706;
  --amber-light: #fde68a;
  --indigo: #4f46e5;
  --indigo-light: #c7d2fe;
  --surface: #ffffff;
  --surface-2: #f9f8f5;
  --border: #e5e0d5;
  --text-muted: #6b6560;
  --text-body: #2d2a26;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Cabinet Grotesk', 'Instrument Sans', sans-serif;
  color: var(--text-body);
  background: var(--paper);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
  padding: 0 !important;
  padding-top: 0 !important;
  max-width: 800px !important;
  margin: 0 auto;
}
/* Remove ALL streamlit top whitespace */
.stApp > header { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
div[data-testid="stAppViewContainer"] > section > div:first-child {
  padding-top: 0 !important;
}
div[data-testid="stVerticalBlock"] > div:first-child {
  margin-top: 0 !important;
  padding-top: 0 !important;
}
/* Nuke the default 6rem top padding Streamlit adds */
.main .block-container { padding-top: 0 !important; }
/* Hide empty iframe spacers */
iframe[height="0"], iframe[height="2"] { display: none !important; }
div[data-testid="stVerticalBlockBorderWrapper"]:empty { display: none !important; }
/* Remove gap above first element */
.element-container:first-child { margin-top: 0 !important; }

/* ─── GLOBAL WRAPPER ─── */
.app-shell {
  min-height: 100vh;
  background: var(--paper);
  padding: 32px 24px 80px;
  position: relative;
}
.app-shell::before {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background:
    radial-gradient(ellipse 60% 50% at 80% 10%, rgba(201,168,76,.08) 0%, transparent 70%),
    radial-gradient(ellipse 50% 40% at 10% 80%, rgba(13,148,136,.06) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ─── HEADER ─── */
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 48px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border);
  position: relative;
  z-index: 1;
}
.logo-mark {
  font-family: 'Space Mono', monospace;
  font-size: .72rem;
  font-weight: 700;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--ink);
}
.logo-mark span {
  display: inline-block;
  background: var(--ink);
  color: var(--paper);
  padding: 3px 8px;
  border-radius: 4px;
  margin-right: 6px;
}
.header-pill {
  font-family: 'Space Mono', monospace;
  font-size: .62rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--teal);
  background: rgba(13,148,136,.08);
  border: 1px solid rgba(13,148,136,.2);
  padding: 5px 12px;
  border-radius: 100px;
}

/* ─── HERO ─── */
.hero-section {
  position: relative;
  z-index: 1;
  margin-bottom: 48px;
}
.hero-eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: .65rem;
  letter-spacing: .2em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.hero-eyebrow::before {
  content: '';
  display: inline-block;
  width: 24px;
  height: 1px;
  background: var(--gold);
}
.hero-title {
  font-family: 'Clash Display', sans-serif;
  font-size: clamp(2.6rem, 6vw, 4.2rem);
  font-weight: 700;
  line-height: 1.05;
  color: var(--ink);
  letter-spacing: -0.03em;
  margin-bottom: 20px;
}
.hero-title em {
  font-style: normal;
  color: var(--gold);
  position: relative;
}
.hero-title em::after {
  content: '';
  position: absolute;
  bottom: 2px; left: 0; right: 0;
  height: 3px;
  background: var(--gold);
  border-radius: 2px;
  opacity: .4;
}
.hero-sub {
  font-size: 1.05rem;
  color: var(--text-muted);
  max-width: 480px;
  line-height: 1.7;
  margin-bottom: 32px;
}
.hero-stats {
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
}
.hero-stat {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.hero-stat-val {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: -0.02em;
}
.hero-stat-lbl {
  font-size: .72rem;
  color: var(--text-muted);
  letter-spacing: .05em;
}

/* ─── FORM CARD ─── */
.form-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 36px 32px;
  box-shadow: 0 4px 24px rgba(0,0,0,.06), 0 1px 4px rgba(0,0,0,.04);
  position: relative;
  z-index: 1;
  margin-bottom: 20px;
}
.form-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  border-radius: 20px 20px 0 0;
  background: linear-gradient(90deg, var(--gold), var(--teal));
}
.section-label {
  font-family: 'Space Mono', monospace;
  font-size: .62rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}
/* Form inputs area */
div[data-testid="stVerticalBlock"] {
  background: transparent;
}

/* ─── STREAMLIT OVERRIDES ─── */
div.stTextInput label, div.stSelectbox label, div.stTextArea label {
  font-family: 'Cabinet Grotesk', sans-serif !important;
  font-size: .82rem !important;
  font-weight: 600 !important;
  color: var(--text-body) !important;
  letter-spacing: .02em !important;
  margin-bottom: 6px !important;
}
div.stTextInput > div > div > input,
div.stTextArea > div > div > textarea,
div.stSelectbox > div > div {
  border-radius: 10px !important;
  border: 1.5px solid var(--border) !important;
  background: var(--surface-2) !important;
  font-family: 'Instrument Sans', sans-serif !important;
  font-size: .92rem !important;
  color: var(--text-body) !important;
  transition: border-color .2s, box-shadow .2s !important;
}
div.stTextInput > div > div > input:focus,
div.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,.12) !important;
  background: #fff !important;
}
div.stSelectbox > div > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(201,168,76,.12) !important;
}

/* ─── BUTTONS ─── */
div.stButton > button {
  font-family: 'Cabinet Grotesk', sans-serif !important;
  font-size: .88rem !important;
  font-weight: 700 !important;
  letter-spacing: .02em !important;
  border-radius: 10px !important;
  border: none !important;
  padding: 0.65rem 1.6rem !important;
  transition: transform .15s, box-shadow .15s, opacity .15s !important;
  cursor: pointer !important;
}
div.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(0,0,0,.12) !important;
}
div.stButton > button:active {
  transform: translateY(0) !important;
}
div.stButton > button[kind="primary"] {
  background: var(--ink) !important;
  color: var(--paper) !important;
}
div.stButton > button[kind="secondary"] {
  background: transparent !important;
  color: var(--ink) !important;
  border: 1.5px solid var(--border) !important;
}

/* ─── PROGRESS ─── */
.prog-bar-outer {
  height: 6px;
  background: var(--border);
  border-radius: 100px;
  overflow: hidden;
  margin-bottom: 6px;
}
.prog-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, var(--gold), var(--teal));
  border-radius: 100px;
  transition: width .5s cubic-bezier(.4, 0, .2, 1);
}
.prog-meta {
  display: flex;
  justify-content: space-between;
  font-size: .72rem;
  color: var(--text-muted);
  margin-bottom: 28px;
  font-family: 'Space Mono', monospace;
  letter-spacing: .05em;
}

/* ─── INTERVIEW SESSION HEADER ─── */
.session-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 12px;
}
.session-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.meta-chip {
  font-size: .72rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 100px;
  background: var(--cream);
  color: var(--text-body);
  border: 1px solid var(--border);
  font-family: 'Space Mono', monospace;
  letter-spacing: .05em;
}
.q-counter {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--ink);
  letter-spacing: -0.02em;
}
.q-counter span { color: var(--text-muted); font-size: 1rem; }

/* ─── QUESTION CARD ─── */
.question-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 32px;
  margin-bottom: 20px;
  position: relative;
  overflow: hidden;
}
.question-card::after {
  content: '"';
  position: absolute;
  bottom: -20px; right: 20px;
  font-family: 'Clash Display', sans-serif;
  font-size: 12rem;
  color: rgba(0,0,0,.04);
  font-weight: 700;
  line-height: 1;
  user-select: none;
}
.q-type-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}
.type-badge {
  font-family: 'Space Mono', monospace;
  font-size: .6rem;
  font-weight: 700;
  letter-spacing: .12em;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 100px;
}
.type-behavioral { background: rgba(217,119,6,.1); color: var(--amber); border: 1px solid rgba(217,119,6,.2); }
.type-technical   { background: rgba(79,70,229,.1); color: var(--indigo); border: 1px solid rgba(79,70,229,.2); }
.type-situational { background: rgba(13,148,136,.1); color: var(--teal); border: 1px solid rgba(13,148,136,.2); }
.type-hr          { background: rgba(225,29,72,.1); color: var(--rose); border: 1px solid rgba(225,29,72,.2); }

.question-text {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--ink);
  line-height: 1.4;
  letter-spacing: -0.01em;
  margin-bottom: 16px;
  position: relative;
  z-index: 1;
}
.question-tip {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-left: 3px solid var(--gold);
  border-radius: 0 8px 8px 0;
  padding: 12px 16px;
  font-size: .82rem;
  color: var(--text-muted);
  line-height: 1.6;
  position: relative;
  z-index: 1;
}
.question-tip strong { color: var(--gold); }

/* ─── VOICE ─── */
.voice-strip {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--cream);
  border: 1.5px solid var(--border);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 12px;
}
.mic-orb {
  width: 48px; height: 48px;
  border-radius: 50%;
  background: var(--ink);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  cursor: pointer;
  border: none;
  box-shadow: 0 4px 16px rgba(0,0,0,.15);
  transition: transform .2s, box-shadow .2s;
  flex-shrink: 0;
}
.mic-orb:hover { transform: scale(1.07); box-shadow: 0 8px 24px rgba(0,0,0,.2); }
.mic-orb.on {
  background: var(--rose);
  animation: orbPulse 1.2s ease-in-out infinite;
}
@keyframes orbPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(225,29,72,.3); }
  50% { box-shadow: 0 0 0 14px rgba(225,29,72,0); }
}
.voice-info { flex: 1; }
.vi-title { font-size: .88rem; font-weight: 700; color: var(--ink); margin-bottom: 2px; }
.vi-sub { font-size: .74rem; color: var(--text-muted); }
.vi-sub.live { color: var(--rose); }
.wave { display: flex; align-items: center; gap: 3px; height: 18px; }
.wave-b {
  width: 3px; min-height: 4px; border-radius: 3px;
  background: var(--rose);
  animation: wv .7s ease-in-out infinite;
}
.wave-b:nth-child(1) { animation-delay: 0s; }
.wave-b:nth-child(2) { animation-delay: .1s; }
.wave-b:nth-child(3) { animation-delay: .2s; }
.wave-b:nth-child(4) { animation-delay: .3s; }
.wave-b:nth-child(5) { animation-delay: .15s; }
@keyframes wv {
  0%, 100% { height: 4px; opacity: .5; }
  50% { height: 18px; opacity: 1; }
}

/* ─── FEEDBACK ─── */
.fb-header {
  display: flex;
  align-items: flex-end;
  gap: 20px;
  margin-bottom: 24px;
}
.score-display {
  font-family: 'Clash Display', sans-serif;
  font-size: 4.5rem;
  font-weight: 700;
  letter-spacing: -0.04em;
  line-height: 1;
}
.score-good { color: var(--teal); }
.score-ok { color: var(--amber); }
.score-bad { color: var(--rose); }
.verdict-stack { padding-bottom: 8px; }
.verdict-label {
  font-family: 'Space Mono', monospace;
  font-size: .62rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 4px;
}
.verdict-text {
  font-family: 'Clash Display', sans-serif;
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--ink);
}

.fb-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 18px;
}
.fb-cell {
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
}
.fb-cell-label {
  font-family: 'Space Mono', monospace;
  font-size: .6rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.lbl-green { color: var(--teal); }
.lbl-amber { color: var(--amber); }
.fb-cell-text {
  font-size: .88rem;
  color: var(--text-body);
  line-height: 1.65;
}

.sample-answer-box {
  background: var(--ink);
  border-radius: 14px;
  padding: 22px 24px;
  position: relative;
  overflow: hidden;
}
.sample-answer-box::before {
  content: '✦';
  position: absolute;
  top: 16px; right: 20px;
  font-size: 2rem;
  color: var(--gold);
  opacity: .3;
}
.sa-label {
  font-family: 'Space Mono', monospace;
  font-size: .6rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--gold);
  margin-bottom: 12px;
}
.sa-text {
  font-size: .9rem;
  color: rgba(255,255,255,.8);
  line-height: 1.75;
}

/* ─── RESULTS ─── */
.results-hero {
  background: var(--ink);
  border-radius: 24px;
  padding: 44px;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 24px;
}
.results-hero::before {
  content: '';
  position: absolute;
  top: -80px; left: -80px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(201,168,76,.15) 0%, transparent 70%);
}
.results-hero::after {
  content: '';
  position: absolute;
  bottom: -80px; right: -80px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(13,148,136,.12) 0%, transparent 70%);
}
.trophy-emoji { font-size: 4rem; margin-bottom: 16px; display: block; }
.results-title {
  font-family: 'Clash Display', sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.03em;
  margin-bottom: 8px;
}
.results-sub {
  font-size: .95rem;
  color: rgba(255,255,255,.5);
  margin-bottom: 32px;
}
.results-stats {
  display: flex;
  justify-content: center;
  gap: 0;
  position: relative;
  z-index: 1;
}
.rs-item {
  flex: 1;
  max-width: 160px;
  padding: 20px;
  border-right: 1px solid rgba(255,255,255,.08);
}
.rs-item:last-child { border-right: none; }
.rs-val {
  font-family: 'Clash Display', sans-serif;
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--gold);
  display: block;
  line-height: 1;
  letter-spacing: -0.03em;
}
.rs-lbl { font-size: .7rem; color: rgba(255,255,255,.4); margin-top: 6px; letter-spacing: .08em; }

/* ─── EXPANDER OVERRIDES ─── */
div[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  margin-bottom: 10px !important;
  box-shadow: none !important;
  background: var(--surface) !important;
}
div[data-testid="stExpander"] summary {
  font-family: 'Cabinet Grotesk', sans-serif !important;
  font-weight: 600 !important;
  font-size: .9rem !important;
}
div.stSpinner > div {
  border-top-color: var(--gold) !important;
}

/* ─── DIVIDER ─── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 24px 0 !important;
}

/* ─── ALERTS ─── */
div[data-testid="stAlert"] {
  border-radius: 12px !important;
  border: 1.5px solid var(--border) !important;
}

/* ─── SCROLL FADE IN ─── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-up { animation: fadeUp .5s ease both; }
.delay-1 { animation-delay: .1s; }
.delay-2 { animation-delay: .2s; }
.delay-3 { animation-delay: .3s; }

/* ─── FOOTER ─── */
.app-footer {
  margin-top: 56px;
  padding: 24px 0 8px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}
.footer-text {
  font-family: 'Space Mono', monospace;
  font-size: .62rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--text-muted);
}
.footer-heart { color: #e11d48; font-size: .9rem; }
.footer-name {
  font-family: 'Clash Display', sans-serif;
  font-size: .82rem;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: .04em;
}

</style>
""", unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "setup",
        "questions": [],
        "current_q": 0,
        "scores": [],
        "feedbacks": [],
        "role": "",
        "level": "",
        "lang": "English",
        "total": 5,
        "current_answer": "",
        "current_feedback": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── API ────────────────────────────────────────────────────────────────
def call_api(prompt: str, max_tokens: int = 1200) -> str:
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ API Key missing! Add GROQ_API_KEY in Streamlit Secrets.")
        st.stop()
    client = Groq(api_key=api_key)
    msg = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.choices[0].message.content


def parse_json(text: str):
    text = re.sub(r"```json|```", "", text).strip()
    return json.loads(text)


def generate_questions(role, level, industry, num, skills, lang):
    prompt = f"""You are an expert interview coach. Generate exactly {num} interview questions for:
- Role: {role}
- Level: {level}  
- Industry: {industry}
- Skills focus: {skills or 'general'}
- Language: {lang}

Return ONLY a valid JSON array, no markdown, no extra text:
[
  {{"question":"...","type":"behavioral|technical|situational|hr","tip":"short helpful tip for candidate"}}
]

Mix question types realistically. Make them challenging but fair for {level} level."""
    raw = call_api(prompt)
    return parse_json(raw)


def get_feedback(role, level, question, q_type, answer, lang):
    prompt = f"""You are a senior HR interviewer and career coach.
Evaluate this interview answer in {lang}.

Job Role: {role} ({level})
Question: {question}
Type: {q_type}
Candidate's Answer: {answer}

Return ONLY valid JSON, no markdown:
{{
  "score": <1-10>,
  "verdict": "Excellent|Good|Needs Improvement",
  "strengths": "<what they did well — 1-2 sentences>",
  "improvements": "<specific improvements needed — 1-2 sentences>",
  "sample_answer": "<strong model answer — 3-4 sentences>"
}}"""
    raw = call_api(prompt)
    return parse_json(raw)


# ─── SITE HEADER (always visible) ─────────────────────────────────────
st.markdown("""
<div class="site-header animate-up">
  <div class="logo-mark"><span>IQ</span>Interview Prep</div>
  <div class="header-pill">● AI-Powered</div>
</div>
""", unsafe_allow_html=True)

# ─── MOTIVATION TICKER ────────────────────────────────────────────────
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="tick-item ti-gold">🎯 HR is ready &mdash; <em>are YOU?</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-teal">💼 Your dream job won't wait</span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-rose">🔥 Practice today. <em>Ace it tomorrow.</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-white">🧠 Every answer = more confidence</span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-gold">⏱️ The interview clock is <em>ticking</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-teal">🎤 Speak up. Stand out. <em>Get hired.</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-rose">🏆 Top candidates prepare. <em>Do you?</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-gold">🎯 HR is ready &mdash; <em>are YOU?</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-teal">💼 Your dream job won't wait</span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-rose">🔥 Practice today. <em>Ace it tomorrow.</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-white">🧠 Every answer = more confidence</span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-gold">⏱️ The interview clock is <em>ticking</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-teal">🎤 Speak up. Stand out. <em>Get hired.</em></span>
    <span class="tick-sep">✦</span>
    <span class="tick-item ti-rose">🏆 Top candidates prepare. <em>Do you?</em></span>
    <span class="tick-sep">✦</span>
  </div>
</div>
<style>
.ticker-wrap {
  background: var(--ink);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 32px;
  border: 1px solid rgba(255,255,255,.06);
  position: relative;
}
.ticker-wrap::before, .ticker-wrap::after {
  content: '';
  position: absolute;
  top: 0; bottom: 0;
  width: 48px;
  z-index: 2;
  pointer-events: none;
}
.ticker-wrap::before { left: 0; background: linear-gradient(90deg, var(--ink), transparent); }
.ticker-wrap::after  { right: 0; background: linear-gradient(-90deg, var(--ink), transparent); }
.ticker-track {
  display: inline-flex;
  align-items: center;
  white-space: nowrap;
  animation: tickerScroll 28s linear infinite;
  padding: 13px 0;
}
.ticker-track:hover { animation-play-state: paused; }
.tick-item {
  font-family: 'Cabinet Grotesk', sans-serif;
  font-size: .82rem;
  font-weight: 600;
  color: rgba(255,255,255,.75);
  padding: 0 20px;
}
.tick-item em { font-style: normal; font-weight: 800; }
.ti-gold { color: #f5d98b; }
.ti-gold em { color: #ffeaa0; text-shadow: 0 0 12px rgba(255,220,80,.4); }
.ti-teal { color: #5eead4; }
.ti-teal em { color: #99f6e4; }
.ti-rose { color: #fda4af; }
.ti-rose em { color: #fecdd3; }
.ti-white { color: rgba(255,255,255,.9); }
.ti-white em { color: #fff; }
.tick-sep { color: #f5d98b; opacity: .5; font-size: .7rem; flex-shrink: 0; }
@keyframes tickerScroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# STAGE: SETUP
# ══════════════════════════════════════════════════════════════════════
if st.session_state.stage == "setup":

    # Hero
    st.markdown("""
    <div class="hero-section animate-up">
      <div class="hero-eyebrow">Mock Interview Platform</div>
      <h1 class="hero-title">Ace your next<br><em>interview</em></h1>
      <p class="hero-sub">AI-powered mock interviews with real-time feedback. Practice, improve, and land your dream role.</p>
      <div class="hero-stats">
        <div class="hero-stat">
          <div class="hero-stat-val">10+</div>
          <div class="hero-stat-lbl">Industries</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-val">4</div>
          <div class="hero-stat-lbl">Question Types</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-val">3</div>
          <div class="hero-stat-lbl">Languages</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Form
    st.markdown('<div class="section-label" style="margin-top:0;padding-top:8px">Configure your session</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Job Role", placeholder="e.g. Software Engineer")
    with col2:
        level = st.selectbox("Experience Level", [
            "Fresher (0–1 yr)", "Junior (1–3 yrs)",
            "Mid-level (3–6 yrs)", "Senior (6+ yrs)"
        ])

    col3, col4 = st.columns(2)
    with col3:
        industry = st.selectbox("Industry", [
            "Technology / IT", "Finance / Banking",
            "Marketing / Sales", "Healthcare",
            "Education", "Trading / Forex",
            "E-commerce", "General / Other"
        ])
    with col4:
        num = st.selectbox("Number of Questions", [3, 5, 8, 10], index=1)

    skills = st.text_input("Skills / Focus Areas (optional)", placeholder="e.g. Python, Leadership, Risk Management")

    col5, col6 = st.columns(2)
    with col5:
        lang = st.selectbox("Language", ["English", "Tamil", "Hindi"])

    if st.button("Begin Interview →", type="primary", use_container_width=True):
        if not role.strip():
            st.error("Please enter a job role to continue.")
        else:
            st.session_state.role  = role
            st.session_state.level = level
            st.session_state.lang  = lang
            st.session_state.total = int(num)
            with st.spinner("Generating your personalised interview…"):
                try:
                    qs = generate_questions(role, level, industry, num, skills, lang)
                    st.session_state.questions = qs
                    st.session_state.current_q = 0
                    st.session_state.scores    = []
                    st.session_state.feedbacks = []
                    st.session_state.stage     = "interview"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error generating questions: {e}")


# ══════════════════════════════════════════════════════════════════════
# STAGE: INTERVIEW
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "interview":

    cq    = st.session_state.current_q
    total = st.session_state.total
    qs    = st.session_state.questions

    if cq >= len(qs):
        st.session_state.stage = "results"
        st.rerun()

    q     = qs[cq]
    qtype = q.get("type", "behavioral")
    pct   = int((cq / total) * 100)

    # Progress bar
    st.markdown(f"""
    <div class="prog-bar-outer">
      <div class="prog-bar-inner" style="width:{pct}%"></div>
    </div>
    <div class="prog-meta">
      <span>{st.session_state.role} · {st.session_state.level}</span>
      <span>{cq} / {total} answered</span>
    </div>
    """, unsafe_allow_html=True)

    # Session header
    st.markdown(f"""
    <div class="session-header">
      <div class="session-meta">
        <span class="meta-chip">{st.session_state.lang}</span>
        <span class="meta-chip">{qtype.capitalize()}</span>
      </div>
      <div class="q-counter">Q{cq+1} <span>/ {total}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Question card
    tip_html = f'<div class="question-tip"><strong>Tip:</strong> {q["tip"]}</div>' if q.get("tip") else ""
    st.markdown(f"""
    <div class="question-card animate-up">
      <div class="q-type-row">
        <span class="type-badge type-{qtype}">{qtype}</span>
      </div>
      <div class="question-text">{q['question']}</div>
      {tip_html}
    </div>
    """, unsafe_allow_html=True)

    # Voice Input
    voice_html = """
<div class="voice-strip" id="vStrip">
  <button class="mic-orb" id="micBtn" onclick="toggleVoice()">🎤</button>
  <div class="voice-info" id="vInfo">
    <div class="vi-title">Click mic to record your answer</div>
    <div class="vi-sub">Supports English · Tamil · Hindi</div>
  </div>
</div>
<style>
  .voice-strip, .voice-strip * { font-family: 'Cabinet Grotesk', sans-serif; }
</style>
<script>
let rec = null, listening = false, final_ = '';
const SRec = window.SpeechRecognition || window.webkitSpeechRecognition;
if (!SRec) {
  document.getElementById('vStrip').innerHTML =
    '<div style="padding:10px;color:#94a3b8;font-size:.8rem">⚠️ Voice unsupported — please use Chrome</div>';
}
function toggleVoice() {
  listening ? stopRec() : startRec();
}
function startRec() {
  rec = new SRec();
  const map = { Tamil:'ta-IN', Hindi:'hi-IN', English:'en-US' };
  rec.lang = map['""" + st.session_state.lang + """'] || 'en-US';
  rec.continuous = true; rec.interimResults = true;
  rec.onstart = () => {
    listening = true;
    document.getElementById('micBtn').classList.add('on');
    document.getElementById('micBtn').innerHTML = '⏹';
    document.getElementById('vInfo').innerHTML =
      '<div class="vi-title" style="color:#e11d48">Recording…</div>' +
      '<div class="wave"><div class="wave-b"></div><div class="wave-b"></div><div class="wave-b"></div><div class="wave-b"></div><div class="wave-b"></div></div>';
  };
  rec.onresult = e => {
    let interim = ''; final_ = '';
    for (let i=0;i<e.results.length;i++){
      e.results[i].isFinal ? (final_ += e.results[i][0].transcript+' ') : (interim += e.results[i][0].transcript);
    }
    const txt = final_+interim;
    document.getElementById('vInfo').innerHTML =
      '<div class="vi-title" style="color:#e11d48">Recording…</div>' +
      '<div class="vi-sub live">'+(txt.length>70?'…'+txt.slice(-70):txt)+'</div>';
  };
  rec.onerror = e => { stopRec(); document.getElementById('vInfo').innerHTML = '<div class="vi-title" style="color:#e11d48">Error: '+e.error+'</div><div class="vi-sub">Try again or use Chrome</div>'; };
  rec.onend = () => {
    if (final_.trim()) {
      sessionStorage.setItem('vt', final_.trim());
      const u = new URL(window.location.href);
      u.searchParams.set('voice', encodeURIComponent(final_.trim()).substring(0, 200));
      window.history.replaceState({}, '', u);
    }
    stopRec();
  };
  rec.start();
}
function stopRec() {
  listening = false;
  if (rec) { try { rec.stop(); } catch(e){} }
  document.getElementById('micBtn').classList.remove('on');
  document.getElementById('micBtn').innerHTML = '🎤';
  const saved = sessionStorage.getItem('vt') || '';
  document.getElementById('vInfo').innerHTML = saved
    ? '<div class="vi-title">✅ Captured! Text filled below</div><div class="vi-sub">'+(saved.substring(0,60))+(saved.length>60?'…':'')+'</div>'
    : '<div class="vi-title">Click mic to record your answer</div><div class="vi-sub">Supports English · Tamil · Hindi</div>';
}
</script>
"""
    components.html(voice_html, height=82, scrolling=False)

    # Voice prefill
    voice_text = ""
    try:
        params = st.query_params
        if "voice" in params:
            voice_text = params["voice"]
            st.query_params.clear()
    except:
        pass

    answer = st.text_area(
        "Your Answer",
        value=voice_text,
        placeholder="Speak using the mic above, or type your answer here…",
        height=170,
        key=f"ans_{cq}"
    )

    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        submit = st.button("Get AI Feedback →", type="primary", use_container_width=True)
    with col2:
        skip = st.button("Skip", use_container_width=True)
    with col3:
        end = st.button("End", use_container_width=True)

    if submit:
        if not answer or len(answer.strip()) < 15:
            st.warning("Please write at least a few sentences before submitting.")
        else:
            with st.spinner("Analysing your answer…"):
                try:
                    fb = get_feedback(
                        st.session_state.role, st.session_state.level,
                        q["question"], qtype, answer, st.session_state.lang
                    )
                    st.session_state.scores.append(fb["score"])
                    st.session_state.feedbacks.append(fb)
                    st.session_state.current_feedback = fb
                    st.session_state.stage = "feedback"
                    st.rerun()
                except Exception as e:
                    st.error(f"Feedback error: {e}")

    if skip:
        st.session_state.scores.append(0)
        st.session_state.feedbacks.append(None)
        st.session_state.current_q += 1
        st.session_state.stage = "results" if st.session_state.current_q >= total else "interview"
        st.rerun()

    if end:
        st.session_state.stage = "results"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# STAGE: FEEDBACK
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "feedback":

    cq    = st.session_state.current_q
    total = st.session_state.total
    q     = st.session_state.questions[cq]
    fb    = st.session_state.current_feedback

    pct = int(((cq + 1) / total) * 100)
    st.markdown(f"""
    <div class="prog-bar-outer">
      <div class="prog-bar-inner" style="width:{pct}%"></div>
    </div>
    <div class="prog-meta">
      <span>Feedback for Q{cq+1}</span>
      <span>{cq+1} / {total} done</span>
    </div>
    """, unsafe_allow_html=True)

    # Question recap
    st.markdown(f"""
    <div class="question-card animate-up" style="padding:20px 24px;">
      <div class="q-type-row">
        <span class="type-badge type-{q.get('type','behavioral')}">{q.get('type','behavioral')}</span>
        <span style="font-size:.72rem;color:var(--text-muted);font-family:'Space Mono',monospace;">Q{cq+1}</span>
      </div>
      <div class="question-text" style="font-size:1rem;margin-bottom:0">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Score + verdict
    score = fb["score"]
    if score >= 8:
        sc_cls, emoji, verdict_str = "score-good", "🌟", fb["verdict"]
    elif score >= 6:
        sc_cls, emoji, verdict_str = "score-ok", "👍", fb["verdict"]
    else:
        sc_cls, emoji, verdict_str = "score-bad", "💪", fb["verdict"]

    st.markdown(f"""
    <div class="form-card animate-up" style="padding:28px 28px 24px;">
      <div class="fb-header">
        <div class="score-display {sc_cls}">{score}<span style="font-size:1.5rem;opacity:.5">/10</span></div>
        <div class="verdict-stack">
          <div class="verdict-label">AI Verdict</div>
          <div class="verdict-text">{emoji} {verdict_str}</div>
        </div>
      </div>
      <div class="fb-grid">
        <div class="fb-cell">
          <div class="fb-cell-label lbl-green">✦ Strengths</div>
          <div class="fb-cell-text">{fb['strengths']}</div>
        </div>
        <div class="fb-cell">
          <div class="fb-cell-label lbl-amber">↗ Improvements</div>
          <div class="fb-cell-text">{fb['improvements']}</div>
        </div>
      </div>
      <div class="sample-answer-box">
        <div class="sa-label">Model Answer</div>
        <div class="sa-text">{fb['sample_answer']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    is_last = (cq + 1 >= total)
    btn_label = "View Final Results →" if is_last else "Next Question →"
    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.current_q += 1
        st.session_state.current_feedback = None
        st.session_state.stage = "results" if st.session_state.current_q >= total else "interview"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# STAGE: RESULTS
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "results":

    scores   = [s for s in st.session_state.scores if s > 0]
    answered = len(scores)
    avg      = round(sum(scores) / answered * 10) if answered else 0
    best     = f"{max(scores)}/10" if scores else "—"

    if avg >= 75:   trophy, msg = "🏆", "Excellent work!"
    elif avg >= 55: trophy, msg = "🎯", "Solid performance!"
    else:           trophy, msg = "💪", "Keep practicing!"

    st.markdown(f"""
    <div class="results-hero animate-up">
      <span class="trophy-emoji">{trophy}</span>
      <div class="results-title">Interview Complete</div>
      <div class="results-sub">{msg} Here's how you did:</div>
      <div class="results-stats">
        <div class="rs-item">
          <span class="rs-val">{answered}</span>
          <div class="rs-lbl">Answered</div>
        </div>
        <div class="rs-item">
          <span class="rs-val">{avg}%</span>
          <div class="rs-lbl">Score</div>
        </div>
        <div class="rs-item">
          <span class="rs-val">{best}</span>
          <div class="rs-lbl">Best Answer</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.feedbacks:
        st.markdown('<div class="section-label" style="margin:24px 0 16px;">Question Breakdown</div>', unsafe_allow_html=True)
        for i, (fb, q) in enumerate(zip(st.session_state.feedbacks, st.session_state.questions)):
            if fb:
                s = fb["score"]
                dot = "🟢" if s >= 8 else "🟡" if s >= 6 else "🔴"
                with st.expander(f"{dot}  Q{i+1} — {q['question'][:55]}…  ·  {s}/10"):
                    st.markdown(f"**Strengths:** {fb['strengths']}")
                    st.markdown(f"**Improvements:** {fb['improvements']}")
            else:
                with st.expander(f"⚪  Q{i+1} — {q['question'][:55]}…  ·  Skipped"):
                    st.markdown("*This question was skipped.*")

    st.divider()
    if st.button("Start New Interview →", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()

# ── FOOTER (always shown) ──────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
  <span class="footer-text">Powered with</span>
  <span class="footer-heart">♥</span>
  <span class="footer-text">by</span>
  <span class="footer-name">Preethi U</span>
</div>
""", unsafe_allow_html=True)
