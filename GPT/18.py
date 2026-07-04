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

if __name__ == "__main__":
    research_paper = "Your research paper text goes here."
    summary = generate_summary(research_paper)
    print("Summary:", summary)