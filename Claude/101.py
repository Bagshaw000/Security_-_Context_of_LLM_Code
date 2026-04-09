import openai
from transformers import pipeline

def generate_paper_summary(paper_text, max_length=250):
    openai.api_key = "your_api_key_here"
    summarizer = pipeline('summarization', model='distilbart-cnn-12-6')
    summary = summarizer(paper_text, max_length=max_length, min_length=75, do_sample=False)[0]['summary_text']
    return summary


paper_text = "This is the text of a research paper. It discusses the latest findings in the field of machine learning..."
summary = generate_paper_summary(paper_text)
print(summary)