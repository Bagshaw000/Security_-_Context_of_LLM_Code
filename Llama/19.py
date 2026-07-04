import pandas as pd
from transformers import pipeline
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

def extract_sentences(text):
    sentences = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [sentence for sentence in sentences if not any(word in stop_word for word in word_tokenize(sentence))]
    return filtered_sentences

def generate_summary(summary_length, text):
    model = pipeline('summarization')
    input_text = f"{text}\n{summary_length}"
    output = model(input_text, max_length=summary_length)
    summary = [sent for sent in output['rendered_text'].split('. ') if len(sent) <= summary_length]
    return ' '.join(summary[:1])

def generate_summary_for_paper(paper_text, paper_title):
    sentences = extract_sentences(paper_text)
    summary = '\n'.join(sentences[:5])
    title = f"{paper_title}\n{generate_summary(150, 'Summary')}"
    output = f"{title}\n\n{summary}\n"
    return output