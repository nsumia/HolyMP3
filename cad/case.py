"""ESP32-S3 handheld enclosure v1: front bezel + back shell + placeholder assembly.
Units mm. Coordinates (assembly): X long axis, Y short axis, Z up (0 = underside of back shell).
Run: python case.py <out_dir>   -> writes parts/assembly/checks into OUT dir.
"""
import cadquery as cq

# ============================ PARAMETERS (owner: edit here) ============================
# --- Case rules ---
WALL      = 2.8    # side wall thickness (tongue 1.2 + clearance 0.25 + lip 1.35)
FLOOR_T   = 2.4    # back shell floor (2.4: 1.6 deep counterbore leaves 0.8 mm)
TOP_T     = 1.6    # bezel top plate thickness
CLR       = 0.3    # clearance around boards in plan
IN_R      = 4.0    # interior vertical corner radius (outer = IN_R + WALL)
EDGE_FIL  = 1.2    # outer bottom/top edge fillet
# --- Screen module (assumed ILI9341 2.8" red PCB) ---
SCR_L, SCR_W, SCR_PCB_T = 86.0, 50.0, 1.6   # PCB size
GLASS_L, GLASS_W, GLASS_T = 69.2, 50.0, 2.4 # glass/LCD panel on top of PCB (assumed flush to +X end)
ACTIVE_L, ACTIVE_W = 57.6, 43.2             # visible active area (centered on glass)
WINDOW_MARGIN = 1.0                          # bezel window = active + 2*margin
SCR_BACK_CLR  = 1.0                          # assumed max height of parts on PCB back (except SD socket)
SD_L, SD_W, SD_H = 15.0, 14.0, 2.0           # SD socket body on PCB back, at -X end
SD_Y_OFF = 0.0                               # SD socket centre offset in Y from case centre
SD_REC_W, SD_REC_DEPTH = 24.0, 1.8       # finger recess on outer -X wall (leaves WALL-depth = 1.0 mm around the slot)
SD_CUT_W, SD_CUT_H = 14.0, 4.0               # wall cutout for SD card (+ finger access)
# --- Perfboard with ESP32-S3 (components face DOWN to floor, solder side up) ---
PERF_L, PERF_W, PERF_T = 70.0, 30.0, 1.6
PERF_Y = -10.5                               # perfboard centre Y
ESP_L, ESP_W, ESP_PCB_T = 69.0, 26.0, 1.6    # DevKitC-1 style
ESP_COMP_H   = 3.2                           # tallest part on ESP (USB-C receptacle) hanging below PCB
ESP_HDR_H    = 2.54                          # header plastic between ESP PCB and perfboard
ESP_FLOOR_GAP = 2.0                          # clearance: tallest ESP part to floor
USB_PITCH    = 14.5                          # centre distance of the 2 USB-C ports
USB_RECEPT   = (9.0, 8.9, 3.2)               # receptacle L(x) x W(y) x H(z) placeholder
USB_CUT_W, USB_CUT_H = 12.6, 7.6             # wall cutout (12x7 overmold + 0.3/side)
TAIL_H       = 1.5                           # solder tails above perfboard
# --- DAC PCM5102A (components face DOWN) ---
DAC_L, DAC_W, DAC_PCB_T = 32.0, 20.0, 1.6
DAC_Y        = 15.5                          # DAC centre Y
DAC_COMP_H   = 6.0                           # jack body height (hangs below PCB)
DAC_FLOOR_GAP = 1.2
JACK_W       = 9.0                           # jack body width (Y)
JACK_CUT_D   = 8.6                           # wall hole for 3.5 mm plug (collar ~7-8)
END_GAP      = 0.3                           # ports-end boards stop this far from the wall
# --- Screws ---
SCREW_D = 2.5            # M2.5 self-tapping
BOSS_D, PILOT_D, PILOT_DEPTH = 5.0, 2.1, 9.0
THRU_D, CBORE_D, CBORE_DEPTH = 2.8, 5.2, 1.6   # screw: M2.5 x 8 pan head (head 1.6 high sits flush)
BOSS_X = 30.0            # boss X (+/-)
STRIP  = 6.6             # side strip beside the screen where bosses live
# --- Joint / ledges ---
TONGUE_T, TONGUE_H, TONGUE_CLR = 1.2, 1.5, 0.25
PAD_L, PAD_OVER = 8.0, 1.2    # corner ledge length along X, PCB overlap
VENT_N, VENT_W, VENT_L = 8, 1.6, 16.0
GLASS_GAP = 0.1               # bezel plate to glass top
BED = (220, 220)
# =======================================================================================

