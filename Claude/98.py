import openai
import os

def generate_summary(paper_text, model="text-davinci-002", max_tokens=250, temperature=0.7, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"Summarize the following research paper:\n\n{paper_text}\n\nSummary:"

    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    summary = response.choices[0].text.strip()
    return summary