# Pinouts — BF Goodrich FQIS 10106-03

Connector pinout and signal definitions for the benchtop fuel quantity indicator. See [`README.md`](README.md) for unit identification and the benchtop-vs-installed caveat.

> [!NOTE]
> These pin assignments are corroborated by the **747 WDM** fuel quantity indicating pages (ATA 28-41-11) — see the wiring excerpts in `schematics/wdm/`. The ARINC pairs are labeled **FQPU input** in the WDM (the gauge is fed by the Fuel Quantity Processor Unit). Pins left blank below are unverified, not confirmed-unused.

## WDM wiring references

- `schematics/wdm/ctr-wing-tank-gauge-strapping.png` — WDM 28-41-11 wiring for the center-wing-tank indicator (N9603, connector ON9603): the ID strap wires (Q9017–Q9021) and both FQPU ARINC pairs.
- `schematics/wdm/fuel-gauge-wiring.png` — WDM wiring at the P4 flight engineer's panel showing how the fuel indicators, the N9607 fuel quantity totalizer, the gauge-test switch, and the S9600 gross-weight-select switch share the FQPU ARINC lines.

## Connector

24-pin connector. The R/W/D column records the signal direction **relative to the gauge**:

- **R** — input the gauge reads
- **W** — strapping/reference common the gauge presents for external wiring (write)
- **D** — output the gauge drives _(none identified yet)_

| Pin | Function | Signal | R/W/D | Notes |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 | FQPU secondary input | ARINC 429 B | R | from Fuel Quantity Processor Unit |
| 5 | FQPU secondary input | ARINC 429 A | R | from Fuel Quantity Processor Unit |
| 6 | ID A | 0/1 (X2/X1) | R | tank-index strap bit (MSB) |
| 7 | ID B | 0/1 (X2/X1) | R | tank-index strap bit |
| 8 | ID C | 0/1 (X2/X1) | R | tank-index strap bit |
| 9 |  |  |  |  |
| 10 | shield | gnd | R |  |
| 11 | chassis ground | gnd | R |  |
| 12 | chassis ground | gnd | R |  |
| 13 | shield | gnd | R |  |
| 14 | ID X1 | TODO: measure V | W | strap common = logic **1** |
| 15 | ID D | 0/1 (X2/X1) | R | tank-index strap bit (LSB) |
| 16 | ID X2 | gnd | W | strap common = logic **0** |
| 17 | FQPU primary input | ARINC 429 B | R | from Fuel Quantity Processor Unit |
| 18 | FQPU primary input | ARINC 429 A | R | from Fuel Quantity Processor Unit |
| 19 | DC ground | gnd | R |  |
| 20 | DC power | 28 VDC | R | from **28 V DC ground-handling bus** (ATA 28-41-11) |
| 21 | Lighting | 5 VAC  | R | Rectified and ADC converts to display brightness |
| 22 | Lighting | 5 VAC | R |  |
| 23 | DC ground | gnd | R |  |
| 24 | DC power | 28 VDC | R | from **28 V DC essential bus** (ATA 28-41-14) |

## Tank ID strapping — decoded

Pins 6, 7, 8, 15 (ID A/B/C/D) encode which tank this gauge represents. Each ID pin is strapped to one of the two commons: **X2 (pin 16) = logic 0**, **X1 (pin 14) = logic 1**. The four bits `[A B C D]` (MSB→LSB) form a sequential tank index. Decoded from WDM 28-41-11 pg 14 (`schematics/wdm/ctr-wing-tank-gauge-strapping.png`):

| ID A B C D | Index | Tank |
|---|---|---|
| 0 0 0 0 | 0 | **Center wing (CTR)** — our DUT |
| 0 0 0 1 | 1 | Main 4 |
| 0 0 1 0 | 2 | Main 3 |
| 0 0 1 1 | 3 | Main 2 |
| 0 1 0 0 | 4 | Main 1 |
| 0 1 0 1 | 5 | Reserve 4 |
| 0 1 1 0 | 6 | Reserve 3 |
| 0 1 1 1 | 7 | Reserve 2 |
| 1 0 0 0 | 8 | Reserve 1 |

The center-wing DUT is index **0** — all four ID pins strapped to X2. The strap is the gauge's tank **self-ID** on the shared FQPU bus (all gauges sit on the same ARINC lines); it is *not* the units source and *not* the same as the ARINC SDI. The center gauge reads its quantity at **SDI 1** (see [`bench-test.md`](bench-test.md) and [`quirks.md`](quirks.md)).
