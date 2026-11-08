# ESP32-S3 handheld case, rev 2: FIT note (r1 kept as FIT-r1.md)

Source: `case.py` (CadQuery). All dimensions below are parameters in its top block. Change them and re-run
`~/tools/cad-venv/bin/python case.py <outdir>`; it re-exports the parts and re-runs the interference and port checks.

## Overall
- Outer: **92.2 x 69.4 x 21.5 mm** (X x Y x Z), outer corner R6.8, edge fillet 1.2.
- Wall 2.8, floor 2.4, bezel plate 1.6. Parting plane at z = 17.44 (screen PCB top).
- Back shell prints 92.2 x 69.4 x 18.9. Bezel prints 92.2 x 69.4 x 18.94 (plate plus screw bosses; r1 check.json wrongly said 4.1). Both fit a 220x220 bed easily.
- Joint: 1.2 mm tongue on the shell, 0.25 mm clearance, 1.35 mm outer lip on the bezel (wall 2.8 at the joint).
- Z stack (from outside of the floor): floor 0-2.4, ESP PCB 7.6-9.2 (components face down), perfboard 11.74-13.34,
  solder tails to 14.84, screen PCB 15.84-17.44, glass to 19.84, bezel plate 19.94-21.54.

## Prominent: unmeasured screen window
The active-area position on the glass is **not measured**. The window is only 1.0 mm larger than the 57.6 x 43.2 active area on each side, and is centred on the assumed glass. If the real active area is offset, the window will clip it. Measure the offset and set `WINDOW_MARGIN` / the glass offset before printing the bezel.

