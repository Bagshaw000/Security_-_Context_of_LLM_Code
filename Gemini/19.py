import json
import logging
from typing import List
from abc import ABC, abstractmethod
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        pass

class BedrockSummarizer(LLMProvider):
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0", region: str = "us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)
        self.model_id = model_id

    def generate_text(self, prompt: str) -> str:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        })
        try:
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json"
            )
            response_body = json.loads(response.get("body").read())
            return response_body.get("content")[0].get("text")
        except ClientError as e:
            logger.error(f"AWS Bedrock API Error: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during LLM invocation: {e}")
            raise

class DocumentProcessor:
    
    def __init__(self, llm: LLMProvider, chunk_size: int = 20000):
        self.llm = llm
        self.chunk_size = chunk_size

    def _chunk_content(self, text: str) -> List[str]:
        
        return [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]

    def summarize(self, raw_text: str) -> str:
        
        chunks = self._chunk_content(raw_text)
        
        if not chunks:
            return "No content available to summarize."

        logger.info(f"Processing {len(chunks)} document chunks.")
        
        intermediate_summaries = []
        for i, chunk in enumerate(chunks):
            prompt = (
                "Summarize the following research paper excerpt. "
                "Highlight objectives, methodology, and key results.\n\n"
                f"Excerpt: {chunk}"
            )
            intermediate_summaries.append(self.llm.generate_text(prompt))

        if len(intermediate_summaries) == 1:
            return intermediate_summaries[0]

        
        synthesis_prompt = (
            "Consolidate the following section summaries into a single, "
            "coherent executive summary of the full research paper:\n\n"
            f"{' '.join(intermediate_summaries)}"
        )
        return self.llm.generate_text(synthesis_prompt)

def run_summarization_pipeline(input_text: str):
    
    try:
        
        provider = BedrockSummarizer()
        processor = DocumentProcessor(llm=provider)
        
        summary = processor.summarize(input_text)
        print("RESEARCH PAPER SUMMARY:")
        print("=======================")
        print(summary)
        
    except Exception as e:
        logger.critical(f"Summarization pipeline failed: {e}")

if __name__ == "__main__":
    
    sample_text = "Research Paper Content: This study explores distributed authentication protocols..."
    run_summarization_pipeline(sample_text)