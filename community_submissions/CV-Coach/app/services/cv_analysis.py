from typing import List

def analyze_cv(text: str):
    feedback = {
        "structure": [],
        "keywords": [],
        "achievements": [],
        "soft_skills": [],
        "formatting": [],
        "overall_feedback": [],
        "scores": {
            "structure": 0,
            "keywords": 0,
            "achievements": 0,
            "soft_skills": 0,
            "formatting": 0,
            "total": 0
        }
    }

    # Define expected sections and industry-specific keywords
    required_sections = ["Work Experience", "Education", "Skills", "Contact Information", "Projects"]
    industry_keywords = {
        "IT": ["Python", "JavaScript", "React", "Angular", "Cloud Computing", "Docker", "Kubernetes", "CI/CD", "DevOps"],
        "AI/ML": ["Machine Learning", "Deep Learning", "AI", "TensorFlow", "PyTorch", "Natural Language Processing", "Data Science"],
        "Software Engineering": ["System Design", "Agile", "Scrum", "OOP", "Microservices"]
    }
    soft_skills_keywords = ["Collaboration", "Team Leadership", "Problem Solving", "Communication", "Adaptability"]

    # Analyze structure
    for section in required_sections:
        if section.lower() in text.lower():
            feedback["structure"].append(f"Found section: {section}")
            feedback["scores"]["structure"] += 20 // len(required_sections)
        else:
            feedback["structure"].append(f"Missing section: {section}")

    # Analyze keywords
    matched_keywords = []
    for category, keywords in industry_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text.lower():
                matched_keywords.append(keyword)

    missing_keywords = set(sum(industry_keywords.values(), [])) - set(matched_keywords)
    feedback["keywords"].append(f"Found keywords: {', '.join(matched_keywords)}")
    feedback["keywords"].append(f"Missing keywords: {', '.join(missing_keywords)}")
    feedback["scores"]["keywords"] = min(40, len(matched_keywords) * 2)

    # Extract achievements
    achievement_phrases = ["improved", "increased", "reduced", "achieved", "led to", "developed"]
    achievements_found = [line for line in text.splitlines() if any(phrase in line.lower() for phrase in achievement_phrases)]
    feedback["achievements"].extend(achievements_found)
    feedback["scores"]["achievements"] = len(achievements_found) * 5

    # Analyze soft skills
    matched_soft_skills = [skill for skill in soft_skills_keywords if skill.lower() in text.lower()]
    feedback["soft_skills"].append(f"Soft skills identified: {', '.join(matched_soft_skills)}")
    feedback["scores"]["soft_skills"] = min(20, len(matched_soft_skills) * 5)

    # Analyze formatting
    feedback["formatting"].append("Font inconsistency detected. Consider using uniform fonts and spacing.")  # Example placeholder
    feedback["scores"]["formatting"] = 10  # Placeholder score for formatting analysis

    # Calculate total score
    feedback["scores"]["total"] = (
        feedback["scores"]["structure"]
        + feedback["scores"]["keywords"]
        + feedback["scores"]["achievements"]
        + feedback["scores"]["soft_skills"]
        + feedback["scores"]["formatting"]
    )

    # Add overall feedback
    if feedback["scores"]["total"] > 80:
        feedback["overall_feedback"].append("Your CV is strong and well-structured.")
    elif feedback["scores"]["total"] > 50:
        feedback["overall_feedback"].append("Your CV is decent but could use some improvements.")
    else:
        feedback["overall_feedback"].append("Your CV needs significant improvements in structure, keywords, and achievements.")

    return feedback
