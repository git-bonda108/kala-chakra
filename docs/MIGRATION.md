# Migrating this codebase to your own Git repository

The code currently lives on the Cursor cloud remote for this agent run. Here
are three ways to move it to a repository you own. **Never paste a personal
access token into the chat** — use one of the token-safe paths below.

## Option A — "Create repo" button (easiest, no token sharing)

In the Cursor agent view (the panel showing this run), use the **Create repo**
action. It publishes the current `main` branch to a new GitHub repository under
your account. This is the intended path for a New Project session and requires
no token from you to the agent.

## Option B — Let the agent push to an existing repo (token as a secret)

1. Create the empty target repo on GitHub (no README/license, to avoid a
   conflicting root commit).
2. Cursor Dashboard → **Cloud Agents → Secrets** → add:
   ```
   Name:  GITHUB_TOKEN
   Value: <a GitHub PAT with 'repo' scope>
   ```
3. Send the agent your repo URL, e.g. `https://github.com/<you>/<repo>.git`, in
   a **new** message (a fresh run picks up the secret). The agent will run:
   ```bash
   bash scripts/migrate_to_github.sh https://github.com/<you>/<repo>.git
   ```
   which adds a `github` remote and pushes `main` (and tags).

## Option C — Do it yourself locally

From a machine already authenticated to GitHub (via `gh auth login` or an SSH
key), and with the project files (download from the agent, or after Option A):

```bash
git init            # if starting from a plain copy of the files
git add -A
git commit -m "Kala Chakra — Vedic horoscope studio"
git branch -M main
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main
```

## Notes

- Bundled Noto fonts under `assets/fonts/` are committed so the PDF renders
  Telugu/Hindi anywhere.
- `node_modules`, `.env`, and local scratch are git-ignored; nothing secret is
  in history.
- The GR-001 handover PDF under `docs/` is reference material; remove it if you
  do not want it in your public repo.
