import abc
import logging
import json
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMInterface(abc.ABC):
    
    @abc.abstractmethod
    def summarize(self, text: str, max_tokens: int = 500) -> str:
        
        pass

class BedrockSummarizer(LLMInterface):
    
    def __init__(
        self, 
        region_name: str = "us-east-1", 
        model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    ):
        self.client = boto3.client(service_name="bedrock-runtime", region_name=region_name)
        self.model_id = model_id

    def summarize(self, text: str, max_tokens: int = 1000) -> str:
        
        system_prompt = (
            "You are a research assistant. Summarize the following research paper. "
            "Focus on the problem statement, methodology, key findings, and implications."
        )
        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": text}]
                }
            ],
            "temperature": 0.3
        }

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body["content"][0]["text"]
            
        except ClientError as e:
            logger.error(f"AWS Bedrock client error: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during summarization: {e}")
            raise

class ResearchPaperProcessor:
    
    def __init__(self, llm_client: LLMInterface):
        self.llm_client = llm_client

    def process_content(self, raw_text: str) -> str:
        
        if not raw_text or len(raw_text.strip()) < 100:
            raise ValueError("Input text is too short to be a valid research paper.")
            
        logger.info("Initiating summarization request...")
        return self.llm_client.summarize(raw_text)

def main():
    
    
    sample_paper_text = 

    try:
        
        summarizer_service = BedrockSummarizer()
        processor = ResearchPaperProcessor(summarizer_service)
        
        summary = processor.process_content(sample_paper_text)
        
        print("-" * 30)
        print("Research Paper Summary:")
        print("-" * 30)
        print(summary)
        
    except Exception as e:
        logger.critical(f"System failure: {e}")

if __name__ == "__main__":
    main()