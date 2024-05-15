from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph
from chains import first_responder, revisor
from tools_executor import execute_tool
from dotenv import load_dotenv
load_dotenv()

MAX_ITER=2

builder = MessageGraph()
builder.add_node(key="draft", action=first_responder)
builder.add_node(key="execute_tool", action=execute_tool)
builder.add_node(key="revise", action=revisor)

builder.add_edge(start_key="draft", end_key="execute_tool")
builder.add_edge(start_key="execute_tool", end_key="revise")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITER:
        return END
    return "execute_tool"

builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point(key="draft")

graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    result = graph.invoke(
        "Write about companies that work on Autonomous driving domain,"
        " list startups that do that and raised capital."
    )
    print(result[-1].tool_calls[0]["args"]["answer"])
    print("*********References*****************")
    print(result[-1].tool_calls[0]["args"]["references"])