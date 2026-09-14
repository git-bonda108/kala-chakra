# Configuration — API keys & secrets

The app runs **fully without any key** (grounded local narrator, all three
languages, PDF export). A key only unlocks *live* features.

## What a key unlocks

| Feature | Needs a key? |
| --- | --- |
| Rashi / nakshatra / lagna / dasha (calc_core) | No — always deterministic |
| Predictions & remedies (local narrator) | No |
| Predictions & remedies via **OpenAI Agents SDK** | Yes (`OPENAI_API_KEY`) |
| **Image (vision) OCR** of uploaded handwritten sheets | Yes (`OPENAI_API_KEY`) |
| PDF / text document parsing & cross-validation | No |

## Where to put `OPENAI_API_KEY`

Keys are read from the **environment only**. There is deliberately **no key
input in the UI** — that is the wrong place for a credential in an enterprise
app. The sidebar only shows whether live agents are enabled.

### 1. Cursor Cloud secret (persists across agent runs) — recommended
Cursor Dashboard → **Cloud Agents → Secrets** → add:

```
Name:  OPENAI_API_KEY
Value: sk-...
```

Secrets are injected as environment variables into **new** agent VMs. A VM that
was already running before you added the secret will not see it — start a fresh
agent (or a new message that boots a new run) to pick it up. Scope can be
user-level or repo-level; user secrets override team secrets.

### 2. Local `.env` (when you run it on your own machine)
```bash
cp .env.example .env
echo "OPENAI_API_KEY=sk-..." >> .env
# or simply:
export OPENAI_API_KEY=sk-...
streamlit run app.py
```

`.env` is git-ignored, so the key never gets committed.

## Model used

Vision OCR uses `gpt-4o-mini`. Specialist agents use the OpenAI Agents SDK
default model. Both are configurable in `kala/parsing.py` and
`kala/orchestration.py` if you want a different model.
