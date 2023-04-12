# Wellness SmartChat
A Chatbot using AI to ask questions about Wellness

This project is to explore the capabilities of Chat-GPT with sources of Wellness information.
Based on a list of YouTube channels the chat-bot transcribes the content of all the videos and provide it to the AI chatbot, enriching its knowledge. The user can interact with the chat-bot in any human language about Wellness.

## Installation:
- Clone the repository
- Create a config.env file on the root level with the following line of code.
```bash
OPENAI_API_KEY="your-openai-api-key"
```
- Replace "your-openai-api-key" with your OpenAI Api Key
- You can get one OpenAI Api Key at https://platform.openai.com/account/api-keys

## How to Use:
- Run backendmain.py to transcribe the videos
- Run main.py to start the chat-bot with the knowledge created

PS: It is possible to include more channels in channels.txt

## Next Steps:
- Have multiple sources of information (spotify, apple, etc.)
- Save user chat history
- Create a version of the SmartChat for other subjects (Finance, Parenting, Beauty, etc.)


## License:

Distributed under the MIT License. See `LICENSE.txt` for more information.