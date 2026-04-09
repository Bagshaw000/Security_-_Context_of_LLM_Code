import openai
import os

def summarize_paper(paper_text, max_summary_length=150):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following research paper in {max_summary_length} words or less:\n\n{paper_text}",
        max_tokens=max_summary_length,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    summary = response.choices[0].text.strip()
    return summary