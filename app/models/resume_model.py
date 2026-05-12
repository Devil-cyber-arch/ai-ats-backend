from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector

from app.database import Base

class Resume(Base):

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    extracted_text = Column(String)

    skills = Column(String)

    email = Column(String)

    phone = Column(String)

    experience = Column(String)

    education = Column(String)

    summary = Column(String)

    embedding = Column(Vector(384))


    
    