# Yusuf AI Assistant

A personal assistant project being built step by step: browser chat first, followed by voice input and spoken replies, then Windows and Android interfaces.

## What's included now

- Responsive dark chat interface at `/`
- FastAPI backend
- `GET /health` — check whether the server is running
- `GET /api/status` — see whether an API key is configured (the key itself is never returned)
- `POST /api/chat` — send a message to the AI model
- `/docs` — interactive API documentation
- API key loaded from a local `.env` file, not from browser code

## Run on Windows with VS Code

### 1. Install the tools

Install Python 3.11 or newer and Visual Studio Code. In VS Code, install the Microsoft Python extension.

### 2. Download your repository

Open PowerShell or the VS Code terminal and run:

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
- API testing page: http://127.0.0.1:8000/docs

To stop the server, click the terminal and press **Ctrl+C**.

## Run the basic automated tests

After installing dependencies, run:

\`\`\`powershell
python -m pytest
\`\`\`

The tests check that the homepage loads, the health endpoint responds, status does not reveal the API key, and chat reports a clear setup error when no key is configured.

## Test the chat endpoint

You can test from the chat interface or from `/docs`, using `POST /api/chat`:

```json
{
  "message": "Explain photosynthesis in simple Hindi.",
  "language": "Hindi"
}
```

## Planned next steps

1. Run and test the local browser interface.
2. Improve chat behavior and add conversation controls.
3. Add voice input and text-to-speech.
4. Add a Windows desktop companion.
5. Build the Android interface.
6. Add settings, accessibility, and privacy controls.

## Security and deployment notes

- Never commit a real API key. Keep it in your local `.env` file or a hosting provider's secret manager.
- Do not embed the API key in browser or mobile application code.
- CORS is open for development convenience; restrict allowed origins before public deployment.
- This project is a development starter, not a production-secured public service.


## NEXORA AI Android app (version 1.1)

The Android project is in `android/`. It is a secure HTTPS WebView shell around the existing FastAPI web app. The AI provider key stays on the backend and is never packaged in the APK.

### Deploy the backend

1. Create a new Web Service in Render and connect this repository/branch.
2. Use the included `render.yaml` blueprint (or set the same build/start commands).
3. Add the private environment variables in Render:
   - `OPENAI_API_KEY`: your provider key (keep it private).
   - `NEXORA_ACCESS_CODE`: create a long, unique access code and share it only with intended app users.
   - `OPENAI_MODEL`: optional; defaults to `gpt-4.1-mini`.
4. Wait for the service to deploy. Check `https://YOUR-SERVICE/health`; it should return status `ok`.

Do not put either secret in GitHub source files or in the Android app.

### Build the APK with GitHub Actions

1. Open **Settings → Secrets and variables → Actions** in GitHub.
2. Add repository secret `NEXORA_BACKEND_URL` with the HTTPS Render service URL (for example, `https://your-service.onrender.com`).
3. Open **Actions → Build NEXORA AI Android APK** and run the workflow, or push a change under `android/`.
4. When the run succeeds, open the run's **Artifacts** section and download `NEXORA-AI-1.1-debug`. Extract the ZIP to get `app-debug.apk`.
5. Transfer the APK to the Android phone and install it. If no backend URL was configured at build time, the app asks for the HTTPS server address on first launch.

The workflow creates a debug APK for testing. A Play Store release needs a separately signed release build and Play App Signing setup.
