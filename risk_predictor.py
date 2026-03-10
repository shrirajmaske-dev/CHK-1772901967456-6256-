# ============================================================
# FILE: risk_predictor.py
# PURPOSE: Predict ATS/recruiter rejection risk from similarity score
# INPUTS:  similarity_score (float, 0–100)
# OUTPUTS: risk_label (str): "Low" | "Medium" | "High"
#          risk_color (str): hex color for UI display
#          risk_message (str): human-readable explanation
# ============================================================


def predict_rejection_risk(similarity_score: float) -> dict:
    """
    Maps a similarity score to a rejection risk tier with UI metadata.

    Args:
        similarity_score (float): Value between 0.0 and 100.0

    Returns:
        dict: {
            "label":   str  — "Low" | "Medium" | "High",
            "color":   str  — hex color string,
            "message": str  — explanation shown to user,
            "emoji":   str  — visual indicator
        }
    """
    score = float(similarity_score)

    if score >= 70:
        return {
            "label":   "Low",
            "color":   "#22c55e",   # green
            "emoji":   "✅",
            "message": (
                f"Your resume matches {score:.1f}% of the job description. "
                "Strong alignment — you are likely to pass initial screening."
            )
        }
    elif  70 >= score >= 45:
        return {
            "label":   "Medium",
            "color":   "#f59e0b",   # amber
            "emoji":   "⚠️",
            "message": (
                f"Your resume matches {score:.1f}% of the job description. "
                "Moderate alignment — consider adding more relevant keywords and skills."
            )
        }
    else:
        return {
            "label":   "High",
            "color":   "#ef4444",   # red
            "emoji":   "🚨",
            "message": (
                f"Your resume matches only {score:.1f}% of the job description. "
                "Low alignment — your resume may be filtered out by ATS before a human reviews it."
            )
        }
