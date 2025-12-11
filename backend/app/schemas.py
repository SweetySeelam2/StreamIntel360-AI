from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    mode: str = "content_intel"  # or "explore", "compare"

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[Dict[str, Any]] = []

class TitleAnalysisRequest(BaseModel):
    title_name: str
    description: Optional[str] = None
    target_regions: Optional[List[str]] = None