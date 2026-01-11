#!/bin/bash

echo "Installing git hooks"

REPO_ROOT=$(git rev-parse --show-toplevel)
cp "$REPO_ROOT/scripts/git-hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"

echo "Success! Pre-commit hook installed."
