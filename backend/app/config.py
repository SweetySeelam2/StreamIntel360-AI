import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    # or your provider of choice
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHAT_MODEL: str = "gpt-4.1-mini"
    VECTOR_DB_DIR: str = "data/chroma_index"

settings = Settings()