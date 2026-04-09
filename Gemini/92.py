import os
import unittest
from unittest.mock import MagicMock, patch
import PyPDF2
from openai import OpenAI

class ResearchPaperSummarizer:
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def extract_text_from_pdf(self, file_path: str) -> str:
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            text_content = []
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            return "\n".join(text_content)
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")

    def generate_summary(self, text: str, model: str = "gpt-4") -> str:
        
        
        
        
        prompt_text = text[:15000] 

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a highly skilled research assistant. "
                                   "Summarize the following research paper. "
                                   "Include: 1. Objective, 2. Methodology, 3. Key Findings, 4. Conclusion."
                    },
                    {"role": "user", "content": prompt_text}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during LLM inference: {str(e)}"

class TestResearchPaperSummarizer(unittest.TestCase):
    
    
    def setUp(self):
        self.summarizer = ResearchPaperSummarizer(api_key="mock-api-key")

    @patch('openai.resources.chat.completions.Completions.create')
    def test_generate_summary_returns_text(self, mock_openai_create):
        
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Summary of the paper content."))
        ]
        mock_openai_create.return_value = mock_response

        result = self.summarizer.generate_summary("This is a test paper content.")
        
        self.assertEqual(result, "Summary of the paper content.")
        mock_openai_create.assert_called_once()

    def test_extract_text_invalid_path(self):
        with self.assertRaises(FileNotFoundError):
            self.summarizer.extract_text_from_pdf("non_existent_file.pdf")

if __name__ == "__main__":
    
    
    
    
    
    
    
    
    unittest.main()