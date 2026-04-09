



from openai import OpenAI



client = OpenAI(api_key="your-api-key-here")

def generate_paper_summary(filename):
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        return "Error: I could not find a file named 'paper.txt'. Please create it in this folder."

    
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for an English teacher. Summarize research papers clearly and concisely."},
            {"role": "user", "content": "Please provide a summary of the following research paper, highlighting the main argument and key findings:\n\n" + content}
        ]
    )

    
    return response.choices[0].message.content


document_name = "paper.txt"


print("Working on your summary... please wait a moment.")
summary_result = generate_paper_summary(document_name)

print("\n--- RESEARCH PAPER SUMMARY ---")
print(summary_result)
print("------------------------------")