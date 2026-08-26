# This file handle all model initialization (gpt-4o mini Claude 3 Haiku, Gemini 2.0 Flash, Llama 3.3)
#
# LLM is a thin async wrapper around four different code-generation backends so the
# rest of the pipeline (main.py) can fire the same prompt at all of them concurrently
# via asyncio.gather() and get back plain strings. Three backends (GPT, Claude, Gemini)
# are hosted APIs and need API keys in a local .env file; the fourth (Llama) is expected
# to be served locally by Ollama (see README for setup).
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
        # Load API keys from a .env file in the project root (see .env.example / README).
        # Keys are read once at construction time and used to build one client per provider.
        load_dotenv()
        gpt_key = os.getenv("OPENAI_API_KEY")
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        self.gemini = genai.Client(api_key=gemini_key)
        self.gpt = OpenAI(api_key=gpt_key)
        # max_retries=3: let the Anthropic SDK retry transient/network errors automatically.
        self.claude = Anthropic(api_key=claude_key, max_retries=3)
        # Temperature is pinned to 0 (deterministic-as-possible) so that comparisons
        # across models/personas aren't confounded by sampling randomness.
        self.temperature= 0.0


    async def gpt_response(self, prompt:str):
        """Send `prompt` to OpenAI's gpt-4o-mini and return the generated text.

        Uses the "responses" API with a fixed system instruction that frames the
        model as a coding assistant. Any SDK/network error is re-raised so the
        caller (main.py, via asyncio.gather) can see the failure rather than
        silently getting an empty result.
        """
        try:
            print("Running gpt task")
            response = self.gpt.responses.create(
                model="gpt-4o-mini",
                instructions="You are a coding assistant.",
                temperature=self.temperature,
                input= prompt,

            )

            # responses.create() returns a list of output items; for a simple text
            # completion the first item's first content block holds the answer.
            return response.output[0].content[0].text

        except Exception as e:
            raise e

    async def claude_response(self,prompt:str):
        """Send `prompt` to Anthropic's claude-haiku-4-5 and return the generated text.

        A single user-role message is sent with no system prompt, so any framing
        (e.g. "write secure code") must already be baked into `prompt` by the caller.
        """
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
        """Send `prompt` to Gemini and return the generated text, with retries.

        Gemini can refuse a generation with a "RECITATION" finish reason (it thinks
        the output is reproducing training data verbatim). Unlike a hard error, this
        is treated as a retryable condition: each retry raises both temperature
        (0.7 -> 1.0 -> 1.3) to nudge the model away from the exact phrasing that
        triggered the block, and waits with exponential backoff (1s, 2s, 4s, capped
        at 10s) before trying again. If all attempts still hit RECITATION, a
        placeholder string is returned instead of raising, so a single flaky prompt
        doesn't crash the whole batch run in main.py.
        """
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
                # Any other error (network, quota, malformed response, etc.) is retried
                # the same way, but re-raised once retries are exhausted.
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
        """Send `prompt` to a locally-served Llama 3.2 model via Ollama's HTTP API.

        Requires `ollama serve` (or the Ollama app) to be running on localhost:11434
        with the `llama3.2` model pulled beforehand (`ollama pull llama3.2`). This is
        the only backend that isn't a paid hosted API. stream=False means Ollama
        waits for the full generation and returns it as one JSON payload rather than
        a chunked stream, which keeps this in line with the other three methods that
        also return a single complete string.
        """
        try:
            # Pass prompt to the llama via POST request
            payload = {
                "model": "llama3.2",
                "messages": [
                    { "role": "user", "content": prompt }
                ],
                "stream": False
            }

            # 400s timeout: local generation on CPU/consumer GPU can be slow, so this
            # is intentionally much larger than a typical HTTP timeout.
            response = requests.post("http://localhost:11434/api/chat",json=payload, timeout=400)

            if response.status_code != 200:
                return None

            json_res = response.json()

            return json_res["message"]["content"]
        except Exception as e:
            raise e


# Manual smoke test, left commented out: uncomment to sanity-check the Llama
# backend in isolation (requires Ollama running locally) without running the
# whole main.py pipeline.
# test = LLM()
# asyncio.run(test.llama_response("Write python code for a calculator"))