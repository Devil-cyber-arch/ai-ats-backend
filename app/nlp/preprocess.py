import spacy

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):

    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:

        if (
            not token.is_stop
            and not token.is_punct
            and not token.is_space
        ):

            cleaned_tokens.append(token.lemma_.lower())

    return cleaned_tokens