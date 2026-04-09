import asyncio
from datetime import datetime
import json
import time

import pandas as pd
from src.prompt_combination import PromptCombination
from src.model import LLM
from src.util import ensure_python_prompt, remove_comments_and_docstrings

async def main():
    llm_model = LLM()
    prompt_comb = PromptCombination()
    df = pd.read_csv("dataset/paraphrases_personas_14May.csv")
    gpt_data = dict()
    claude_data = dict()
    gemini_data = dict()
    
    

    # print(df.shape[0])

    # Loop through all rows in the dataframe
    for row in df.itertuples():
        # Carry out both ensure python and non ensure python code
        print(row.Index)
        prompt = prompt_comb.original_task_persona(row.original_phrase, row.persona)
        ensure_py = ensure_python_prompt(str(prompt))
        # print(ensure_py)
        
        
        
        # claude ,gpt,
        gemini =await asyncio.gather(
        # llm_model.claude_response(ensure_py),
        #                                 llm_model.gpt_response(ensure_py), 
                                        llm_model.gemini_response(ensure_py)
                                          )

        

        # claude_data[row.Index] = remove_comments_and_docstrings(claude[0]) 
        
        # gpt_data[row.Index] = remove_comments_and_docstrings(gpt[0])
        print("Response Text")
        print(gemini[0])
        
        gemini_data[row.Index] = remove_comments_and_docstrings(gemini[0])
        
        await asyncio.sleep(5)
       
        
    
    # with open('result/'+"GPT"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
    #     json.dump(gpt_data, file, indent=4)
        
    # with open('result/'+"Claude"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
    #     json.dump(claude_data, file, indent=4)
        
    with open('result/'+"Gemini"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gemini_data, file, indent=4)
    
    
    # Loop through and create file na
    
    
   
   
   
        
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")