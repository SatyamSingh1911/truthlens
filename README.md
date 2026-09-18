# TruthLens

**Track:** Track 2 — Real-World AI Products  
**Product brief:** TruthLens — a misinformation triage platform  
**Hackathon ID:** AZIS-HMJYFM

## Live deployment

Replace this with the deployed public URL after deployment:

`https://YOUR-APP-URL.example`

## Standard API

**Standard API: No / Browser-agent UI grading.**

This implementation exposes a small JSON endpoint at `/api/claims` for convenience, but the primary product is the browser UI. Change the Standard API line above only if the hackathon organizers define a different API contract for Track 2.

## What is implemented

1. **Submit a claim** — claim text, source platform, category, and optional source link.
2. **Risk flags** — automatic Sensational, Shouting, and Unsourced flags; 2+ flags becomes High Risk.
3. **Review workflow** — Unverified claims can be moved to Verified True, False, or Misleading with a short reviewer note.
4. **Public feed** — all claims are visible, with category/status filters and status/risk badges.
5. **Detail view** — full claim text, flags, reviewer note, status, source link, and submission time.

## Decision Points

See [`DECISIONS.md`](DECISIONS.md).

- DP1: Risk first, then recency.
- DP2: Unverified claims remain visible but are clearly labeled.
- DP3: Original claims are immutable after submission.

## Local run

Requires Python 3.11+.

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

For production-style local serving:

```bash
pip install gunicorn
gunicorn app:app
```

## Risk-flag rules

- Text containing `breaking`, `shocking`, or `share before deleted` → **Sensational**
- More than 50% of alphabetic characters are uppercase → **Shouting**
- Missing source link → **Unsourced**
- Two or more flags → **High Risk**

The rules are deterministic and intentionally transparent.

## Test flow

1. Open the public feed.
2. Click **Submit a claim**.
3. Submit a claim with no source link and wording such as `BREAKING: SHOCKING NEWS`.
4. Confirm Sensational + Shouting + Unsourced and **High Risk**.
5. Open the claim detail.
6. Select Verified True / False / Misleading and add a reviewer note.
7. Return to the feed and filter by category/status.
8. Open the detail again and confirm the review note and original flags are present.

## Deployment

This repository is designed for a simple Python web deployment such as Render.

Build/install command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn app:app
```

No environment secrets or authentication are required for the basic app.

### Important submission step

Before submitting the hackathon entry, replace:

`AZIS-HMJYFM`

in the root `README.md` with the **exact Hackathon ID from your profile**, and replace the deployment placeholder with the real public URL.
