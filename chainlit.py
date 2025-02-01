import chainlit as cl
from pathlib import Path
from agents import SQLAgent
from utils import setup_logging
from settings import setting

logger = setup_logging(Path("logs/dev.log"))


@cl.on_chat_start
async def start():
    agent = SQLAgent(setting=setting)

    cl.user_session.set("agent", agent)
    await cl.Message(content="Hello! I am a SQL Agent. Ask me anything about the company and user.").send()

@cl.on_message
async def run(message: cl.Message):
    agent = cl.user_session.get("agent")
    msg = cl.Message(content="", author="Assistant")

    res = await cl.make_async(agent.query)(message.content)

    response = ""

    for token in res.response_gen:
        response += token + " "
        await msg.stream_token(token)

    agent.add_message("user", message.content)
    agent.add_message("system", response)
    logger.info(f"User: {message.content} - System: {response}")

    await msg.send()
