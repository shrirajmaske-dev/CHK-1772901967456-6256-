



# ============================================================
# FILE: app.py
# PURPOSE: HireReady AI — Streamlit UI entry point
# USAGE:   streamlit run app.py
# NOTE:    Only this file imports other project modules.
#          All modules are stateless and return data only.
# ============================================================

import json
import os
import streamlit as st

from resume_parser    import extract_resume_text, extract_resume_skills
from jd_analyzer      import extract_jd_skills
from similarity_engine import calculate_similarity
from risk_predictor   import predict_rejection_risk
from ats_checker      import check_ats_compatibility
from suggestion_engine import generate_suggestions


# ── Helpers ────────────────────────────────────────────────

@st.cache_data
def load_json(path: str) -> dict | list:
    """Load and cache a JSON data file."""
    with open(path, "r") as f:
        return json.load(f)


def flatten_skills(skill_db: dict) -> list:
    """Flatten all domain skill lists into a single deduplicated list."""
    all_skills = []
    for skills in skill_db.values():
        all_skills.extend(skills)
    return list(set(all_skills))


def render_score_card(label: str, value: str, color: str, subtitle: str = ""):
    """Render a styled metric card using HTML."""
    st.markdown(
        f"""
        <div style="
            background: #1e1e2e;
            border-left: 5px solid {color};
            border-radius: 10px;
            padding: 18px 22px;
            margin-bottom: 10px;
        ">
            <div style="color:#aaa; font-size:13px; text-transform:uppercase;
                        letter-spacing:1px;">{label}</div>
            <div style="color:{color}; font-size:32px; font-weight:800;
                        margin:4px 0;">{value}</div>
            <div style="color:#ccc; font-size:13px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_skill_badge(skill: str, color: str):
    """Render an inline pill/badge for a skill."""
    return (
        f'<span style="background:{color}22; color:{color}; border:1px solid {color}55; '
        f'border-radius:20px; padding:4px 12px; font-size:13px; '
        f'margin:3px; display:inline-block;">{skill}</span>'
    )


# ── Page Config ────────────────────────────────────────────

st.set_page_config(
    page_title="HireReady AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Global style overrides
st.markdown("""
<style>
    body, .stApp { background-color: #0f0f1a; color: #e2e2e2; }
    h1, h2, h3 { color: #ffffff; }
    .stTextArea textarea { background: #1a1a2e; color: #e2e2e2; border-color: #333; }
    .stFileUploader { background: #1a1a2e; border-radius: 10px; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 2rem; font-weight: 600; font-size: 15px;
        transition: 0.2s;
    }
    .stButton>button:hover { opacity: 0.85; transform: scale(1.02); }
    .stExpander { background: #1a1a2e; border-radius: 10px; }
    hr { border-color: #2a2a3e; }
    .section-title {
        font-size: 18px; font-weight: 700; color: #a78bfa;
        border-bottom: 2px solid #2a2a3e; padding-bottom: 6px;
        margin: 24px 0 14px;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center; padding: 30px 0 10px;">
    <div style="font-size:48px;">🎯</div>
    <h1 style="font-size:42px; font-weight:900; margin:0;
               background: linear-gradient(135deg, #6366f1, #a78bfa, #ec4899);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        HireReady AI
    </h1>
    <p style="color:#888; font-size:16px; margin-top:8px;">
        Upload your resume · Paste a job description · Get AI-powered gap analysis
    </p>
</div>
<hr/>
""", unsafe_allow_html=True)


# ── Load Data ──────────────────────────────────────────────

BASE_DIR = os.path.dirname(__file__)

skill_db       = load_json(os.path.join(BASE_DIR, "data", "skill_database.json"))
questions_db   = load_json(os.path.join(BASE_DIR, "data", "interview_questions.json"))
all_skills     = flatten_skills(skill_db)


# ── Input Section ──────────────────────────────────────────

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-title">📄 Upload Resume (PDF)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Drop your resume PDF here",
        type=["pdf"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}**")

with col_right:
    st.markdown('<div class="section-title">📋 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        label="Paste the job description",
        placeholder="Paste the full job description here...",
        height=200,
        label_visibility="collapsed"
    )

st.markdown("<br>", unsafe_allow_html=True)
analyze_clicked = st.button("🔍  Analyze My Resume", use_container_width=True)


# ── Analysis ───────────────────────────────────────────────

if analyze_clicked:

    # ── Validation ──
    if not uploaded_file:
        st.error("Please upload your resume PDF before analyzing.")
        st.stop()
    if not jd_text.strip():
        st.error("Please paste a job description before analyzing.")
        st.stop()

    with st.spinner("Analyzing your resume against the job description..."):

        # 1. Parse resume
        resume_text   = extract_resume_text(uploaded_file)
        resume_skills = extract_resume_skills(resume_text, all_skills)

        # 2. Analyze JD
        jd_skills = extract_jd_skills(jd_text, all_skills)

        # 3. Similarity score
        similarity_score = calculate_similarity(resume_text, jd_text)

        # 4. Rejection risk
        risk = predict_rejection_risk(similarity_score)

        # 5. ATS compatibility
        ats_result = check_ats_compatibility(resume_text, jd_skills)

        # 6. Suggestions
        suggestions = generate_suggestions(ats_result["missing_skills"], questions_db)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:22px; font-weight:800; color:#fff; margin-bottom:18px;">
        📊 Analysis Results
    </div>
    """, unsafe_allow_html=True)

    # ── Score Cards ──
    c1, c2, c3 = st.columns(3)
    with c1:
        render_score_card(
            "Similarity Score",
            f"{similarity_score:.1f}%",
            "#6366f1",
            "Resume vs Job Description"
        )
    with c2:
        render_score_card(
            "ATS Compatibility",
            f"{ats_result['score']:.1f}%",
            "#22d3ee",
            f"{len(ats_result['matched_skills'])} / {ats_result['total_required']} skills matched"
        )
    with c3:
        render_score_card(
            "Rejection Risk",
            f"{risk['emoji']} {risk['label']}",
            risk["color"],
            risk["message"][:60] + "..."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Skill Breakdown ──
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
        if ats_result["matched_skills"]:
            badges = "".join(
                render_skill_badge(s, "#22c55e")
                for s in ats_result["matched_skills"]
            )
            st.markdown(f'<div style="line-height:2.2">{badges}</div>', unsafe_allow_html=True)
        else:
            st.info("No matched skills detected.")

    with col_b:
        st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
        if ats_result["missing_skills"]:
            badges = "".join(
                render_skill_badge(s, "#ef4444")
                for s in ats_result["missing_skills"]
            )
            st.markdown(f'<div style="line-height:2.2">{badges}</div>', unsafe_allow_html=True)
        else:
            st.success("Your resume covers all required skills! 🎉")

    # ── Resume Skills Detected ──
    with st.expander("📝 All Skills Detected in Your Resume", expanded=False):
        if resume_skills:
            badges = "".join(render_skill_badge(s, "#a78bfa") for s in resume_skills)
            st.markdown(f'<div style="line-height:2.4">{badges}</div>', unsafe_allow_html=True)
        else:
            st.warning("No known skills were detected in your resume text.")

    # ── Improvement Suggestions ──
    st.markdown('<div class="section-title">💡 Improvement Suggestions & Interview Prep</div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<p style="color:#aaa; margin-bottom:16px;">{suggestions["summary"]}</p>',
        unsafe_allow_html=True
    )

    if suggestions["skill_tips"]:
        for tip_data in suggestions["skill_tips"]:
            with st.expander(f"🔧 {tip_data['skill'].title()}", expanded=False):

                st.markdown(f"**💬 How to address this gap:**")
                st.markdown(f"> {tip_data['tip']}")

                if tip_data["questions"]:
                    st.markdown("**🎤 Interview Questions to Prepare:**")
                    for i, q in enumerate(tip_data["questions"], 1):
                        st.markdown(f"**Q{i}.** {q}")

                if tip_data["resources"]:
                    st.markdown("**📚 Learning Resources:**")
                    for url in tip_data["resources"]:
                        st.markdown(f"- [{url}]({url})")
    else:
        st.success("No improvements needed — your resume is well-aligned! 🚀")

    # ── Risk Detail Banner ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background:{risk['color']}18; border:1px solid {risk['color']}55;
                    border-radius:10px; padding:16px 22px; margin-top:10px;">
            <span style="font-size:20px;">{risk['emoji']}</span>
            <strong style="color:{risk['color']}; margin-left:8px;">
                Rejection Risk: {risk['label']}
            </strong>
            <p style="color:#ccc; margin:6px 0 0; font-size:14px;">{risk['message']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────

st.markdown("""
<hr/>
<div style="text-align:center; color:#555; font-size:13px; padding: 10px 0 20px;">
    HireReady AI · Built with Streamlit, pdfplumber &amp; scikit-learn
</div>
""", unsafe_allow_html=True)
