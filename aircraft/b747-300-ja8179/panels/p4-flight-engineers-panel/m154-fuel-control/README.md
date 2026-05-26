# M154 — Fuel Control / Quantity Indicating

> _The fuel quantity indicating group on the flight engineer's panel: per-tank fuel gauges, the fuel quantity totalizer, the gross-weight-select switch, and the gauge-test function (747 WDM ATA 28-41)._

Module within [`p4-flight-engineers-panel`](../README.md).

This README is the **leaf** of the panel tree — there are no subfolders for individual instruments. Each install slot is a row in the slot table below, linking to the unit's intrinsic doc in [`/avionics/`](../../../../../avionics/).

## Function

Displays fuel quantity per tank and aggregate (totalized) fuel load to the flight engineer. Each tank has its own digital fuel quantity indicator fed by the Fuel Quantity Processor Unit (FQPU) over ARINC 429; the gauges share the FQPU bus and select their own data by tank-ID strap and ARINC SDI. The totalizer sums tank quantities, and the gross-weight-select switch drives a gross-weight readout.

## Slots

Each fuel quantity indicator is the **same BF Goodrich digital FQIS family**, differentiated only by its ID strap (tank index) and ARINC SDI. Only the center-wing gauge has been bench-characterized so far (it is our DUT); the other tank gauges are documented against the same unit folder pending dataplate confirmation of their dash numbers.

| Slot | Position | Unit | Sources | Notes |
|---|---|---|---|---|
| ctr-wing-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU primary + secondary ARINC 429 | strap index 0 (CTR); reads at SDI 2. Bench DUT |
| main-1-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 4; dash/PN to confirm |
| main-2-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 3; dash/PN to confirm |
| main-3-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 2; dash/PN to confirm |
| main-4-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 1; dash/PN to confirm |
| reserve-1-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 8; dash/PN to confirm |
| reserve-2-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 7; dash/PN to confirm |
| reserve-3-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 6; dash/PN to confirm |
| reserve-4-tank-gauge | fuel indicators | [fqis-bfgoodrich-10106-03](../../../../../avionics/fqis-bfgoodrich-10106-03/) | FQPU ARINC 429 | strap index 5; dash/PN to confirm |
| fuel-quantity-totalizer | fuel panel | _not yet documented_ | FQPU ARINC 429 | WDM equipment N9607 (ATA 28-41-14) |
| gross-weight-select | fuel panel | _not yet documented_ | discrete to totalizer | WDM equipment S9600; 5 V DC + CH A/B select lines |

Tank-index → tank mapping and strap encoding are in the unit's [`pinouts.md`](../../../../../avionics/fqis-bfgoodrich-10106-03/pinouts.md).

## Module-level interconnects

All fuel quantity indicators and the totalizer sit on the **shared FQPU ARINC 429 bus** (primary pair + secondary pair). Each gauge picks out its own tank by ID strap and listens on its installation SDI. A panel **gauge-test** switch (WDM connector DM154B) is wired across the indicators to drive the `888.8` lamp/segment test. The **gross-weight-select** switch feeds the totalizer with 5 V DC and channel-A/B select discretes.

## Wiring reference

- [`wdm-28-41-11-14a-b1828.pdf`](wdm-28-41-11-14a-b1828.pdf) — 747 WDM page 28-41-11-14A (effectivity B1828) for JA8179, fuel indicators / totalizer / gauge-test / gross-weight-select wiring on this panel.

> [!NOTE]
> The strap-to-tank index mapping above is decoded from the generic WDM 28-41-11 strap scheme. The per-slot strap wiring for *this* airframe should be confirmed against the PDF above before being treated as production-validated.
