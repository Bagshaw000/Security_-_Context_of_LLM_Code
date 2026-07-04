





from openai import OpenAI



client = OpenAI(api_key="YOUR_API_KEY_HERE")



paper_content = 


print("The computer is now reading the paper and writing a summary...")

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
        "role": "system", 
        "content": "You are a helpful assistant that summarizes research papers for an English teacher. Provide a clear, concise summary and list the main findings."
    },
    {
        "role": "user", 
        "content": f"Please summarize this research paper: {paper_content}"
    }
  ]
)


print("\n--- RESEARCH PAPER SUMMARY ---")
print(completion.choices[0].message.content)
print("\n--- END OF SUMMARY ---")