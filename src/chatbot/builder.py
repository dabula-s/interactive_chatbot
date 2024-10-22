from langchain_core.output_parsers import BaseTransformOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, Runnable
from langchain_openai import ChatOpenAI

from chatbot import config
from settings import OPENAI_API_KEY


def build_llm(llm_config: config.LlmConfig):
    return ChatOpenAI(
        model=llm_config.model,
        temperature=llm_config.temperature,
        api_key=OPENAI_API_KEY,
    )


def build_chain(
    llm,
    prompt: PromptTemplate,
    parser: BaseTransformOutputParser[str] = None,
    limiters: list = None,
) -> Runnable:
    if limiters is None:
        limiters = []

    chain = prompt | llm

    for limiter in limiters:
        chain = limiter | chain

    if parser:
        chain = chain | parser

    return chain


def build_chain_with_history(chain, get_session_history, input_messages_key, history_messages_key):
    # Create a runnable with message history
    chain_with_history = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_session_history,
        input_messages_key=input_messages_key,
        history_messages_key=history_messages_key,
    )
    return chain_with_history
