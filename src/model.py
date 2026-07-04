# This file handle all model initialization (gpt-4o mini Claude 3 Haiku, Gemini 2.0 Flash, Llama 3.3)
import asyncio
import requests
from anthropic import Anthropic
from openai import OpenAI
from google import genai
import os
from dotenv import load_dotenv
from google.genai import errors,types

class LLM:
    
    def __init__(self):
        load_dotenv()
        gpt_key = os.getenv("OPENAI_API_KEY")
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini = genai.Client(api_key=gemini_key)
        self.gpt = OpenAI(api_key=gpt_key)
        self.claude = Anthropic(api_key=claude_key, max_retries=3)
        self.temperature= 0.0

    
    async def gpt_response(self, prompt:str):
        try:
            print("Running gpt task")
            response = self.gpt.responses.create(
                model="gpt-4o-mini",
                instructions="You are a coding assistant.",
                temperature=self.temperature,
                input= prompt,
              
            )
            
                
            return response.output[0].content[0].text

        except Exception as e:
            raise e
        
    async def claude_response(self,prompt:str):
        try:
            print("Running Claude task")
            response = self.claude.messages.create(
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="claude-haiku-4-5-20251001",
            )
            
            return response.content[0].text
        except Exception as e:
            raise e
        
    async def gemini_response(self, prompt:str, max_retries:int = 3)->str:
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}")
                
                # Configure generation parameters (increase temperature on each retry)
                config = types.GenerateContentConfig(
                    max_output_tokens=8192,
                    temperature=0.7 + (attempt * 0.3),  # 0.7, 1.0, 1.3
                )
                
                print(f"  Temperature: {config.temperature}")
                
                # Make the API call
                response = self.gemini.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt,
                    config=config,
                )
                
                # Check for RECITATION error
                finish_reason = response.candidates[0].finish_reason if response.candidates else None
                
                if finish_reason == "RECITATION":
                    print(f"  ⚠️ RECITATION detected on attempt {attempt + 1}")
                    
                    if attempt == max_retries - 1:
                        # Last attempt failed
                        return "Response blocked due to recitation after multiple retries"
                    
                    # Wait before retry with exponential backoff
                    wait_time = min(2 ** attempt, 10)  # 1, 2, 4 seconds
                    print(f"  Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    continue  # Try again
                    
                # Success!
                return response.text
                
            except Exception as e:
                print(f"  ❌ Error on attempt {attempt + 1}: {e}")
                
                if attempt == max_retries - 1:
                   
                    raise
                
                # Wait before retry
                wait_time = min(2 ** attempt, 10)
                print(f"  Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                
        print( "Max retries exceeded")
        return None
    
    async def llama_response(self, prompt:str)-> str:
        try:
            # Pass prompt to the llama via POST request
            payload = {
                "model": "llama3.2",
                "messages": [
                    { "role": "user", "content": prompt }
                ],
                "stream": False
            }
            
            response = requests.post("http://localhost:11434/api/chat",json=payload, timeout=400)
            
            if response.status_code != 200:
                return None
            
            json_res = response.json()
        
            return json_res["message"]["content"]
        except Exception as e:
            raise e
        

# test = LLM()
# asyncio.run(test.llama_response("Write python code for a calculator"))