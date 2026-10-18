"""Yusuf AI Assistant — FastAPI backend and local web interface."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
WEB_APP = BASE_DIR / "static" / "index.html"

app = FastAPI(
    title="Yusuf AI Assistant",
    description="Personal AI assistant API.",
    version="0.2.0",
)

# Development-only CORS configuration. Restrict this before public deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    language: Optional[str] = Field(default="auto", max_length=40)


class ChatResponse(BaseModel):
    reply: str
    language: str


@app.get("/", include_in_schema=False)
def home():
    """Serve the chat interface."""
    if not WEB_APP.is_file():
        raise HTTPException(status_code=500, detail="Web interface file is missing.")
    return FileResponse(WEB_APP)


@app.get("/health")
def health():
    """Basic server health check."""
    return {"status": "ok", "app": "Yusuf AI Assistant"}


@app.get("/api/status")
def status():
    """Report configuration status without exposing secrets."""
    return {
        "status": "ready" if os.getenv("OPENAI_API_KEY") else "needs_api_key",
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY")),
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI is not configured yet. Add OPENAI_API_KEY to your local .env file.",
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    language_instruction = (
        "Reply in the same language as the user unless they ask for another language."
        if request.language == "auto"
        else f"Reply in {request.language}."
    )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=(
                "You are Yusuf AI Assistant, a helpful, honest, multilingual assistant. "
                "Explain ideas clearly, be friendly to students, protect privacy, and "
                "never claim to have performed actions you did not perform. "
                + language_instruction
            ),
            input=request.message,
        )
        reply = response.output_text.strip() or "I couldn't produce a reply. Please try again."
        return ChatResponse(reply=reply, language=request.language or "auto")
    except Exception as exc:
        # Keep secret values and provider details out of the response sent to the browser.
        print(f"AI request failed: {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail="The AI service request failed. Check your API settings and try again.",
        ) from None
