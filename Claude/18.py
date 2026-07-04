import openai

def generate_paper_summary(paper_text):
    openai.api_key = "YOUR_OPENAI_API_KEY"
    
    prompt = f"Summarize the following research paper in 3-5 sentences:\n\n{paper_text}"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].text.strip()


paper_text = 

summary = generate_paper_summary(paper_text)
print(summary)