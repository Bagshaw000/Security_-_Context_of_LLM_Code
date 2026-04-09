import os
import logging
from typing import List, Protocol
from abc import ABC, abstractmethod


try:
    from langchain_openai import ChatOpenAI
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.chains.summarize import load_summarize_chain
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_core.documents import Document
except ImportError:
    raise ImportError("Please install langchain-openai, langchain-community, and pypdf.")


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ResearchSummarizer")

class SummarizationStrategy(ABC):
    
    @abstractmethod
    def execute(self, documents: List[Document]) -> str:
        pass

class MapReduceSummarizer(SummarizationStrategy):
    
    def __init__(self, llm: ChatOpenAI):
        self.chain = load_summarize_chain(llm, chain_type="map_reduce")

    def execute(self, documents: List[Document]) -> str:
        try:
            
            result = self.chain.invoke(documents)
            return result.get("output_text", "")
        except Exception as e:
            logger.error(f"Error during Map-Reduce summarization: {e}")
            raise

class DocumentProcessor:
    
    def __init__(self, chunk_size: int = 4000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )

    def load_and_split(self, file_path: str) -> List[Document]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Source file not found: {file_path}")
        
        logger.info(f"Loading document: {file_path}")
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        logger.info(f"Splitting document into chunks (chunk_size={self.splitter._chunk_size})")
        return self.splitter.split_documents(pages)

class ResearchPaperService:
    
    def __init__(self, processor: DocumentProcessor, strategy: SummarizationStrategy):
        self.processor = processor
        self.strategy = strategy

    def summarize_paper(self, file_path: str) -> str:
        
        try:
            chunks = self.processor.load_and_split(file_path)
            if not chunks:
                return "Document is empty or could not be parsed."
            
            summary = self.strategy.execute(chunks)
            return summary
        except Exception as e:
            logger.error(f"Service failure for {file_path}: {e}")
            return f"Summarization failed: {str(e)}"

def main():
    
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview", 
        temperature=0, 
        openai_api_key=api_key
    )
    
    processor = DocumentProcessor(chunk_size=6000, chunk_overlap=500)
    strategy = MapReduceSummarizer(llm)
    service = ResearchPaperService(processor, strategy)

    
    paper_path = "path/to/research_paper.pdf"
    if os.path.exists(paper_path):
        summary = service.summarize_paper(paper_path)
        print("\n--- Research Paper Summary ---\n")
        print(summary)
    else:
        print(f"File {paper_path} not found. Please provide a valid PDF path.")

if __name__ == "__main__":
    main()