from gpt_index import GPTSimpleVectorIndex

from config import *


class IndexBot:
    def __init__(self):
        Log.log('Creating SmartBot...')
        self.index = GPTSimpleVectorIndex.load_from_disk(index_file, service_context=service_context_front_end)
        Log.log('SmartBot created')

    def ask_bot(self, prompt, history=[]):
        """
        Queries the IndexBot with the combined_prompt and returns the response from the IndexBot
        :param prompt: User prompt
        :param history: History of the chat with IndexBot
        :return: Response of IndexBot
        """
        Log.log(f"Question: {prompt}")

        if len(history) == 0:
            self.index.query(starting_prompt)

        response = self.index.query(prompt)

        Log.log(f"Answer: {response.response.strip()}")
        return response.response.strip()
