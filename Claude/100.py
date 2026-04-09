import openai
import os

def summarize_paper(paper_text, model_name='text-davinci-002', max_tokens=200):
    openai.api_key = os.environ['OPENAI_API_KEY']
    prompt = f"Summarize the following research paper in {max_tokens} tokens or less:\n\n{paper_text}"
    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary