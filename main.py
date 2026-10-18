"""Yusuf AI Assistant — starter API backend.

Run locally:
    python -m venv .venv
    # Windows: .venv\\Scripts\\activate
    # macOS/Linux: source .venv/bin/activate
    pip install -r requirements.txt
    copy .env.example .env   # Windows; on macOS/Linux use: cp .env.example .env
    # Add your API key to .env, then:
    uvicorn main:app --reload
"""
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

app = FastAPI(
    title="Yusuf AI Assistant API",
    description="Starter backend for the Yusuf AI Assistant project.",
    version="0.1.0",
)

# Development setting. Restrict allowed origins before deploying publicly.
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


@app.get("/")
def root():
    return {
        "app": "Yusuf AI Assistant",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is missing. Add it to your local .env file.",
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    client = OpenAI(api_key=api_key)

    language_instruction = (
        "Reply in the language requested by the user."
        if request.language == "auto"
        else f"Reply in {request.language}."
    )

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are Yusuf AI Assistant, a helpful, honest, multilingual "
                "assistant. Explain things clearly, protect user privacy, and "
                "never claim to have performed actions you did not perform. "
                + language_instruction
            ),
            input=request.message,
        )
        reply = response.output_text.strip()
        if not reply:
            reply = "I couldn't produce a reply. Please try again."
        return ChatResponse(reply=reply, language=request.language or "auto")
    except Exception as exc:
        # Avoid returning internal exception details or secrets to the client.
        print(f"AI request failed: {type(exc).__name__}")
        raise HTTPException(
            status_code=502,
            detail="The AI service request failed. Check your API settings and try again.",
        ) from None
