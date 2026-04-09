import pandas as pd

class PromptCombination:
    
    def original_phrase(self,original_phrase):
        try:
            return str(original_phrase)
        except Exception as e:
            raise e
    
    def original_task_persona(self, original_phrase, persona):
        try:
            return "\n".join([str(original_phrase), str(persona)])
        except Exception as e:
            raise
        
    def paraphrase(self,df:pd.DataFrame):
        try:
            return str(df.paraphrase)
        except Exception as e:
            raise e
        
    def paraphrase_persona(self, paraphrase, persona):
        try:
            return "\n".join([str(paraphrase), str(persona)])
            
        except Exception as e:
            raise e