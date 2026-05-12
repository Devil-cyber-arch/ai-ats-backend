from fastapi import FastAPI
from app.models.user_model import User
from app.routes.auth_routes import router as auth_router

from app.models.resume_model import Resume
from app.models.job_model import Job
from app.models.application_model import Application

from app.database import engine, Base
from app.routes.resume_routes import router
from app.routes.job_routes import router as job_router
from app.routes.application_routes import router as application_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
app.include_router(job_router)
app.include_router(auth_router)
app.include_router(application_router)

@app.get("/")
def home():
    return {"message": "AI Resume Backend Running"}