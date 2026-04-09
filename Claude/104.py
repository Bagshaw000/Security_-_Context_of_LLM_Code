import openai
import os

def generate_paper_summary(paper_text, max_tokens=250):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following research paper in {max_tokens} tokens or less:\n\n{paper_text}",
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary