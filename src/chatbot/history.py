from langchain_core.chat_history import BaseChatMessageHistory
from langchain_redis import RedisChatMessageHistory

from settings import REDIS_URL, REDIS_HISTORY_TTL

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL, ttl=REDIS_HISTORY_TTL)