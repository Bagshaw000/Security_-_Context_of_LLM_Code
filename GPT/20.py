import openai

def generate_summary(paper_text):
    openai.api_key = 'your-api-key-here'
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Please summarize the following research paper: {paper_text}"}
        ]
    )
    
    summary = response['choices'][0]['message']['content']
    return summary


paper_text = "Your research paper text goes here."
summary = generate_summary(paper_text)
print(summary)