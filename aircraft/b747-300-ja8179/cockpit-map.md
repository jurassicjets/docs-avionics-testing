# Cockpit Map — JA8179

Overall cockpit layout for the 747-300, JA8179. The goal of this page is to let a contributor look at a photo, find a panel, and click through to the instrument-level docs.

## Overview photos

_Drop wide-angle cockpit photos in `photos/` (create when needed) and reference them here._

- _Forward view from cockpit door:_
- _Captain's seat view:_
- _First officer's seat view:_
- _Flight engineer's station:_

## Panels

Panel locations in the cockpit, with cross-references to the panel docs. Boeing P-designators per the 747-300 WDM/AMM. P-numbers marked _(verify)_ are commonly-used assignments that should be confirmed against the WDM before they're treated as authoritative.

| P-# | Region | Panel folder | Notes |
|---|---|---|---|
| P1 | Forward, captain (left) | [panels/p1-captains-panel](panels/p1-captains-panel/README.md) | captain's main instruments |
| P2 _(verify)_ | Forward, center | [panels/p2-center-instrument-panel](panels/p2-center-instrument-panel/README.md) | engine instruments |
| P3 | Forward, first officer (right) | [panels/p3-first-officers-panel](panels/p3-first-officers-panel/README.md) | first officer's main instruments |
| P4 | Flight engineer's station | [panels/p4-flight-engineers-panel](panels/p4-flight-engineers-panel/README.md) | fuel (m154), electrical, hydraulics, pneumatics, APU; CIVA CDU (1 of 3) |
| P5 _(verify)_ | Forward overhead | [panels/p5-overhead-panel](panels/p5-overhead-panel/README.md) | electrical, hydraulics, fuel, pneumatics, APU |
| P7 _(verify)_ | Glareshield | [panels/p7-glareshield](panels/p7-glareshield/README.md) | autopilot mode control, annunciators |
| P8 | Aft pedestal | [panels/p8-aft-pedestal](panels/p8-aft-pedestal/README.md) | aft electronic control panel — CIVA CDUs (2 of 3) |
| P9 _(verify)_ | Pedestal | _not yet documented_ | pedestal panel — designator/contents to confirm |
| P10 _(verify)_ | Center pedestal | [panels/p10-center-pedestal](panels/p10-center-pedestal/README.md) | throttle quadrant, comm/nav radios, transponder |

_Add rows for additional side panels, circuit-breaker panels, or auxiliary panels as they're documented. Drop or correct any P-designator that doesn't match the WDM for this airframe._

## Panel-to-system cross-reference

When useful, document which panels host the controls and indicators for each major aircraft system. Helps when chasing a wire from "the warning lit up on the overhead" back to the unit that drove it.

_To be filled in._
