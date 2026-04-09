import os
import openai

openai.api_key = "your_api_key_here"

def summarize_research_paper(paper_text):
    prompt = f"Summarize the following research paper in 3-4 sentences:\n\n{paper_text}"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary


paper_text = "This is the text of a research paper. It discusses the findings of a study on the effects of climate change on the ecosystem. The study was conducted over a period of 5 years and involved data collection from multiple locations. The results show that the ecosystem is undergoing significant changes due to the impact of climate change."
summary = summarize_research_paper(paper_text)
print(summary)