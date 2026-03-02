import streamlit as st
from groq import Groq
import json
import re

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎤 AI Interview Prep Bot",
    page_icon="🎤",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 780px; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border-radius: 20px;
    padding: 36px 32px;
    text-align: center;
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,.08);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,.25), transparent 70%);
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 8px;
    letter-spacing: -0.03em;
}
.hero p { color: rgba(255,255,255,.6); font-size: .95rem; margin: 0; }
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,.25);
    border: 1px solid rgba(99,102,241,.4);
    color: #a5b4fc;
    font-size: .72rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    padding: 5px 14px; border-radius: 100px;
    margin-bottom: 14px;
}

/* ── CARDS ── */
.card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,.05);
}
.card-dark {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    color: #fff;
}

/* ── QUESTION ── */
.q-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}
.q-num {
    background: rgba(99,102,241,.12);
    border: 1px solid rgba(99,102,241,.25);
    color: #6366f1;
    font-size: .72rem; font-weight: 700;
    letter-spacing: .08em; text-transform: uppercase;
    padding: 4px 12px; border-radius: 100px;
}
.q-type-badge {
    font-size: .72rem; font-weight: 700;
    padding: 4px 10px; border-radius: 100px;
}
.type-behavioral { background: rgba(245,158,11,.12); color: #d97706; border: 1px solid rgba(245,158,11,.25); }
.type-technical   { background: rgba(99,102,241,.12); color: #6366f1; border: 1px solid rgba(99,102,241,.25); }
.type-situational { background: rgba(16,185,129,.12); color: #059669; border: 1px solid rgba(16,185,129,.25); }
.type-hr          { background: rgba(236,72,153,.12); color: #db2777; border: 1px solid rgba(236,72,153,.25); }

.q-text {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem; font-weight: 700;
    color: #0f172a; line-height: 1.45;
    margin-bottom: 14px;
}
.q-tip {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 10px;
    padding: 12px 14px;
    font-size: .82rem; color: #0369a1;
    margin-bottom: 16px;
}

/* ── FEEDBACK ── */
.fb-good    { background: #ecfdf5; border: 1.5px solid #6ee7b7; border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.fb-ok      { background: #fffbeb; border: 1.5px solid #fcd34d; border-radius: 14px; padding: 22px; margin-bottom: 16px; }
.fb-improve { background: #fef2f2; border: 1.5px solid #fca5a5; border-radius: 14px; padding: 22px; margin-bottom: 16px; }

.score-big {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem; font-weight: 800;
    line-height: 1;
}
.score-good    { color: #059669; }
.score-ok      { color: #d97706; }
.score-improve { color: #dc2626; }

.sample-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-top: 14px;
    font-size: .88rem;
    color: #475569;
    line-height: 1.7;
}
.sample-label {
    font-size: .68rem; font-weight: 700;
    letter-spacing: .1em; text-transform: uppercase;
    color: #6366f1; margin-bottom: 7px;
}

/* ── PROGRESS ── */
.progress-wrap {
    background: #f1f5f9;
    border-radius: 100px;
    height: 8px;
    margin-bottom: 8px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    transition: width .6s ease;
}
.progress-text {
    font-size: .78rem; color: #64748b;
    text-align: right; margin-bottom: 16px;
}

/* ── RESULTS ── */
.result-box {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border-radius: 20px; padding: 36px;
    text-align: center; color: #fff;
    margin-bottom: 20px;
}
.result-box h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    margin: 16px 0 8px;
}
.result-box p { color: rgba(255,255,255,.6); margin-bottom: 24px; }

.stat-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 24px;
}
.stat-item {
    background: rgba(255,255,255,.08);
    border: 1px solid rgba(255,255,255,.1);
    border-radius: 12px; padding: 16px;
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem; font-weight: 800;
    color: #a5b4fc; display: block; line-height: 1;
}
.stat-lbl { font-size: .72rem; color: rgba(255,255,255,.45); margin-top: 5px; }

/* ── STREAMLIT OVERRIDES ── */
div.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: transform .2s, box-shadow .2s !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,.15) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: #fff !important;
}
div.stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: .92rem !important;
}
div.stTextArea textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,.1) !important;
}
div.stSelectbox > div { border-radius: 10px !important; }
div.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
}
div.stSpinner { text-align: center; }
</style>
""", unsafe_allow_html=True)


# ── Session State ──────────────────────────────────────────────────────
def init_state():
    defaults = {
        "stage": "setup",       # setup | interview | feedback | results
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


# ── Claude API ─────────────────────────────────────────────────────────
def call_claude(prompt: str, max_tokens: int = 1200) -> str:
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


# ── Generate Questions ─────────────────────────────────────────────────
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

    raw = call_claude(prompt)
    return parse_json(raw)


# ── Get Feedback ───────────────────────────────────────────────────────
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

    raw = call_claude(prompt)
    return parse_json(raw)


# ══════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <div class="hero-badge">✨ Powered by Claude AI</div>
  <h1>🎤 Interview Prep Bot</h1>
  <p>AI mock interviews · Real feedback · Land your dream job</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# STAGE: SETUP
# ══════════════════════════════════════════════════════════════════════
if st.session_state.stage == "setup":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### ⚙️ Setup Your Interview")

    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("💼 Job Role", placeholder="e.g. Software Engineer, Sales Manager")
    with col2:
        level = st.selectbox("📊 Experience Level", [
            "Fresher (0–1 yr)", "Junior (1–3 yrs)",
            "Mid-level (3–6 yrs)", "Senior (6+ yrs)"
        ])

    col3, col4 = st.columns(2)
    with col3:
        industry = st.selectbox("🏭 Industry", [
            "Technology / IT", "Finance / Banking",
            "Marketing / Sales", "Healthcare",
            "Education", "Trading / Forex",
            "E-commerce", "General / Other"
        ])
    with col4:
        num = st.selectbox("📝 Questions", [3, 5, 8, 10], index=1)

    skills = st.text_input("🎯 Skills / Focus (optional)", placeholder="e.g. Python, Leadership, Risk Management")

    col5, col6 = st.columns(2)
    with col5:
        lang = st.selectbox("🌐 Language", ["English", "Tamil", "Hindi"])
    with col6:
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 Start Mock Interview", type="primary", use_container_width=True):
        if not role.strip():
            st.error("Please enter a Job Role!")
        else:
            st.session_state.role    = role
            st.session_state.level   = level
            st.session_state.lang    = lang
            st.session_state.total   = int(num)

            with st.spinner("🤖 Generating your interview questions..."):
                try:
                    qs = generate_questions(role, level, industry, num, skills, lang)
                    st.session_state.questions  = qs
                    st.session_state.current_q  = 0
                    st.session_state.scores     = []
                    st.session_state.feedbacks  = []
                    st.session_state.stage      = "interview"
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating questions: {e}")


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

    q = qs[cq]

    # Progress
    pct = int((cq / total) * 100)
    st.markdown(f"""
    <div class="progress-wrap">
      <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <div class="progress-text">{cq} of {total} completed</div>
    """, unsafe_allow_html=True)

    # Session info
    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(f"**Role:** {st.session_state.role}")
    col_b.markdown(f"**Level:** {st.session_state.level}")
    col_c.markdown(f"**Q {cq+1} / {total}**")

    st.divider()

    # Question card
    qtype = q.get("type","behavioral")
    type_class = f"type-{qtype}"
    st.markdown(f"""
    <div class="card">
      <div class="q-header">
        <span class="q-num">Question {cq+1} of {total}</span>
        <span class="q-type-badge {type_class}">{qtype.capitalize()}</span>
      </div>
      <div class="q-text">{q['question']}</div>
      {'<div class="q-tip">💡 ' + q["tip"] + '</div>' if q.get("tip") else ''}
    </div>
    """, unsafe_allow_html=True)

    # Answer input
    answer = st.text_area(
        "✍️ Your Answer",
        placeholder="Type your answer here... Take your time, structure your thoughts clearly.",
        height=160,
        key=f"answer_{cq}"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("✨ Get AI Feedback", type="primary", use_container_width=True)
    with col2:
        skip = st.button("⏭ Skip", use_container_width=True)

    if submit:
        if not answer or len(answer.strip()) < 15:
            st.warning("Please write a proper answer (at least a few sentences).")
        else:
            with st.spinner("🤖 Analysing your answer..."):
                try:
                    fb = get_feedback(
                        st.session_state.role,
                        st.session_state.level,
                        q["question"],
                        qtype,
                        answer,
                        st.session_state.lang
                    )
                    st.session_state.scores.append(fb["score"])
                    st.session_state.feedbacks.append(fb)
                    st.session_state.current_feedback = fb
                    st.session_state.stage = "feedback"
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Feedback error: {e}")

    if skip:
        st.session_state.scores.append(0)
        st.session_state.feedbacks.append(None)
        st.session_state.current_q += 1
        if st.session_state.current_q >= total:
            st.session_state.stage = "results"
        st.rerun()

    st.divider()
    if st.button("🔚 End Session & See Results"):
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

    # Progress
    pct = int(((cq + 1) / total) * 100)
    st.markdown(f"""
    <div class="progress-wrap">
      <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    <div class="progress-text">{cq+1} of {total} completed</div>
    """, unsafe_allow_html=True)

    # Question recap
    st.markdown(f"""
    <div class="card">
      <div style="font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#64748b;margin-bottom:8px">
        Question {cq+1}
      </div>
      <div style="font-size:1rem;font-weight:600;color:#0f172a;">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Feedback
    score   = fb["score"]
    verdict = fb["verdict"]
    if score >= 8:
        fb_class  = "fb-good"
        score_cls = "score-good"
        emoji     = "🌟"
    elif score >= 6:
        fb_class  = "fb-ok"
        score_cls = "score-ok"
        emoji     = "👍"
    else:
        fb_class  = "fb-improve"
        score_cls = "score-improve"
        emoji     = "💪"

    st.markdown(f"""
    <div class="{fb_class}">
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px">
        <div class="score-big {score_cls}">{score}<span style="font-size:1.2rem">/10</span></div>
        <div>
          <div style="font-size:1.05rem;font-weight:700;color:#0f172a">{emoji} {verdict}</div>
          <div style="font-size:.78rem;color:#64748b;margin-top:2px">AI Evaluation</div>
        </div>
      </div>
      <div style="font-size:.9rem;color:#374151;line-height:1.7;margin-bottom:8px">
        ✅ <strong>Strengths:</strong> {fb['strengths']}
      </div>
      <div style="font-size:.9rem;color:#374151;line-height:1.7">
        🎯 <strong>Improve:</strong> {fb['improvements']}
      </div>
      <div class="sample-box">
        <div class="sample-label">✨ Model Answer</div>
        {fb['sample_answer']}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Next button
    is_last = (cq + 1 >= total)
    btn_label = "🏁 See Final Results" if is_last else "➡️ Next Question"

    if st.button(btn_label, type="primary", use_container_width=True):
        st.session_state.current_q += 1
        st.session_state.current_feedback = None
        if st.session_state.current_q >= total:
            st.session_state.stage = "results"
        else:
            st.session_state.stage = "interview"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════
# STAGE: RESULTS
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "results":

    scores   = [s for s in st.session_state.scores if s > 0]
    answered = len(scores)
    avg      = round(sum(scores) / answered * 10) if answered else 0
    best     = f"{max(scores)}/10" if scores else "—"

    if avg >= 75:
        trophy = "🏆"; overall = "Excellent Performance!"
    elif avg >= 55:
        trophy = "🎯"; overall = "Good Performance!"
    else:
        trophy = "💪"; overall = "Keep Practicing!"

    st.markdown(f"""
    <div class="result-box">
      <div style="font-size:4rem">{trophy}</div>
      <h2>Interview Complete!</h2>
      <p>{overall} Here's your summary:</p>
      <div class="stat-grid">
        <div class="stat-item">
          <span class="stat-val">{answered}</span>
          <div class="stat-lbl">Questions Answered</div>
        </div>
        <div class="stat-item">
          <span class="stat-val">{avg}%</span>
          <div class="stat-lbl">Average Score</div>
        </div>
        <div class="stat-item">
          <span class="stat-val">{best}</span>
          <div class="stat-lbl">Best Answer</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Score breakdown
    if st.session_state.feedbacks:
        st.markdown("#### 📊 Question Breakdown")
        for i, (fb, q) in enumerate(zip(st.session_state.feedbacks, st.session_state.questions)):
            if fb:
                score = fb["score"]
                color = "#059669" if score >= 8 else "#d97706" if score >= 6 else "#dc2626"
                with st.expander(f"Q{i+1}: {q['question'][:60]}... — Score: {score}/10"):
                    st.markdown(f"**✅ Strengths:** {fb['strengths']}")
                    st.markdown(f"**🎯 Improve:** {fb['improvements']}")
            else:
                with st.expander(f"Q{i+1}: {q['question'][:60]}... — Skipped"):
                    st.markdown("*This question was skipped.*")

    st.divider()
    if st.button("🔄 Start New Interview", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_state()
        st.rerun()
