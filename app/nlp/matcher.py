from app.nlp.embeddings import calculate_similarity

def calculate_match(
    resume_skills,
    job_skills,
    resume_text,
    job_description
):

    # Skill matching
    resume_set = set(
        skill.strip().lower()
        for skill in resume_skills
    )

    job_set = set(
        skill.strip().lower()
        for skill in job_skills
    )

    matched_skills = resume_set.intersection(job_set)

    skill_score = (
        len(matched_skills) / len(job_set)
    ) * 100

    # Semantic similarity
    semantic_score = calculate_similarity(
        resume_text,
        job_description
    )

    # Final weighted score
    final_score = (
        (0.6 * semantic_score) +
        (0.4 * skill_score)
    )

    return {
        "skill_score": round(skill_score, 2),
        "semantic_score": round(semantic_score, 2),
        "final_score": round(final_score, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(job_set - matched_skills)
    }