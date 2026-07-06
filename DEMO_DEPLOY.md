# Deploy the public Guest Demo (titan-omega-demo)

The guest tour is a **public, read-only** Space anyone can open — no login — that
shows the full Titan universe with **labelled SAMPLE data** and **all actions
disabled**. It ships with **no API keys**, so there is nothing to steal and no
LLM quota to burn. Your real product source stays in the private repos.

I couldn't finish this step autonomously: the cached HF git token on this machine
is invalid, and the browser extension dropped. It's ~3 minutes for you:

## Step 1 — Create the demo Space (1 min)
1. Go to **huggingface.co/new-space** (logged in as `careermind2026`).
2. Owner `careermind2026`, Space name **`titan-omega-demo`**, License other,
   **SDK = Docker** (blank template), Visibility **Public**. Create.

## Step 2 — Turn on guest mode + keep it safe (1 min)
In the new Space → **Settings → Variables and secrets**:
- Add a **Variable** (not secret): `TITAN_GUEST_MODE` = `1`
- Add a **Variable**: `TITAN_REQUIRE_AUTH` = `0`
- **Do NOT add any LLM/API keys.** The demo needs none. (Ask Titan / live AI
  features simply stay quiet on the demo — that's intended. The 3D universe,
  War Room replay, finance/CRM sample panels, boot sequence all work without keys.)

## Step 3 — Auto-deploy from the new repo (1 min)
The repo already has a workflow that pushes to `titan-omega-demo` (and ONLY that
space — it can never touch your production app).
1. In GitHub → `AbdullahRathoreVA/titan-omega-infinity` → **Settings → Secrets and
   variables → Actions → New repository secret**: `HF_TOKEN` = a Hugging Face
   token with **write** access (huggingface.co/settings/tokens → New token → Write).
2. GitHub → **Actions** tab → run **"Sync to Hugging Face Hub (DEMO SPACE)"** →
   Run workflow. (Or push any commit.)
3. Watch it build: `https://huggingface.co/api/spaces/careermind2026/titan-omega-demo`
   → wait for `"stage":"RUNNING"`.

## Step 4 — Verify (30 sec)
Open `https://careermind2026-titan-omega-demo.hf.space` — it should boot straight
into the universe (no login), show a "GUEST TOUR · read-only · sample data" badge,
and greet "WELCOME TO TITAN". Try clicking an action → it's blocked (403). 
This is the link you put on your resume, Upwork, and LinkedIn.

> Anti-theft recap: source is private, demo has no secrets, all writes are 403,
> and the code is served (not downloadable). Someone could screen-record the UI —
> that's just marketing — but they cannot take the working system or your keys.
