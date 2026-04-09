



from openai import OpenAI



api_key = "ENTER_YOUR_API_KEY_HERE"



paper_text = 


def generate_summary(text):
    
    client = OpenAI(api_key=api_key)
    
    
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant that creates clear, concise summaries of academic research papers for a teacher."
            },
            {
                "role": "user", 
                "content": "Please provide a summary of the following research paper. Focus on the main argument, the methods used, and the final conclusion:\n\n" + text
            }
        ]
    )
    
    
    return response.choices[0].message.content



print("The AI is now reading the paper and writing your summary. Please wait...")

try:
    summary = generate_summary(paper_text)
    print("\n--- RESEARCH PAPER SUMMARY ---")
    print(summary)
    print("\n--- END OF SUMMARY ---")
except Exception as e:
    print("An error occurred. Please check if your API key is correct.")
    print("Error details:", e)