# Jurassic Jets — Avionics Documentation

Bench-test notes, pinout discoveries, signal traces, and "how does this LRU actually work" writeups for the electromechanical and early-digital avionics that lived in 707s, 727s, 737-classics, 747-classics, DC-8s, DC-9s, L-1011s, and their kin.

This repo is the institutional knowledge base for what we learn at the bench. It's organized so a contributor — sim enthusiast or active commercial captain — can find the unit they care about, see what's known about it, and add what they've learned.

## Navigation

The repo splits content along two axes: how the *airframe* is configured, and what each *unit* is.

- **[avionics/](avionics/)** — Unit-level registry. One folder per LRU type, documenting pinouts, behavior, bench tests, quirks, datasheets — written once regardless of how many copies exist or how many airframes carry it.
- **[aircraft/](aircraft/)** — Per-airframe configuration. Each aircraft has cockpit map and `panels/<panel>/<module>/` — the module README is the leaf and lists each install slot, linking out to `avionics/`. Currently: [b747-300-ja8179](aircraft/b747-300-ja8179/README.md).
- **[systems/](systems/)** — Cross-cutting topics that span multiple instruments and airframes: ARINC 429, synchros, 28 VDC distribution, 400 Hz AC, etc. Also where generic test methods (sniffing a bus, exciting a synchro) live, alongside the protocol they apply to.
- **[templates/](templates/)** — Starter scaffolds. Copy-paste, then fill in.
- **[glossary.md](glossary.md)** — Acronyms, part-number conventions, and term-of-art definitions.

## Contributing

Read **[CONTRIBUTING.md](CONTRIBUTING.md)** before adding content. It covers naming conventions, the per-instrument file skeleton, image and large-file handling, and how to handle instruments that appear in multiple aircraft.

## Docs site

Rendered with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed to **[avionics-docs.jurassicjets.com](https://avionics-docs.jurassicjets.com/)** on every push to `main` via [GitHub Actions](https://github.com/jurassicjets/docs-avionics-testing/blob/main/.github/workflows/docs.yml). GitHub also renders the markdown directly in this repo, so you don't need any tooling to read or contribute.

### Building the site locally

MkDocs forbids `docs_dir` from being the parent of `mkdocs.yml`, but we want content to live at the repo root rather than under a `docs/` wrapper. The build uses a tiny staging step ([`scripts/stage_docs.sh`](scripts/stage_docs.sh)) that creates a `_site_src/` directory of symlinks pointing back to the real files. Edits to the source files are visible immediately because they're symlinks, so `mkdocs serve` works normally after one stage.

```bash
pip install -r requirements-docs.txt
./scripts/stage_docs.sh
mkdocs serve
```

Then open <http://localhost:8000>. Edits to existing files hot-reload; if you add a new top-level item (a new directory at the repo root), re-run `./scripts/stage_docs.sh`.
