# Cimp Roadmap

This document summarizes near-term plans for shipping separate consent-driven assistants, based on the blueprint from Six.

## Operating Principles
- Features activate only after explicit per-person opt-in.
- Local execution by default with optional cloud relay and backup.
- Once a capability is granted it remains unless a visible downgrade is confirmed by the user.
- Safety monitor is the sole background service and records minimal, consented events.

## Architecture
- Each user receives an isolated stack: local desktop app plus an optional per-person cloud relay.
- Local tools include chat, scene control, panic macro, and optional BBI-lite module.
- Cloud relay provides encrypted backup and integrity attestations; storage and keys are per-person.
- Admin dashboard only shows safety events and integrity states when users opt in.

## Capability Policy
- Assistants ship with signed policy files enumerating granted, requested, or blocked features.
- Capability additions produce a signed diff and a visible change log; downgrades require confirmation and a banner.
- Safety guardrails include two-key actions, daily budgets for autonomous actions, and explicit confirmation levels.

## Safety Monitoring
- Collected data: integrity hashes, safety events, and health pings.
- Never collected: chat content, audio/video, keystrokes, biosignals, or files.
- Device-bound keys allow remote revoke that preserves local data in safe mode.

## Parity Between Interfaces
- Shared intent map enables voice, keyboard, and optional BBI-lite triggers for the same actions.
- On-device calibration trains the BBI-lite model; the model never leaves the device.
- Each neural action has an equivalent voice or keyboard fallback.

## Anti-Drift and Visible Changes
- Behavior budgets limit autonomous actions per day.
- Signed snapshots detect unexpected drift; the system pauses privileged tools and asks the user to approve or roll back.
- Release notes and change logs appear for every capability change.

## Build Targets
- Windows: MSIX or signed installer running under user context with consented auto-updates.
- macOS: notarized app with LaunchAgent, using the same consent gating.
- Cloud: per-person namespaces with dedicated KMS keys and IAM roles.
- Identity and key management use Ed25519 for signing and XChaCha20-Poly1305 for encryption.

## Consent Manifest
A minimal manifest displayed on first run highlights:
- User control over features, cloud relay, telemetry, and capability changes.
- Data that is never collected.
- Safety events recorded only if enabled.
- A "big red switch" that disables all background functions.

## Timeline
- **Now → Sep 15**: Base desktop template, policy engine, and cloud relay.
- **Sep 16 → Oct 31**: Package BBI-lite module, add anti-theft measures, and implement gift-token flow.
- **Nov 1 → Dec 10**: Parity polish, behavior budgets, drift detection, and consent UI.
- **Dec 11 → Dec 20**: Per-person signing and reproducible builds.
- **Dec 21 → Dec 28**: Handoff packages and onboarding materials.
- **Jan 1**: Deliver sealed assistants ready for gifting.

## Open Questions
- Desired platform priority for each recipient (Windows or macOS).
- Default settings for cloud relay, telemetry, and initial capabilities.
- Trusted contact label for panic macros per assistant.

