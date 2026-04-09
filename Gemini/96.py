import boto3
import json
import logging
import io
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from botocore.exceptions import ClientError


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResearchPaperService:
    

    def __init__(self, region: str = "us-east-1", model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region
        )
        self.model_id = model_id

    def extract_text_from_pdf(self, file_path: str) -> str:
        
        try:
            text_content = []
            with open(file_path, "rb") as f:
                reader = PdfReader(f)
                for page in reader.pages:
                    text_content.append(page.extract_text())
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {str(e)}")
            raise

    def generate_summary(self, document_text: str, summary_type: str = "executive") -> str:
        
        
        
        
        context_limit = 100000 
        truncated_text = document_text[:context_limit]

        prompt_config = {
            "executive": "Provide a high-level executive summary focusing on the problem statement and business impact.",
            "technical": "Provide a deep technical summary focusing on methodology, architecture, and empirical results."
        }

        system_prompt = (
            "You are a Principal Research Scientist. Summarize the following research paper "
            "with a focus on technical accuracy and clarity. "
            f"{prompt_config.get(summary_type, prompt_config['executive'])}"
        )

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Paper Content:\n\n{truncated_text}"
                        }
                    ]
                }
            ],
            "temperature": 0.1 
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

        except ClientError as e:
            logger.error(f"Bedrock API invocation failed: {e.response['Error']['Message']}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred during summarization: {str(e)}")
            raise

    def process_pipeline(self, pdf_path: str) -> Dict[str, Any]:
        
        logger.info(f"Starting processing pipeline for: {pdf_path}")
        
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text.strip():
            raise ValueError("Extracted text is empty. PDF might be image-based or corrupted.")

        summary = self.generate_summary(raw_text)
        
        return {
            "source": pdf_path,
            "summary": summary,
            "status": "COMPLETED"
        }

if __name__ == "__main__":
    
    
    service = ResearchPaperService()
    
    try:
        
        
        pass
    except Exception as err:
        logger.error(f"Service execution failed: {err}")