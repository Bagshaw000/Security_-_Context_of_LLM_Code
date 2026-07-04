import openai
import os


openai.api_key = os.environ["OPENAI_API_KEY"]

def generate_paper_summary(paper_text):
    prompt = f"Summarize the following research paper in a few concise sentences:\n\n{paper_text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()