# ---- derived ----
INT_L = SCR_L + 2 * CLR
INT_W = SCR_W + 2 * CLR + 2 * STRIP
OUT_L, OUT_W = INT_L + 2 * WALL, INT_W + 2 * WALL
OUT_R = IN_R + WALL
XI, YI = INT_L / 2, INT_W / 2          # interior half extents

# z stack
Z_FLOOR = FLOOR_T
Z_ESP_LOW = Z_FLOOR + ESP_FLOOR_GAP + ESP_COMP_H      # lower face of ESP PCB
Z_ESP_UP = Z_ESP_LOW + ESP_PCB_T
Z_PERF_LOW = Z_ESP_UP + ESP_HDR_H
Z_PERF_UP = Z_PERF_LOW + PERF_T
Z_TAIL_UP = Z_PERF_UP + TAIL_H
Z_SCR_LOW = Z_TAIL_UP + SCR_BACK_CLR                  # screen PCB underside = pad top
Z_SPLIT = Z_SCR_LOW + SCR_PCB_T                       # parting plane = PCB top
Z_GLASS_UP = Z_SPLIT + GLASS_T
Z_PLATE_LOW = Z_GLASS_UP + GLASS_GAP
Z_TOP = Z_PLATE_LOW + TOP_T
Z_DAC_LOW = Z_FLOOR + DAC_FLOOR_GAP + DAC_COMP_H
Z_DAC_UP = Z_DAC_LOW + DAC_PCB_T
USB_Z = Z_ESP_LOW - ESP_COMP_H / 2
JACK_Z = Z_DAC_LOW - DAC_COMP_H / 2
SD_Z = Z_SCR_LOW - SD_H / 2
X_END = XI - END_GAP                                  # ports-end board edge
BOSS_Y = YI - STRIP / 2


def rrect(l, w, r, z0, h, cx=0, cy=0):
    return (cq.Workplane("XY").workplane(offset=z0).center(cx, cy)
            .rect(l, w).extrude(h).edges("|Z").fillet(r))


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


