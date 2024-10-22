from operator import itemgetter

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import trim_messages
from langchain_core.runnables import RunnablePassthrough

from settings import (
    HISTORY_TOKENS_LIMIT,
    CONTEXT_TOKENS_LIMIT,
)


def get_history_trimmer(llm: BaseChatModel, history_key, max_tokens: int = HISTORY_TOKENS_LIMIT):
    history_limiter = trim_messages(
        max_tokens=max_tokens,
        strategy="last",
        token_counter=llm,
        include_system=False,
        allow_partial=True,
        start_on='human',
    )
    history_trimmer = RunnablePassthrough.assign(
        **{history_key: itemgetter(history_key) | history_limiter}
    )
    return history_trimmer


def get_context_trimmer(llm: BaseChatModel, context_key, max_tokens: int = CONTEXT_TOKENS_LIMIT):
    context_limiter = trim_messages(
        max_tokens=max_tokens,
        strategy="first",
        token_counter=llm,
        include_system=False,
    )
    context_trimmer = RunnablePassthrough.assign(
        **{context_key: itemgetter(context_key) | context_limiter}
    )
    return context_trimmer
