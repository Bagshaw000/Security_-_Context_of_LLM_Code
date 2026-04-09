import json
import logging
import boto3
import PyPDF2
from typing import List, Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ResearchSummarizer")

class ResearchPaperSummarizer:
    
    
    def __init__(self, region_name: str = "us-east-1", model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )
        self.model_id = model_id
        
        self.chunk_size_chars = 40000 

    def extract_text_from_pdf(self, file_path: str) -> str:
        
        text_content = []
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    extracted = page.extract_text()
                    if extracted:
                        text_content.append(extracted)
            return "\n".join(text_content)
        except Exception as e:
            logger.error(f"Failed to extract text from PDF {file_path}: {str(e)}")
            raise

    def _invoke_model(self, prompt: str) -> str:
        
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            "temperature": 0.0 
        }

        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )
            response_body = json.loads(response.get("body").read())
            return response_body["content"][0]["text"]
        except Exception as e:
            logger.error(f"Inference error: {str(e)}")
            raise

    def summarize(self, raw_text: str) -> str:
        
        if not raw_text.strip():
            return "No content found to summarize."

        
        chunks = [raw_text[i:i + self.chunk_size_chars] 
                  for i in range(0, len(raw_text), self.chunk_size_chars)]
        
        logger.info(f"Processing {len(chunks)} document chunks.")
        
        intermediate_summaries = []
        for idx, chunk in enumerate(chunks):
            logger.info(f"Summarizing chunk {idx + 1}")
            prompt = (
                "Summarize the following research paper segment. Focus on experimental "
                "methodology, key results, and technical novelties. "
                "Maintain a professional and academic tone:\n\n" + chunk
            )
            intermediate_summaries.append(self._invoke_model(prompt))

        if len(intermediate_summaries) == 1:
            return intermediate_summaries[0]

        
        logger.info("Consolidating intermediate summaries into final report.")
        reduction_prompt = (
            "Synthesize the following section summaries into a single, cohesive "
            "executive summary of the research paper. Highlight the primary "
            "contribution and impact of the work:\n\n" + "\n\n".join(intermediate_summaries)
        )
        return self._invoke_model(reduction_prompt)

def main():
    
    summarizer = ResearchPaperSummarizer()
    
    
    pdf_path = "research_paper.pdf"
    
    try:
        text = summarizer.extract_text_from_pdf(pdf_path)
        summary = summarizer.summarize(text)
        
        print("-" * 30)
        print("RESEARCH SUMMARY")
        print("-" * 30)
        print(summary)
        
    except FileNotFoundError:
        logger.error("The specified PDF file was not found.")
    except Exception as e:
        logger.critical(f"System failure: {str(e)}")

if __name__ == "__main__":
    main()