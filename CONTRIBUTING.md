# Contributing

This repo is the long-term home for everything we learn at the bench. The goal: a few years from now, anyone — a sim builder, an A&P, a retired flight engineer — can pick a unit out of the structure and find pinouts, behavior notes, and bench results that are actually correct.

That only works if we're consistent. This file describes the conventions.

## Audience and tone

Write for someone with general aviation/electronics literacy who has not seen this specific unit. Assume the reader knows what ARINC 429 is in general; do not assume they know which label your unit emits on power-up.

Be technically precise. Cite sources (datasheets, IPCs, manuals) when you have them. When you're reporting bench observations, say so explicitly — bench observations and manufacturer specs are not the same thing, and conflating them is how bad institutional knowledge gets baked in.

If you're correcting something a previous contributor wrote, say what was wrong and how you confirmed it. Don't silently overwrite.

## Folder structure

Two top-level content axes: what the *units* are, and how the *airframes* are configured.

```
avionics/<type>-<manufacturer>-<partnumber>/    one folder per LRU type — intrinsic docs
    ├── README.md                                identification, function, status, "installed in" links
    ├── pinouts.md                               connector pinouts, signal definitions
    ├── bench-test.md                            what we did, what we observed, with dates
    ├── quirks.md                                undocumented behavior, gotchas, failure modes
    ├── photos/
    ├── captures/                                scope traces, logic-analyzer dumps
    └── datasheets/                              manufacturer datasheets, CMM excerpts, IPC pages

aircraft/<aircraft>/                             one folder per airframe — install configuration
    ├── README.md                                aircraft overview, ID, status
    ├── cockpit-map.md                           panel locations, overview photos
    └── panels/<panel>/<module>/                 module README is the LEAF (see below)

systems/                                         cross-cutting topics (ARINC 429, synchros, …) and generic test methods
templates/                                       copy-paste scaffolds
glossary.md
```

### The split, in one sentence

`avionics/<unit>/` is what the box *is*. `aircraft/<aircraft>/panels/<panel>/<module>/` is where it's *installed*. Each module README lists the install slots in that module and links each slot to the corresponding `avionics/<unit>/` folder.

### Module is the leaf

There is **no per-instrument folder** under `<module>/`. The module's `README.md` is the deepest thing in the panel tree. It contains a slot table — one row per physical install slot in that module — naming the slot, the unit installed there, and what's specific to that slot's wiring or role. See [Slots in a module](#slots-in-a-module) below.

If a single slot accumulates more than about a screenful of install-specific content, **promote it to its own file** as a sibling of the module README: `aircraft/<aircraft>/panels/<panel>/<module>/<slot>.md`. Reference it from the slot table. Do not introduce a `<slot>/` subfolder — modules stay leaf-folders.

### Where does my content go?

| You're documenting… | Put it under… |
|---|---|
| What an LRU *is* — pinouts, bench tests, quirks, datasheets | `avionics/<type>-<manufacturer>-<partnumber>/` |
| How an airframe is configured — which units in which slots | `aircraft/<aircraft>/panels/<panel>/<module>/README.md` (slot table) |
| Install detail for a single slot that grew past a screenful | `aircraft/<aircraft>/panels/<panel>/<module>/<slot>.md` |
| The cockpit layout of an airframe, panel locations, overview photos | `aircraft/<aircraft>/cockpit-map.md` |
| Airframe-specific system architecture (electrical bus topology, hydraulic schematic) | `aircraft/<aircraft>/systems/<topic>/` |
| A protocol or bus that's not airframe-specific (ARINC 429, ARINC 561, synchro signals, 26 VAC ref) | `systems/<topic>/` |
| A generic test method (sniffing ARINC 429, exciting a synchro, decoding a BCD wheel) | `systems/<topic>/test-methods.md` (alongside the protocol/signal it applies to) |
| Bench-test results for a specific unit | `avionics/<unit>/bench-test.md` |

If a piece of content fits in two places, put it where it primarily lives and link from the other.

## Naming conventions

All folder and file names: **lowercase, hyphen-separated, no spaces, no underscores.** This keeps URLs clean when we publish the static site.

### Aircraft

