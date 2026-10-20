# Claude Code Instructions — Yusuf AI Assistant

## Project goal
Build Yusuf AI Assistant step by step, prioritizing a reliable voice-first assistant and beginner-friendly development. The current project is a Python/FastAPI browser chat starter; do not assume an Android APK already exists.

## Before changing code
1. Inspect the existing files and tests first.
2. Explain the plan briefly before large changes.
3. Preserve existing working behavior and avoid rewriting the project unnecessarily.
4. Run the available automated tests and report the exact results. Do not claim the app was run or verified unless it was actually run.

## Development priorities
1. Make the current FastAPI app run reliably on Windows with VS Code.
2. Keep API keys server-side in `.env`; never put secrets in frontend, mobile code, commits, logs, or examples.
3. Add voice input and spoken responses with clear permission handling and a text fallback.
4. After the browser version is stable, plan the Windows and Android interfaces as separate, testable steps.
5. Give the owner beginner-friendly setup and testing instructions.

## Safety and security
- Never ask the owner to paste API keys, passwords, recovery codes, or access tokens into chat or commit them to GitHub.
- Do not expose secrets or weaken authentication/security to make a demo work.
- Avoid destructive commands and do not delete or overwrite user work without explaining the change first.
- Keep `.env` and other secrets out of version control.

## Working style
- Prefer small, reviewable changes.
- Update README instructions when setup or behavior changes.
- Report files changed, tests run, results, and any remaining limitations.
- Do not claim deployment, APK generation, device testing, or publishing unless those actions were completed and verified.