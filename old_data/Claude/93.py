import openai
import os

def summarize_paper(paper_text, max_tokens=200, temperature=0.7):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following research paper in {max_tokens} tokens:\n\n{paper_text}",
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )
    
    return response.choices[0].text.strip()