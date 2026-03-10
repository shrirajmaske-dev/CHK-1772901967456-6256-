# ============================================================
# FILE: resume_parser.py
# PURPOSE: Extract raw text and detected skills from a resume PDF
# INPUTS:  uploaded file object (from Streamlit), skill_list (list of str)
# OUTPUTS: resume_text (str), detected_skills (list of str)
# ============================================================

import re
import pdfplumber


def extract_resume_text(file) -> str:
    """
    Reads an uploaded PDF file and extracts all text content.

    Args:
        file: A file-like object (e.g. from st.file_uploader)

    Returns:
        str: Full extracted text from the PDF, lowercased and cleaned.
    """
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"[ERROR] Could not parse PDF: {str(e)}"

    # Normalize whitespace and lowercase
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


def extract_resume_skills(text: str, skill_list: list) -> list:
    """
    Detects known skills from resume text using keyword matching.

    Args:
        text (str): Lowercased resume text from extract_resume_text()
        skill_list (list): Flat list of all known skills to match against

    Returns:
        list: Skills found in the resume text (deduplicated, sorted)
    """
    if not text or not skill_list:
        return []

    detected = set()
    for skill in skill_list:
        # Match whole-word or phrase occurrences
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text):
            detected.add(skill.lower())

    return sorted(list(detected))
