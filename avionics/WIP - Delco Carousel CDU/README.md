README for the Delco Carousel CDU

_________________________________
**OVERVIEW**

The Delco Carousel Control/Display Unit (CDU) is the cockpit-mounted operator interface for the Delco Carousel IV / IV-A inertial navigation system — commonly referred to as **CIVA** (Carousel IV-A). It's a 1970s-era avionics computer that lets the crew enter waypoints, monitor present position, and control the INS mode of operation. The CDU has no INS sensors of its own — it talks to a separate INS Mode Selector Unit (MSU) and the navigation computer over a 6-wire serial bus (ARINC 561), and renders/captures all crew interaction.

The CDU has three numeric displays (latitude, longitude, waypoint number), six annunciator lamps (ALERT, INSERT, HOLD, REMOTE, BAT, WARN), a numeric keypad with combo-key special functions, a waypoint thumbwheel, and a mode selector knob.

_________________________________
**VARIATIONS**

The Carousel family includes:

- **Carousel IV** — the original generation
- **Carousel IV-A (CIVA)** — the most common refit; the variant most surviving units in collector / restoration use today are
- **Carousel IVE** and other later derivatives — less common in commercial service

Within CIVA itself, captain-side and first-officer-side units may differ in mounting hardware and dimming bus only; the electrical interface is the same.

Part numbers vary by manufacturer batch and refit. Verify against the unit's nameplate.

| Field | Value |
|---|---|
| Type | Control / Display Unit (CDU) for Carousel IV-A INS |
| Manufacturer | Delco Electronics |
| Part number | _TBD — read from unit nameplate_ |
| Common names | CIVA CDU, Carousel CDU, Carousel IV CDU |
| Era | Mid 1970s onward; many units still in service through 1990s |

_________________________________
**APPLICABILITY**

Used in many wide-body and long-range jets of the 1970s–1980s era. Within Jurassic Jets:

- **B747-300 JA8179** — three units installed: two on P8 (aft pedestal) and one on P9 (flight engineer's panel). _(Slot links to be added once panel/module READMEs are scaffolded.)_

Outside our scope, the same CDU appears in 707-300, 727, early 737, DC-8, DC-10, L-1011, and the wide-body Airbus A300/A310 generation.

_________________________________
**DEPENDENCIES AND INTEGRATIONS**

The CDU is part of a multi-LRU INS system. On its own it does nothing — it must be wired into:

- **+28 VDC primary bus** for power.
- **ARINC 561 6-wire serial bus** (TX from navigation computer → CDU, RX from CDU → navigation computer). Three twisted shielded pairs each direction: CLK, SYNC, DATA.
- **Mode Select Unit (MSU)** — a separate panel (typically overhead) that carries the BAT-LOW and READY-NAV indications and the OFF / STBY / ALIGN / NAV / ATT mode rotary. The CDU's BAT and WARN lamps are independent of the MSU lamps.
- **Battery / Backup power** — the CIVA system has a battery-backed alignment so a brief AC power loss doesn't lose the alignment. The CDU's BAT lamp annunciates this state.

Discrete inputs and outputs:

- **BAT lamp** — driven by a discrete 28 VDC sink/source. Lights when the INS is running on backup battery.
- **WARN lamp** — discrete; system-level master warning for the INS.

The CDU does **not** consume sensor data directly (no synchros, no DC analog inputs from heading/airspeed). All interaction is via ARINC 561 serial.

_________________________________
**OPERATION AND FUNCTION**

**Displays:**

- **Left display (8 chars)** — latitude (`DDD MM.MM N` or `S`).
- **Right display (9 chars)** — longitude (`DDD MM.MM W` or `E`). Note: in CIVA's sign convention, **West is the "positive" hemisphere** for longitude (opposite the X-Plane / IRS / GPS convention).
- **Waypoint display (4 chars)** — selected waypoint identifier and digit field.

**Controls:**

- **Numeric keypad** — digits 0–9, plus combination keys: pressing two number keys simultaneously OR's their BCD codes into a single transmitted nibble. Bench-confirmed combos: `3+9` (BCD `1011` = 0xB), `7+9` (BCD `1111` = 0xF). Other out-of-range nibbles (0xA, 0xC, 0xD, 0xE) are reserved for combos not yet observed.
- **Waypoint thumbwheel** — selects waypoint 0–15 (4-bit BCD).
- **Mode selector** — 8-position rotary (3-bit code, values 0–7).
- **WPT CHG / INSERT / CLEAR / DATA SEL** — momentary buttons whose bit positions in the RX word are partly mapped (see RX format reference) and partly still TBD from bench captures.

**Annunciator lamps:**

- **ALERT** (driven by ARINC, bit 31 of the WP/Lights word, label 0x80)
- **INSERT** (bit 21)
- **HOLD** (bit 20)
- **REMOTE** (bit 17)
- **BAT** (driven by discrete signal, NOT carried over ARINC)
- **WARN** (driven by discrete signal, NOT carried over ARINC)

**Communication:**

- **ARINC 561 TX side (computer → CDU)** uses three labels:
  - `0x20` — latitude word (BCD lat + sign flags)
  - `0x40` — longitude word (BCD lon + sign flags)
  - `0x80` — waypoint number + lamp flags
- **ARINC 561 RX side (CDU → computer)** transmits 32-bit state words on panel events (button presses, dial / mode changes) and as a steady-state keepalive. The CDU output **is** spec ARINC 561 compliant: proper 8-bit label phase, 1-bit inter-phase gap, 24-bit data phase. Multiple distinct labels appear on the RX side, each with its own data-field semantics:

  | RX label | Meaning |
  |---|---|
  | `0x80` | panel keepalive / state register — number keys, dial, mode, AUTO/MAN, HOLD, REMOTE, WPT CHG (the bit layout in the data field is documented in `civa_panel_integration.md`). Steady-state value is sent ~every second; transient values appear when a button or dial state changes. |
  | `0x40` | INSERT pressed after a longitude entry — bench-confirmed 2026-05-05 (`0x92365740` observed during a non-wptchg lon insert). |
  | `0x20` | INSERT pressed after a latitude entry — inferred from the `civa_panel.py` symmetry with `0x40`; not yet bench-confirmed. |
  | `0xC0` | observed firing alongside `0x40` during a normal lon INSERT (data field `0xf00632c0` matched the post-INSERT `0x80` transient `0xf0063280` exactly, only the label byte differing). Specific meaning unknown — a comment in LukTronics' `civa_panel.py` claims "INSERT during a waypoint-change session," but that claim is unsourced (not in CIVA.ino, jjCIVA.ino, or Rob Archer's bit-register notes) and is contradicted by the bench observation that it fires outside a wptchg session. See OPEN QUESTIONS. |

  A wildcard label-`0xFF` configuration on the RX channel catches every label code in one logic-block variable, which is the practical way to handle the multi-label dispatch — the host then reads the label byte from bits 0–7 and routes per the table above.

