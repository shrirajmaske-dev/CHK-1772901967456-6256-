# ============================================================
# FILE: jd_analyzer.py
# PURPOSE: Extract required skills from a job description
# INPUTS:  jd_text (str), skill_list (list of str)
# OUTPUTS: jd_skills (list of str)
# ============================================================

import re


def extract_jd_skills(jd_text: str, skill_list: list) -> list:
    """
    Identifies required skills mentioned in a job description.

    Args:
        jd_text (str): Raw job description text entered by the user
        skill_list (list): Flat list of all known skills to match against

    Returns:
        list: Skills found in the JD (deduplicated, sorted)
    """
    if not jd_text or not skill_list:
        return []

    normalized = re.sub(r'\s+', ' ', jd_text).strip().lower()
    detected = set()

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, normalized):
            detected.add(skill.lower())

    return sorted(list(detected))
