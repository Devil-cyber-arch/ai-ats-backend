import re

def extract_email(text):

    match = re.search(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

    return match.group(0) if match else None


def extract_phone(text):

    match = re.search(
        r"\+?\d[\d\s\-]{8,}\d",
        text
    )

    return match.group(0) if match else None


def extract_experience(text):

    match = re.search(
        r"(\d+)\+?\s+years",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(1)

    return "Not Found"


def extract_education(text):

    education_keywords = [
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "bsc",
        "msc",
        "phd"
    ]

    found = []

    text_lower = text.lower()

    for word in education_keywords:

        if word in text_lower:

            found.append(word)

    return found