from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat, analyze, admin

app = FastAPI(
    title="StreamIntel360 API",
    description="Multi-agent content intelligence backend for StreamIntel360.",
    version="0.1.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {
        "status": "ok",
        "message": "StreamIntel360 backend is running",
        "docs": "/docs",
    }

# IMPORTANT: global /api prefix only here
app.include_router(chat.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
app.include_router(admin.router, prefix="/api")