from typing import Annotated,TypedDict
import operator
from langchain.messages import AnyMessage


class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int = 0
