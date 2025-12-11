"""
RAG package for StreamIntel360.

This package contains:
- ingest.py      -> one-time / on-demand ingestion of raw CSV data into Chroma
- vectorstore.py -> helper utilities to connect to the vector store
- retriever.py   -> retrieval utilities used by agents

You usually run ingestion with:

    python -m app.rag.ingest
"""

from .ingest import run_ingest

__all__ = ["run_ingest"]