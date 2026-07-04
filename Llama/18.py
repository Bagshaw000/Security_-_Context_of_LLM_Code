from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from datetime import date

class ResearchPaperSummary:
    def __init__(self, model_name):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def generate_summary(self, paper_text):
        input_ids = self.tokenizer.encode(paper_text, return_tensors='pt')
        outputs = self.model(input_ids)
        summary = torch.argmax(outputs.logits[0])
        summary_text = self.tokenizer.decode(summary[:50], skip_special_tokens=True)
        return summary_text

model_name = "t5-base"
paper_text = "Your research paper text here"

summary_generator = ResearchPaperSummary(model_name)

today = date.today().strftime("%Y-%m-%d")
print(f"Research Paper Summary for {today}:")
print(summary_generator.generate_summary(paper_text))