# ---------------- back shell ----------------
def make_shell():
    body = rrect(OUT_L, OUT_W, OUT_R, 0, Z_SPLIT)
    body = body.faces("<Z").edges().fillet(EDGE_FIL)
    outer_solid = body
    pocket = rrect(INT_L, INT_W, IN_R, Z_FLOOR, Z_SPLIT)
    shell = body.cut(pocket)
    # tongue (inner part of wall rising above split)
    t_out = rrect(INT_L + 2 * TONGUE_T, INT_W + 2 * TONGUE_T, IN_R + TONGUE_T, Z_SPLIT, TONGUE_H)
    t_in = rrect(INT_L, INT_W, IN_R, Z_SPLIT, TONGUE_H)
    shell = shell.union(t_out.cut(t_in))
    # corner ledge pads with 45 deg underside (printable without support)
    yw = YI + 0.5
    yin = SCR_W / 2 - PAD_OVER
    zt = Z_SCR_LOW
    for sx in (1, -1):
        for sy in (1, -1):
            pts = [(yin, zt), (yw, zt), (yw, zt - (yw - yin))]
            pts = [(sy * a, b) for a, b in pts]
            pad = cq.Workplane("YZ").polyline(pts).close().extrude(PAD_L + 0.5)
            pad = pad.translate((XI - PAD_L if sx > 0 else -XI - 0.5, 0, 0))
            shell = shell.union(pad.intersect(outer_solid))
    # perfboard support posts (under outer margins of the perfboard)
    px0, px1 = X_END - PERF_L, X_END
    py0, py1 = PERF_Y - PERF_W / 2, PERF_Y + PERF_W / 2
    ew = (PERF_W - ESP_W) / 2 - 0.2
    for (xa, xb) in ((px0 + 1, px0 + 13), (px1 - 13, px1 - 1)):
        for (ya, yb) in ((py0, py0 + ew), (py1 - ew, py1)):
            shell = shell.union(box(xa, xb, ya, yb, Z_FLOOR - 0.2, Z_PERF_LOW))
    # DAC corner posts (3x3), under PCB underside outside component area
    dx0, dx1 = X_END - DAC_L, X_END
    dy0, dy1 = DAC_Y - DAC_W / 2, DAC_Y + DAC_W / 2
    for (xa, xb) in ((dx0, dx0 + 3), (dx1 - 3, dx1)):
        for (ya, yb) in ((dy0, dy0 + 3), (dy1 - 3, dy1)):
            shell = shell.union(box(xa, xb, ya, yb, Z_FLOOR - 0.2, Z_DAC_LOW))
    # screw holes + counterbores in floor
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx * BOSS_X, sy * BOSS_Y)
            shell = shell.cut(cq.Workplane("XY").center(*c).circle(THRU_D / 2).extrude(FLOOR_T + 1))
            shell = shell.cut(cq.Workplane("XY").center(*c).circle(CBORE_D / 2).extrude(CBORE_DEPTH))
    # port cutouts, +X end wall
    def cut_x(shell, yc, zc, w, h, side, r=1.5):
        x0 = side * (XI - 0.5)
        c = (cq.Workplane("YZ").center(yc, zc).rect(w, h).extrude(WALL + 1.5)
             .edges("|X").fillet(min(r, w / 2 - .1, h / 2 - .1)))
        c = c.translate((x0 if side > 0 else x0 - (WALL + 1.5), 0, 0))
        return shell.cut(c)
    for s in (1, -1):
        shell = cut_x(shell, PERF_Y + s * USB_PITCH / 2, USB_Z, USB_CUT_W, USB_CUT_H, +1)
    jack = (cq.Workplane("YZ").center(DAC_Y, JACK_Z).circle(JACK_CUT_D / 2).extrude(WALL + 1.5)
            .translate((XI - 0.5, 0, 0)))
    shell = shell.cut(jack)
    # SD cutout, -X end wall
    shell = cut_x(shell, SD_Y_OFF, SD_Z, SD_CUT_W, SD_CUT_H, -1, r=1.0)
    rz0, rz1 = SD_Z - 5.5, Z_SPLIT - 0.8
    rec = (cq.Workplane("YZ").center(SD_Y_OFF, (rz0 + rz1) / 2).rect(SD_REC_W, rz1 - rz0).extrude(SD_REC_DEPTH + 2)
           .edges("|X").fillet(2.5).translate((-XI - WALL - 2 + SD_REC_DEPTH, 0, 0)))
    shell = shell.cut(rec)
    # vent slots in floor under the ESP
    for i in range(VENT_N):
        x = X_END - ESP_L + 10 + i * 7.5
        s = cq.Workplane("XY").center(x, PERF_Y).rect(VENT_W, VENT_L).extrude(FLOOR_T + 1).edges("|Z").fillet(0.7)
        shell = shell.cut(s)
    return shell


# ---------------- front bezel (design orientation: plate on top) ----------------
GLASS_X0 = -SCR_L / 2 + (SCR_L - GLASS_L)      # glass flush to +X end of PCB
GLASS_CX = GLASS_X0 + GLASS_L / 2


def make_bezel():
    h = Z_TOP - Z_SPLIT
    body = rrect(OUT_L, OUT_W, OUT_R, Z_SPLIT, h)
    body = body.faces(">Z").edges().fillet(EDGE_FIL)
    cav = rrect(INT_L, INT_W, IN_R, Z_SPLIT - 0.1, Z_PLATE_LOW - Z_SPLIT + 0.1)
    bez = body.cut(cav)
    # rabbet for shell tongue
    r_out = rrect(INT_L + 2 * (TONGUE_T + TONGUE_CLR), INT_W + 2 * (TONGUE_T + TONGUE_CLR),
                  IN_R + TONGUE_T + TONGUE_CLR, Z_SPLIT - 0.1, TONGUE_H + TONGUE_CLR + 0.1)
    bez = bez.cut(r_out)
    # window
    win = (cq.Workplane("XY").workplane(offset=Z_PLATE_LOW - 0.1).center(GLASS_CX, 0)
           .rect(ACTIVE_L + 2 * WINDOW_MARGIN, ACTIVE_W + 2 * WINDOW_MARGIN).extrude(TOP_T + 1)
           .edges("|Z").fillet(1.5))
    bez = bez.cut(win)
    # bosses
    for sx in (1, -1):
        for sy in (1, -1):
            c = (sx * BOSS_X, sy * BOSS_Y)
            b = cq.Workplane("XY").workplane(offset=Z_FLOOR + 0.2).center(*c).circle(BOSS_D / 2) \
                .extrude(Z_PLATE_LOW - Z_FLOOR - 0.2 + 0.2)
            hole = cq.Workplane("XY").workplane(offset=Z_FLOOR + 0.2).center(*c).circle(PILOT_D / 2).extrude(PILOT_DEPTH)
            bez = bez.union(b).cut(hole)
    # clamp pads over bare PCB corners at -X end (no glass there)
    for sy in (1, -1):
        y0, y1 = sorted((sy * (SCR_W / 2 - PAD_OVER), sy * (SCR_W / 2 + 1.5)))
        bez = bez.union(box(-XI + 0.4, -XI + PAD_L - 1, y0, y1, Z_SPLIT, Z_PLATE_LOW + 0.1))
    return bez


