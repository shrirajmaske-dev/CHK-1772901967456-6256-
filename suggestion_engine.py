# ============================================================
# FILE: suggestion_engine.py
# PURPOSE: Generate improvement suggestions and interview questions
#          for skills the candidate is missing
# INPUTS:  missing_skills (list of str), questions_db (dict)
# OUTPUTS: suggestions (dict) with tips and interview questions
# ============================================================


def generate_suggestions(missing_skills: list, questions_db: dict) -> dict:
    """
    Returns actionable improvement tips and interview prep questions
    for each missing skill.

    Args:
        missing_skills (list): Skills found in JD but absent from resume
        questions_db (dict):   Loaded interview_questions.json content

    Returns:
        dict: {
            "skill_tips": list of dict — [
                {
                    "skill":       str,
                    "tip":         str,
                    "questions":   list of str,
                    "resources":   list of str
                }
            ],
            "summary": str — high-level recommendation message
        }
    """
    if not missing_skills:
        return {
            "skill_tips": [],
            "summary": "🎉 Your resume already covers all the required skills for this role!"
        }

    # Generic learning resource templates per skill category
    resource_map = {
        "python":           ["https://docs.python.org/3/tutorial/", "https://realpython.com"],
        "javascript":       ["https://javascript.info", "https://developer.mozilla.org"],
        "react":            ["https://react.dev/learn", "https://scrimba.com/learn/learnreact"],
        "machine learning": ["https://www.coursera.org/learn/machine-learning", "https://kaggle.com/learn"],
        "deep learning":    ["https://www.deeplearning.ai", "https://pytorch.org/tutorials/"],
        "sql":              ["https://sqlzoo.net", "https://mode.com/sql-tutorial/"],
        "aws":              ["https://aws.amazon.com/training/", "https://acloudguru.com"],
        "docker":           ["https://docs.docker.com/get-started/", "https://play-with-docker.com"],
        "kubernetes":       ["https://kubernetes.io/docs/tutorials/", "https://killercoda.com"],
        "linux":            ["https://linuxjourney.com", "https://overthewire.org/wargames/bandit/"],
        "default":          ["https://www.udemy.com", "https://www.coursera.org", "https://roadmap.sh"]
    }

    improvement_tip_map = {
        "python":           "Add Python projects to GitHub. Highlight libraries like Pandas, FastAPI, or Scikit-learn.",
        "javascript":       "Build small interactive web apps. Contribute to open-source JS projects.",
        "react":            "Create a portfolio site using React. Publish components on GitHub.",
        "machine learning": "Complete a Kaggle competition. Document your model-building process in a notebook.",
        "deep learning":    "Replicate a research paper implementation. Share it on GitHub with a README.",
        "sql":              "Practice on LeetCode Database problems. Add SQL to your resume with specific query types.",
        "aws":              "Get AWS Cloud Practitioner certified. Deploy a personal project on AWS.",
        "docker":           "Containerize one of your existing projects. Add a Dockerfile to your GitHub repos.",
        "kubernetes":       "Deploy a microservice app with K8s locally using Minikube. Document the setup.",
        "linux":            "Use Linux as your daily driver or set up a VirtualBox VM. Practice CLI commands daily.",
        "nlp":              "Build a text classification or sentiment analysis project using Hugging Face.",
        "pytorch":          "Re-implement a classic deep learning architecture (e.g. ResNet) from scratch.",
        "pandas":           "Create a data analysis case study on Kaggle or GitHub using a public dataset.",
        "default":          "Add hands-on projects using this skill to your GitHub and mention them on your resume."
    }

    skill_tips = []
    for skill in missing_skills:
        key = skill.lower()

        # Fetch interview questions (fall back to default)
        questions = questions_db.get(key, questions_db.get("default", []))[:3]

        # Fetch tip
        tip = improvement_tip_map.get(key, improvement_tip_map["default"])

        # Fetch resources
        resources = resource_map.get(key, resource_map["default"])

        skill_tips.append({
            "skill":     skill,
            "tip":       tip,
            "questions": questions,
            "resources": resources
        })

    count = len(missing_skills)
    summary = (
        f"You are missing {count} skill{'s' if count != 1 else ''} required for this role. "
        "Focus on adding project-based evidence for each missing skill to your resume."
    )

    return {
        "skill_tips": skill_tips,
        "summary":    summary
    }
