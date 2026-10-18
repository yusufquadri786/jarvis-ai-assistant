# Yusuf AI Assistant

My personal AI assistant project: a Python AI backend first, with plans for a voice interface, Android app, and Windows desktop companion.

## Current starter backend

- FastAPI HTTP API
- `GET /` — app status
- `GET /health` — health check
- `POST /api/chat` — send a message to the AI service
- API keys are read from a local `.env` file, not committed to GitHub

## Run locally on Windows

1. Install Python 3.11 or newer.
2. Download or clone this repository.
3. Open a terminal in the repository folder.
4. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Copy the example settings file and add your own API key to the local `.env` file:

   ```powershell
   Copy-Item .env.example .env
   ```

   Never put a real API key in source code or commit your `.env` file.

7. Start the server:

   ```powershell
   uvicorn main:app --reload
   ```

8. Open http://127.0.0.1:8000/docs to try the API, or http://127.0.0.1:8000/health to check the server.

## Test the chat endpoint

In the interactive docs at `/docs`, open `POST /api/chat` and try:

```json
{
  "message": "Explain photosynthesis in simple Hindi.",
  "language": "Hindi"
}
```

You need a valid API key and API access for the selected model. API usage may cost money.

## Next steps

1. Test the backend locally.
2. Add a polished chat interface.
3. Add voice input and text-to-speech.
4. Connect an Android app and Windows desktop interface.
5. Add settings and privacy controls.

## Development note

CORS is open for development convenience. Restrict allowed origins before deploying this API publicly. Do not expose the API key in a mobile app or browser client; keep it on the backend.
