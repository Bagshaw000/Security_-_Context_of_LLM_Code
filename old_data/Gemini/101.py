import openai







client = openai.OpenAI(api_key="your-api-key-here")

def generate_summary(filename):
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            paper_text = file.read()
        
        
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes academic research papers for a teacher."},
                {"role": "user", "content": "Please provide a concise summary of the following research paper, highlighting the main argument and findings:\n\n" + paper_text}
            ]
        )
        
        
        print("\n--- RESEARCH PAPER SUMMARY ---")
        print(response.choices[0].message.content)
        
    except FileNotFoundError:
        print("Error: I could not find a file named " + filename + ". Please check the spelling.")
    except Exception as e:
        print("An error occurred: " + str(e))



generate_summary("my_research_paper.txt")