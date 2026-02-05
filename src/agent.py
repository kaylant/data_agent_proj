"""Minimal LangGraph agent skeleton."""

import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END

load_dotenv()


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
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


def build_graph():
    """Build the LangGraph agent."""
    graph = StateGraph(MessagesState)
    
    # Add nodes
    graph.add_node("agent", agent_node)
    
    # Add edges
    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)
    
    return graph.compile()


if __name__ == "__main__":
    # Quick test
    app = build_graph()
    result = app.invoke({"messages": [("user", "What is 2 + 2?")]})
    print(result["messages"][-1].content)