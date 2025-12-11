from typing import List, Dict, Any
from langchain_core.tools import tool
from ..rag.retriever import retrieve_similar_titles

@tool
def search_similar_titles(query: str) -> List[Dict[str, Any]]:
    """
    Search for titles that are semantically similar to the given query.
    Returns a list of dicts with 'title', 'doc_id', and 'snippet'.
    """
    docs = retrieve_similar_titles(query, k=8)
    results = []
    for d in docs:
        results.append({
            "title": d.metadata.get("title", "Unknown"),
            "doc_id": d.metadata.get("doc_id", ""),
            "snippet": d.page_content[:400],
        })
    return results