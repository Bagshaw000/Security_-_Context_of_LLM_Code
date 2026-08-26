# Small collection of prompt-assembly helpers. Each method builds one flavor
# of the final prompt string sent to the LLMs, from the different columns
# available in the dataset CSVs (a bare task phrase, a task+persona pair, a
# paraphrased task, or a paraphrased task+persona pair). Keeping this as one
# class lets main.py swap prompt strategies without changing the LLM-calling
# code in src/model.py.
import pandas as pd

class PromptCombination:

    def original_phrase(self,original_phrase):
        """Return the original (non-paraphrased, no persona) task phrase as-is."""
        try:
            return str(original_phrase)
        except Exception as e:
            raise e

    def original_task_persona(self, original_phrase, persona):
        """Combine an original task phrase with a persona description.

        The two are simply newline-joined so the persona text reads as
        additional context appended after the task instruction; this is the
        combination used by default in main.py's main() and rank_prompt().
        """
        try:
            return "\n".join([str(original_phrase), str(persona)])
        except Exception as e:
            raise

    def paraphrase(self,df:pd.DataFrame):
        """Return the 'paraphrase' column of a single-row DataFrame as a string
        (a paraphrased task phrase with no persona attached).
        """
        try:
            return str(df.paraphrase)
        except Exception as e:
            raise e

    def paraphrase_persona(self, paraphrase, persona):
        """Combine a paraphrased task phrase with a persona description,
        newline-joined the same way as original_task_persona().
        """
        try:
            return "\n".join([str(paraphrase), str(persona)])

        except Exception as e:
            raise e