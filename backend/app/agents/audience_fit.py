from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from ..config import settings


def run_audience_fit(concept: str, scout_analysis: str) -> Dict[str, str]:
    """
    Audience Fit Agent:
    Takes the concept + content scout analysis and infers target audience,
    regions, age groups, and possible localization needs.
    """
    llm = ChatOpenAI(model=settings.CHAT_MODEL, temperature=0.3)

    prompt = ChatPromptTemplate.from_template(
        """
You are an Audience Fit Agent for a global streaming platform.

User concept:
{concept}

Content Scout Analysis:
{scout}

Task:
1. Identify likely target regions (continents / example countries).
2. Identify likely age ranges (e.g., 13–17, 18–34, 35+).
3. Identify audience segments (e.g., young adults, families, cinephiles, thriller fans).
4. Point out potential cultural sensitivities or localization needs (if any).
5. Summarize in clear bullet points.

Answer in markdown bullet points.
"""
    )

    msgs = prompt.format_messages(concept=concept, scout=scout_analysis)
    resp = llm.invoke(msgs)

    return {"audience_insights": resp.content}