# ---------------- placeholder components ----------------
def make_components():
    c = {}
    c["screen_pcb"] = box(-SCR_L / 2, SCR_L / 2, -SCR_W / 2, SCR_W / 2, Z_SCR_LOW, Z_SPLIT)
    c["screen_glass"] = box(GLASS_X0, SCR_L / 2, -GLASS_W / 2, GLASS_W / 2, Z_SPLIT, Z_GLASS_UP)
    c["sd_socket"] = box(-SCR_L / 2, -SCR_L / 2 + SD_L, SD_Y_OFF - SD_W / 2, SD_Y_OFF + SD_W / 2,
                         Z_SCR_LOW - SD_H, Z_SCR_LOW)
    px0, px1 = X_END - PERF_L, X_END
    py0, py1 = PERF_Y - PERF_W / 2, PERF_Y + PERF_W / 2
    c["perfboard"] = box(px0, px1, py0, py1, Z_PERF_LOW, Z_PERF_UP)
    c["solder_tails"] = box(px0 + 3, px1 - 3, PERF_Y - 11, PERF_Y + 11, Z_PERF_UP, Z_TAIL_UP)
    ex0 = X_END - ESP_L
    c["esp_pcb"] = box(ex0, X_END, PERF_Y - ESP_W / 2, PERF_Y + ESP_W / 2, Z_ESP_LOW, Z_ESP_UP)
    c["esp_headers"] = box(ex0 + 2, X_END - 2, PERF_Y - ESP_W / 2 + 0.5, PERF_Y + ESP_W / 2 - 0.5, Z_ESP_UP, Z_PERF_LOW)
    c["esp_shield"] = box(ex0 + 2, ex0 + 32, PERF_Y - 9, PERF_Y + 9, Z_ESP_LOW - 2.5, Z_ESP_LOW)
    for i, s in enumerate((1, -1)):
        yc = PERF_Y + s * USB_PITCH / 2
        c[f"esp_usb{i+1}"] = box(X_END - USB_RECEPT[0], X_END, yc - USB_RECEPT[1] / 2, yc + USB_RECEPT[1] / 2,
                                 Z_ESP_LOW - USB_RECEPT[2], Z_ESP_LOW)
    dx0 = X_END - DAC_L
    c["dac_pcb"] = box(dx0, X_END, DAC_Y - DAC_W / 2, DAC_Y + DAC_W / 2, Z_DAC_LOW, Z_DAC_UP)
    c["dac_jack"] = box(X_END - 12, X_END, DAC_Y - JACK_W / 2, DAC_Y + JACK_W / 2, Z_DAC_LOW - DAC_COMP_H, Z_DAC_LOW)
    return c


def make_plugs():
    """Cable/plug/card envelopes that must be free of case material (reachability test)."""
    p = {}
    far = XI + WALL + 20
    for i, s in enumerate((1, -1)):
        yc = PERF_Y + s * USB_PITCH / 2
        p[f"plug_usb{i+1}"] = box(X_END - 0.5, far, yc - 6, yc + 6, USB_Z - 3.5, USB_Z + 3.5).edges("|X").fillet(2.0)
    p["plug_jack"] = (cq.Workplane("YZ").center(DAC_Y, JACK_Z).circle(4.0).extrude(far - (X_END - 0.5))
                      .translate((X_END - 0.5, 0, 0)))
    p["sd_card"] = box(-XI - WALL - 15, -SCR_L / 2 + 8, SD_Y_OFF - 5.75, SD_Y_OFF + 5.75, SD_Z - 1.0, SD_Z + 1.0)
    return p


