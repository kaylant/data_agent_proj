"""Minimal LangGraph agent with dataset context."""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, MessagesState, START, END

from src.data_loader import load_dataset, get_schema_summary

load_dotenv()

# Load data once at module level
df = load_dataset()
SCHEMA_SUMMARY = get_schema_summary(df)

SYSTEM_PROMPT = f"""You are a data analyst with expertise in natural gas pipeline data.

{SCHEMA_SUMMARY}

Answer questions about this dataset. Be concise and precise.
"""


def get_llm():
    """Get LLM based on available API keys."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return ChatAnthropic(model="claude-sonnet-4-20250514", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model="gpt-4o", temperature=0)
    else:
        raise ValueError("No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY.")


def agent_node(state: MessagesState):
    """The main agent node that calls the LLM."""
    llm = get_llm()
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def build_graph():
    """Build the LangGraph agent."""
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({"messages": [("user", "What columns are in the dataset?")]})
    print("\n" + result["messages"][-1].content)