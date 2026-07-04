import openai

def summarize_research_paper(api_key, paper_text):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Please summarize the following research paper: {paper_text}"}
            ]
        )
        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    api_key = input("Enter your OpenAI API key: ")
    paper_text = input("Paste the research paper text here: ")
    summary = summarize_research_paper(api_key, paper_text)
    print("Summary of the research paper:")
    print(summary)