"""LangGraph agent with pandas tool."""

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode
from src.data_loader import get_schema_summary, load_dataset
from src.tools import execute_pandas_code, set_dataframe

load_dotenv()

# Load data and configure tools
df = load_dataset()
set_dataframe(df)
SCHEMA_SUMMARY = get_schema_summary(df)

SYSTEM_PROMPT = f"""You are a data analyst for natural gas pipeline data.

{SCHEMA_SUMMARY}

Use the execute_pandas_code tool to answer questions. Always assign your result to 'result'.
Be precise with numbers. Show your methodology.
"""

TOOLS = [execute_pandas_code]


def get_llm():
    """Get LLM with tools bound."""
    if os.getenv("ANTHROPIC_API_KEY"):
        llm = ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
    else:
        raise ValueError("No API key found.")

    return llm.bind_tools(TOOLS)


def agent_node(state: MessagesState):
    """Call the LLM."""
    llm = get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: MessagesState) -> str:
    """Check if we should continue to tools or end."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END


def build_graph():
    """Build the agent graph."""
    graph = StateGraph(MessagesState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({"messages": [("user", "How many unique pipelines are in the dataset?")]})
    print("\n" + result["messages"][-1].content)
