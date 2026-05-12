from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)

def get_embedding(text):

    return model.encode(text)

def calculate_similarity(text1, text2):

    embedding1 = get_embedding(text1)

    embedding2 = get_embedding(text2)

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return round(float(similarity) * 100, 2)