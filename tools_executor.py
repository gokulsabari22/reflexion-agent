from typing import List
import json
from collections import defaultdict
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from chains import parser
from langgraph.prebuilt import ToolInvocation, ToolExecutor
from dotenv import load_dotenv
load_dotenv()

search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
tool_executor = ToolExecutor([tavily_tool])

def execute_tool(state: List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_call = parser.invoke(tool_invocation)

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_call:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(ToolInvocation(
                tool="tavily_search_results_json",
                tool_input=query
            ))
            ids.append(parsed_call["id"])

    outputs = tool_executor.batch(tool_invocations)

    outputs_map = defaultdict(dict)
    for id_, output, invocation in zip(ids, outputs, tool_invocations):
        outputs_map[id_][invocation.tool_input] = output

    # Convert the mapped outputs to ToolMessage objects
    tool_messages = []
    for id_, mapped_output in outputs_map.items():
        tool_messages.append(
            ToolMessage(content=json.dumps(mapped_output), tool_call_id=id_)
        )

    return tool_messages


if __name__ == "__main__":
    print("Hello Executor")