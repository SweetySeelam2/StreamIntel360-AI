from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from ..agents.graph import build_streamintel_graph, StreamIntelState

router = APIRouter(
    prefix="/chat",   # final path: /api/chat
    tags=["chat"],
)


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[str]] = []


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[dict]


def _extract_chat_answer(result: StreamIntelState) -> str:
    """
    Prefer a proper 'answer' key if the graph provides it.
    Otherwise, fall back to 'executive_summary', which is already
    a nice executive-style summary from the agents.
    """
    ans = result.get("answer")
    if isinstance(ans, str) and ans.strip():
        return ans

    exec_summary = result.get("executive_summary")
    if isinstance(exec_summary, str) and exec_summary.strip():
        return exec_summary

    # Last-resort fallback (short, not the huge raw state)
    return "The graph ran, but did not return a final answer field."


def _normalize_recommendation_text(answer: str) -> str:
    """
    Clean up the slightly clunky 'Recommended: Pilot' phrasing coming
    from the prompt/template so the user sees a single, clear line like:

        Recommendation: Greenlight a pilot; strong fit with target audience.

    We handle a few common newline patterns just to be safe.
    """
    if not isinstance(answer, str) or not answer:
        return answer

    replacement = (
        "Recommendation: Greenlight a pilot; strong fit with target audience."
    )

    # Most likely pattern from the current template
    patterns = [
        "Recommendation:\n\nRecommended: Pilot",
        "Recommendation:\r\n\r\nRecommended: Pilot",
        "Recommendation:\nRecommended: Pilot",
        "Recommendation:\r\nRecommended: Pilot",
    ]

    for pat in patterns:
        if pat in answer:
            return answer.replace(pat, replacement)

    # Fallback: if we only see the bare line, still upgrade it
    if "Recommended: Pilot" in answer:
        return answer.replace("Recommended: Pilot", replacement)

    return answer


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    graph = build_streamintel_graph()

    state: StreamIntelState = {
        "concept": request.message,
        "history": request.history or [],
    }

    result = await graph.ainvoke(state)
    answer = _extract_chat_answer(result)
    answer = _normalize_recommendation_text(answer)

    return ChatResponse(
        session_id=str(result.get("session_id", "")),
        answer=answer,
        sources=result.get("sources", []),
    )