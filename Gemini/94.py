import boto3
import json
import os
import unittest
from PyPDF2 import PdfReader

class ResearchSummarizer:
    
    def __init__(self, region_name="us-east-1"):
        
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )

    def extract_text_from_pdf(self, file_path):
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at: {file_path}")
        
        text_content = []
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            return "\n".join(text_content)
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def generate_summary(self, text, model_id="anthropic.claude-3-haiku-20240307-v1:0"):
        
        
        
        truncated_text = text[:60000] 

        prompt_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "You are an expert research assistant. Please provide a concise summary "
                        "of the following research paper. Focus on the problem statement, "
                        "the methodology used, and the key findings.\n\n"
                        f"<paper_content>{truncated_text}</paper_content>"
                    )
                }
            ],
            "temperature": 0.5
        }

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=model_id,
                body=json.dumps(prompt_body)
            )
            
            response_payload = json.loads(response.get("body").read())
            return response_payload["content"][0]["text"]
        except Exception as e:
            return f"Error calling LLM: {str(e)}"

def main():
    
    summarizer = ResearchSummarizer()
    target_file = "research_paper.pdf"
    
    if os.path.exists(target_file):
        print(f"Processing {target_file}...")
        raw_text = summarizer.extract_text_from_pdf(target_file)
        summary = summarizer.generate_summary(raw_text)
        print("\n--- PAPER SUMMARY ---\n")
        print(summary)
    else:
        print(f"Please place a file named '{target_file}' in the directory.")

class TestResearchSummarizer(unittest.TestCase):
    
    
    def setUp(self):
        self.summarizer = ResearchSummarizer()

    def test_invalid_file_path(self):
        with self.assertRaises(FileNotFoundError):
            self.summarizer.extract_text_from_pdf("missing_file.pdf")

    def test_extraction_logic_exists(self):
        self.assertTrue(callable(self.summarizer.extract_text_from_pdf))

if __name__ == "__main__":
    
    print("Running unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResearchSummarizer)
    unittest.TextTestRunner(verbosity=1).run(suite)
    
    
    