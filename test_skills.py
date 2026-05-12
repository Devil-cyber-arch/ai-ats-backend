from app.nlp.preprocess import preprocess_text
from app.nlp.skill_extractor import extract_skills

sample = """
Experienced Python developer with FastAPI and PostgreSQL.
Worked on Machine Learning projects using TensorFlow.
"""

tokens = preprocess_text(sample)

skills = extract_skills(tokens)

print(skills)