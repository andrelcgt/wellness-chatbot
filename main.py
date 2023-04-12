import gradio as gr
from indexbot import IndexBot
from config import *

Log.create_logger("main")

index_bot = IndexBot()


def predict(query, bot_state):
    """
    Queries index_bot with query and bot_state
    :param query: User prompt
    :param bot_state: State of the bot, history
    :return: Response of the index_bot
    """
    response = index_bot.ask_bot(query, bot_state)
    bot_state = bot_state + [(query, response)]
    return bot_state, bot_state


if __name__ == '__main__':

    with gr.Blocks(title=label) as app:
        markdown_text = "# {}\n{}".format(title, description)
        gr.Markdown(markdown_text)
        chatbot = gr.Chatbot(elem_id="chatbot", label=label)
        state = gr.State([])

        with gr.Column():
            txt = gr.Textbox(show_label=False, placeholder=placeholder, value="").style(container=False)
        txt.submit(predict, [txt, state], [chatbot, state])

    app.launch(server_name="0.0.0.0", share=False, inbrowser=True)
