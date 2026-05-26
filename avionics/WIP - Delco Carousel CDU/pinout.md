Pinout for the Delco Carousel CDU

The CDU's main interface is a single rear circular connector. Pin numbers below are placeholders — read the actual pin assignments from the connector backshell label on the unit and update. Signal groupings and direction are accurate to the source documentation; only the physical pin numbers are TBD.

R/W column key:
- **R** = signal received by the CDU (computer / sim drives, CDU listens)
- **W** = signal transmitted by the CDU (CDU drives, computer / sim listens)

<table>
<tr><th>Power</th></tr>
<tr><td>

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | +28 VDC primary | +28 VDC | R | main bus power |
| TBD | power return | gnd | R | bonded to airframe ground |
| TBD | +28 VDC battery backup (?) | +28 VDC | R | verify if separate battery feed exists; CIVA system has battery-backed alignment |
| TBD | dimming bus | 5 VAC / 28 VDC | R | verify voltage and bus per airframe; lights the displays |

</td></tr></table>

<table>
<tr><th>ARINC 561 TX (Computer → CDU)</th></tr>
<tr><td>

Three twisted shielded pairs from the navigation computer. Bipolar signaling, 11.111 kHz nominal CLK rate. Each signal pair has a dedicated return.

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | CLK in | bipolar | R | 11.111 kHz; must remain continuously toggling — see quirk #3 |
| TBD | CLK return | gnd | R | dedicated signal return for CLK pair |
| TBD | SYNC in | bipolar | R | frame envelope; HIGH during label and data phases (no inter-phase gap on TX side) |
| TBD | SYNC return | gnd | R | dedicated signal return for SYNC pair |
| TBD | DATA in | bipolar | R | NRZ, MSB-first within each phase |
| TBD | DATA return | gnd | R | dedicated signal return for DATA pair |

</td></tr></table>

<table>
<tr><th>ARINC 561 RX (CDU → Computer)</th></tr>
<tr><td>

Three signal lines plus a single common signal-ground bond. Bipolar, 11.111 kHz, spec ARINC 561 framing (label phase + 1-bit gap + data phase). Note that the CDU's RX-direction output is at ~12 V signal levels — a level shifter is required before feeding modern 3.3 V CMOS inputs.

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | CLK out | bipolar | W | 11.111 kHz |
| TBD | SYNC out | bipolar | W | frame envelope; LOW during inter-phase gap (spec-compliant) |
| TBD | DATA out | bipolar | W | spec ARINC 561 framing; bits 0–7 carry real ARINC labels |
| TBD | signal GND | gnd | W | bonds to receiver's signal ground; one common return for all three RX lines |

</td></tr></table>

<table>
<tr><th>Discrete Lamps</th></tr>
<tr><td>

The BAT and WARN lamps are NOT carried in the WP/Lights ARINC word — they're separately driven by dedicated discrete lines. The CDU sinks the negative side of each lamp to light it (open-collector / open-drain to ground).

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | BAT lamp + | +28 VDC | R | sourced from bus; common to both lamps |
| TBD | BAT lamp - | sink | R | CDU pulls to ground to illuminate |
| TBD | WARN lamp + | +28 VDC | R | sourced from bus |
| TBD | WARN lamp - | sink | R | CDU pulls to ground to illuminate |

</td></tr></table>

<table>
<tr><th>Lighting / Display Power</th></tr>
<tr><td>

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | display lamps + | dimming bus | R | verify whether 5 VAC or 28 VDC dimming bus per airframe |
| TBD | display lamps - | gnd | R |  |
| TBD | annunciator lamps + | +28 VDC | R | drives ALERT, INSERT, HOLD, REMOTE annunciators |
| TBD | annunciator lamps - | gnd | R |  |

</td></tr></table>

<table>
<tr><th>Chassis / Shield</th></tr>
<tr><td>

| PIN | FUNCTION | SIGNAL | R/W | NOTES |
|--|--|--|--|--|
| TBD | chassis ground | gnd | — | bonded to airframe; not a signal return |
| TBD | shield | shield drain | — | typically bonded only at one end (computer end) |

</td></tr></table>
