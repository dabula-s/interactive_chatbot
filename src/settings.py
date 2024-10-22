import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
REDIS_HISTORY_TTL = int(os.getenv("REDIS_HISTORY_TTL", 3600))

HISTORY_TOKENS_LIMIT = int(os.getenv('HISTORY_TOKENS_LIMIT', 200))
CONTEXT_TOKENS_LIMIT = int(os.getenv('CONTEXT_TOKENS_LIMIT', 200))

DEFAULT_TEMPLATE_STRING = '''Role: As an AI assistant you answer user's questions. 
Style: Formal
Tone: Professional, Polite, Friendly
Format: Text

Instructions:
1. If history provided do not say hello.
2. Answer questions based on messages history and provided context.
3. Track previous questions and responses to maintain context. If a
follow-up question is asked, reference prior interactions to provide a relevant answer.

Context:
{context}

Conversation History:
{history}

Question:
{question}

'''