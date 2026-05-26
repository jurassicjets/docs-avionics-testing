bench testing the Delco Carousel CDU

_________________________________
**EQUIPMENT REQUIRED**

* +28 VDC bench supply, ≥1 A (for primary CDU power and lamp commons)
* +12 VDC bench supply, ≥100 mA (for ARINC 561 TX pull-up rail)
* ARINC 561 driver — at least one of:
    - Aviologic kOutputBoard + kInputBoard pair (preferred — full TX + RX path, tested driver, see `civa_panel_integration.md` in the LukTronics docs)
    - Teensy 4.x running CIVA.ino (Rob Archer) or jjCIVA.ino (Jurassic Jets) for a standalone reference
    - Bit-banged GPIO from a microcontroller of choice if you want to exercise the protocol from scratch
* Logic analyser, ≥4 channel, ≥1 MHz sample rate (for capturing CLK/SYNC/DATA on both directions)
* Oscilloscope (optional but useful for checking signal levels and edge rates)
* 3 × twisted shielded pairs of wire (TX path: CLK, SYNC, DATA — each signal + return), ~6 ft
* 3 × signal lines + 1 × ground for the RX path
* CD4504BE or equivalent CMOS level shifter (12 V → 3.3 V) on the RX side, between CDU output and any modern logic input
* 3 × 4.7 kΩ ¼ W ±5 % pull-up resistors (TX path, to +12 V rail)
* 28 VDC indicator lamps × 2 (or representative loads, ~50–100 mA each) for the BAT and WARN lamp drives if testing those discretes
* DPDT or SPDT switch (optional, for manually exercising lamp drives)
* Multimeter

_________________________________
**TEST SETUP**

**Power.** Connect +28 VDC and ground per the [pinout](pinout.md). Tie the +28 VDC return, the +12 VDC pull-up rail return, and the ARINC driver's signal ground all to a common bench ground.

**TX path (driver → CDU).** Each of CLK, SYNC, DATA on the driver is wired through a 4.7 kΩ pull-up to the +12 VDC rail, then via a twisted shielded pair to the corresponding CDU input. The pair's return wire goes to the dedicated signal return pin on the CDU. With the driver's open-drain output idle, each line should idle HIGH at ≈12 V; when the driver pulls LOW, the line should snap to ≈0 V cleanly within the rise/fall time required for 11.111 kHz operation. Pull-up sizing math is in `arinc561_design.md` §"Pull-up resistor value" in the LukTronics docs.

**RX path (CDU → driver).** The CDU's three output lines (CLK, SYNC, DATA at ≈12 V) feed the CD4504BE level shifter, whose 3.3 V outputs go to the driver's CMOS inputs. Bond the CDU's signal-ground pin to the level shifter ground and to the driver's signal ground. The level shifter is required because the CDU's output swing is 0–12 V, well above modern 3.3 V CMOS input limits, and direct opto-coupling (e.g. LTV-247) is too slow for ARINC's 22 µs half-period at 11.111 kHz.

**Discretes.** Wire +28 VDC through each of the BAT and WARN lamp's "+" pins. Tie each lamp's "-" pin to the CDU's corresponding sink output. The CDU pulls the "-" side to ground to illuminate the lamp. If you don't have the lamps on hand, a simple 28 V indicator and series resistor stand-in works for verifying the sink output is functional.

**Bring-up checklist.**

1. With CDU powered off and ARINC driver disconnected, ohmmeter-check that each TX pin idles HIGH (≈12 V) when the driver's output is in its idle state. Verify each TX signal line pulls LOW correctly when the driver asserts.
2. Apply +28 VDC. CDU display segments may flash through a self-test pattern. Confirm display segments illuminate.
3. Apply ARINC TX. Send a single label `0x20` lat word with `37 45.00 N` and verify the left display reads `37 45.00 N`. If display reads correctly but with wrong sign or shifted digits, see quirks #1 and #6 in [`README.md`](README.md).
4. With panel idle, scope each TX line: confirm 11.111 kHz CLK, SYNC framing (HIGH during label + data phases, no gap), DATA bits MSB-first.
5. With CDU powered, manipulate the keypad and dial; on the logic analyser confirm the CDU emits properly framed ARINC 561 words on the RX side (label phase + 1-bit gap + data phase). The waypoint thumbwheel emits a frame on each detent click; the mode selector likewise.

_________________________________
**PIN CONNECTIONS**

_To be filled in after pinout numbers are verified from unit nameplate. Suggested table format follows the wiring breakdown above:_

