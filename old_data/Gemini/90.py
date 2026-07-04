import boto3
import json
import unittest
from typing import Dict, Any

class ResearchPaperSummarizer:
    

    def __init__(self, region_name: str = "us-east-1", model_id: str = "anthropic.claude-3-haiku-20240307-v1:0"):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        self.model_id = model_id

    def create_prompt(self, paper_content: str) -> str:
        
        return (
            "Summarize the following research paper. Focus on the core problem, "
            "the proposed methodology, the key results, and the conclusion. "
            "Keep the summary technical yet accessible.\n\n"
            f"Paper Content:\n{paper_content}"
        )

    def summarize(self, text: str, max_tokens: int = 1000) -> str:
        
        if not text.strip():
            return "Error: No text provided for summarization."

        prompt = self.create_prompt(text)
        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
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
                body=json.dumps(payload),
                modelId=self.model_id,
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body.get("content")[0].get("text")
        
        except Exception as e:
            return f"An error occurred during inference: {str(e)}"


class TestResearchPaperSummarizer(unittest.TestCase):
    

    def setUp(self):
        
        self.summarizer = ResearchPaperSummarizer(region_name="us-east-1")

    def test_prompt_creation(self):
        sample_text = "AI is evolving rapidly."
        prompt = self.summarizer.create_prompt(sample_text)
        self.assertIn(sample_text, prompt)
        self.assertTrue(prompt.startswith("Summarize"))

    def test_empty_input_handling(self):
        result = self.summarizer.summarize("")
        self.assertEqual(result, "Error: No text provided for summarization.")


if __name__ == "__main__":
    
    
    
    
    
    
    unittest.main()