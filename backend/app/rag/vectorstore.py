import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def _get_paths() -> Tuple[Path, Path]:
    """
    Resolve data and chroma paths from environment, with safe defaults.
    """
    backend_dir = Path(__file__).resolve().parents[2]  # .../StreamIntel360/backend
    default_data_root = backend_dir / ".." / "data"
    default_chroma_dir = default_data_root / "chroma"

    data_root = Path(os.getenv("DATA_ROOT", default_data_root)).resolve()
    chroma_dir = Path(os.getenv("CHROMA_DIR", default_chroma_dir)).resolve()

    return data_root, chroma_dir


def build_vectorstore() -> Chroma:
    """
    Connect to the existing Chroma vector store that was built by ingest.py.

    This does NOT rebuild embeddings – it only loads the persisted index
    from disk using the same embedding model.
    """
    _, chroma_dir = _get_paths()

    embedding_model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    embeddings = OpenAIEmbeddings(model=embedding_model_name)

    vectordb = Chroma(
        collection_name="netflix_catalog",
        embedding_function=embeddings,
        persist_directory=str(chroma_dir),
    )

    return vectordb