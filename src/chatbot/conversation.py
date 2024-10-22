from langchain_core.runnables import Runnable, RunnableConfig


class Conversation:
    def __init__(self, session_id: str, chain: Runnable):
        self.session_id = session_id
        self.chain = chain

    def generate_stream(self, input_: dict):
        return self.chain.stream(
            input=input_,
            config=RunnableConfig(configurable={'session_id': self.session_id}),
        )
