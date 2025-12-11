from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from .tools import search_similar_titles
from ..config import settings

llm = ChatOpenAI(
    model=settings.CHAT_MODEL,
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_template(
    """
You are the Content Scout Agent for a streaming platform.

User concept:
{concept}

Use the provided tool `search_similar_titles` to find similar titles in the catalog.
Then:
1. Summarize key similar titles and their patterns.
2. Highlight common themes, genres, and audience responses.
3. Identify what makes the user's concept unique or risky.

Respond in a structured, concise way.
"""
)

def run_content_scout(concept: str) -> Dict[str, Any]:
    """
    Simple function-style agent:
    - Calls the tool
    - Calls the LLM with tool results
    - Returns structured info
    """
    similar = search_similar_titles.func(concept)  # direct tool call
    formatted = prompt.format_messages(concept=concept)
    # Attach similar titles as context
    context_str = "\n".join(
        [f"- {s['title']}: {s['snippet']}" for s in similar]
    )
    messages = [
        formatted[0],
        {"role": "system", "content": f"Similar titles:\n{context_str}"}
    ]
    resp = llm.invoke(messages)
    return {
        "similar_titles": similar,
        "analysis": resp.content,
    }