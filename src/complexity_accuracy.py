from datetime import datetime
import json
import os
from pathlib import Path

import pandas as pd
from Complexity_metrics import *

def compute_complexity_from_string(code_string):
    """
    Calculate complexity metrics for a single code string
    
    Args:
        code_string (str): The source code as a string
        model: Optional model parameter (kept for compatibility)
        index: Optional index parameter (kept for compatibility)
    
    Returns:
        dict: Dictionary containing all complexity metrics
    """
    try:
        # Analyze code complexity
        cc_result, halstead_result, mi_results = analyze_code_complexity(code_string)
        complexity = cc_result[0].complexity
        vocabulary = halstead_result.total.vocabulary
        length = halstead_result.total.length
        difficulty = halstead_result.total.difficulty
        effort = halstead_result.total.effort
        time = halstead_result.total.time
        mi = mi_results
    except:
        complexity = 0
        vocabulary = 0
        length = 0
        difficulty = 0
        effort = 0
        time = 0
        mi = 0
    
    # Count keywords
    keyword_counts = count_keywords(code_string)
    
    # Extract individual keyword counts
    keyword_metrics = {
        'false': keyword_counts.get('False', 0),
        'none': keyword_counts.get('None', 0),
        'true': keyword_counts.get('True', 0),
        'and': keyword_counts.get('and', 0),
        'as': keyword_counts.get('as', 0),
        'assert': keyword_counts.get('assert', 0),
        'async': keyword_counts.get('async', 0),
        'await': keyword_counts.get('await', 0),
        'break': keyword_counts.get('break', 0),
        'class': keyword_counts.get('class', 0),
        'continue': keyword_counts.get('continue', 0),
        'def': keyword_counts.get('def', 0),
        'del': keyword_counts.get('del', 0),
        'elif': keyword_counts.get('elif', 0),
        'else': keyword_counts.get('else', 0),
        'except': keyword_counts.get('except', 0),
        'finally': keyword_counts.get('finally', 0),
        'for': keyword_counts.get('for', 0),
        'from': keyword_counts.get('from', 0),
        'global': keyword_counts.get('global', 0),
        'if': keyword_counts.get('if', 0),
        'import': keyword_counts.get('import', 0),
        'in': keyword_counts.get('in', 0),
        'is': keyword_counts.get('is', 0),
        'lambda': keyword_counts.get('lambda', 0),
        'nonlocal': keyword_counts.get('nonlocal', 0),
        'not': keyword_counts.get('not', 0),
        'or': keyword_counts.get('or', 0),
        'pass': keyword_counts.get('pass', 0),
        'print': keyword_counts.get('print', 0),
        'raise': keyword_counts.get('raise', 0),
        'return': keyword_counts.get('return', 0),
        'try': keyword_counts.get('try', 0),
        'while': keyword_counts.get('while', 0),
        'with': keyword_counts.get('with', 0),
        'yield': keyword_counts.get('yield', 0)
    }
    
    # Count lines of code
    try:
        loc = count_lines(code_string)
    except:
        loc = 0
    
    # Count other metrics
    loops = count_loops(code_string)
    comparisons = count_comparisons(code_string)
    
    try:
        variables = count_variables_in_code(code_string)
    except:
        variables = 0
    
    string_literals = count_string_literals(code_string)
    numeric_literals = count_numeric_literals(code_string)
    math_operations = count_math_operations(code_string)
    max_nested_blocks_value = max_nested_blocks(code_string)
    unique_words = count_unique_words_in_code(code_string)
    
    # Create results dictionary
    results = {
        'CC': complexity,
        'vocabulary': vocabulary,
        'length': length,
        'difficulty': difficulty,
        'effort': effort,
        'time': time,
        'mi_index': mi,
        'LOC': loc,
        'loops': loops,
        'comparisons': comparisons,
        'variables': variables,
        'string_literals': string_literals,
        'numeric_literals': numeric_literals,
        'math_operations': math_operations,
        'Maxnested_blocks': max_nested_blocks_value,
        'unique_words': unique_words,
        **keyword_metrics
    }
    
    # Convert to DataFrame for consistency with original
    df = pd.DataFrame([results])
    
    return df, results
# with open('result/'+"LlamaRank"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
#         json.dump(df, file, indent=4)

def complexity(folder_path:str,model:str):
    df = {}
    # Read a file 
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            with open(os.path.join(folder_path, filename), 'r') as f:
                content = f.read()
                file_name = filename.split(".")
                comp = compute_complexity_from_string(content)
                temp_dict ={
                
                    "complexity":comp[1]['mi_index']
                }
                df[file_name[0]]= (temp_dict)
               
    sorted_dict = dict(sorted(df.items()))
    with open('result/'+model+"Comp"+datetime.now().strftime("%Y-%m-%d")+".json", 'w') as file:
        json.dump(sorted_dict, file, indent=4)   


p = Path("GPTNew").resolve()
complexity(p,'GPTNew')