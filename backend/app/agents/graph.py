from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

from .content_scout import run_content_scout
from .audience_fit import run_audience_fit
from .competitive import run_competitive
from .executive_summary import run_executive_summary


class StreamIntelState(TypedDict, total=False):
    concept: str

    similar_titles: List[Dict[str, Any]]
    scout_analysis: str

    audience_insights: str
    competitive_insights: str

    executive_summary: str


def content_scout_node(state: StreamIntelState) -> StreamIntelState:
    result = run_content_scout(state["concept"])
    return {
        "similar_titles": result["similar_titles"],
        "scout_analysis": result["analysis"],
    }


def audience_fit_node(state: StreamIntelState) -> StreamIntelState:
    result = run_audience_fit(
        concept=state["concept"],
        scout_analysis=state.get("scout_analysis", ""),
    )
    return result  # contains "audience_insights"


def competitive_node(state: StreamIntelState) -> StreamIntelState:
    result = run_competitive(concept=state["concept"])
    return result  # contains "competitive_insights"


def executive_summary_node(state: StreamIntelState) -> StreamIntelState:
    result = run_executive_summary(
        concept=state["concept"],
        scout_analysis=state.get("scout_analysis", ""),
        audience_insights=state.get("audience_insights", ""),
        competitive_insights=state.get("competitive_insights", ""),
    )
    return result  # contains "executive_summary"


def build_streamintel_graph():
    graph = StateGraph(StreamIntelState)

    graph.add_node("content_scout", content_scout_node)
    graph.add_node("audience_fit", audience_fit_node)
    graph.add_node("competitive", competitive_node)
    graph.add_node("executive_summary", executive_summary_node)

    graph.add_edge(START, "content_scout")
    graph.add_edge("content_scout", "audience_fit")
    graph.add_edge("audience_fit", "competitive")
    graph.add_edge("competitive", "executive_summary")
    graph.add_edge("executive_summary", END)

    return graph.compile()