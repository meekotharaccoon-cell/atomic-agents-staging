#!/usr/bin/env bash
# Helper to commit and push workspace changes.
# Usage: ./scripts/push_changes.sh "Commit message"

set -e

MSG="$1"
if [ -z "$MSG" ]; then
  MSG="chore: update project files (automated)"
fi

git add .
git commit -m "$MSG" || echo "No changes to commit"

# Try to push to current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Pushing to origin/$BRANCH"
git push origin "$BRANCH"
