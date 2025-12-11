from .vectorstore import build_vectorstore

_vectordb = None


def get_vectorstore():
    global _vectordb
    if _vectordb is None:
        _vectordb = build_vectorstore()
    return _vectordb


def retrieve_similar_titles(query: str, k: int = 5):
    vectordb = get_vectorstore()
    docs = vectordb.similarity_search(query, k=k)
    return docs