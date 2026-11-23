"""NEXORA AI — FastAPI backend and web interface."""
import hmac
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
WEB_APP = BASE_DIR / "static" / "index.html"

app = FastAPI(
    title="NEXORA AI",
    description="Private AI assistant API.",
    version="1.1.0",
)

# Cross-origin access is disabled by default. Add trusted origins only if needed.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]
if allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-NEXORA-ACCESS-CODE"],
    )


@app.middleware("http")
async def require_nexora_access_code(request: Request, call_next):
    """Protect API routes with a server-side access code; never ship it in the APK."""
    if request.url.path.startswith("/api/"):
        expected = os.getenv("NEXORA_ACCESS_CODE", "").strip()
        supplied = request.headers.get("X-NEXORA-ACCESS-CODE", "")
        if not expected:
            return JSONResponse(
                status_code=503,
                content={"detail": "Server owner must configure NEXORA_ACCESS_CODE."},
            )
        if not supplied or not hmac.compare_digest(supplied, expected):
            return JSONResponse(
                status_code=401,
                content={"detail": "A valid NEXORA access code is required."},
            )
    return await call_next(request)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    language: Optional[str] = Field(default="auto", max_length=40)


class ChatResponse(BaseModel):
    reply: str
    language: str


@app.get("/", include_in_schema=False)
def home():
    """Serve the NEXORA chat interface."""
    if not WEB_APP.is_file():
        raise HTTPException(status_code=500, detail="Web interface file is missing.")
    return FileResponse(WEB_APP)


@app.get("/health")
def health():
    """Public health check; does not expose configuration or secrets."""
    return {"status": "ok", "app": "NEXORA AI", "version": "1.1"}


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
            detail="AI is not configured yet. The server owner must add OPENAI_API_KEY.",
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    requested_language = request.language or "auto"
    language_instruction = (
        "Reply in the same language as the user unless they ask for another language."
        if requested_language == "auto"
        else f"Reply in {requested_language}."
    )

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=(
                "You are NEXORA AI, a helpful, honest, multilingual assistant. "
                "Explain ideas clearly, protect privacy, and never claim to have "
                "performed actions you did not perform. "
                + language_instruction
            ),
            input=request.message,
        )
        reply = response.output_text.strip() or "I couldn't produce a reply. Please try again."
        return ChatResponse(reply=reply, language=requested_language)
    except Exception as exc:
        # Do not expose provider details, request contents, or secret values to clients.
        print(f"AI request failed: {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail="The AI service request failed. Check server configuration and try again.",
        ) from None
