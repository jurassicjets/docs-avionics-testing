# Fuel Quantity Indicator (FQIS) — BF Goodrich 10106-03

> **Status:** bench-tested
>
> _Digital fuel quantity indicator from a Boeing 747 fuel quantity indicating system. Reads tank quantity over ARINC 429 and drives a digital readout; identifies which tank it serves via hard-wired ID strapping pins._

This is the canonical doc for the unit. It describes what the box *is* — pinouts, signal behavior, bench observations, quirks. Where it's *installed* is documented in each aircraft's panel/module README that links to this folder.

> [!NOTE]
> This folder documents the **benchtop unit, part number 10106-03**. The gauges installed in our airframe may carry a different dash number; they should be very similar but not necessarily identical. Confirm the dataplate part number against this doc before treating any pinout or behavior detail as authoritative for an installed unit.

## Identification

| Field | Value |
|---|---|
| Type | Fuel Quantity Indicator (FQIS) |
| Manufacturer | BF Goodrich |
| Part number | 10106-03 _(benchtop unit; installed units may differ — see note above)_ |
| WDM equipment no. | N9603 — "IND-CTR WNG TANK FUEL QUANTITY" (connector ON9603) |
| Dash variants | Unknown — aircraft units suspected to be a different dash of the same design |
| Common names | Fuel gauge, fuel quantity indicator |
| Era | 747-classic generation _(TODO: confirm production years)_ |

## Function

Displays the fuel quantity for one tank on a two-line digital readout: top line = quantity (LB ×1000, format `XX.X`), bottom line blank for a single-tank install. The gauge receives quantity and mode data over ARINC 429 from the **Fuel Quantity Processor Unit (FQPU)** and presents it. Display units (LB vs KG) are **bus-driven** — set live by the FQPU's units command word, not by strapping.

Per-tank identity *is* set by hard-wired ID strapping pins on the connector (not software config), so the same part can serve any tank position depending on how its ID pins are strapped — see the decoded strap table in [`pinouts.md`](pinouts.md). The benchtop unit is strapped as the **center wing tank** (index 0).

## Power and connector

| Field | Value |
|---|---|
| Primary power | 28 VDC (pins 20, 24; grounds on 11, 12, 19, 23) |
| Reference power | None observed |
| Lighting | Unknown _(TODO: identify dimming bus, if any)_ |
| Connector | 24-pin connector (positions labeled J1–J4 on the unit; pin map in [`pinouts.md`](pinouts.md)) |

## Signal interfaces

Brief summary of inputs and outputs. Detail belongs in [`pinouts.md`](pinouts.md).

- **Inputs (both ARINC 429, sourced from the FQPU):**
  - **Primary** receive pair (pins 18 A / 17 B) — the gauge's **Bus A**
  - **Secondary** receive pair (pins 5 A / 4 B) — the gauge's **Bus B**
  - **Tank ID strapping** — discrete ID bits A/B/C/D (pins 6, 7, 8, 15) strapped to commons X1 (pin 14 = logic 1) and X2 (pin 16 = logic 0) to form a tank index. See [`pinouts.md`](pinouts.md).
- **Outputs:** None confirmed — the gauge appears to be receive-only on ARINC 429.

> [!IMPORTANT]
> The gauge requires **both Bus A and Bus B communicating continuously** to display a quantity. A fault on either bus blanks the number and shows the bus-fault code (see [`quirks.md`](quirks.md)). The two buses are the primary (18/17) and secondary (5/4) FQPU pairs.

For ARINC 429 bus mechanics and generic sniffing/driving methods, see `systems/arinc-429/` _(topic not yet created — see [systems/README.md](../../systems/README.md))_.

## Dependencies and integrations

- **Fed by:** Fuel Quantity Processor Unit (**FQPU**, WDM equipment `M9600`) over the primary and secondary ARINC 429 pairs. The FQPU computes tank quantity from the tank probes and broadcasts it; all tank gauges share the same ARINC lines and pick out their own data by SDI / strap.
- **Shares the FQPU bus with:** the N9607 **fuel quantity totalizer** and the S9600 **gross-weight-select switch** (see `schematics/wdm/fuel-gauge-wiring.png`).
- A panel **gauge-test** switch is wired to the indicators (visible in the same WDM excerpt).

## Installed in

Serves the center-wing-tank position of the 747 fuel quantity indicating system (ATA 28-41) on **B747-300 JA8179**.

- **B747-300 JA8179** — [P4 flight engineer's panel / m154-fuel-control](../../aircraft/b747-300-ja8179/panels/p4-flight-engineers-panel/m154-fuel-control/README.md)

## Documents in this folder

- [`pinouts.md`](pinouts.md) — connector pinouts and signal definitions.
- [`bench-test.md`](bench-test.md) — what we did at the bench, what we observed.
- [`quirks.md`](quirks.md) — undocumented behavior, gotchas, failure modes.
- `datasheets/` — 747 WDM pages for the fuel quantity indicating system (ATA 28-21 / 28-41).
- `schematics/` — KiCad project for the ARINC 429 brute-force tester fixture used on the bench.
- `scripts/` — Arduino sketch for the ARINC 429 tester and a Python ARINC decoder with captured data.

## Sources

- 747 Wiring Diagram Manual pages, fuel quantity indicating system — `datasheets/747_WDM_PDF_28-21-11-*`, `28-41-11-*`, `28-41-12-*` (B1776).
- Bench observations, 2026-05 (see [`bench-test.md`](bench-test.md)).

## Open questions

Things we don't know yet, or where bench observations and documentation disagree. Future contributors should look here first.

- What part numbers / dash variants are actually installed in JA8179, and how do they differ from the benchtop 10106-03?
- **The comm-health gate.** The gauge shows `-A.b` (both-bus fault) and won't display a quantity even though it is provably decoding our synthetic bus live (relabeling the SDI 2 units word flips LB↔KG in real time). "Receiving valid ARINC words" is not the same as "bus communicating" to this gauge — it runs a stricter per-bus health check whose exact criterion (specific label/value/coherence the *configured* FQPU emits) we have not reproduced. This is the main blocker; see [`bench-test.md`](bench-test.md). Resolving it likely needs the FQIS ICD/CMM or a ground-truth capture from a configured FQPU.
- Which exact label(s)/encoding carry the center-tank quantity at SDI 2 (candidates `256`/`257` BNR), and what validity assertion accompanies them.
