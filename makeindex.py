import os

from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex

from config import *


class MakeIndex:

    @staticmethod
    def construct_index():
        """
        Creates the index of information for the ChatBot
        """
        MakeIndex._check_paths_existence()

        Log.log('Indexing...')

        # Loads all transcriptions
        documents = SimpleDirectoryReader(transcriptions_path).load_data()

        # Creates the index
        idx = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context_back_end)
        idx.save_to_disk(index_file)

        Log.log('Indexed!')

    @staticmethod
    def _check_paths_existence():
        """
        Check if all paths necessary exists. If any doesn't exist create it
        """
        MakeIndex._check_path_existence(audios_path)
        MakeIndex._check_path_existence(log_path)
        MakeIndex._check_path_existence(transcriptions_path)
        MakeIndex._check_path_existence(videos_list_path)

    @staticmethod
    def _check_path_existence(path):
        """
        Check if a path exists. If it doesn't exist create it
        :param path: path to create if necessary
        """
        if not os.path.exists(path):
            os.makedirs(path)
