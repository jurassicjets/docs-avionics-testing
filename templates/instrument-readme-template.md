# <Type> — <Manufacturer> <Part Number>

> **Status:** acquired | bench-tested | documented | production-validated
>
> _One-line description of what this LRU is and what it does._

This is the canonical doc for the unit. It describes what the box *is* — pinouts, signal behavior, bench observations, quirks. Where it's *installed* is documented in each aircraft's panel/module READMEs that link to this folder.

Use this template when creating `avionics/<type>-<manufacturer>-<partnumber>/README.md`.

## Identification

| Field | Value |
|---|---|
| Type | e.g., Radio Magnetic Indicator (RMI) |
| Manufacturer | e.g., Collins |
| Part number | e.g., 331A-9G |
| Dash variants | List any cosmetically-different dash numbers covered by this folder |
| Common names | Names by which crews/mechanics refer to it |
| Era | Approximate years of production / service |

## Function

What this unit does in the cockpit, in two or three sentences. What information does it display or process? What does the crew do with it?

## Power and connector

| Field | Value |
|---|---|
| Primary power | e.g., 28 VDC, ~0.5 A |
| Reference power | e.g., 26 VAC 400 Hz for synchro reference |
| Lighting | e.g., 5 VAC dimming bus |
| Connector | Manufacturer/series, pin count |

## Signal interfaces

Brief summary of inputs and outputs. Detail belongs in [`pinouts.md`](pinouts.md).

- **Inputs:** e.g., synchro heading from compass system, VOR bearing from NAV receiver
- **Outputs:** none / discrete flags / etc.

## Installed in

Every install slot across our airframes that carries this unit. Each entry links to the module README that documents the slot.

- **B747-300 JA8179**
  - [P1 / flight-instruments / captains-rmi](../../aircraft/b747-300-ja8179/panels/p1-captains-panel/flight-instruments/README.md)
  - [P3 / flight-instruments / first-officers-rmi](../../aircraft/b747-300-ja8179/panels/p3-first-officers-panel/flight-instruments/README.md)

If this unit is known to appear in airframes outside our current scope (per manuals, IPC entries), list them as references rather than links.

## Documents in this folder

- [`pinouts.md`](pinouts.md) — connector pinouts and signal definitions.
- [`bench-test.md`](bench-test.md) — what we did at the bench, what we observed.
- [`quirks.md`](quirks.md) — undocumented behavior, gotchas, failure modes.
- `photos/` — photos of the unit.
- `captures/` — scope traces, logic-analyzer dumps.
- `datasheets/` — manufacturer datasheets, CMM excerpts, IPC pages.

## Sources

Where this information came from. Cite manufacturer documents by part number and revision, and note where the document lives (in `datasheets/`, an external archive, etc.).

- e.g., Collins CMM 34-25-37, Rev 8 (in `datasheets/`)
- e.g., Bench observations, 2026-04 (see `bench-test.md`)

## Open questions

Things we don't know yet, or where bench observations and documentation disagree. Future contributors should look here first.

- _e.g., Pin 14 reads ~0.7 V on power-up but isn't called out in the CMM. Possibly a test point._
