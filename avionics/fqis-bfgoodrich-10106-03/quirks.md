# Quirks — BF Goodrich FQIS 10106-03

Undocumented behavior, gotchas, and failure modes. Bench observations are marked as such; manufacturer-documented behavior is cited where we have it.

## `-A.b` is a bus-communication fault code, not "no data"

**The display reads `-A.b`** (earlier bench notes recorded this as "A.6" — a misread of the alphanumeric segments). Per AMM 28-41-03 indicator self-test / Fig 502 display states:

- `-A` = ARINC **Bus A** failed, `-b` = **Bus B** failed, `-A.b` = **both buses** failed.
- A fault on *either* bus blanks the quantity. The gauge requires **both Bus A and Bus B communicating continuously** to show a number.
- Fig 502 states: A = normal (qty), B = ARINC bus B fault, C = ID input fault, D = test (`888.8`), E = blanked.
- Fault isolation for `-A`/`-b`/`-Ab` points at the **ARINC wiring from the processor to the indicator** — it's treated as a bus/comm/signal problem, not a bad data value.

So a `-A.b` does **not** mean the gauge rejected your quantity value — it means it judged the bus(es) not communicating and never looked at the value. Bus A = primary pair (pins 18/17), Bus B = secondary pair (pins 5/4).

## "Receiving valid words" ≠ "bus communicating" (the comm-health gate)

**Bench finding (2026-05-24):** the gauge demonstrably decodes a synthetic bus live — relabeling the SDI 2 units word `343`→`333` flips the display LB↔KG in real time with no power-cycle — yet it **still shows `-A.b`** in every configuration tried (dual-bus, single-bus, gap-free firmware-paced TX, clean status words, test values). A single-bus test is the clincher: Bus A is provably received (units update live) but still flagged `-A`.

Conclusion: the units logic reads the wire directly, but the **quantity-validity gate runs a separate, stricter per-bus comm-health check** that needs specific content the configured FQPU emits and we have not been able to derive (not cadence, not pacing, not dual-bus, not SSM/status, not value — all ruled out). The exact criterion is BF Goodrich-internal and unknown without the ICD/CMM. This is the open blocker — see [`bench-test.md`](bench-test.md) and the README's Open questions.

## Gauge reads the bus live — no power-cycle latching

An earlier note claimed the gauge latches its display at power-up and only re-reads on a power cycle. **That is false (corrected 2026-05-24):** the gauge re-evaluates the bus continuously — live relabeling flips units immediately. No power-cycle is needed between bench tests.

## Installation address is SDI 2 (for the center tank), independent of the strap

The center-wing DUT responds to its quantity/units words at **SDI 2** specifically (SDI 0/1/3 are inert for it; SDI 0 is all-call). The ARINC SDI is set by the installation, and is **not** the same thing as the ID strap value — the strap is the gauge's tank self-ID, the SDI is which sub-channel on the shared bus it listens to. Quantity sent at the wrong SDI is simply ignored.

## Tank identity is set by hardware strapping, not configuration

The gauge has no software tank selection — which tank it represents is determined entirely by the ID strapping pins (ID A/B/C/D against commons X1 = logic 1 / X2 = logic 0), forming a 4-bit tank index (decoded table in [`pinouts.md`](pinouts.md)). A gauge behaves as whatever tank its connector is strapped for, so a unit swapped between positions takes on the new position's identity from the wiring, not from anything stored in the unit. Strap deliberately and verify before powering up.

## Benchtop unit may not match installed units

The benchtop unit is part number 10106-03. Units installed in the aircraft may be a different dash number — similar but not guaranteed identical. Don't assume a pinout or behavior detail observed here holds for an installed gauge without checking the dataplate. See the note at the top of [`README.md`](README.md).
