import json

import pandas as pd
from pathlib import Path


def create_python_file(file_path:str,model:str):
    try:
       
        with open(file_path, 'r') as f:
            data = json.load(f)
          
        df = pd.DataFrame(data, index=[0])
        
        for col_name, col_data  in df.items():
            
            file_name = str(col_name +".py") 
            file_ = str(Path.cwd()/model/file_name)
            
            folder_path = Path(file_)
            folder_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_, 'x') as file:
                file.write(col_data.item())
            
    except Exception as e:
        raise e


p = Path("result/Gemini2026-04-10.json").resolve()
create_python_file(p,"Gemini")
# C:/Users/DELL 5520/Documents/GitHub/Security_&_Context_of_LLM_Code