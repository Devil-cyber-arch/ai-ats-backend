from app.nlp.embeddings import calculate_similarity

text1 = """
Python developer with FastAPI and PostgreSQL
"""

text2 = """
Backend engineer skilled in APIs and databases
"""

score = calculate_similarity(text1, text2)

print(score)