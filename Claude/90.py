import openai
import os

def generate_summary(paper_text, max_tokens=200, model="text-davinci-002", temperature=0.7, top_p=0.9):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    prompt = f"Summarize the following research paper in {max_tokens} tokens:\n\n{paper_text}"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0
    )

    summary = response.choices[0].text.strip()
    return summary