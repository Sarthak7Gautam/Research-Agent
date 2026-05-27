import sys
from pathlib import Path
import warnings

warnings.filterwarnings(action="ignore")

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.utils.model_initialization import LLMInitialization
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_tavily.tavily_search import TavilySearch
from langchain_community.utilities.arxiv import ArxivAPIWrapper

load_dotenv()


@tool
def make_websearch(query: str, max_results: int = 2, search_depth: str = "basic"):
    """This tool makes a web search on the Tavily Search API"""

    tools = TavilySearch(max_results=max_results, search_depth=search_depth)
    results = tools.invoke({"query": f"{query}"})
    urls = []
    contents = []
    for result in results["results"]:
        if result.get("url"):
            urls.append(result.get("url"))

        if result.get("content"):
            contents.append(result.get("content"))

    return urls, contents


model = LLMInitialization().load_groq_llm()

tools = [make_websearch]
tools_with_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
