import os
from pathlib import Path
from typing import List

import pandas as pd
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv  # <-- make sure this import exists

load_dotenv() 

def _get_paths():
    """
    Resolve data and chroma paths from environment, with safe defaults.
    This does NOT depend on app.config, so you can run it standalone.
    """
    backend_dir = Path(__file__).resolve().parents[2]  # .../StreamIntel360/backend
    default_data_root = backend_dir / ".." / "data"
    default_chroma_dir = default_data_root / "chroma"

    data_root = Path(os.getenv("DATA_ROOT", default_data_root)).resolve()
    chroma_dir = Path(os.getenv("CHROMA_DIR", default_chroma_dir)).resolve()

    raw_dir = data_root / "raw"

    print("=== Ingest configuration ===")
    print(f"Backend dir : {backend_dir}")
    print(f"DATA_ROOT   : {data_root}")
    print(f"RAW dir     : {raw_dir}")
    print(f"CHROMA_DIR  : {chroma_dir}")
    print("============================")

    return raw_dir, chroma_dir


def _load_netflix_titles(raw_dir: Path) -> List[Document]:
    """
    Load netflix_titles.csv from data/raw and turn each row into a Document.
    """
    csv_path = raw_dir / "netflix_titles.csv"
    if not csv_path.exists():
        print(f"[ERROR] netflix_titles.csv not found at {csv_path}")
        return []

    print(f"[INFO] Loading titles from {csv_path} ...")
    try:
        df = pd.read_csv(csv_path)
    except UnicodeDecodeError:
        print("[WARN] utf-8 decode failed, retrying with 'latin-1' encoding...")
        df = pd.read_csv(csv_path, encoding="latin-1")

    # Fill missing text fields
    for col in ["title", "description", "listed_in", "type", "country"]:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str)

    if "release_year" in df.columns:
        df["release_year"] = df["release_year"].fillna("").astype(str)

    docs: List[Document] = []

    for _, row in df.iterrows():
        parts = [
            f"Title: {row.get('title', '')}",
            f"Type: {row.get('type', '')}",
            f"Genres: {row.get('listed_in', '')}",
            f"Country: {row.get('country', '')}",
            f"Year: {row.get('release_year', '')}",
            f"Description: {row.get('description', '')}",
        ]
        text = " | ".join(p for p in parts if p)

        metadata = {
            "show_id": row.get("show_id", ""),
            "title": row.get("title", ""),
            "type": row.get("type", ""),
            "genres": row.get("listed_in", ""),
            "country": row.get("country", ""),
            "release_year": row.get("release_year", ""),
        }

        docs.append(Document(page_content=text, metadata=metadata))

    print(f"[INFO] Loaded {len(docs)} documents from netflix_titles.csv")
    return docs

def run_ingest():
    """
    Main ingestion pipeline:
    - resolve paths
    - load netflix_titles.csv as Documents
    - embed with OpenAIEmbeddings
    - save to Chroma vector store
    """
    raw_dir, chroma_dir = _get_paths()
    chroma_dir.mkdir(parents=True, exist_ok=True)

    docs = _load_netflix_titles(raw_dir)
    if not docs:
        print("[ERROR] No documents loaded. Aborting ingestion.")
        return

    embedding_model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    print(f"[INFO] Using embedding model: {embedding_model_name}")

    embeddings = OpenAIEmbeddings(model=embedding_model_name)

    print(f"[INFO] Building Chroma index in {chroma_dir} ...")
    vectordb = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="netflix_catalog",
        persist_directory=str(chroma_dir),
    )

    vectordb.persist()

    print("[INFO] Ingestion complete.")
    print(f"[INFO] Stored approximately {len(docs)} embeddings in Chroma at {chroma_dir}")


def main():
    run_ingest()


if __name__ == "__main__":
    main()