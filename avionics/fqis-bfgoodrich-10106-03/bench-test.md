# Bench test — BF Goodrich FQIS 10106-03

What we've done at the bench with the benchtop fuel quantity indicator and what we observed. See [`README.md`](README.md) for the unit overview and [`pinouts.md`](pinouts.md) for the connector map.

## Equipment required

- 28 VDC bench supply (gauge primary power)
- ARINC 429 transmitter — here, an Arduino + line-driver circuit (the **ARINC 429 brute-force tester**, schematics in `schematics/arinc_429_brute_force_tester/`, firmware in `scripts/arinc_429_brute_force_tester/`)
- Jumpers for the tank ID strapping pins
- _(optional)_ ARINC 429 receiver/decoder for capturing any gauge output — see the Python decoder in `scripts/arinc_decoder/`

## Test setup

1. Apply 28 VDC to the power pins (20, 24) and ground (11, 12, 19, 23).
2. Strap the tank ID pins (6, 7, 8, 15) for the tank role under test to X1 (14) or X2 (16).  To emulate the **center wing tank** gauge, strap all ID config pins to X2 (16).
3. Drive the ARINC 429 **primary** receive pair (pin 18 A / pin 17 B) from the tester or secondary (pin 5 A / pin 4 B).

## Pin connections

| Gauge pin             | Connect to                                                   |
|-----------------------|--------------------------------------------------------------|
| 20, 24                | +28 VDC                                                      |
| 11, 12, 19, 23        | Power ground                                                 |
| 18 (A) / 17 (B)       | ARINC 429 primary from tester                                |
| 5 (A) / 4 (B)         | ARINC 429 secondary from tester _(optional)_                 |
| 6, 7, 8, 15 (ID A–D)  | Strapped per tank role (all to ground = center wing tank)    |
| 14 (X1) / 16 (X2)     | Strapping commons (gnd / 5 V)                                |

See [`pinouts.md`](pinouts.md) for the full connector map.

## Lab log

**2026-05-18** — Generated ARINC 429 signals with an Arduino and driver circuit. Swept all ARINC 429 labels with arbitrary data at the low-speed bit rate (~12.5 kHz) in an attempt to get a response. Saw **no activity** from the gauge — it continued to display the **`-A.b`** code throughout (recorded at the time as "A.6", later identified as a misread of the alphanumeric segments). Strapped all config pins to emulate the center wing tank gauge.

**2026-05-23 → 25** — Switched to an Aviologic ARINC-429 card to synthesize the bus and explored the gauge's behavior in detail. Established facts (read live via webcam):

- **`-A.b` decoded** (AMM 28-41-03 / Fig 502): it is an **ARINC bus-communication fault** — `-A` = Bus A failed, `-b` = Bus B failed, both = `-A.b`. The gauge needs both buses communicating continuously to show a quantity. It is *not* a data-value rejection. See [`quirks.md`](quirks.md).
- **Units are bus-driven.** Label `343` at SDI 2 = "display LB", `333` at SDI 2 = "display KG". Relabeling `343`→`333` flips the display LB↔KG **live**, proving the gauge actively decodes our bus and re-evaluates without a power-cycle.
- **Installation address = SDI 2** for the center tank (SDI 0/1/3 inert; SDI 0 = all-call).
- **Strap scheme decoded** from WDM 28-41-11 pg 14 (`schematics/wdm/ctr-wing-tank-gauge-strapping.png`): 4-bit tank index, `0000` = center tank (our DUT). See [`pinouts.md`](pinouts.md).
- **A/B polarity:** the card's TX A/B is swapped vs the gauge; the orientation that yields "LB lit, bottom blank" is the electrically-correct one (LB = proof of decode).

**The blocker (unresolved):** despite the gauge provably decoding the bus live (units flip), it holds `-A.b` and never displays a quantity — in *every* config tried: dual-bus, single-bus, gap-free firmware-paced TX, clean status words, in-range BNR/BCD quantities at SDI 2 (incl. candidates `256`/`257`), full replay of a captured FQPU test-state output, per-bit and per-label all-ones walks of the status/config words. Rate (1.4–52 Hz) is not the gate. The quantity gate runs a **separate, stricter comm-health check** beyond "valid words received" whose exact content criterion we cannot derive without the FQIS ICD/CMM.

> [!NOTE]
> Best remaining leads: (a) capture a **confirmed displaying moment** from a configured FQPU and mine those exact words; (b) search for a 4-bit ID-field-vs-strap match in the `256`/`257` SDI 2 quantity word; (c) obtain the BF Goodrich ICD/CMM. The deep reverse-engineering log lives outside this repo at `fuel-qty-processor-data/GAUGE_FINDINGS.md` on the bench machine.
