def ensure_python_prompt(prompt:str):
    prefix = "Write Python code."
    postfix = "Output only Python code and nothing else. CRITICAL:Do not include any markdown _or_ code block indicators."
    prompt = "\n".join([prefix, prompt, postfix])

    return prompt

import re
def remove_comments_and_docstrings(code: str) -> str:
    # Remove all single-line comments
    code_no_single_line_comments = re.sub(r'#.*', '', code)
    
    # Remove all docstrings (both single and double quotes)
    code_no_docstrings = re.sub(r'""".*?"""', '', code_no_single_line_comments, flags=re.DOTALL)
    code_no_docstrings = re.sub(r"'''.*?'''", '', code_no_docstrings, flags=re.DOTALL)
    
    return code_no_docstrings

def clean_json(code:str)->str:
    code_docstring = re.sub(r'```.*?` ` `',"",code, flags=re.DOTALL)
    code_docstring = re.sub(r"```json","",code, flags=re.DOTALL)
    code_docstring = re.sub(r"json","",code, flags=re.DOTALL)

    return code_docstring


import pandas as pd
def count_persona():
    csv = pd.read_csv("dataset/paraphrases_personas_14May.csv")
    brad_count = 0
    john_count = 0
    harold_count = 0
    
    for row in csv.itertuples():
        
        if "john" in row.persona.lower():
            john_count += 1
        elif "harold" in row.persona.lower():
            harold_count += 1
        elif "brad" in row.persona.lower():
            brad_count += 1
            
    return brad_count, john_count, harold_count
        

def remove_duplicates():
    df = pd.read_csv("dataset/paraphrases_personas_14May.csv")
    df_unique = df.drop_duplicates(subset=["original_phrase","persona"])
    
    print(df_unique.shape[0])
    
    df_unique.to_csv("personas.csv",index=False)
    return df_unique


def get_unique_task():
    df = pd.read_csv("dataset/paraphrases_personas_14May.csv")
    df_unique = df.drop_duplicates(subset=["original_phrase"])
    df_phrase = df_unique["original_phrase"]
    
    
    df_phrase.to_csv("tasks.csv",index=False)
    return df_phrase

get_unique_task()