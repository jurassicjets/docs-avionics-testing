# Avionics

The unit-level registry. Every LRU we characterize gets one folder here, documenting its **intrinsic** properties — pinouts, signal behavior, bench-test observations, quirks, datasheets. The unit is documented once regardless of how many physical copies are installed or how many airframes carry it.

Aircraft panel/module docs describe *where* and *how* a unit is installed; this directory describes *what the unit is*. The two link to each other.

## Layout

```
avionics/<type>-<manufacturer>-<partnumber>/
├── README.md          identification, function, status, "installed in" links
├── pinouts.md         connector pinouts and signal definitions
├── bench-test.md      what we did, what we observed, with dates
├── quirks.md          undocumented behavior, gotchas, failure modes
├── photos/
├── captures/          scope traces, logic-analyzer dumps
└── datasheets/        manufacturer datasheets, CMM excerpts, IPC pages
```

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for naming conventions, the file skeleton, and the slot-linking convention used in module READMEs.

## Index

_Add units here as they're documented. Group by function — the categories below are starters; add more as needed._

### Flight instruments
- _e.g._ `adi-collins-329b-8g` — Attitude Director Indicator

### Navigation
- _e.g._ `rmi-collins-331a-9g` — Radio Magnetic Indicator
- _e.g._ `civa-cdu-...` — CIVA INS Control Display Unit

### Communication

### Engine instruments

### Aircraft systems