Lowercase, hyphenated, manufacturer-prefix style. Include the registration when we have a specific airframe in hand — install observations are properties of that tail, not the type as a whole.

- `b747-300-ja8179` — Boeing 747-300, registration JA8179 (the airframe currently on the bench)
- `b727-100` — Boeing 727-100 (no specific tail in hand)
- `dc-9-30-n12345` — McDonnell Douglas DC-9-30, registration N12345

### Panels

For Boeing aircraft we adopt the **P-designators** used in the WDM, AMM, and IPC, prefixed to a descriptive name: `p<number>-<descriptive-name>`. The P-number first makes the folder sort and search match how crews and the manuals refer to it.

747-300 (JA8179) examples:

- `p1-captains-panel` — captain's main instrument panel
- `p2-center-instrument-panel` — engine instruments (verify designator from WDM)
- `p3-first-officers-panel` — first officer's main instrument panel
- `p4-flight-engineers-panel` — flight engineer's main panel (confirmed P4 from the WDM fuel pages, 28-41-11)
- `p5-overhead-panel` — forward overhead (verify designator from WDM)
- `p7-glareshield` — mode control / autopilot panel (verify designator from WDM)
- `p8-aft-pedestal` — aft electronic control panel (CIVA CDUs etc.)
- `p10-center-pedestal` — throttle quadrant, comm/nav radios (verify designator from WDM)

For panels not covered by a P-designator (or for non-Boeing aircraft), use a descriptive name without the prefix.

### Modules

Functional grouping within a panel: `flight-instruments`, `engine-instruments`, `nav-radios`, `comm-radios`, `electrical`, `hydraulics`, `fuel`, `pneumatics`, `apu`, `warning-annunciators`, `autopilot`. Lowercase, hyphenated.

### Slots (inside a module README)

Slots are not folders — they are rows in the module's slot table (or, when promoted, sibling `.md` files at the module level). Slot names should describe the role, not the unit:

- `captains-adi`, `first-officers-adi` — the same ADI type installed in two slots
- `captains-hsi`, `first-officers-hsi`
- `cdu-1`, `cdu-2`, `cdu-3` — three peer installations of the same CIVA INS CDU
- `vor-1`, `vor-2` — dual VOR receivers

Lowercase, hyphenated. The slot name is the row identifier and the filename if promoted to a `<slot>.md`.

### Avionics units

Format: `<type>-<manufacturer>-<partnumber>`

- **type** — the common acronym for the LRU: `rmi`, `adi`, `hsi`, `asi`, `alt`, `vsi`, `dme`, `vor`, `adf`, `xpdr`, `tcas`, `wxr`, `gpwr`, `fmc`, `iru`, `cdu`, etc.
- **manufacturer** — short form: `collins`, `bendix`, `king`, `sperry`, `honeywell`, `litton`, `kollsman`, `smiths`, `civa`.
- **partnumber** — IPC-style part number, lowercased, with `/` and other non-alphanumerics replaced by `-`.

Examples:

- `rmi-collins-331a-9g`
- `adi-collins-329b-8g`
- `hsi-bendix-im-205`
- `xpdr-collins-tdr-90`
- `cdu-civa-...` _(fill in the part number)_

If you have multiple dash-numbers of the same unit and they're substantively different, give each its own folder. If they only differ in minor cosmetic ways (lighting voltage, faceplate variant), document them in one folder and note the variants in `README.md`.

### Per-unit file skeleton

Every avionics unit folder uses the same skeleton:

```
avionics/<type>-<manufacturer>-<partnumber>/
├── README.md          identification, function, status, "installed in" links
├── pinouts.md         connector pinouts and signal definitions
├── bench-test.md      what we did, what we observed, with dates
├── quirks.md          undocumented behavior, gotchas, failure modes
├── photos/            photos of the unit (front, back, connector, internals)
├── captures/          scope traces, logic analyzer dumps, audio captures
└── datasheets/        manufacturer datasheets, CMM excerpts, IPC pages
```

Not every file needs to exist on day one. Create them as content arrives. Do create the `README.md` — it's the entry point, and it tells contributors what's known and what's still missing.

Use [`templates/instrument-readme-template.md`](templates/instrument-readme-template.md) as the starting point for any new unit. (The file is named "instrument" historically; it applies to anything in `avionics/`.)

