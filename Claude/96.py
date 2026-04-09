import openai
import os


openai.api_key = "your_api_key_here"

def generate_summary(paper_text, max_tokens=200):
    
    prompt = f"Summarize the following research paper in {max_tokens} tokens or less:\n\n{paper_text}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    summary = response.choices[0].text.strip()
    return summary


paper_text = 

summary = generate_summary(paper_text)
print(summary)