## Assumed dimensions (please measure and replace)
| Item | Value |
|---|---|
| Screen PCB | 86.0 x 50.0 x 1.6 |
| Screen glass/panel | 69.2 x 50.0 x 2.4, flush with the +X end of the PCB (assumed, the PCB's SD end is the bare part) |
| Active area | 57.6 x 43.2, centred on the glass; bezel window = active + 1.0 mm each side (59.6 x 45.2) |
| Parts on PCB back | max 1.0 mm high, except SD socket 15 x 14 x 2.0 at the -X end, centred in Y |
| Screen mounting holes | not used (case clamps the PCB at its edges) |
| Perfboard | 70 x 30 x 1.6, centre Y = -10.5 |
| ESP32-S3 DevKitC-1 style | 69 x 26 x 1.6, mounted components-down on the perfboard, USB end flush with the perfboard +X end |
| ESP tallest part (USB-C) | 3.2 mm; two receptacles 9.0 x 8.9 x 3.2, pitch 14.5 mm (centred on the board) |
| Header plastic ESP to perfboard | 2.54; solder tails above perfboard 1.5 |
| DAC PCM5102A | 32 x 20 x 1.6, jack body 12 x 9 x 6 high, jack axis 3 mm below PCB underside, jack on the +X edge, DAC centre Y = +15.5 |
| Clearances | 0.3 mm around boards in plan; 2.0 mm ESP parts to floor; 1.2 mm DAC jack to floor |
| Boards end gap | boards stop 0.3 mm short of the +X wall |
| Cable overmold | 12 x 7 mm, cutouts 12.6 x 7.6; jack hole 8.6 mm for an 8 mm plug collar |
| SD card cutout | 14 x 4 mm in the -X wall, centred on Y, inside a 24 mm wide x 1.8 mm deep external finger recess (1.0 mm wall around the slot) |

If the ESP is NOT on the perfboard, or the DAC jack is on a long edge, or the SD slot sits off-centre, change `PERF_Y`,
`DAC_Y`, `SD_Y_OFF` and the cutouts; the layout is otherwise independent.

## Features
- Tongue and rabbet joint, 4 x M2.5 self-tapping screws from the back: shell has a 2.8 mm through hole with a 5.2 x 1.6 counterbore (head sits flush, 0.8 mm floor under it);
  bezel has 5.0 mm bosses with 2.1 mm pilot holes, 9 mm deep (ends z 11.6).
  **Screws: 4 x M2.5 x 8 mm pan head.** Head seats at z 1.6, tip reaches z 9.6, about 7 mm engagement, pilot continues 2 mm past the tip.
  Bosses sit in 6.6 mm side strips beside the screen at X = +/-30, Y = +/-28.6; boss edge is 0.6 mm from the perfboard and DAC edges.
- Screen PCB sits on four 45-degree corner ledges (shell) and is clamped by the bezel plate on the glass plus two pads over the bare PCB corners.
- Perfboard sits on four thin posts under its outer margins (outside the ESP footprint). The DAC sits on four 3 x 3 posts.
  The boards are captured between the floor posts and the screen PCB, with no screws. A dab of hot glue is optional.
- SD slot: 14 x 4 mm tunnel plus a 24 mm wide finger recess on the outer -X wall, leaving 1.0 mm of wall around the slot.
- BOOT/RESET are on the ESP face that points at the floor and are not reachable. Normal USB flashing uses auto-reset and does not need them; for recovery, open the case or add pinholes in the floor once the button positions are measured.
- Vents: 8 slots 1.6 x 16 in the floor under the ESP.
- Ports on the +X end: 2 x USB-C cutouts, 3.5 mm jack hole. SD card slot cutout on the -X end.
- Touchscreen only: no button openings.

## Battery bay decision: skipped
A 52 x 36 x 7 mm bay cannot go beside the boards (the interior is about 86.6 x 65.4 mm and fully used in plan), so it would
sit under or over the stack: +7 mm, which is more than the 5 mm allowed, and the case would reach 28 mm (target < 25).
Skipped. For v2, raise the shell by about 8 mm and add a charger; the parametric stack makes this a small change.

## Checks (from `check.json`)
- Pairwise interference between shell, bezel and all 14 placeholder blocks: **0 overlaps** (re-run on r2) (threshold 0.01 mm3).
- Port reachability: a 12 x 7 cable-overmold envelope (rounded) at each USB-C, an 8 mm plug cylinder at the jack and an SD card
  envelope, each extended 15 mm outside the case, intersect **0 mm3** of case material, and touch their port component.
- `cad-check.py`: both STEP files valid, 1 solid each, STL watertight.

## Print settings (PLA, 0.4 mm nozzle)
- Layer height 0.2 mm (0.16 for a nicer bezel face), 3 perimeters (about 1.2 mm), 4 top/bottom layers.
- Infill 20% gyroid (the 5 mm bosses are solid perimeters).
- **Back shell**: floor on the bed, open side up. No supports. Pad undersides are 45 degrees. The USB and SD cutout tops are 12-14 mm bridges and the jack hole top is an 8.6 mm round bridge, all fine with bridging.
  Do not use supports there.
- **Bezel**: plate face-down on the bed (the supplied STL and STEP are already in print orientation). Bosses grow upward. No supports.
  Use an ironing/smooth sheet for the best face. The STL is exported flipped; the assembly STEP is in design orientation.
- Material about 29 cm3 solid, roughly 25 to 30 g at these settings.
- Pilot hole 2.1 mm suits M2.5 self-tapping in PLA; if screws split the bosses use 2.2 mm.
- Tolerance: hole sizes may need +/-0.1 mm after the first test print. Print the shell first to test the board fit.

## Files
back-shell-r2.{step,stl}, front-bezel-r2.{step,stl}, assembly-r2.step (with placeholder blocks), iso-r2.png, exploded-r2.png,
internal_nobezel-r2.png, check-r2.json, case-r2.py (r1 files unchanged).

## Screws
M2.5 x 8 pan head (ISO 7045 head is ~1.8 mm tall, so it sits ~0.2 mm proud of the 1.6 mm counterbore). Use a low-profile/wafer head for a truly flush back.
