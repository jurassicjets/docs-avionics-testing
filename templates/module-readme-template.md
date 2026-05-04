# <Module Name>

> _One-line description of what this module is and where it sits within the panel._

Module within [`<panel-name>`](../README.md). _(Update the link when copying — point it at the parent panel's README.)_

This README is the **leaf** of the panel tree — there are no subfolders for individual instruments. Each install slot in the module is a row in the slot table below, linking to the unit's intrinsic doc in `/avionics/`. If a slot needs more than a row's worth of install-specific notes, add a `### Slot name` subsection beneath the table; if it grows past about a screenful, promote it to a sibling `<slot>.md` file at the module level (do **not** create a `<slot>/` subfolder).

## Function

What this module does — what role does this functional grouping of instruments play in the cockpit?

## Slots

| Slot | Position | Unit | Sources | Notes |
|---|---|---|---|---|
| _e.g._ captains-adi | upper center | [adi-collins-329b-8g](../../../../../avionics/adi-collins-329b-8g/) | VG-1; reverts to VG-2 | command bars from FD-1 |
| | | | | |

The relative path from this module README to a unit doc is `../../../../../avionics/<unit>/` (five levels up, then down into `avionics/`). Verify the link renders on GitHub before merging.

## Slot install detail

Add a `### <Slot Name>` subsection per slot only when the slot has more install-specific content than fits in a table row. Examples of what belongs here: signal-source selection logic, reversion behavior, dimming-bus particulars, mount-adapter quirks, harness deviations from the WDM. When this section grows past a screenful, promote it to `<slot-name>.md` and link from the slot table.

## Module-level interconnects

Wiring or signal flow that runs *between* slots in this module — e.g., a shared 26 VAC reference, a daisy-chained heading bus. If interconnects span multiple modules or are described in airframe-level docs, link out instead of duplicating.
