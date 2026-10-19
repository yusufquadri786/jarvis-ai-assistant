# JARVIS ULTRA AI

Beginner-friendly Windows desktop chat assistant using the DeepSeek API.

## Features
- Dark desktop chat interface
- DeepSeek-powered answers
- Safe shortcuts to YouTube, Google, and TradingView
- Ctrl+Enter to send messages
- Configuration via a local environment file

## Windows setup
1. Install Python 3.10 or newer.
2. Open this folder in VS Code or PyCharm.
3. Run `py -m pip install -r requirements.txt` in the terminal.
4. Copy `.env.example` to `.env`.
5. Edit `.env` locally and set `DEEPSEEK_API_KEY=your_key`.
6. Run `py app.py` or double-click `run_jarvis.bat`.

Check DeepSeek platform pricing and account requirements before use. Keep your key private and never upload `.env` to GitHub.

## Limitations and safety
This is a starter app, not a finished autonomous agent. Microphone voice control and broad computer control are not implemented yet. It does not place live trades. Use paper trading for learning; AI cannot guarantee profits. Only access devices, accounts, and networks you are authorized to use.
