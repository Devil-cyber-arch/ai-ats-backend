SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "fastapi",
    "django",
    "flask",
    "react",
    "node.js",
    "docker",
    "kubernetes",
    "sql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "git",
    "aws"
]

def extract_skills(tokens):

    detected_skills = set()

    text = " ".join(tokens)

    for skill in SKILLS:

        if skill.lower() in text:
            detected_skills.add(skill)

    return list(detected_skills)