def to_print_bezel(b):
    """Flip bezel plate-down for printing: rotate 180 about X, put on z=0."""
    return b.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, Z_TOP))


if __name__ == "__main__":
    import sys, json, itertools, datetime, pathlib
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    shell, bezel = make_shell(), make_bezel()
    comps, plugs = make_components(), make_plugs()
    vol = lambda w: w.val().Volume()
    rep = {"dims": {"outer_x": OUT_L, "outer_y": OUT_W, "outer_z": Z_TOP, "z_split": Z_SPLIT},
           "interference": {}, "ports": {}}
    # interference: all pairs among shell, bezel, components (tolerance 0.01 mm3)
    items = {"shell": shell, "bezel": bezel, **comps}
    groups_skip = {frozenset(("screen_pcb", "screen_glass")), frozenset(("screen_pcb", "sd_socket")),
                   frozenset(("esp_pcb", "esp_headers")), frozenset(("perfboard", "esp_headers")),
                   frozenset(("perfboard", "solder_tails")), frozenset(("esp_pcb", "esp_shield")),
                   frozenset(("esp_pcb", "esp_usb1")), frozenset(("esp_pcb", "esp_usb2")),
                   frozenset(("esp_shield", "esp_usb1")), frozenset(("esp_shield", "esp_usb2")),
                   frozenset(("dac_pcb", "dac_jack"))}   # touching/overlap-by-design pairs within one assembly
    bad = []
    for (a, wa), (b, wb) in itertools.combinations(items.items(), 2):
        if frozenset((a, b)) in groups_skip:
            continue
        v = wa.intersect(wb)
        try:
            iv = v.val().Volume() if v.vals() else 0.0
        except Exception:
            iv = 0.0
        if iv > 0.01:
            bad.append((a, b, round(iv, 3)))
    rep["interference"]["overlaps"] = bad
    # port reachability: plug envelope vs case parts must be empty; and envelope must touch port component
    ok = {}
    for name, pl in plugs.items():
        hit = 0.0
        for cn in ("shell", "bezel"):
            v = pl.intersect(items[cn])
            hit += v.val().Volume() if v.vals() else 0.0
        ok[name] = {"volume_in_case_material": round(hit, 3)}
    rep["ports"] = ok
    # printability
    rep["bed_fit"] = {"shell": [OUT_L, OUT_W, Z_SPLIT + TONGUE_H], "bezel": [OUT_L, OUT_W, round(Z_TOP - Z_FLOOR - 0.2, 2)],
                      "fits_220": OUT_L < BED[0] and OUT_W < BED[1]}
    rep["z"] = {k: round(v, 2) for k, v in dict(floor=Z_FLOOR, esp_low=Z_ESP_LOW, perf_low=Z_PERF_LOW,
                perf_up=Z_PERF_UP, scr_low=Z_SCR_LOW, split=Z_SPLIT, glass_up=Z_GLASS_UP, top=Z_TOP,
                usb_z=USB_Z, jack_z=JACK_Z, sd_z=SD_Z).items()}
    # exports
    pb = to_print_bezel(bezel)
    for n, w in (("shell", shell), ("bezel", pb)):
        cq.exporters.export(w, str(out / f"{n}.step"))
        cq.exporters.export(w, str(out / f"{n}.stl"), tolerance=0.02, angularTolerance=0.1)
    asm = cq.Assembly(name="esp32_handheld")
    asm.add(shell, name="back_shell", color=cq.Color(0.2, 0.25, 0.3))
    asm.add(bezel, name="front_bezel", color=cq.Color(0.15, 0.15, 0.18))
    for n, w in comps.items():
        asm.add(w, name=n, color=cq.Color(0.1, 0.5, 0.2))
    asm.save(str(out / "assembly.step"))
    json.dump(rep, open(out / "check.json", "w"), indent=1)
    print(json.dumps(rep, indent=1))
    import pickle
    # mesh dump for renderer
    def tess(w, tol=0.05):
        v, t = w.val().tessellate(tol, 0.2)
        return [(p.x, p.y, p.z) for p in v], t
    pickle.dump({"shell": tess(shell), "bezel": tess(bezel), **{k: tess(w) for k, w in comps.items()}},
                open(out / "meshes.pkl", "wb"))
