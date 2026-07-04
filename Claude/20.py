import openai
import os

def generate_summary(paper_text, model_name="text-davinci-002", max_tokens=500):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    response = openai.Completion.create(
        engine=model_name,
        prompt=f"Summarize the following research paper in a concise and informative way:\n\n{paper_text}",
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary


research_paper_text = 

summary = generate_summary(research_paper_text)
print(summary)