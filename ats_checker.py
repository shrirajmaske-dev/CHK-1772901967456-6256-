# ============================================================
# FILE: ats_checker.py
# PURPOSE: Check how well a resume satisfies ATS keyword requirements
# INPUTS:  resume_text (str), jd_skills (list of str)
# OUTPUTS: ats_result (dict) with score, matched, and missing skills
# ============================================================

import re


def check_ats_compatibility(resume_text: str, jd_skills: list) -> dict:
    """
    Compares resume text against required JD skills to produce an ATS score.

    Args:
        resume_text (str): Lowercased full text extracted from the resume
        jd_skills (list): Skills detected from the job description

    Returns:
        dict: {
            "score":          float  — ATS match percentage (0–100),
            "matched_skills": list   — skills present in both resume and JD,
            "missing_skills": list   — skills in JD but absent from resume,
            "total_required": int    — total number of JD skills checked
        }
    """
    if not jd_skills:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "total_required": 0
        }

    if not resume_text:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": jd_skills,
            "total_required": len(jd_skills)
        }

    matched = []
    missing = []

    for skill in jd_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text):
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(jd_skills)
    score = round((len(matched) / total) * 100, 2) if total > 0 else 0.0

    return {
        "score":          score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "total_required": total
    }