_________________________________
**QUIRKS**

The Carousel CDU predates ARINC 419's formal sign-matrix codification, and its designers took several non-standard choices that surprise anyone expecting strict spec behavior. These are intrinsic to the unit and need to be handled at the driver level:

1. **Sign bits are independent flags, not the ARINC 419 sign matrix.** On the TX side, bit 30 carries N-or-W and bit 31 carries S-or-E, set independently. The standard ARINC 419 §2.1.5 2-bit matrix (00=N/E, 11=S/W) does not apply.
2. **TX framing has no inter-phase gap.** Going from label phase to data phase, SYNC stays HIGH continuously from label bit 0 through data bit 23. The CDU's input decoder counts clock edges instead of looking for a SYNC-LOW gap. (RX side, by contrast, **is** spec-compliant with the inter-phase gap.)
3. **Continuous CLK required during inter-burst gaps.** The CDU's input decoder uses the incoming CLK as its internal scan-state clock. With spec-gated CLK (CLK quiet between bursts), the panel appears unresponsive — keypresses don't update for ~1 s. CLK must keep toggling at 11.111 kHz during the inter-burst gap (with SYNC LOW) for the panel to stay alive.
4. **Longitude positive direction is West.** Opposite the X-Plane / GPS / IRS convention. Driver code must invert sign before computing the bit-30/31 flags.
5. **Multi-key keypad combos via bitwise OR.** The keypad has no separate scan codes for combo keys — it OR's the BCD codes of any keys pressed simultaneously and reports the result in bits 22–25 of the RX word. Decoding is straightforward: 0–9 = single digit; 0xB = "3+9"; 0xF = "7+9"; other out-of-range values reserved for future combos.
6. **Trim-to-terminator gotcha for display strings.** Source datarefs (e.g. Philipp Münzel's CIVA plugin) emit fixed-width buffers padded with NUL. Driver code must trim trailing NUL / space before BCD-packing or the panel's rightmost display position blanks out.
7. **TX uses bits 0–7 as a register-select ID, not a real ARINC label.** `0x20` selects the lat register, `0x40` lon, `0x80` WP/Lights. These are wire-format-compatible with ARINC 561 framing but are not entries in the ARINC 561 label-code registry. (Again: this is TX-only. RX-side labels **are** real.)
8. **The same label byte means different things on TX vs RX.** `0x20` and `0x40` are the obvious cases: on TX they mean "here's the latitude/longitude to display," on RX they mean "the operator just committed a latitude/longitude entry by pressing INSERT." A driver must dispatch on direction first, then on label byte. The TX register-select scheme (quirk #7) and the RX event-label scheme are separate naming spaces that happen to overlap on these byte values.

_________________________________
**BENCH STATUS**

Status: **bench-tested**

Initial bench characterization was completed in May 2026 against a real Delco CIVA CDU on the Aviologic kOutputBoard / kInputBoard pair. Bench captures confirmed RX framing is spec ARINC 561 compliant; TX framing is non-standard per the quirks above. See [`bench-test.md`](bench-test.md) for the test setup, equipment, and lab log.

_________________________________
**REFERENCES**

- **`civa_panel_integration.md`** — companion integration spec in the LukTronics Aviologic project at `~/Documents/LukTronics/aviologic/docs/civa_panel_integration.md`. Contains the full TX/RX format reference, troubleshooting guide, and software-side decoding implementation notes.
- **`arinc561_design.md`** — same project, signal-level design (pull-up sizing, pin allocation, rise-time analysis) at `~/Documents/LukTronics/aviologic/docs/arinc561_design.md`.
- **CIVA.ino** (Rob Archer) — canonical Teensy reference firmware, `~/Documents/Jurassic Jets/Document Repositories/747documents/Avionics/CIVA/From Rob Archer/CIVA/CIVA.ino`.
- **jjCIVA.ino** (Jurassic Jets) — simplified Teensy variant, `~/Documents/Jurassic Jets/Document Repositories/747documents/Coding Repositories/747coding/Teensy Code/jjCIVA/jjCIVA.ino`.
- **ARINC Characteristic 561-11** §5.0 (Basic Digital Signal Standards).
- **ARINC Specification 419-3** §2.0 (MELT classification of digital systems).
- **Philipp Münzel's CIVA INS plugin for X-Plane** — `de/philippmuenzel/xciva` dataref family.

_________________________________
**OPEN QUESTIONS**

Things we don't know yet, or where bench observations and source documentation disagree:

- **Meaning of label `0xC0` on RX.** Bench-observed firing alongside a `0x40` during a regular (non-wptchg) lon INSERT, with the data field exactly matching the post-INSERT `0x80` transient. Two reasonable hypotheses:
    - Bitwise-composed register-select code (`0xC0 == 0x80 | 0x40`) meaning "post-INSERT panel-state echo with the lon register flagged as just-committed" — i.e., a state-register repeat with a hint about which register triggered the event.
    - A dedicated handshake / acknowledgement event whose meaning is independent of the register that triggered it.

  To distinguish, capture INSERT in five contexts on a controlled bench session and tabulate the labels and data fields that result: POS-mode lat INSERT, POS-mode lon INSERT, WAYPT-mode lat INSERT, WAYPT-mode lon INSERT, and a real waypoint-change session INSERT. The pattern across these five should determine which hypothesis is correct (or surface a third).

- **Full RX label-to-event mapping.** We've now observed `0x80` (panel keepalive / state register), `0x40` (lon-insert), and `0xC0` (unknown). Per `civa_panel.py` symmetry, `0x20` is expected for lat-insert but not yet bench-confirmed. Whether other event categories (CLEAR, DATA-SELECTOR pushes, mode rotation past particular detents) emit further dedicated labels is open. Run an extended bench session covering every panel input and log the label distribution.

- **DATA-SELECTOR button bit positions on the RX `0x80` panel-state word.** Rob Archer's `Data Bit Registers for Civa.txt` shows TK-GS, HDG-DA, XTK-TKE, POS, WAYPT, DIS-TIME, WIND, DSRTKSTS distinguishing in the bits 8–12 area when MODE_SEL=9, but exact bit-to-button assignments aren't enumerated. VCD-capture each data-selector press to map them.

- **Bit 12 on the RX `0x80` word.** Marked `???` in Rob Archer's reference; never decoded by `jjCIVA.ino`. Possibly an INSERT-active flag distinct from WPT CHG (bit 21), or part of the data-selector field above.

- **Out-of-range BCD combo nibbles** (`0xA`, `0xC`, `0xD`, `0xE`) on the keypad-press field (bits 22–25) — currently unmapped; identify which physical key combinations produce them.

- **Carousel IV vs IV-A interface differences.** Whether the original Carousel IV uses the same 6-wire ARINC 561 or an earlier 12-wire variant. Verify if a Carousel IV unit becomes available.

- **Manufacturer part number ranges across refit batches.** Catalog actual P/Ns and dash variants observed in our airframes vs. what's documented in the AMM.
