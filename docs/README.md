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

For local-build instructions and the repo layout, see the [project root README](https://github.com/jurassicjets/docs-avionics-testing#readme).
