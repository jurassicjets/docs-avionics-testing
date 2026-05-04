# Bench

Documentation for the test bench itself: the rig we use to power up and characterize avionics, the fixtures we've built, the equipment, and the standard procedures.

## What goes here

- **Equipment** — power supplies, signal generators, ARINC 429 bus analyzers, oscilloscopes, logic analyzers, multimeters. What we have, what each piece is rated for, where to find documentation.
- **Fixtures** — connector breakouts, mount adapters, harness builds. Photos, schematics, BOMs.
- **Procedures** — generic test procedures that apply to a class of units (e.g., "first-power-on procedure for a synchro-driven instrument", "ARINC 429 label sniffing"). Instrument-specific procedures live in the instrument's `bench-test.md`.
- **Safety** — high-voltage warnings, 400 Hz hazards, capacitor discharge, ESD.

## Suggested layout

```
bench/
├── README.md
├── equipment/         what's on the bench, with manuals/datasheets
├── fixtures/          breakouts, adapters, harnesses we've built
├── procedures/        reusable test procedures
└── safety.md          safety notes that apply to all bench work
```

## Index

_Add bench content here as it's created._
