from fastapi import Depends
from app.auth import verify_token

from fastapi import APIRouter

from app.database import SessionLocal
from app.models.job_model import Job
from app.models.resume_model import Resume
from app.nlp.matcher import calculate_match
from app.nlp.embeddings import get_embedding
from sqlalchemy import text

import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from app.models.resume_model import Resume

router = APIRouter()

@router.post("/create-job")
def create_job(
    job_data: dict,
    user = Depends(verify_token)
):

    if user["role"] != "recruiter":

        return {
        "error": "Only recruiters can create jobs"
        }

    db = SessionLocal()

    embedding = get_embedding(
    job_data["description"]
    ).tolist()

    new_job = Job(
        title=job_data["title"],
        description=job_data["description"],
        skills=job_data["skills"],
        embedding=embedding
    )

    db.add(new_job)

    db.commit()

    db.refresh(new_job)

    db.close()

    return {
        "message": "Job created successfully",
        "job_id": new_job.id
    }
@router.get("/match/{resume_id}/{job_id}")
def match_resume_to_job(resume_id: int, job_id: int):

    db = SessionLocal()

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not resume or not job:

        db.close()

        return {
            "error": "Resume or Job not found"
        }

    resume_skills = resume.skills.split(",")

    job_skills = job.skills.split(",")

    result = calculate_match(
        resume_skills,
        job_skills,
        resume.extracted_text,
        job.description
    )

    db.close()

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "job_title": job.title,
        "match_result": result
    }
@router.get("/top-candidates/{job_id}")
def top_candidates(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        db.close()

        return {
            "error": "Job not found"
        }

    resumes = db.query(Resume).all()

    ranked_candidates = []

    for resume in resumes:

        resume_skills = resume.skills.split(",")

        job_skills = job.skills.split(",")

        result = calculate_match(
            resume_skills,
            job_skills,
            resume.extracted_text,
            job.description
        )

        ranked_candidates.append({
            "resume_id": resume.id,
            "filename": resume.filename,
            "final_score": result["final_score"],
            "skill_score": result["skill_score"],
            "semantic_score": result["semantic_score"]
        })

    ranked_candidates.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    db.close()

    return ranked_candidates
@router.get("/vector-match/{job_id}")
def vector_match(job_id: int):

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        db.close()

        return {
            "error": "Job not found"
        }

    query = text("""

        SELECT
            id,
            filename,
            embedding <=> CAST(:job_embedding AS vector)
            AS distance

        FROM resumes

        ORDER BY distance ASC

        LIMIT 5

    """)

    result = db.execute(
        query,
        {
            "job_embedding": "[" + ",".join(
            map(str, job.embedding)
            ) + "]"
        }
    )

    matches = []

    for row in result:

        similarity_score = round(
            (1 - row.distance) * 100,
            2
        )

        matches.append({
            "resume_id": row.id,
            "filename": row.filename,
            "similarity_score": similarity_score
        })

    db.close()

    return matches
@router.get("/rank-candidates/{job_id}")
def rank_candidates(
    job_id: int,
    user = Depends(verify_token)
):

    if user["role"] != "recruiter":

        return {
            "error": "Only recruiters allowed"
        }

    db = SessionLocal()

    job = db.query(Job).filter(
        Job.id == job_id
    ).first()

    if not job:

        return {
            "error": "Job not found"
        }

    resumes = db.query(Resume).all()

    ranked_candidates = []

    for resume in resumes:

        resume_embedding = np.array(
            resume.embedding
        ).reshape(1, -1)

        job_embedding = np.array(
            job.embedding
        ).reshape(1, -1)

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding
        )[0][0]

        score = float(
            round(similarity * 100, 2)
        )

        ranked_candidates.append({

            "resume_id": resume.id,

            "filename": resume.filename,

            "match_score": score
        })

    ranked_candidates = sorted(
        ranked_candidates,
        key=lambda x: x["match_score"],
        reverse=True
    )

    db.close()

    return ranked_candidates