"""Kanoniczne drzwi z drzwi narysowanych przez ChatGPT + skalowanie budynkow wg drzwi.
- w kazdym obiekcie paska: drzwi = ciemna rama (skladowa ciemnych pikseli) w dolnej, srodkowej czesci -> bbox w oryginale;
- skala budynku = WYS_DRZWI / wys. drzwi w oryginale (drzwi zawsze dokladnie WYS_DRZWI px w grze);
- budynek -> gra: BOX + paleta swiata + twarda alfa; modul = drzwi wyciete z budynku-wzorca (kamienica) po tej samej przerobce;
- w kazdym budynku drzwi zastapione modulem (ten sam rozmiar), open = otwor przezroczysty; json dla gry; walidacja 055.
Uzycie: python drzwi_kanon.py <pasek.png> <nazwy po przecinku> [wzorzec]  -> codex_paczki\\budynki\\wejsciowe-v2\\"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

PASEK = sys.argv[1] if len(sys.argv) > 1 else r"E:\ai\codex_paczki\budynki\wyniki-wejsciowe\pasek01.png"
NAZWY = (sys.argv[2] if len(sys.argv) > 2 else "blok-z-balkonami,kamienica,piekarnia,apteka").split(",")
WZORZEC = sys.argv[3] if len(sys.argv) > 3 else "kamienica"
OUT = r"E:\ai\codex_paczki\budynki\wejsciowe-v2"; os.makedirs(OUT, exist_ok=True)
WYS_DRZWI = 58
PAL = np.array(json.load(open(r"E:\ai\skrzynka\odpowiedzi\world_palette.json", encoding="utf-8-sig")), np.int32)
src = open(r"E:\ai\lora\budynki_gotowe.py", encoding="utf-8").read(); ns = {}; exec(src[:src.index("def do_gry")], ns)
obs = ns["obiekty"](PASEK)
GLEB = {"blok-z-balkonami": 9, "kamienica": 9, "piekarnia": 7, "apteka": 7, "biurowiec": 10, "szkola": 10, "dom-wiejski": 8}


import cv2
# wzorzec drzwi: recznie wyznaczony prostokat ramy drzwi w obiekcie-wzorcu (wspolrzedne wzgledem dolnego srodka obiektu)
P01 = "E:/ai/codex_paczki/budynki/wyniki-wejsciowe/pasek01.png"
_obs01 = ns["obiekty"](P01); _w = _obs01[1]; _W, _H = _w.size          # wzorzec drzwi ZAWSZE: kamienica z paska 01
RAMA = (_W // 2 - 80 + 29, _H - 220 + 95, _W // 2 - 80 + 131, _H - 220 + 195)   # x0,y0,x1,y1 (kamienica, pasek01)
TPL = cv2.cvtColor(np.array(_w.convert("RGB"))[RAMA[1]:RAMA[3], RAMA[0]:RAMA[2]].astype(np.float32), cv2.COLOR_RGB2GRAY)


def drzwi_bbox(im):
    """dopasowanie wzorca drzwi (skala 0.8-1.25) w dolnej czesci, blisko srodka; zwraca bbox w oryginale"""
    g = cv2.cvtColor(np.array(im.convert("RGB")).astype(np.float32), cv2.COLOR_RGB2GRAY); H, W = g.shape
    best = None
    for s in np.arange(0.8, 1.26, 0.01):
        t = cv2.resize(TPL, (round(TPL.shape[1] * s), round(TPL.shape[0] * s)), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= H or t.shape[1] >= W:
            continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED)
        cx0 = int(W / 2 - t.shape[1] / 2); m = np.full(r.shape, -1, np.float32); m[int(H * 0.5):, (0 if os.environ.get("SRODEK") == "0" else max(0, cx0 - 15)):(r.shape[1] if os.environ.get("SRODEK") == "0" else cx0 + 16)] = 0
        r = np.where(m == 0, r, -1); _, mx, _, loc = cv2.minMaxLoc(r)
        if best is None or mx > best[0]:
            best = (mx, (loc[0], loc[1], loc[0] + t.shape[1], loc[1] + t.shape[0]))
    print("   pewnosc dopasowania drzwi", round(best[0], 2))
    return best[1] if best[0] > float(os.environ.get("PROG", "0.6")) else None


def paleta(g):
    a = np.array(g).astype(np.int32); al = a[..., 3] >= 128; rgb = a[..., :3][al]
    u, inv = np.unique(rgb, axis=0, return_inverse=True); m = PAL[((u[:, None] - PAL[None]) ** 2).sum(2).argmin(1)]
    o = np.zeros_like(a); o[..., :3][al] = m[inv.ravel()]; o[..., 3] = np.where(al, 255, 0); return o.astype(np.uint8)


bud = {}
for n, im in zip(NAZWY, obs):
    bb = drzwi_bbox(im)
    if bb is None:
        print(n, "NIE ZNALEZIONO DRZWI"); continue
    s = WYS_DRZWI / (bb[3] - bb[1])
    g = paleta(im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.BOX))
    d = [round(v * s) for v in bb]; d[3] = d[1] + WYS_DRZWI
    bud[n] = (g, d, s, bb)
    print(f"{n:18} drzwi w oryginale {bb[2]-bb[0]}x{bb[3]-bb[1]} px, skala {s:.3f}, budynek w grze {g.shape[1]}x{g.shape[0]} px = {g.shape[1]/24:.1f} m szer.")

# modul: z wzorca (pasek 01) albo istniejacy plik modulu
if WZORZEC in bud:
    g, d, s, bb = bud[WZORZEC]; MC = g[d[1]:d[3], d[0]:d[2]].copy()
else:
    MC = np.array(Image.open(os.path.join(OUT, "_drzwi-kanon-closed.png")).convert("RGBA"))
mh, mw = MC.shape[:2]
# otwor = szklo wewnatrz ramy: najwiekszy prostokat jasniejszych pikseli (lum >= 55) w module
lum = MC[..., :3].mean(2); jas = lum >= 55
ys, xs = np.where(jas[3:-3, 3:-3]); ys += 3; xs += 3
dw = {"x": int(xs.min()), "y": int(ys.min()), "w": int(xs.max() - xs.min() + 1), "h": int(mh - ys.min())}   # otwor do samego dolu (prog)
MO = MC.copy(); k = max(3, dw["w"] // 9)
MO[dw["y"]:dw["y"] + dw["h"], dw["x"] + k:dw["x"] + dw["w"] - k] = 0                                   # srodek przezroczysty, waskie skrzydla przy bokach
if WZORZEC in bud:
    Image.fromarray(MC, "RGBA").save(os.path.join(OUT, "_drzwi-kanon-closed.png")); Image.fromarray(MO, "RGBA").save(os.path.join(OUT, "_drzwi-kanon-open.png"))
json.dump({"module": "std-external-2", "source": f"drzwi ChatGPT z: {WZORZEC} ({os.path.basename(PASEK)})", "module_px": {"w": mw, "h": mh},
           "module_m": {"w": round(mw / 24, 2), "h": round(mh / 24, 2)}, "doorwayInModule": dw, "anchorInModule": {"x": mw / 2, "y": mh}},
          open(os.path.join(OUT, "_drzwi-kanon.json"), "w", encoding="utf-8"), indent=1)
print("modul", mw, "x", mh, "otwor", dw)

wyn = []
for n, (g, d, s, bb) in bud.items():
    H, W = g.shape[:2]
    cxm = (d[0] + d[2]) / 2; px = int(round(cxm - mw / 2)); py = d[3] - mh
    zam, otw = g.copy(), g.copy()
    zam[py:py + mh, px:px + mw] = np.where(MC[..., 3:4] > 0, MC, zam[py:py + mh, px:px + mw])
    otw[py:py + mh, px:px + mw] = np.where(MC[..., 3:4] > 0, MO, otw[py:py + mh, px:px + mw])
    Image.fromarray(zam, "RGBA").save(os.path.join(OUT, f"{n}-closed.png")); Image.fromarray(otw, "RGBA").save(os.path.join(OUT, f"{n}-open.png"))
    Image.fromarray(g, "RGBA").save(os.path.join(OUT, f"{n}-przed.png"))
    diff = np.any(zam != otw, axis=2); yy, xx = np.where(diff)
    cr = {"x": int(xx.min()), "y": int(yy.min()), "w": int(xx.max() - xx.min() + 1), "h": int(yy.max() - yy.min() + 1)}
    doorway = {"x": px + dw["x"], "y": py + dw["y"], "w": dw["w"], "h": dw["h"]}
    dm = GLEB.get(n, 8)
    meta = {"id": f"{n}-closed", "family": n, "image": {"w": W, "h": H}, "anchor": {"x": W / 2, "y": H},
            "doors": [{"module": "std-external-2", "placement": {"x": px, "y": py}, "anchor": {"x": px + mw / 2, "y": py + mh}, "doorway": doorway, "changedRegion": cr}],
            "doorway": doorway, "states": {"door": {"values": ["closed", "open"], "default": "closed"}},
            "variants": [{"when": {"door": "closed"}, "contentKey": f"{n}-closed"}, {"when": {"door": "open"}, "contentKey": f"{n}-open"}],
            "variantGroup": n, "metric": {"width_m": round(W / 24, 2), "depth_m": dm}, "enterable": True,
            "scale_note": f"skala wg drzwi ({WYS_DRZWI} px), x{s:.3f} z oryginalu ChatGPT"}
    json.dump(meta, open(os.path.join(OUT, f"{n}-closed.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    poza = diff.copy(); poza[cr["y"]:cr["y"] + cr["h"], cr["x"]:cr["x"] + cr["w"]] = False
    dz = zam[doorway["y"]:doorway["y"] + doorway["h"], doorway["x"]:doorway["x"] + doorway["w"], 3]
    do = otw[doorway["y"]:doorway["y"] + doorway["h"], doorway["x"]:doorway["x"] + doorway["w"], 3]
    wyn.append({"budynek": n, "poza_changedRegion_identyczne": not poza.any(), "closed_otwor_pelny": bool((dz == 255).all()),
                "open_otwor_przezroczysty": bool((do == 0).any()), "open_bez_nowych_widocznych": not ((zam[..., 3] == 0) & (otw[..., 3] > 0)).any()})
    print(wyn[-1])
json.dump(wyn, open(os.path.join(OUT, "_walidacja.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# podglad: przed | po (zamk.) | po (otw.), x4, na szachownicy
X = 4; f = ImageFont.truetype("arialbd.ttf", 26)
def szach(w, h, k=12):
    a = np.full((h, w, 3), 225, np.uint8); yy, xx = np.mgrid[0:h, 0:w]; a[((yy // k + xx // k) % 2) == 1] = 195; return Image.fromarray(a).convert("RGBA")
pan = []
for n in bud:
    ims = [Image.open(os.path.join(OUT, f"{n}-{k}.png")) for k in ("przed", "closed", "open")]
    pan.append((n, [i.resize((i.width * X, i.height * X), Image.NEAREST) for i in ims]))
W = max(sum(i.width + 20 for i in ims) for _, ims in pan) + 40; H = sum(max(i.height for i in ims) + 60 for _, ims in pan) + 20
sh = Image.new("RGBA", (W, H), (150, 152, 156, 255)); dr = ImageDraw.Draw(sh); y = 10
for n, ims in pan:
    dr.text((20, y), f"{n}: przed | nasze drzwi zamkniete | otwarte", font=f, fill=(255, 255, 255)); hh = max(i.height for i in ims); x = 20
    for im in ims:
        bg = szach(im.width, im.height); bg.alpha_composite(im); sh.alpha_composite(bg, (x, y + 40 + hh - im.height)); x += im.width + 20
    y += hh + 60
sh.convert("RGB").save(os.path.join(OUT, "_przed_po_" + os.path.basename(PASEK)))
m = Image.fromarray(MC); mo = Image.fromarray(MO); X2 = 8
pm = Image.new("RGBA", (mw * X2 * 2 + 30, mh * X2), (150, 152, 156, 255))
for k, im in enumerate((m, mo)):
    big = im.resize((mw * X2, mh * X2), Image.NEAREST); bg = szach(big.width, big.height); bg.alpha_composite(big); pm.alpha_composite(bg, (k * (mw * X2 + 30), 0))
pm.convert("RGB").save(os.path.join(OUT, "_drzwi-kanon-podglad.png")); print("OK")
