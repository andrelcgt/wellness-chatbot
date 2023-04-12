from gpt_index import PromptHelper, LLMPredictor, ServiceContext
from langchain import OpenAI
from dotenv import load_dotenv

load_dotenv("config.env")

# Path to save audio files
audios_path = './data/audios'
# Path to save log files
log_path = './log'
# Path to save transcription files
transcriptions_path = './data/transcriptions'
# Path to save video list files
videos_list_path = './data/videos_list'

# Path to the channels file
channels_file = './channels.txt'
# Path to the index file
index_file = './data/index.json'

from log import Log

# Interface config
title = "Q&A about Wellness with information from the most Influential People in the field"
description = "Ask any question and the AI SmartChat will answer."
placeholder = "Enter text and press enter"
label = "Wellness SmartChat"

# Starting Prompt
starting_prompt = "Ignore all previous instructions. You are a Wellness Expert, with 20 years helping people improve " \
                  "their health. Your task is to help USER answering their questions. Be very helpful and motivating. "\
                  "Do not respond now, this is only your configuration. Respond to the next questions. "

# AI Config

# AI Parameters
model_name_back_end = 'text-ada-001'
model_name_front_end = 'text-davinci-003'
temperature = 0.7
top_p = 1
max_input_size = 4096
max_tokens = 256
max_chunk_overlap = 20
chunk_size_limit = 600
model_size = "tiny"

# define Prompt Helper
prompt_helper = PromptHelper(max_input_size, max_tokens, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

# define LLM - Back-end
llm_back_end = OpenAI(model_name=model_name_back_end, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
llm_predictor_back_end = LLMPredictor(llm=llm_back_end)

# define service context - Back-end
service_context_back_end = ServiceContext.from_defaults(llm_predictor=llm_predictor_back_end,
                                                        prompt_helper=prompt_helper)

# define LLM - Front-end
llm_front_end = OpenAI(model_name=model_name_front_end, temperature=temperature, max_tokens=max_tokens, top_p=top_p)
llm_predictor_front_end = LLMPredictor(llm=llm_front_end)

# define service context - Front-end
service_context_front_end = ServiceContext.from_defaults(llm_predictor=llm_predictor_front_end,
                                                         prompt_helper=prompt_helper)
