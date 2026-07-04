import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_paper_summary(paper_text, max_tokens=200):
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