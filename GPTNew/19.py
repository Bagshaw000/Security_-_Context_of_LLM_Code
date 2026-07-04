import requests
import json

class ResearchPaperSummarizer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.llm-service.com/summarize"

    def generate_summary(self, paper_text):
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"text": paper_text}
            )
            response.raise_for_status()
            summary = response.json().get("summary", "No summary available.")
            return summary
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return "Error generating summary."
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return "Error generating summary."
        except json.JSONDecodeError:
            print("Error decoding JSON response.")
            return "Error generating summary."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error generating summary."


if __name__ == "__main__":
    api_key = "your_api_key_here"
    summarizer = ResearchPaperSummarizer(api_key)
    paper_text = "Your research paper text goes here."
    summary = summarizer.generate_summary(paper_text)
    print(summary)