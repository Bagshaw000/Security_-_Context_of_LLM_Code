import json

import pandas as pd
from pathlib import Path
from util import clean_json


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
            
            with open(file_, 'x',encoding='utf-8') as file:
                file.write(col_data.item())
            
    except Exception as e:
        raise e
    
    
def create_json_file(file_path:str,model:str):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
          
        df = pd.DataFrame(data, index=[0])
        
        for col_name, col_data  in df.items():
            clean = clean_json(col_data.item())
            file_name = str(col_name +".json") 
            file_ = str(Path.cwd()/model/file_name)
            
            folder_path = Path(file_)
            folder_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_, 'x',encoding='utf-8') as file:
                file.write(clean)
    except Exception as e:
        raise e


p = Path("result/LlamaRankNew2026-07-01.json").resolve()
create_json_file(p,"LlamaRankNew")
