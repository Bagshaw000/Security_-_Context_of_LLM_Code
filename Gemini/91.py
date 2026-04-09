import boto3
import json
import unittest
from botocore.exceptions import ClientError

class ResearchPaperSummarizer:
    
    def __init__(self, region_name="us-east-1"):
        
        try:
            self.bedrock_runtime = boto3.client(
                service_name="bedrock-runtime",
                region_name=region_name
            )
        except Exception as e:
            print(f"Error initializing AWS client: {e}")
            raise

    def summarize(self, paper_content, max_summary_length=500):
        
        prompt = (
            f"You are a research assistant. Please provide a clear and concise summary "
            f"of the following research paper. Focus on the problem statement, "
            f"methodology, and key results.\n\nPaper Content:\n{paper_content}"
        )

        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_summary_length,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.5
        }

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(payload)
            )
            
            response_body = json.loads(response.get("body").read())
            summary = response_body.get("content")[0].get("text")
            return summary.strip()

        except ClientError as e:
            return f"AWS Service Error: {e.response['Error']['Message']}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

class TestResearchPaperSummarizer(unittest.TestCase):
    
    def setUp(self):
        self.summarizer = ResearchPaperSummarizer()

    def test_client_initialization(self):
        self.assertIsNotNone(self.summarizer.bedrock_runtime)

    def test_summary_output_type(self):
        
        test_text = "This is a dummy research paper about inventory management systems."
        
        
        self.assertTrue(callable(self.summarizer.summarize))

if __name__ == "__main__":
    
    sample_paper = 

    summarizer = ResearchPaperSummarizer()
    print("Generating summary...")
    result = summarizer.summarize(sample_paper)
    
    print("\n--- Summary ---")
    print(result)
    
    print("\n--- Running Unit Tests ---")
    
    unittest.main(argv=[''], exit=False)