| Pin | Function | Signal source / sink |
|--|--|--|
| TBD | +28 VDC primary | bench supply +28 V |
| TBD | power return | bench supply ground / common |
| TBD | TX CLK in | ARINC driver CLK output via 4.7 kΩ to +12 V |
| TBD | TX CLK return | driver signal ground |
| TBD | TX SYNC in | ARINC driver SYNC output via 4.7 kΩ to +12 V |
| TBD | TX SYNC return | driver signal ground |
| TBD | TX DATA in | ARINC driver DATA output via 4.7 kΩ to +12 V |
| TBD | TX DATA return | driver signal ground |
| TBD | RX CLK out | CD4504BE input → driver CMOS pin |
| TBD | RX SYNC out | CD4504BE input → driver CMOS pin |
| TBD | RX DATA out | CD4504BE input → driver CMOS pin |
| TBD | RX signal GND | level-shifter ground / driver signal ground |
| TBD | BAT lamp + | +28 VDC bus |
| TBD | BAT lamp - | through lamp to ground (CDU sinks to illuminate) |
| TBD | WARN lamp + | +28 VDC bus |
| TBD | WARN lamp - | through lamp to ground (CDU sinks to illuminate) |

_________________________________
_________________________________
**LAB LOG**

5/5/26 — Captured the post-INSERT label sequence on the ARINC 561 monitor in the Aviologic configurator while pressing INSERT after a longitude entry. Three frames in close succession (no waypoint-change session active):

* `t = ...11543`: label **`0x40`** with data field `0x923657` (full word `0x92365740`). This is the lon-INSERT event — confirms that the panel emits a dedicated label code per inserted register, not a bit position in the `0x80` lights word as we'd previously assumed.
* `t = ...11551` (+8 ms): label **`0x80`** with data field `0xf00632` (full word `0xf0063280`). This is the panel-state register transient — different from the steady-state `0xf0062080` by bits 9 and 12 set. Probably the panel signaling "INSERT now active" via the panel-state-register data field rather than a separate label.
* `t = ...11579` (+28 ms after the `0x40`): label **`0xC0`** with data field `0xf00632` (full word `0xf00632c0`). Data field is byte-identical to the `0x80` transient above — only the label byte differs. Steady-state `0x80` resumes shortly after.

Implications:

* INSERT presses come on dedicated label codes (`0x40` for lon, `0x20` for lat by symmetry — pending confirmation), NOT as a bit position in the `0x80` panel-state word. The README's "INSERT bit position is unknown" framing was wrong; updated.
* The `0xC0` frame is unexplained. The claim in `civa_panel.py` that `0xC0` means "INSERT during a waypoint-change session" is unsourced (not in CIVA.ino, jjCIVA.ino, or Rob Archer's `Data Bit Registers for Civa.txt`) and is contradicted by this capture (no wptchg session was active). Hypothesis to test next session: `0xC0 == 0x80 | 0x40`, meaning "post-INSERT panel-state echo with the lon-register-just-committed bit also set." Will distinguish via a focused capture session in five INSERT contexts (POS-mode lat, POS-mode lon, WAYPT-mode lat, WAYPT-mode lon, real wptchg INSERT).

Debugging note: despite `0x40` arriving cleanly and being routed to `_rx_handle_lon_insert` per `civa_panel.py:1041`, the Felis `but_INSERT` dataref is not being driven high. Expected pipeline `_rx_handle_lon_insert` → `_fire_but_insert_pulse` → `_df_but_INSERT.value = 1.0` is failing somewhere downstream of dispatch. Add print statements at `civa_panel.py:1038` (`_rx_decode` after `label = rx & 0xFF`), `:1070` (top of `_rx_handle_lon_insert`), and `:1079` (top of `_fire_but_insert_pulse`) to identify which step short-circuits. Most likely candidates: `self._sim_kind` is `"munzel"` rather than `"felis"` (so the Felis-specific dataref write never happens, the Münzel `cdu/insert` command fires instead), or the Felis dataref binding is wrong.

5/4/26 — Initial documentation drafted from `civa_panel_integration.md` (LukTronics aviologic project) and the cross-referenced ARINC 561 design notes. Per those captures, the May 2026 bench session against a real Delco CIVA CDU confirmed:

* RX-side framing IS spec ARINC 561 compliant — proper 8-bit label phase, 1-bit inter-phase gap, 24-bit data phase. Real ARINC labels appear in bits 0–7 (at the time, only `0x80` had been observed; the 5/5/26 entry above adds `0x40` and `0xC0`).
* TX-side framing is NOT spec ARINC 419 compliant — sign bits are independent flags, no inter-phase gap, CLK must remain continuously toggling. See `README.md` quirks for the full list.
* Pull-up sizing of 4.7 kΩ to +12 V verified for the TX path.
* Combo-key behavior bench-confirmed for `3+9` (BCD `0xB`) and `7+9` (BCD `0xF`) on 2026-05-03.

Open items (as of 5/5/26): identify the meaning of label `0xC0`; bench-confirm `0x20` for lat-insert; map data-selector button bit positions on the `0x80` word; verify physical pinout against unit nameplate.
