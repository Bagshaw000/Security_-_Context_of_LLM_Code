import os
import requests

class ResearchPaperSummarizer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.llm.example/summarize"

    def validate_input(self, text):
        if not isinstance(text, str) or len(text) == 0:
            raise ValueError("Input must be a non-empty string.")

    def generate_summary(self, paper_text):
        self.validate_input(paper_text)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {"text": paper_text}

        try:
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            summary = response.json().get("summary", "")
            return summary
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

if __name__ == "__main__":
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise EnvironmentError("API key not found. Set the LLM_API_KEY environment variable.")

    summarizer = ResearchPaperSummarizer(api_key)
    paper_text = "Your research paper text goes here."
    summary = summarizer.generate_summary(paper_text)
    if summary:
        print("Summary:", summary)