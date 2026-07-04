import boto3
import json
import unittest
from PyPDF2 import PdfReader

class ResearchPaperSummarizer:
    
    def __init__(self, region_name="us-east-1"):
        
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime", 
            region_name=region_name
        )
        
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    def extract_text(self, file_path, limit_pages=10):
        
        try:
            reader = PdfReader(file_path)
            extracted_text = ""
            page_count = min(len(reader.pages), limit_pages)
            
            for i in range(page_count):
                page = reader.pages[i]
                extracted_text += page.extract_text() + "\n"
                
            return extracted_text.strip()
        except Exception as e:
            return f"Error processing PDF: {str(e)}"

    def get_summary(self, text):
        
        if not text:
            return "No text provided for summarization."

        
        context_text = text[:18000]

        prompt = (
            "Summarize the following research paper. Provide a concise overview of: "
            "1. Research Objective, 2. Methodology, 3. Key Findings, and 4. Conclusion.\n\n"
            f"Paper Content:\n{context_text}"
        )

        
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        }

        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(native_request)
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body["content"][0]["text"]
        except Exception as e:
            return f"Error during LLM invocation: {str(e)}"

class TestSummarizer(unittest.TestCase):
    
    def setUp(self):
        self.summarizer = ResearchPaperSummarizer()

    def test_empty_text_input(self):
        result = self.summarizer.get_summary("")
        self.assertEqual(result, "No text provided for summarization.")

    def test_client_initialization(self):
        self.assertIsNotNone(self.summarizer.bedrock_client)

def main():
    
    summarizer = ResearchPaperSummarizer()
    
    
    
    
    
    

    
    print("Running unit tests...")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    main()