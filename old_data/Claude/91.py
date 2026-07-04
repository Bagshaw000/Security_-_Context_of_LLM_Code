import openai
import os


openai.api_key = "YOUR_API_KEY_HERE"

def generate_summary(paper_text):
    
    prompt = f"Summarize the following research paper in a concise and informative way:\n\n{paper_text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary


paper_text = "This is the text of a research paper. It discusses the latest findings in the field of machine learning..."
summary = generate_summary(paper_text)
print(summary)