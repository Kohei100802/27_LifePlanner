#!/bin/bash
set -e

if ! command -v fswatch >/dev/null 2>&1; then
  echo "fswatchがありません。brew install fswatch で導入してください" >&2
  exit 1
fi

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI(gh)がありません。brew install gh で導入・gh auth login を実行してください" >&2
  exit 1
fi

REPO_NAME=$(basename "$(pwd)")

fswatch -o . | (while read; do 
    git add . && git diff --quiet --exit-code --cached || {
        git commit --no-verify -m "Auto-commit at $(date)"
        if git remote get-url origin > /dev/null 2>&1; then
            git push origin main || {
                echo "Push failed, checking if remote repository exists..."
                if ! gh repo view "$REPO_NAME" > /dev/null 2>&1; then
                    echo "Creating GitHub repository: $REPO_NAME"
                    gh repo create "$REPO_NAME" --public --source=. --push
                else
                    echo "Repository exists but push failed. Manual intervention required."
                fi
            }
        else
            echo "No remote repository configured. Creating GitHub repository: $REPO_NAME"
            gh repo create "$REPO_NAME" --public --source=. --push
        fi
    }
done) &

echo "Auto-push watcher started in background. Stop with: pkill -f fswatch"
