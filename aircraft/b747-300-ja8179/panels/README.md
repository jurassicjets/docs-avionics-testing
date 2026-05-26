# Panels — JA8179

Cockpit panels for the 747-300, JA8179, named with Boeing P-designators per the WDM/AMM. Each panel folder contains modules; each module's `README.md` is the leaf — it lists install slots, each linking out to the corresponding unit doc in [`/avionics/`](../../../avionics/).

For an annotated cockpit overview with panel locations, see [`../cockpit-map.md`](../cockpit-map.md). For the structural conventions (folder/file naming, slot tables, when to promote a slot to its own file), see the repo-level [`CONTRIBUTING.md`](../../../CONTRIBUTING.md).

## Index

_Add panels here as they're created. Don't pre-scaffold empty panels — create the folder when you have a module or slot to put in it._

| P-# | Panel folder | Description | Status |
|---|---|---|---|
| P1 | [p1-captains-panel](p1-captains-panel/README.md) | captain's main instrument panel | _stubbed / in progress / documented_ |
| P3 | [p3-first-officers-panel](p3-first-officers-panel/README.md) | first officer's main instrument panel | |
| P4 | [p4-flight-engineers-panel](p4-flight-engineers-panel/README.md) | flight engineer's panel — fuel (m154), plus 1 of 3 CIVA CDUs | in progress |
| P8 | [p8-aft-pedestal](p8-aft-pedestal/README.md) | aft electronic control panel (2 of 3 CIVA CDUs) | |

P-designators and additional panels (P2, P5, P7, P10, side panels) — see [`../cockpit-map.md`](../cockpit-map.md). Some assignments need WDM verification before they're treated as authoritative.
