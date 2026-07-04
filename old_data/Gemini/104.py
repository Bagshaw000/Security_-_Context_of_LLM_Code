






import openai


my_api_key = "YOUR_OPENAI_API_KEY_HERE"

def summarize_research_paper():
    
    client = openai.OpenAI(api_key=my_api_key)

    try:
        
        with open("paper.txt", "r", encoding="utf-8") as file:
            paper_text = file.read()

        print("The computer is now reading your paper and writing a summary. Please wait...")

        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes academic research papers for a teacher."},
                {"role": "user", "content": "Please provide a clear, bulleted summary of the main points of this research paper:\n\n" + paper_text}
            ]
        )

        
        summary = response.choices[0].message.content

        
        print("\n--- RESEARCH PAPER SUMMARY ---")
        print(summary)
        print("\n--- END OF SUMMARY ---")

    except FileNotFoundError:
        print("Error: I could not find a file named 'paper.txt'.")
        print("Please make sure you have created a text file with that exact name in this folder.")
    except Exception as e:
        print("An error occurred. This might be due to an invalid API key or an internet issue.")
        print("Details for troubleshooting:", e)


if __name__ == "__main__":
    summarize_research_paper()