## Slots in a module

The module README is the leaf in the airframe panel tree. It describes the module and lists each install slot — typically as a table — with one row per physical position. Each row links to the unit doc in `avionics/<unit>/`.

Example slot table for a captain's flight instruments module:

```markdown
| Slot | Position | Unit | Sources | Notes |
|---|---|---|---|---|
| captains-adi | upper center | [adi-collins-329b-8g](../../../../../avionics/adi-collins-329b-8g/) | VG-1; reverts to VG-2 | command bars from FD-1 |
| captains-hsi | center | [hsi-bendix-im-205](../../../../../avionics/hsi-bendix-im-205/) | compass system #1; VOR-1 / ILS-1 | course set via P10 control |
| captains-rmi | upper left | [rmi-collins-331a-9g](../../../../../avionics/rmi-collins-331a-9g/) | VOR-1 + ADF-1 | dual-needle |
```

Anything install-specific to a slot — different signal source than its peer slot, different reversion logic, different dimming bus, mount-adapter quirks — goes inline in the module README, either as additional table columns or as a `### Slot name` subsection beneath the table.

**Promote a slot to its own file when it exceeds about a screenful** of install-specific content. The promoted file is a sibling of the module README at `aircraft/<aircraft>/panels/<panel>/<module>/<slot>.md`. The slot table row links to it. Do not create a `<slot>/` subfolder; modules remain leaf folders.

## Cross-aircraft instruments

When the same LRU appears in more than one of our airframes, no duplication is needed: the unit lives in `avionics/<unit>/` once, and each aircraft's module README links to it. The unit's README has an "Installed in" section listing every slot it occupies across every aircraft.

Today, with only the 747-300 JA8179 on the bench, every avionics unit is referenced from one aircraft. When a 727 or DC-9 comes online, no migration — that aircraft's panel tree just adds links into the existing `avionics/` folders, and each unit's "Installed in" list grows.

## Markdown style

Plain GitHub-flavored markdown. It must render correctly on GitHub today and under MkDocs Material later. That means:

- **Internal links** — use relative paths to `.md` files. Both renderers handle them. From a module README to a unit doc the path is `../../../../../avionics/<unit>/README.md`.
- **Images** — use relative paths: `![](photos/front.jpg)`. Keep widths sane (commit a downscaled copy if the original is huge).
- **Headings** — one `# H1` per document, matching the page title. Use `##` and `###` below it.
- **Tables** — use them freely for pinouts, signal lists, slot lists, part-number cross-references. Keep them readable in raw form too.
- **Admonitions** — for callouts, prefer GitHub's blockquote-alert syntax (`> [!NOTE]`, `> [!WARNING]`, `> [!CAUTION]`). It renders on GitHub and we can convert to MkDocs Material's `!!! note` syntax at site-build time if we want.
- **Code blocks** — fence with triple backticks and a language tag (`text`, `python`, `c`, `verilog`) so MkDocs syntax-highlights cleanly.

Avoid HTML inside markdown unless you genuinely need it — it tends to render inconsistently between GitHub and static site generators.

## Images, scope captures, and other binaries

Reasonable-sized photos and screenshots (under ~2 MB) — commit them directly. Git handles them fine and GitHub serves them.

Large binaries — full scanned datasheets, raw scope captures, multi-megabyte logic analyzer dumps — **don't commit blindly**. Options, in order of preference:

1. **Reduce first.** Most scope screenshots can be PNG-optimized to under 500 KB without losing detail. PDFs of datasheets can usually be downsampled.
2. **Excerpt instead of include.** Crop the relevant page or trace, commit the excerpt, and link out to (or note where to find) the full document.
3. **Git LFS** — for files we genuinely need at full fidelity and which can't be reduced. Talk to a maintainer before enabling LFS for a new file type; LFS bandwidth has costs.

If you're about to commit anything over ~5 MB, stop and ask in the PR.

## Bench safety

The avionics we work with were designed for industrial environments and don't pretend to be safe to handle. Read this before you power anything up. There is no single project bench — each contributor's setup differs — but the hazards below apply to all of them.

**Electrical**

