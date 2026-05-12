from fastapi import APIRouter, UploadFile, File
import shutil

from app.database import SessionLocal
from app.models.resume_model import Resume

from app.nlp.info_extractor import (
    extract_email,
    extract_phone,
    extract_experience,
    extract_education
)

from app.nlp.pdf_parser import extract_text_from_pdf
from app.nlp.preprocess import preprocess_text
from app.nlp.skill_extractor import extract_skills
from app.nlp.embeddings import get_embedding
from app.nlp.summarizer import generate_summary

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    # Save file
    file_path = f"resumes/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract PDF text
    extracted_text = extract_text_from_pdf(file_path)

    # NLP preprocessing
    tokens = preprocess_text(extracted_text)

    # Extract skills
    skills = extract_skills(tokens)

    email = extract_email(extracted_text)

    phone = extract_phone(extracted_text)

    experience = extract_experience(
        extracted_text
    )

    education = extract_education(
        extracted_text
    )

    embedding = get_embedding(extracted_text).tolist()

    summary = generate_summary(extracted_text)

    # Database session
    db = SessionLocal()

    # Create resume record
    new_resume = Resume(
        filename=file.filename,
        extracted_text=extracted_text,
        skills=", ".join(skills),
        email=email,
        phone=phone,
        experience=experience,
        education=", ".join(education),
        embedding=embedding,
        summary=summary
    )

    db.add(new_resume)

    db.commit()

    db.refresh(new_resume)

    db.close()

    return {
        "message": "Resume processed successfully",
        "resume_id": new_resume.id,
        "filename": file.filename,
        "skills": skills
    }