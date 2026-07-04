import openai
import os

def generate_summary(paper_text, max_length=300, temperature=0.7):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    prompt = f"Summarize the following research paper in {max_length} words or less:\n\n{paper_text}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_length,
        n=1,
        stop=None,
        temperature=temperature,
    )
    
    summary = response.choices[0].text.strip()
    return summary


paper_text = 

summary = generate_summary(paper_text)
print(summary)