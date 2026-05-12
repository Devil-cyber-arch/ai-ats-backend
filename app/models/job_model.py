from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector

from app.database import Base

class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    skills = Column(String)

    embedding = Column(Vector(384))