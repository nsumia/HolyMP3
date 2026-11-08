"""Render iso.png / exploded.png / internal_nobezel.png from out/meshes.pkl with a numpy z-buffer."""
import sys, pickle, numpy as np
from PIL import Image
out, dest = sys.argv[1], sys.argv[2]
M = pickle.load(open(f"{out}/meshes.pkl", "rb"))
COL = {"shell": (150, 170, 205), "bezel": (60, 60, 72), "screen_glass": (15, 25, 80), "screen_pcb": (160, 30, 30),
       "sd_socket": (200, 200, 200), "perfboard": (190, 160, 70), "solder_tails": (220, 220, 220),
       "esp_pcb": (30, 30, 30), "esp_headers": (20, 20, 20), "esp_shield": (190, 190, 200),
       "esp_usb1": (230, 230, 230), "esp_usb2": (230, 230, 230), "dac_pcb": (40, 60, 160), "dac_jack": (20, 20, 20)}
def render(dz, fn, skip=(), W=1500, H=1100, az=-50, el=30):
    a, e = np.radians(az), np.radians(el)
    R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, np.cos(e), -np.sin(e)], [0, np.sin(e), np.cos(e)]])
    P = []
    for k, (v, t) in M.items():
        if k in skip: continue
        v = np.array(v, float); v[:, 2] += dz.get(k, dz.get("comp", 0) if k not in ("shell", "bezel") else 0)
        P.append((k, v, np.array(t)))
    allv = np.vstack([p[1] for p in P]); ctr = (allv.min(0) + allv.max(0)) / 2
    def cam(v): w = (v - ctr) @ R.T @ Rx.T; return w   # x right, y depth(away), z up
    allc = cam(allv); span = max(np.ptp(allc[:, 0]) / W, np.ptp(allc[:, 2]) / H) * 1.1
    img = np.full((H, W, 3), 255, np.uint8); zb = np.full((H, W), -1e9)
    Ld = np.array([0.5, -0.7, 0.8]); Ld /= np.linalg.norm(Ld)
    for k, v, t in P:
        c = cam(v); sx = c[:, 0] / span + W / 2; sy = H / 2 - c[:, 2] / span; d = -c[:, 1]
        base = np.array(COL.get(k, (120, 120, 120)), float)
        for tri in t:
            p = np.stack([sx[tri], sy[tri]], 1); dd = d[tri]
            n = np.cross(c[tri[1]] - c[tri[0]], c[tri[2]] - c[tri[0]]); nn = np.linalg.norm(n)
            if nn < 1e-9: continue
            n /= nn
            if n[1] > 0: n = -n   # two-sided
            # light in camera space approx: use view-space normal
            sh = 0.45 + 0.55 * max(0, n @ np.array([-0.4, -0.6, 0.7]))
            x0, x1 = int(max(p[:, 0].min(), 0)), int(min(p[:, 0].max() + 1, W - 1))
            y0, y1 = int(max(p[:, 1].min(), 0)), int(min(p[:, 1].max() + 1, H - 1))
            if x1 < x0 or y1 < y0: continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
            den = (p[1, 1] - p[2, 1]) * (p[0, 0] - p[2, 0]) + (p[2, 0] - p[1, 0]) * (p[0, 1] - p[2, 1])
            if abs(den) < 1e-9: continue
            l1 = ((p[1, 1] - p[2, 1]) * (xs - p[2, 0]) + (p[2, 0] - p[1, 0]) * (ys - p[2, 1])) / den
            l2 = ((p[2, 1] - p[0, 1]) * (xs - p[2, 0]) + (p[0, 0] - p[2, 0]) * (ys - p[2, 1])) / den
            l3 = 1 - l1 - l2
            m = (l1 >= -1e-6) & (l2 >= -1e-6) & (l3 >= -1e-6)
            z = l1 * dd[0] + l2 * dd[1] + l3 * dd[2]
            sub = zb[y0:y1 + 1, x0:x1 + 1]; upd = m & (z > sub)
            sub[upd] = z[upd]; img[y0:y1 + 1, x0:x1 + 1][upd] = np.clip(base * sh, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(f"{dest}/{fn}")
render({"comp": 0}, "iso.png")
render({"comp": 24, "bezel": 62}, "exploded.png", H=1500)
render({"comp": 0}, "internal_nobezel.png", skip=("bezel",))
