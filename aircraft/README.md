# Aircraft

Per-airframe install configuration. Each aircraft we work with gets a self-contained folder with its cockpit map, panel/module tree, and any airframe-specific system architecture docs. Unit-level documentation (pinouts, bench tests, quirks) lives in [`../avionics/`](../avionics/) and is referenced from the panel tree.

## Layout

```
aircraft/<aircraft>/
├── README.md                       overview, ID, status, navigation
├── cockpit-map.md                  panel locations, overview photos
├── panels/<panel>/<module>/        module README is the LEAF — slot table, links to ../../../../../avionics/<unit>/
├── systems/                        (optional) airframe-specific system architecture
└── photos/                         (optional) cockpit overview photos
```

`<module>/README.md` is the deepest folder in the panel tree. It lists the install slots in that module — each slot a row in a table, linking to the unit it carries in `avionics/`. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the slot-table convention.

## Naming convention

Aircraft folder names: lowercase, hyphenated. For airframes we have a specific tail in hand for, include the registration so install observations are unambiguously tied to the airframe they came from.

- `b747-300-ja8179` — Boeing 747-300, registration JA8179
- `b727-100` — Boeing 727-100 (no specific tail)
- `dc-9-30-n12345` — McDonnell Douglas DC-9-30, registration N12345

If a future aircraft of the same type/registration is added, distinguish them however makes sense (a suffix, a reorg into series subfolders) — but cross that bridge when it appears.

## Cross-aircraft instruments

When the same LRU appears in more than one of our aircraft, no duplication is needed: each aircraft's panel tree links to the same `avionics/<unit>/` folder, and the unit's "Installed in" list grows. See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for the full convention.

## Index

- [b747-300-ja8179](b747-300-ja8179/README.md) — Boeing 747-300, JA8179. _First aircraft on the bench._

_Add aircraft here as they're documented._
