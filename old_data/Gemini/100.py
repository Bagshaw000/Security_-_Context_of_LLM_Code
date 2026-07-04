



import openai


client = openai.OpenAI(api_key='your-api-key-here')

def generate_summary():
    
    try:
        with open('paper.txt', 'r', encoding='utf-8') as file:
            research_paper_text = file.read()
    except FileNotFoundError:
        print("Error: I couldn't find a file named 'paper.txt'. Please make sure it is in the same folder.")
        return

    print("Sending the paper to the AI... please wait.")

    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes research papers for an English teacher."},
            {"role": "user", "content": f"Please provide a concise summary of this research paper:\n\n{research_paper_text}"}
        ]
    )

    
    summary_result = response.choices[0].message.content

    
    with open('summary.txt', 'w', encoding='utf-8') as output_file:
        output_file.write(summary_result)

    print("Success! Your summary has been saved to a file named 'summary.txt'.")


if __name__ == "__main__":
    generate_summary()