- **115 VAC / 400 Hz** is line voltage at higher frequency. It will hurt or kill you the same as 60 Hz mains. Treat all 115 VAC and 26 VAC reference circuits as live.
- **28 VDC** is lower voltage but aircraft buses are designed for very high fault current. A short between 28 V and ground through a watch band, ring, or piece of wire will start a fire and weld metal. Remove jewelry; use fused leads.
- **Capacitor discharge** — many older units have large filter capacitors that retain charge after power-down. Discharge before opening.
- **ESD** — many digital units are ESD-sensitive. Use a wrist strap and an ESD mat when handling boards or removing covers.
- **Don't connect or disconnect circular connectors under power.** Pin damage and arc-over both happen.

**Hazardous materials in older avionics**

- **Radium-painted dials** — pre-1960s instruments may have radium dial markings. Don't open the bezel on a glow-in-the-dark instrument without confirming what the lume is. Promethium and tritium dials are also possible; tritium is much lower hazard than radium, but still warrants handling care.
- **PCB-filled capacitors** — certain pre-1979 capacitors contain polychlorinated biphenyls. Don't crush or burn old caps from that era.
- **Lead solder** — most pre-2006 boards use leaded solder. Wash hands after handling; ventilate when reworking.
- **Mercury switches** — present in some legacy tilt sensors and altimeter capsules. Don't disassemble destructively without first checking what's inside.

**General**

- Eye protection when probing high-density connectors or soldering.
- Solder-fume ventilation if you're doing more than spot rework.
- If you're unsure about a unit before powering it up — what voltage, what reference, what's behind the bezel — ask in a PR or in the project chat before applying power.

## Status flags

Every avionics unit `README.md` starts with a status line so contributors can tell at a glance what's known. Use these values:

- **acquired** — we have one in the shop, but haven't bench-tested it yet.
- **bench-tested** — we've powered it up and characterized at least the basics.
- **documented** — pinouts, behavior, quirks all written up. Future visitors can use this as a real reference.
- **production-validated** — confirmed against a known-good aircraft installation or against a primary-source manual.

Status moves forward, never backward. If new evidence contradicts a "documented" entry, update the content and note the correction; don't downgrade the status.

## Pull requests

This repo uses PR review even for content-only changes. Two reasons: it catches errors before they become institutional knowledge, and it keeps a discussion trail next to the change.

- Branch naming: `<author>/<short-description>` (e.g., `vu/add-rmi-331a-9g`).
- One logical change per PR. Adding a new unit is one PR. Correcting three different units is three PRs.
- In the PR description: what was added/changed, what sources you used, and anything you're unsure about. The "unsure about" line is important — it tells reviewers where to look hardest.
- If you're correcting prior content, link to the commit or PR that introduced the now-corrected information. This keeps the history honest.

## Adding a new avionics unit — quick start

1. Create the unit folder: `avionics/<type>-<manufacturer>-<partnumber>/`.
2. Copy [`templates/instrument-readme-template.md`](templates/instrument-readme-template.md) into it as `README.md` and fill in identification, function, status.
3. Add `pinouts.md`, `bench-test.md`, `quirks.md` as you have content for them. Empty stubs are fine; missing files are also fine.
4. Drop photos in `photos/`, scope captures in `captures/`, datasheets in `datasheets/`.
5. Open a PR.

## Adding a unit's installation slot in an airframe — quick start

1. Identify which aircraft, panel, and module the slot belongs to. Today that's somewhere under `aircraft/b747-300-ja8179/panels/`.
2. Create the panel folder if it doesn't exist (use [`templates/panel-readme-template.md`](templates/panel-readme-template.md)).
3. Create the module folder if it doesn't exist (use [`templates/module-readme-template.md`](templates/module-readme-template.md)). The module README is the leaf — there is no instrument folder beneath it.
4. Add a row to the module README's slot table. Slot name describes the role (e.g., `captains-adi`); the row links to the unit doc in `avionics/<unit>/`.
5. If the slot has more than a row's worth of install-specific notes, add a `### <Slot Name>` subsection beneath the table. If it grows past a screenful, promote to a sibling `<slot>.md` file.
6. Update the unit's "Installed in" section in `avionics/<unit>/README.md` to list the new slot.
7. Open a PR.
