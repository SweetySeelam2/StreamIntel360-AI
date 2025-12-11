from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings


def run_executive_summary(
    concept: str,
    scout_analysis: str,
    audience_insights: str,
    competitive_insights: str,
) -> Dict[str, str]:
    """
    Executive Summary Agent:
    Combines analyses into a concise Go/No-Go style summary.
    """
    llm = ChatOpenAI(model=settings.CHAT_MODEL, temperature=0.25)

    prompt = ChatPromptTemplate.from_template(
        """
You are an Executive Summary Agent supporting senior leadership at a global streaming company.

Concept:
{concept}

Content Scout Analysis:
{scout}

Audience Insights:
{audience}

Competitive Insights:
{competitive}

Write a structured executive summary with sections:
1. One-paragraph Overview (2–4 sentences)
2. 3–5 bullet "Why this could work"
3. 3–5 bullet "Key risks"
4. A short recommendation line at the end: "Recommended: Go", or "Recommended: Pilot", or "Recommended: No-Go".

Be concise but specific.
"""
    )

    msgs = prompt.format_messages(
        concept=concept,
        scout=scout_analysis,
        audience=audience_insights,
        competitive=competitive_insights,
    )

    resp = llm.invoke(msgs)
    return {"executive_summary": resp.content}