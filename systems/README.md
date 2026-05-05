# Systems

Cross-cutting topics that span multiple instruments — buses, protocols, power distribution, signal types. If a topic is intrinsic to *how* a class of instruments communicates rather than to any one instrument, it lives here. Each topic folder also holds the **generic test methods** for that bus or signal type — how to sniff it, drive it, excite it on the bench — alongside the reference for what it is.

## What goes here

- **Digital buses** — ARINC 429, ARINC 561, ARINC 568, ARINC 615.
- **Analog signal types** — synchros, resolvers, AC ratiometric inputs, DC analog.
- **Power** — 28 VDC distribution, 115 VAC / 400 Hz, 26 VAC reference, emergency bus topology.
- **Audio** — interphone, hot-mic conventions, sidetone.
- **Discretes** — open/ground signaling conventions, lamp drivers, weight-on-wheels logic.

Each topic folder typically contains:

- `README.md` — what the system *is*: mechanics, conventions, reference.
- `test-methods.md` — how to sniff, drive, or characterize it from the bench (applies to any unit using this signal type).
- Supporting files (label tables, fixture notes, captures) as needed.

## What doesn't go here

Instrument-specific behavior — even if it involves one of these systems — goes in `avionics/<unit>/`. Use this directory for the *general* protocol or signal-type reference (and the *general* test methods), then link to it from individual unit docs.

## Index

_Add system topics here as they're created._

Suggested starter topics, in rough priority order:

- `arinc-429/` — bus mechanics, label structure, common labels, sniffing/driving methods.
- `synchros/` — 3-wire synchro signals, 26 VAC reference, common excitation schemes, bench excitation methods.
- `28-vdc/` — typical aircraft DC distribution and protection.
- `400hz-ac/` — aircraft AC power, why 400 Hz, transformer behavior.
