from app.models.resume_model import Resume
from app.models.job_model import Job
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from fastapi import APIRouter, Depends

from app.database import SessionLocal

from app.models.application_model import Application

from app.auth import verify_token

router = APIRouter()

@router.post("/shortlist")
def shortlist_candidate(
    data: dict,
    user = Depends(verify_token)
):

    if user["role"] != "recruiter":

        return {
            "error": "Only recruiters allowed"
        }

    db = SessionLocal()

    resume = db.query(Resume).filter(
        Resume.id == data["resume_id"]
    ).first()

    job = db.query(Job).filter(
        Job.id == data["job_id"]
    ).first()

    if not resume or not job:

        return {
            "error": "Resume or Job not found"
        }

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

    final_score = float(
        round(similarity * 100, 2)
    )

    if final_score >= 65:

        status = "shortlisted"

    else:

        status = "rejected"

    application = Application(
        resume_id=data["resume_id"],
        job_id=data["job_id"],
        status=status
    )

    db.add(application)

    db.commit()

    db.refresh(application)

    db.close()

    return {
        "match_score": final_score,
        "status": status
    }