# Migration & Comparison — Project Titan Omega → Titan Omega Infinity

Imported snapshot: original `main` @ `b3f0255` (2026-07-06). The original repo
(`AbdullahRathoreVA/Project-titan-omega`) is frozen as the permanent backup and
still drives the founder's private Space. This repo evolves independently.

## Implemented differences (day 0 — verified, tests 32/32, build clean)

| Area | Original | Infinity |
|---|---|---|
| Public demo | None — auth wall ("demo access on request") | **Guest tour**: `TITAN_GUEST_MODE=1` → no login, read-only API (mutations 403), labelled SAMPLE finance/CRM data, "WELCOME TO TITAN" boot, GUEST badge. Founder login still unlocks full control on the same deploy. |
| Demo safety | n/a | Demo Space ships with **zero API keys** — nothing to steal, no LLM quota to burn; source stays in private repos. |
| Licensing | none | Proprietary commercial LICENSE (Founder / Agency / Enterprise tiers). |
| Strategy docs | scattered specs | COMMERCIAL_PLAYBOOK.md (positioning, pricing, launch plan, honest forecasts). |
| Showcase media | in-repo `docs/media` (breaks HF pushes) | removed — media lives in the public showcase repo. |

## Planned (roadmap — NOT yet implemented; ordered by revenue impact)

1. Dodo Payments checkout + license key validation (needed for license sales).
2. Setup wizard + `.env.example` + one-command installer (buyer onboarding).
3. Postgres/SQLAlchemy persistence replacing JSON snapshot store. **Breaking.**
4. Multi-tenant auth (JWT sessions, per-workspace stores). **Breaking.**
5. White-label theming (name/logo/colors via env).
6. Enterprise pack: RBAC, audit log, SSO — only after paying customers ask.

## Migration steps (original → Infinity), when you switch your own deploy

1. Copy Space secrets to the new Space (GROQ/GEMINI/OPENROUTER/TAVILY/GITHUB/
   TELEGRAM_*/TITAN_* — strip whitespace!).
2. Export `data/` snapshot from the old deploy; import before first boot.
3. Point the Cloudflare Telegram Worker's `TITAN_URL` at the new Space.
4. Update Make.com scenario URLs.
5. Keep the old Space running until the new one passes `/api/doctor`.

## Compatibility promise

Until the Postgres/multi-tenant refactors land, every original feature works
identically here — same endpoints, same env vars, same Docker image contract.
