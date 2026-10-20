# Voice MVP for Yusuf AI Assistant

## First milestone: push-to-talk in the existing web app

The first voice milestone should be a user-tapped microphone button and optional spoken replies. This works as a bridge while the native Windows and Android clients are planned.

### Behavior
- The microphone starts only after the user presses the button and grants browser permission.
- Speech is transcribed into the message box so the user can review it before sending.
- Spoken replies are optional and can be disabled with a checkbox.
- Text chat remains available if microphone permission or browser speech recognition is unavailable.
- The first milestone does not use an always-on microphone or automatically listen for a wake phrase.

### Important browser limitations
- Speech recognition support varies by browser and operating system; test in current Chrome or Edge.
- Browser speech recognition may rely on the browser vendor's speech service. Do not treat it as guaranteed offline or private on-device transcription.
- Speech synthesis voices vary by device. Voice cloning is not part of this milestone and must not imitate another person's voice without their consent.

## Next native milestones

1. Windows companion: local microphone capture and speech output, visible listening indicator, mute control, and a wake-word prototype that does not send audio to the backend before activation.
2. Android companion: native microphone permission flow, foreground service only where allowed, notification with a clear stop control, and battery/privacy behavior tested on the target phone.
3. Shared authenticated backend: device enrollment, revocation, TLS, and user-owned settings/tasks.
4. Approval gate: show a review card before sending messages, publishing, commenting, recording screens, deleting files, or taking other sensitive actions.

## Acceptance checklist

- [ ] User can type and chat without granting microphone permission.
- [ ] Push-to-talk starts only after a tap.
- [ ] User can review speech transcription before submitting it.
- [ ] Spoken replies can be turned off.
- [ ] Microphone errors are shown without breaking text chat.
- [ ] No wake-word background listening is enabled by default.
- [ ] Sensitive app actions require explicit confirmation.
- [ ] Tests run locally before this milestone is merged.

## Not implemented by this document

This is a design contract, not a claim that voice controls, wake-word detection, screen recording, phone control, voice cloning, or a native APK have already been implemented.