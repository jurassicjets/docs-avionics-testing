# Jurassic Jets — Avionics Documentation

Bench-test notes, pinout discoveries, signal traces, and "how does this LRU actually work" writeups for the electromechanical and early-digital avionics that lived in 707s, 727s, 737-classics, 747-classics, DC-8s, DC-9s, L-1011s, and their kin.

The full documentation lives in **[`docs/`](docs/)** and is rendered at:

**[avionics-docs.jurassicjets.com](https://avionics-docs.jurassicjets.com/)**

For contribution guidelines, see [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Building the site locally

```bash
pip install -r requirements-docs.txt
mkdocs serve
```

Then open <http://localhost:8000>. Edits hot-reload.

## Repository layout

- [`docs/`](docs/) — all documentation content (the published site).
- [`mkdocs.yml`](mkdocs.yml) — MkDocs Material configuration.
- [`requirements-docs.txt`](requirements-docs.txt) — Python deps for building the docs.
- [`.github/workflows/docs.yml`](.github/workflows/docs.yml) — builds and deploys on every push to `main`.
