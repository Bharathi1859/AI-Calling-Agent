from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.staticfiles import StaticFiles
from app.api.conversations import router as conversation_router
from app.api.customers import router as customer_router
from app.api.calls import router as call_router
from app.api.voice import router as voice_router


app = FastAPI(
    title="AI Calling Agent API",
    description="Backend API for AI-powered two-way calling agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/audio",
    StaticFiles(directory="test_audio"),
    name="audio"
)

app.include_router(customer_router)
app.include_router(call_router)
app.include_router(conversation_router)
app.include_router(voice_router)

@app.get("/")
def root():
    return {
        "message": "AI Calling Agent API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }