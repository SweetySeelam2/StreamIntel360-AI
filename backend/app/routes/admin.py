from fastapi import APIRouter
from ..rag.ingest import run_ingest

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.post("/rebuild_index")
async def rebuild_index():
    run_ingest()
    return {"status": "ok", "message": "Index rebuilt"}