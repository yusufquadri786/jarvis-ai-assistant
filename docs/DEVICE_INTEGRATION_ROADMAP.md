# Cross-device integration roadmap

## Goal

Build one Yusuf AI Assistant experience shared by a Windows laptop and Android phone, with voice-first interaction, shared preferences/tasks, modular app integrations, and explicit approval for sensitive actions.

The current repository is a FastAPI browser-chat starter. This plan does not assume that a Windows agent or Android APK already exists.

## Target architecture

- **Shared backend (FastAPI):** AI provider adapter, authenticated device sessions, task orchestration, integration registry, audit events, and synchronized settings/tasks.
- **Windows companion (later phase):** a small local agent that exposes only allowlisted actions (for example, open an approved app or open a URL). Never provide unrestricted shell execution to model output.
- **Android companion (later phase):** a native app with microphone and notification permissions requested in context; use Android-supported intents and APIs. Do not promise control of every other app.
- **Voice layer:** speech-to-text and text-to-speech behind interfaces, with text input/output as a reliable fallback.
- **Provider adapters:** start with the existing OpenAI integration. Add another provider only behind the same interface and make provider selection configurable; never require multiple models to run for every request.
- **App integrations:** separate adapters with explicit scopes, capability declarations, and per-action approval requirements.

## Approval and privacy rules

1. Read-only actions may run when the user has connected the relevant account and granted the required scope.
2. Ask for confirmation before sending messages, publishing posts, commenting, deleting or overwriting files, making purchases, changing account settings, or executing commands with external effects.
3. Do not automate bulk comments, spam, or platform-rule evasion. Use official APIs and their current permissions/rate limits where available.
4. Keep API keys and OAuth refresh tokens server-side or in the OS credential store. Never commit secrets or put provider keys in browser/mobile bundles.
5. Authenticate every remote device. Do not expose an unauthenticated local server to the public internet. Use TLS for remote connections and provide a way to revoke a device session.
6. Keep a minimal audit trail of actions and approvals without logging secrets or unnecessary message content.
7. Fail closed: if permissions, connection status, or approval state is unclear, explain the blocker and do not perform the action.

## Delivery phases

### Phase 0 — Baseline and contracts
- Preserve the existing /api/chat, /health, and /api/status behavior.
- Add automated tests for integration capability metadata and approval policy.
- Define stable request/response schemas before device clients are built.

### Phase 1 — Reliable browser/backend foundation
- Run the current app and existing tests locally on Windows.
- Tighten development configuration before any public deployment (including CORS and authentication).
- Add conversation state and settings only after tests cover the current behavior.

### Phase 2 — Voice on the current interface
- Add push-to-talk first, then optional wake-word support only if feasible and privacy-safe.
- Show microphone permission state and keep a text fallback.
- Test Hindi and English speech on actual supported devices.

### Phase 3 — Windows companion
- Start with a small allowlisted set of local actions and visible approval prompts.
- Require an authenticated connection to the backend; never accept arbitrary model-generated commands.

### Phase 4 — Android companion
- Build a native Android client that shares the backend and user settings.
- Use Android intents/permissions for supported tasks; provide clear limits for actions other apps do not expose.

### Phase 5 — App integrations, one at a time
Prioritize a task/reminder provider, file storage, calendar/email where available, then official Meta APIs for eligible Instagram/WhatsApp Business workflows. For every adapter, document required account type, permissions, limits, setup, and tests. Personal-app capabilities may differ from business APIs.

### Phase 6 — Release readiness
- Add device revocation, data export/deletion controls, error reporting without secrets, dependency checks, and end-to-end tests.
- Produce and verify a Windows package and Android APK only after the clients exist and can be built and tested.

## First implementation task

Start with **Phase 0**: define a small integration-capability schema and approval policy, plus tests. This is safer and easier to validate than attempting broad device automation in one change. No app account is considered connected until its OAuth/API setup is completed and verified.
