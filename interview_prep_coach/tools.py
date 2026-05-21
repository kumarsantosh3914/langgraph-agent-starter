from langchain_core.tools import Tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun

serper = GoogleSerperAPIWrapper()
tool_search = Tool(
    name="search",
    func=serper.run,
    description="Search the web for information about a company, role, or interviews topics",
)

wikipedia = WikipediaAPIWrapper()
tool_wiki = WikipediaQueryRun(api_wrapper=wikipedia)

tools = [tool_search, tool_wiki]