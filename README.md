# Yusuf AI Assistant

A personal assistant project being built step by step: browser chat first, followed by voice input and spoken replies, then Windows and Android interfaces.

## What's included now

- Responsive dark chat interface at `/`
- FastAPI backend
- `GET /health` — check whether the server is running
- `GET /api/status` — see whether an API key is configured (the key itself is never returned)
- `GET /api/integrations` — show the planned integration catalogue and approval expectations; this does **not** mean accounts are connected
- `POST /api/chat` — send a message to the AI model
- `/docs` — interactive API documentation
- API key loaded from a local `.env` file, not from browser code

## Run on Windows with VS Code

### 1. Install the tools

Install Python 3.11 or newer and Visual Studio Code. In VS Code, install the Microsoft Python extension.

### 2. Download your repository

```powershell
git clone https://github.com/yusufquadri786/jarvis-ai-assistant.git
cd jarvis-ai-assistant
code .
```

If the `code .` command is unavailable, open VS Code and choose **File → Open Folder**, then select the downloaded `jarvis-ai-assistant` folder.

### 3. Create a virtual environment

In the VS Code terminal (PowerShell), run:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use the environment's Python directly instead:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Configure the API key

Copy the template:

```powershell
Copy-Item .env.example .env
```

Open `.env` in VS Code and put your own API key after `OPENAI_API_KEY=`. Keep the key private. Do not paste it into chat messages, browser code, screenshots, or GitHub commits. The real `.env` file is ignored by Git.

You need API access and billing may apply. If you don't have an API key yet, you can still open the interface and check the server, but AI replies will show a setup message.

### 6. Start Yusuf AI Assistant

```powershell
python -m uvicorn main:app --reload
```

Keep the terminal open while using the app.

### 7. Open the app

- Chat interface: http://127.0.0.1:8000
- Server check: http://127.0.0.1:8000/health
- API settings status: http://127.0.0.1:8000/api/status
- Planned integrations: http://127.0.0.1:8000/api/integrations
- API testing page: http://127.0.0.1:8000/docs

To stop the server, click the terminal and press **Ctrl+C**.

## Run the automated tests

After installing dependencies, run:

```powershell
python -m pytest
```

The tests check the homepage, health endpoint, API-key secrecy, missing-key behavior, integration catalogue, and confirmation policy. A successful test run must be performed locally; a repository change alone does not prove the app runs.

## Test the chat endpoint

You can test from the chat interface or from `/docs`, using `POST /api/chat`:

```json
{
  "message": "Explain photosynthesis in simple Hindi.",
  "language": "Hindi"
}
```

## Cross-device development plan

See [`docs/DEVICE_INTEGRATION_ROADMAP.md`](docs/DEVICE_INTEGRATION_ROADMAP.md) for the phased plan for Windows and Android clients, voice, app integrations, and sensitive-action approvals.

## Security and deployment notes

- Never commit a real API key. Keep it in your local `.env` file or a hosting provider's secret manager.
- Do not embed the API key in browser or mobile application code.
- The integration catalogue is planning metadata; no external app accounts are connected by it.
- Ask for confirmation before sending messages, publishing posts, commenting, deleting files, purchases, or other externally visible/destructive actions.
- CORS is open for development convenience; restrict allowed origins before public deployment.
- This project is a development starter, not a production-secured public service.
