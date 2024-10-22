from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, computed_field

from settings import DEFAULT_TEMPLATE_STRING, HISTORY_TOKENS_LIMIT, CONTEXT_TOKENS_LIMIT


class PromptConfig(BaseModel):
    input_key: str = 'question'
    history_key: str = 'history'
    context_key: str = 'context'
    template_string: str = DEFAULT_TEMPLATE_STRING

    @computed_field
    @property
    def prompt(self) -> PromptTemplate:
        return PromptTemplate(
            input_variables=[self.input_key, self.history_key, self.context_key],
            template=self.template_string,
        )

class LlmConfig(BaseModel):
    model: str = 'gpt-3.5-turbo'
    temperature: float = 0.3

class ChainConfig(BaseModel):
    limit_history: bool = True
    history_max_tokens: int = HISTORY_TOKENS_LIMIT
    limit_context: bool = True
    context_max_tokens: int = CONTEXT_TOKENS_LIMIT
