from dotenv import load_dotenv
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI

from log import Log
from transcriber import Transcriber
from videos import Videos


class MakeIndex:
    transcriptions_path = './data/transcriptions'
    audios_path = "./data/audios"
    videos_file = "./data/videos.txt"
    index_file = "./data/index.json"

    def __init__(self, model_name='text-ada-001', max_tokens=256, max_input_size=4096,
                 max_chunk_overlap=20, chunk_size_limit=600, temperature=0):
        """
        Object to create the index of information for the ChatBot
        :param model_name: model name
        :param max_tokens: number of output tokens
        :param max_input_size: maximum input size
        :param max_chunk_overlap: maximum chunk overlap
        :param chunk_size_limit: chunk size limit
        :param temperature: temperature
        """
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.max_input_size = max_input_size
        self.max_chunk_overlap = max_chunk_overlap
        self.chunk_size_limit = chunk_size_limit
        self.temperature = temperature

    def construct_index(self):
        """
        Creates the index of information for the ChatBot
        """

        Log.log('Indexing...')

        # Transcribes all videos in the list
        Videos.load_videos(self.videos_file)
        Transcriber.load_transcriptions(self.videos_file, self.audios_path, self.transcriptions_path)

        # define Prompt Helper
        prompt_helper = PromptHelper(
            self.max_input_size, self.max_tokens, self.max_chunk_overlap, chunk_size_limit=self.chunk_size_limit)

        # define LLM
        llm_predictor = LLMPredictor(llm=OpenAI(
            temperature=self.temperature, model_name=self.model_name, max_tokens=self.max_tokens))

        # Loads all transcriptions
        documents = SimpleDirectoryReader(self.transcriptions_path).load_data()

        # Creates the index
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        idx = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        idx.save_to_disk(self.index_file)

        Log.log('Indexed!')


if __name__ == '__main__':
    Log.create_logger("make_index")
    load_dotenv("config.env")
    make_index = MakeIndex()
    make_index.construct_index()
