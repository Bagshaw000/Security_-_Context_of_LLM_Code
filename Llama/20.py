import pandas as pd
from transformers import pipeline


summarizer = pipeline('summarization')


df = pd.read_csv("your_papers.csv")  


def generate_summary(text):
    summary = summarizer(text, max_length=150)
    return summary[0]['summary_text']


for index, row in df.iterrows():
    paper_text = row['text']  
    summary = generate_summary(paper_text)
    print(summary)