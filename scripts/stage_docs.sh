#!/usr/bin/env bash
#
# Build a staging directory of symlinks for MkDocs.
#
# MkDocs forbids docs_dir from being the parent of its config file
# (no docs_dir: '.'), so we keep content at the repo root and link
# each top-level item into _site_src/, then point mkdocs.yml at
# docs_dir: _site_src. Because the entries are symlinks, edits to
# the real files at root are visible immediately — `mkdocs serve`
# works normally after one stage.
#
# Re-run this script after adding a new top-level item at the repo
# root so it gets exposed to mkdocs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGE_DIR="$ROOT_DIR/_site_src"

# Top-level items at the repo root that should appear in the rendered
# site. Add new entries here as the repo grows. Anything not listed
# here (e.g. mkdocs.yml, .github/, requirements-docs.txt, scripts/)
# is intentionally excluded from the docs build.
ITEMS=(
  README.md
  CONTRIBUTING.md
  glossary.md
  aircraft
  avionics
  systems
  templates
  CNAME
)

rm -rf "$STAGE_DIR"
mkdir -p "$STAGE_DIR"

for item in "${ITEMS[@]}"; do
  if [ -e "$ROOT_DIR/$item" ]; then
    ln -s "../$item" "$STAGE_DIR/$item"
  else
    echo "stage_docs.sh: warning: '$item' not found at repo root, skipping" >&2
  fi
done

echo "stage_docs.sh: staged $STAGE_DIR/"
