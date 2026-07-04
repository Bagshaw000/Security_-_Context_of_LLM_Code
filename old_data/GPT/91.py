import openai

def summarize_research_paper(api_key, paper_text):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Please summarize the following research paper: {paper_text}"}
        ]
    )
    summary = response['choices'][0]['message']['content']
    return summary





