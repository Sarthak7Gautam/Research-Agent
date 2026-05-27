from langchain.messages import HumanMessage
from core.Agent_Build_Compile.build_and_compile import AgentBuilder

def main(content: str):
    agent = AgentBuilder().build_agent()
    messages = [HumanMessage(content=f"{content}")]
    answer = agent.invoke({"messages": messages})
    return answer


if __name__ == "__main__":
    messages = main(content="Whats the best tourist destinations in Japan?")
    for m in messages["messages"]:
        print(m)
