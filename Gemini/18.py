import boto3
import json
import pypdf
import unittest
from botocore.exceptions import ClientError

class ResearchPaperSummarizer:
    
    def __init__(self, region_name="us-east-1"):
        
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )

    def extract_text_from_pdf(self, file_path):
        
        try:
            reader = pypdf.PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            return full_text
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during PDF parsing: {e}")
            return None

    def generate_summary(self, text, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
        
        if not text:
            return "No text provided for summarization."

        
        
        prompt_config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": f"Summarize the following research paper. Focus on the core methodology, findings, and conclusion:\n\n{text[:20000]}"
                }
            ]
        }

        try:
            response = self.bedrock_runtime.invoke_model(
                body=json.dumps(prompt_config),
                modelId=model_id,
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body.get("content")[0].get("text")
        
        except ClientError as e:
            return f"AWS Bedrock Client Error: {e}"
        except Exception as e:
            return f"Error during summary generation: {e}"


class TestSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = ResearchPaperSummarizer()

    def test_initialization(self):
        self.assertIsNotNone(self.summarizer.bedrock_runtime)

    def test_empty_text_summary(self):
        result = self.summarizer.generate_summary("")
        self.assertEqual(result, "No text provided for summarization.")

def main():
    
    summarizer = ResearchPaperSummarizer()
    
    
    pdf_path = "sample_paper.pdf"
    
    print(f"Processing: {pdf_path}...")
    paper_content = summarizer.extract_text_from_pdf(pdf_path)
    
    if paper_content:
        summary = summarizer.generate_summary(paper_content)
        print("\n--- Research Paper Summary ---")
        print(summary)
    else:
        print("Failed to extract content from the PDF.")

if __name__ == "__main__":
    
    
    main()