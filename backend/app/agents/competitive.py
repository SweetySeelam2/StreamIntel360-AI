from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings
from .tools import search_similar_titles


def run_competitive(concept: str) -> Dict[str, str]:
    """
    Competitive Intelligence Agent:
    Uses semantic search to find similar titles and reasons about
    how saturated or open the market space is.
    """
    llm = ChatOpenAI(model=settings.CHAT_MODEL, temperature=0.35)

    # Step 1: use RAG tool to find similar titles
    similar: List[Dict[str, Any]] = search_similar_titles.func(concept)

    similar_str = "\n".join(
        [f"- {s['title']}: {s['snippet'][:300]}..." for s in similar]
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are a Competitive Intelligence Agent for a streaming platform.

New concept:
{concept}

Here are some similar titles already in the catalog:
{similar}

Task:
1. Assess how crowded/saturated this space is (high / medium / low).
2. Identify what patterns you see among the similar titles (themes, tones, regions).
3. Suggest angles for differentiation (how this new concept could stand out).
4. Flag any obvious strategic risks (e.g., "market fatigue for this genre").

Respond in markdown with headings:
## Saturation
## Patterns
## Differentiation
## Strategic Risks
"""
    )

    msgs = prompt.format_messages(concept=concept, similar=similar_str)
    resp = llm.invoke(msgs)

    return {"competitive_insights": resp.content}