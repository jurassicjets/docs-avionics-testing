# Fuel Quantity Indicator (FQIS) — BF Goodrich 10106-03

> **Status:** bench-tested
>
> _Digital fuel quantity indicator that displays fuel quantiy computed by FQIS in the equipment bay via shared redundant Arinc 429 buses; tank is identified via hard-wired ID strapping pins._

## Identification

| Field | Value |
|---|---|
| Type | Fuel Quantity Indicator  |
| Manufacturer | Simmonds / BF Goodrich |
| Part number | 10106-03 _(benchtop unit; installed units may differ — see note above)_ |
| WDM equipment no. | N9603 — "IND-CTR WNG TANK FUEL QUANTITY" (connector ON9603) |
| Dash variants | TODO: aircraft units suspected to be a different dash of the same design.  ALso believe this is used on the underwing fuel refeuling panel of 737 classics |
| Common names | Fuel gauge, fuel quantity indicator |
| Era | 747-classic generation _(TODO: confirm production years)_ |

> [!NOTE]
> This folder documents the **benchtop unit, part number 10106-03**. The gauges installed in our airframe may carry a different dash number; they should be very similar but not necessarily identical. Confirm the dataplate part number against this doc before treating any pinout or behavior detail as authoritative for an installed unit.

## Function

Displays the fuel quantity for one tank on a two-line digital readout: top line = quantity (BCD format `XXX.X` x 1000 lb or kg), bottom line blank for a single-tank install under normal operation. Between the two lines the unit (lb or kg) is displayed as well as x1000. The decimal point on both lines is always displayed at all times, even when blank. Display units (LB vs KG) are **bus-driven** based on the label used for the fuel quantity, not by strapping. [Units are specified via strapping on the FQPU].

Per-tank identity *is* set by hard-wired ID strapping pins on the connector (not software config), so the same part can serve any tank position depending on how its ID pins are strapped — see the decoded strap table in [`pinouts.md`](pinouts.md). The benchtop unit was tested with the convenient strapping of the **center wing tank**.

## Power and connector

| Field | Value |
|---|---|
| Primary power | 28 VDC redunantly supplied on pins 20 and 24; grounds on 11, 12, 19, 23 |
| Lighting | 5 VAC pins 21 and 22 |
| Connector | 24-pin canon plug J1; pin map in [`pinouts.md`](pinouts.md)) |

## Signal interfaces

Brief summary of inputs and outputs. Detail belongs in [`pinouts.md`](pinouts.md).

- **Inputs (both ARINC 429, sourced from the FQPU):**
  - **Primary** receive pair (pins 18 A / 17 B) — the gauge's **Bus A**
  - **Secondary** receive pair (pins 5 A / 4 B) — the gauge's **Bus B**
  - **Tank ID strapping** — discrete ID bits A/B/C/D (pins 6, 7, 8, 15) strapped to commons X1 (pin 14 = logic 1) and X2 (pin 16 = logic 0) to form a tank index. See [`pinouts.md`](pinouts.md).

  Driving either the primary or secondary bus is sufficient as they are redundant. (Sufficient at least for normal operation.)

- **Outputs:** None.

For ARINC 429 bus mechanics and generic sniffing/driving methods, see `systems/arinc-429/` _(topic not yet created — see [systems/README.md](../../systems/README.md))_.

## Dependencies and integrations

- **Fed by:** Fuel Quantity Processor Unit (**FQPU**, WDM equipment `M9600`) over the primary and secondary ARINC 429 pairs. The FQPU computes tank quantity from the tank probes and broadcasts it; all tank gauges share the same ARINC lines and pick out their own data by SDI / strap.
- **Shares the FQPU bus with:** the N9607 **fuel quantity totalizer** and the S9600 **gross-weight-select switch** (see `schematics/wdm/fuel-gauge-wiring.png`).
- A panel **gauge-test** switch is wired to the indicators (visible in the same WDM excerpt).

## Installed in

These gauges are installed in 747 classics as a retrofit both on the flight deck and fuel refueling panel under the wing.  Also installed in 737 under wing refueling panel.

**B747-300 JA8179** — [P4 flight engineer's panel / m154-fuel-control](../../aircraft/b747-300-ja8179/panels/p4-flight-engineers-panel/m154-fuel-control/README.md)

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

Things we don't know yet, or where bench observations and documentation disagree. Future contributors should tackle these first.

- What part numbers / dash variants are actually installed in JA8179, and how do they differ from the benchtop 10106-03?
- We know that if we send a bogus big number it will display ACC on the bottom line, but it should also be possible to display that when still giving a reading, but a potentially degraded reading. The FQPU monitors things like densitometer value and high-Z failures that are potentially degrading.
