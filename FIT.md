# ESP32-S3 handheld case, rev 3: FIT note (r1, r2 files kept)

Source: `case-r3.py` (= /home/agent/projects/esp32-handheld/cad/case.py). All dimensions are parameters in its top block.
Re-run `~/tools/cad-venv/bin/python case.py <outdir>` to regenerate parts and re-run the interference and port checks.

## r3 changes
1. **Case screws are M2.** 4 x **M2 x 8 pan head**, from the back: through hole 2.4, counterbore 4.4 x 1.6 (4.0 x 1.6 head sits flush, 0.8 mm floor under it),
   bezel bosses 4.4 mm OD with 1.6 mm pilot (1.4 mm wall), pilot 9 mm deep. Head seats at z 1.6, tip reaches z 9.6, pilot ends at z 11.6:
   about 7.0 mm engagement and 2.0 mm margin past the tip. A 1.0 mm conical fillet joins each boss to the bezel plate.
2. **TFT is screwed down with M3**, not clamped. The 4 PCB mounting holes (assumed 3.2 mm dia, centres 3.5 mm in from each edge, i.e. a 79 x 43 pattern)
   get 6.5 mm bezel standoffs resting on the PCB top face, each with a 2.5 mm self-tapping pilot 3.8 mm deep.
   **Screws: 4 x M3 x 5 pan head (head 5.5 x 2.0)**, inserted from the back through the PCB hole into the standoff, so the PCB is clamped between standoff and screw head.
   Tip ends 3.4 mm above the PCB top, 0.4 mm short of the pilot end; the bezel face skin over the pilot is 1.1 mm (plate is 2.4 mm thick for this; screw stays M3 x 5).
   Why not nuts: a nut trap would need ~9 mm standoffs and the screw heads would show on the face. Weak point: only about 3.4 mm of thread in PLA;
   heat-set M3 inserts (4 mm) are a drop-in upgrade if it loosens.
   Assembly order: lay the bezel face down, drop the TFT in face down on the standoffs, fit the four M3 screws, then build up the shell.
   Clearances (checked in the assembly): standoffs vs glass 1.65 mm, vs SD socket, perfboard, DAC and ESP all 0 overlaps. Screw heads sit 1.5 mm above the solder tails.
3. **Full-size SD slot.** Socket assumed 28 x 26 x 3.0 mm on the PCB back at the -X end, centred in Y. Card 32 x 24 x 2.1; fully inserted its end sticks 2.5 mm past the PCB edge.
   Cutout in the -X wall: 26 x 4.0 mm. A 34 mm wide finger recess on the outer wall leaves 1.0 mm of wall (recess spans x -46.1 to -44.3 only). Measured by sectioning the exported shell STEP: wall beside the slot x -44.3..-43.3 = 1.0 mm,
   2.8 mm outside the recess, slot open through the wall. The card end sits about 0.6 mm behind the outer face and can be pinched or pushed (push-push) from the recess.
   To fit the 3 mm socket over the perfboard stack, the screen is 2.5 mm higher than in r2.

## !! Deviation to confirm: glass position
The coordinator asked to keep the glass position, but with the glass flush to the +X end (r2) the two +X mounting holes fall under the glass, which cannot be
(real modules have the holes in the bare PCB ends). In r3 the glass is **centred on the PCB** (8.4 mm bare PCB at each end) and the window is centred with it.
`GLASS_X_SHIFT = 8.4` restores the r2 window position (but then the +X standoffs must be moved or deleted).

## !! Unmeasured
Screen hole pattern, hole diameter, glass offset and active-area offset, and the SD socket size are all assumptions. The window is only 1.0 mm larger than the
57.6 x 43.2 active area on each side. Measure all of these before printing the bezel.

## Overall
- Outer **92.2 x 68.2 x 24.8 mm** (r2: 92.2 x 69.4 x 21.5; the side strips are narrower with the smaller bosses, the stack is 3.3 mm taller). Target < 25 met.
- Wall 2.8, floor 2.4, bezel plate 2.4. Parting plane z = 19.94. Joint: 1.2 tongue, 0.25 clearance, 1.35 lip.
- Shell prints 92.2 x 68.2 x 21.4; bezel 92.2 x 68.2 x 22.2. Fits 220x220.
- Z stack: floor 0-2.4, ESP PCB 7.6-9.2 (components down), perfboard 11.74-13.34, tails to 14.84, screen PCB 18.34-19.94, glass to 22.34, bezel plate 22.44-24.84.
- The corner ledges and clamp pads of r2 are gone (the M3 screws hold the PCB). Bosses at X = +/-30, Y = +/-28.3 (boss edge 0.6 mm from perfboard/DAC).

## Other assumed dimensions (unchanged from r2)
Screen PCB 86 x 50 x 1.6; glass 69.2 x 50 x 2.4; active 57.6 x 43.2, window +1.0 each side; perfboard 70 x 30 x 1.6 (centre Y -10.5);
ESP32-S3 69 x 26 x 1.6 components-down, USB-C receptacles 9 x 8.9 x 3.2 at 14.5 mm pitch; headers 2.54, tails 1.5; DAC 32 x 20 x 1.6, jack 6 high, centre Y +15.5, jack on +X edge;
cutouts USB 12.6 x 7.6, jack 8.6 dia; boards stop 0.3 from the +X wall. BOOT/RESET (components side) are not reachable once built: flash via USB (auto-reset) or add floor pinholes after measuring.
Battery bay: skipped (needs +7 mm, over the 5 mm limit; the case is already 24.8 mm).

## Checks (check-r3.json)
- Interference, shell + bezel + 18 placeholders (incl. M3 screws and PCB holes): 0 overlaps.
- Ports: USB x2, jack: 0 mm3 in case material. Full SD card envelope (fully inserted, then pulled out 15 mm): 0 mm3 in case material, 0 in all other components, and overlaps the socket as expected.
- cad-check.py on both STEPs: valid, 1 solid each, STLs watertight.

## Print (PLA, 0.4 nozzle)
0.2 mm layers, 3 perimeters, 4 top/bottom, 20% infill gyroid. Shell floor-down open side up; bezel plate-down (supplied in print orientation). No supports; USB/SD/jack cutout tops are 4-26 mm bridges.
Test-fit the shell first. Pilot holes may need +/-0.1 mm.

## Files
back-shell-r3.{step,stl}, front-bezel-r3.{step,stl}, assembly-r3.step, iso-r3.png, exploded-r3.png, internal_nobezel-r3.png, check-r3.json, case-r3.py.

## Notes after review (r3 final)
- Boss-base fillet reduced to 0.6 mm (gap to glass edge ~0.5 mm) to allow for glass tolerance.
- M2 pan head (4.0 x 1.6) fits the 4.4 x 1.6 counterbore flush; the 0.8 mm floor under it is 2 to 3 perimeters. Check it on the first test print, and do not overtighten.
- Glass is assumed centred on the TFT PCB (GLASS_X_SHIFT = 0). Measure your module and adjust GLASS_X_SHIFT and the M3 hole pattern before printing.
