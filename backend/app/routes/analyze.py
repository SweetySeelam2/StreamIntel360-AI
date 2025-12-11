from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from ..agents.graph import build_streamintel_graph, StreamIntelState

router = APIRouter(
    prefix="/analyze_title",   # final path: /api/analyze_title
    tags=["analyze"],
)


class TitleAnalysisRequest(BaseModel):
    title_name: str
    description: Optional[str] = None
    target_regions: Optional[List[str]] = None


class TitleAnalysisResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[dict]


def _extract_analysis_answer(result: StreamIntelState) -> str:
    """
    For title analysis we again prefer a dedicated 'analysis' key if it
    ever exists, otherwise we use 'executive_summary'.
    """
    analysis = result.get("analysis")
    if isinstance(analysis, str) and analysis.strip():
        return analysis

    exec_summary = result.get("executive_summary")
    if isinstance(exec_summary, str) and exec_summary.strip():
        return exec_summary

    return "The graph ran, but did not return a final analysis field."


def _normalize_recommendation_text(answer: str) -> str:
    """
    Clean up the 'Recommended: Pilot' phrasing so we surface a single,
    polished recommendation line to the frontend.
    """
    if not isinstance(answer, str) or not answer:
        return answer

    replacement = (
        "Recommendation: Greenlight a pilot; strong fit with target audience."
    )

    patterns = [
        "Recommendation:\n\nRecommended: Pilot",
        "Recommendation:\r\n\r\nRecommended: Pilot",
        "Recommendation:\nRecommended: Pilot",
        "Recommendation:\r\nRecommended: Pilot",
    ]

    for pat in patterns:
        if pat in answer:
            return answer.replace(pat, replacement)

    if "Recommended: Pilot" in answer:
        return answer.replace("Recommended: Pilot", replacement)

    return answer


@router.post("", response_model=TitleAnalysisResponse)
async def analyze_title(request: TitleAnalysisRequest):
    graph = build_streamintel_graph()

    prompt = f"Title: {request.title_name}\n\n"
    if request.description:
        prompt += f"Description: {request.description}\n\n"
    if request.target_regions:
        prompt += f"Target regions: {', '.join(request.target_regions)}\n\n"

    state: StreamIntelState = {
        "concept": prompt,
        "history": [],
    }

    result = await graph.ainvoke(state)
    answer = _extract_analysis_answer(result)
    answer = _normalize_recommendation_text(answer)

    return TitleAnalysisResponse(
        session_id=str(result.get("session_id", "")),
        answer=answer,
        sources=result.get("sources", []),
    )