#!/usr/bin/env bash
# Push this repository to your own GitHub repo.
#
# Usage:
#   GITHUB_TOKEN=<pat>  bash scripts/migrate_to_github.sh https://github.com/<you>/<repo>.git
# or, if the token is already in the environment (e.g. a Cursor secret):
#   bash scripts/migrate_to_github.sh https://github.com/<you>/<repo>.git
#
# The token is used only to construct the push URL and is never printed or
# committed.
set -euo pipefail

REPO_URL="${1:-}"
if [[ -z "$REPO_URL" ]]; then
  echo "error: pass the target repo URL, e.g. https://github.com/you/repo.git" >&2
  exit 1
fi

TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"

# Build an authenticated URL for https remotes when a token is present.
PUSH_URL="$REPO_URL"
if [[ -n "$TOKEN" && "$REPO_URL" == https://github.com/* ]]; then
  PUSH_URL="https://x-access-token:${TOKEN}@github.com/${REPO_URL#https://github.com/}"
fi

# Point/replace a dedicated 'github' remote so the cloud 'origin' is untouched.
if git remote | grep -qx github; then
  git remote set-url github "$PUSH_URL"
else
  git remote add github "$PUSH_URL"
fi

BRANCH="$(git symbolic-ref --short HEAD)"
echo "Pushing branch '$BRANCH' and tags to $REPO_URL ..."
git push -u github "$BRANCH"
git push github --tags || true

# Scrub the token from the stored remote URL.
git remote set-url github "$REPO_URL"
echo "Done. Remote 'github' -> $REPO_URL"
