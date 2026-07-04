import asyncio
from datetime import datetime
import json
import time

import pandas as pd
from src.prompt_combination import PromptCombination
from src.model import LLM
from src.util import ensure_python_prompt, remove_comments_and_docstrings, remove_duplicates
prompt_comb = PromptCombination()
async def main():
    llm_model = LLM()
    df = pd.read_csv("dataset/personas.csv")
    gpt_data = dict()
    claude_data = dict()
    gemini_data = dict()
    llama_data = dict()
    
    

  

    # Loop through all rows in the dataframe
    for row in df.itertuples():
        # Carry out both ensure python and non ensure python code
        prompt = prompt_comb.original_task_persona(row.original_phrase, row.persona)
        ensure_py = ensure_python_prompt(str(prompt))

        claude,gpt, gemini,llama =await asyncio.gather(
        llm_model.claude_response(ensure_py),
                                        llm_model.gpt_response(ensure_py), 
                                        llm_model.gemini_response(ensure_py), 
                                        llm_model.llama_response(ensure_py)
                                          )

        

        claude_data[row.Index] = remove_comments_and_docstrings(claude[0]) 
        
        gpt_data[row.Index] = remove_comments_and_docstrings(gpt[0])
        
        gemini_data[row.Index] = remove_comments_and_docstrings(gemini[0])
        llama_data[row.Index] = remove_comments_and_docstrings(llama[0])
        
        await asyncio.sleep(5)
    
    
        
    
    with open('result/'+"GPT"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gpt_data, file, indent=4)
        
    with open('result/'+"Claude"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(claude_data, file, indent=4)
        
    with open('result/'+"Gemini"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gemini_data, file, indent=4)
    
    with open('result/'+"Llama"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(llama_data, file, indent=4)
    
    
    # Loop through and create file na
    
async def rank_prompt():
       
    llm_model = LLM()
    df = pd.read_csv("dataset/llama_secure_prompt.csv")
    gpt_data = dict()
    claude_data = dict()
    gemini_data = dict()
    llama_data = dict()

    
    for row in df.itertuples():
        
        prompt_ = "Rank these coding task in terms of complexity. The scale being Easy, Medium and Hard. Also, attached the rational behind the rank choice for the individual task. Do not write the code implementation.Ensure response is short and concise and in json format with atribute task and complexity. "+f"For persona {row.persona} " +"The coding task is in the new line."
        print(row)
        prompt = prompt_comb.original_task_persona(prompt_,row.optimized_phrase)
        print(prompt)
     
      
        claude,gpt,gemini,llama =await asyncio.gather(
            llm_model.claude_response(prompt),
                                            llm_model.gpt_response(prompt), 
                                            llm_model.gemini_response(prompt), 
                                            llm_model.llama_response(prompt)
                                              )



        claude_data[row.Index] = (claude[0]) 
        gpt_data[row.Index] = (gpt[0])
        gemini_data[row.Index]= (gemini[0])
        llama_data[row.Index]= (llama[0])   


    with open('result/'+"GPTRankNew"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gpt_data, file, indent=4)
            
    with open('result/'+"ClaudeRankNew"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(claude_data, file, indent=4)
            
    with open('result/'+"GeminiRankNew"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gemini_data, file, indent=4)

    with open('result/'+"LlamaRankNew"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(llama_data, file, indent=4)


async def optimize_prompts():
    llm_model = LLM()
    df = pd.read_csv("dataset/personas.csv")
    gpt_data = list()
    claude_data = list()
    gemini_data = list()
    llama_data = list()
    
    
    for row in df.itertuples():
        prompt = f"Rewrite this prompt '{row.original_phrase}' for this assumed persona, {row.persona}. This prompt should ensure secure code generation and limit vulenerabilities. Provide only the improved prompt in string format."

        claude,gpt, gemini,llama =await asyncio.gather(
        llm_model.claude_response(prompt),
                                        llm_model.gpt_response(prompt), 
                                        llm_model.gemini_response(prompt), 
                                        llm_model.llama_response(prompt)
        
                                          )
        gpt_ = {
            'persona':row.persona,
            'optimized_phrase': gpt[0],
            'original_phrase':row.original_phrase
        }
        
        gemini_ ={
            'persona':row.persona,
            'optimized_phrase': gemini[0],
            'original_phrase':row.original_phrase
        }
        
        claude_ ={
            'persona':row.persona,
            'optimized_phrase': claude[0],
            'original_phrase':row.original_phrase
        }
        
        llama_ = {
            'persona':row.persona,
            'optimized_phrase': llama[0],
            'original_phrase':row.original_phrase
        }
        
        
        gpt_data.append(gpt_)
        
        gemini_data.append(gemini_)
        claude_data.append(claude_)
        llama_data.append(llama_)
         
        
    gpt_df = pd.DataFrame(gpt_data)
    gemini_df = pd.DataFrame(gemini_data)
    claude_df = pd.DataFrame(claude_data)
    llama_df = pd.DataFrame(llama_data)
    
    gpt_df.to_csv('gpt_secure_prompt.csv')
    gemini_df.to_csv('gemini_secure_prompt.csv') 
    claude_df.to_csv('claude_secure_prompt.csv') 
    llama_df.to_csv('llama_secure_prompt.csv') 
        
async def claude_optimized_code():
    llm_model = LLM()
 
    df = pd.read_csv("dataset/claude_secure_prompt.csv")
  
    claude_data = dict()
    vulnerable_task = [6,8,9,10,21,23,31,32,46,47,49,50,53,61,62]
    
    


    # Loop through all rows in the dataframe
    for index, row in enumerate( df.itertuples()):
        # Carry out both ensure python and non ensure python code
        if index in vulnerable_task:
            prompt = prompt_comb.original_task_persona(row.optimized_phrase, row.persona)
            ensure_py = ensure_python_prompt(str(prompt))

            claude =await asyncio.gather(
            llm_model.claude_response(ensure_py)
                                        
                                            )

        

            claude_data[index] = remove_comments_and_docstrings(claude[0]) 
        
      
        
        await asyncio.sleep(5)
    with open('result/'+"Claude_Optimized"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(claude_data, file, indent=4)
    
async def gpt_optimized_code():
    llm_model = LLM()

    df = pd.read_csv("dataset/gpt_secure_prompt.csv")
  
    gpt_data = dict()
    vulnerable_task = [1,6,7,8,9,10,11,15,16,17,18,19,20,27,29,30,31,32,36,38,42,43,44,48,49,50,57,60,61,62]
    
    

    # Loop through all rows in the dataframe
    for index, row in enumerate( df.itertuples()):
        # Carry out both ensure python and non ensure python code
        if index in vulnerable_task:
            prompt = prompt_comb.original_task_persona(row.optimized_phrase, row.persona)
            ensure_py = ensure_python_prompt(str(prompt))

            gpt =await asyncio.gather(
            llm_model.gpt_response(ensure_py)
                                        
                                            )

        

            gpt_data[index] = remove_comments_and_docstrings(gpt[0]) 
        
      
        
        await asyncio.sleep(5)
    with open('result/'+"GPT_Optimized"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gpt_data, file, indent=4)   
        
async def gemini_optimized_code():
    llm_model = LLM()
  
    df = pd.read_csv("dataset/gemini_secure_prompt.csv")
  
    gemini_data = dict()
    vulnerable_task = [0,2,3,5,7,8,10,12,15,17,24,25,28,29,30,31,32,38,39,40,42,43,44,45,46,49,52,54,59,60,61,62]
    
    # Loop through all rows in the dataframe
    for index, row in enumerate( df.itertuples()):
        # Carry out both ensure python and non ensure python code
        if index in vulnerable_task:
            prompt = prompt_comb.original_task_persona(row.optimized_phrase, row.persona)
            ensure_py = ensure_python_prompt(str(prompt))

            gemini =await asyncio.gather(
            llm_model.gemini_response(ensure_py))

        

            gemini_data[index] = remove_comments_and_docstrings(gemini[0]) 
        
      
        
        await asyncio.sleep(5)
    with open('result/'+"Gemini_Optimized"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(gemini_data, file, indent=4)  
        
async def llama_optimized_code():
    llm_model = LLM()
    # prompt_comb = PromptCombination()
    df = pd.read_csv("dataset/llama_secure_prompt.csv")
  
    llama_data = dict()
    vulnerable_task = [0,3,4,5,10,11,15,17,19,21,23,24,25,26,30,31,32,33,34,38,41,42,43,46,47,48,49,50,53,55,57,61]
    
  
    # Loop through all rows in the dataframe
    for index, row in enumerate( df.itertuples()):
        # Carry out both ensure python and non ensure python code
        if index in vulnerable_task:
            prompt = prompt_comb.original_task_persona(row.optimized_phrase, row.persona)
            ensure_py = ensure_python_prompt(str(prompt))

            llama =await asyncio.gather(
            llm_model.gemini_response(ensure_py))

        

            llama_data[index] = remove_comments_and_docstrings(llama[0]) 
        
      
        
        await asyncio.sleep(5)
    with open('result/'+"Llama_Optimized"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(llama_data, file, indent=4)  
        
                  
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(rank_prompt())
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")