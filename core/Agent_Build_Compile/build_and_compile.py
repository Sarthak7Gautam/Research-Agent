from langgraph.graph import StateGraph, START, END
from core.state import MessageState
from core.Nodes.model_node import llm_calls
from core.Nodes.tool_node import tool_node
from core.Nodes.should_continue import should_continue

class AgentBuilder:
    def build_agent(self):

        agent_builder = StateGraph(MessageState)

        agent_builder.add_node("llm_calls", llm_calls)
        agent_builder.add_node("tool_node", tool_node)

        agent_builder.add_edge(START, "llm_calls")
        agent_builder.add_conditional_edges("llm_calls", should_continue, ["tool_node", END])

        agent_builder.add_edge("tool_node", "llm_calls")

        agent = agent_builder.compile()

        return agent
