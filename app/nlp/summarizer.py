from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_summary(text):

    text = text[:2000]

    summary = summarizer(
        text,
        max_length=60,
        min_length=20,
        do_sample=False
    )

    return summary[0]["summary_text"]