from core.utils.prompts import context_prompt
from core.tool_definition.tool_init_and_bind import model_with_tools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from custom_logging.custom_logging import CustomLogging

log = CustomLogging().custom_logger()


def llm_calls(state: dict):
    """LLM decides whether to call a tool or not"""

    log.info("Inside the llm_calls()")
    return {
        "messages": [model_with_tools.invoke([context_prompt] + state["messages"])],
        "llm_calls": state.get("llm_calls", 0) + 1,
    }
