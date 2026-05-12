from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database import Base

class Application(Base):

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)

    resume_id = Column(
        Integer,
        ForeignKey("resumes.id")
    )

    job_id = Column(
        Integer,
        ForeignKey("jobs.id")
    )

    status = Column(String)