@echo off
cd /d "%~dp0"
py -m pip install -r requirements.txt
if not exist .env (
  copy .env.example .env
  echo Created .env. Add your DeepSeek API key, save, then run this file again.
  notepad .env
  pause
  exit /b
)
py app.py
pause
