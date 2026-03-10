# ============================================================
# FILE: similarity_engine.py
# PURPOSE: Calculate semantic similarity between resume and JD
# INPUTS:  resume_text (str), jd_text (str)
# OUTPUTS: similarity_score (float, 0–100)
# ============================================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes the TF-IDF cosine similarity between resume and job description.

    Args:
        resume_text (str): Full extracted text from the resume
        jd_text (str): Full job description text

    Returns:
        float: Similarity score as a percentage (0.0 to 100.0), rounded to 2dp
    """
    if not resume_text or not jd_text:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),   # unigrams + bigrams for better phrase matching
            min_df=1
        )
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return round(float(score[0][0]) * 100, 2)
    except Exception:
        return 0.0
