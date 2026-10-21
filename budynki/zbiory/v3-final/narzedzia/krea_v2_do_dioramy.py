"""Obrazy Krea 2 + LoRA budynki v2 -> format dioramy (jak drzwi_kanon.py): wyciecie z tla magenta, skala gry, paleta swiata, twarda alfa,
budynki wejsciowe: skala wg drzwi (58 px) + wklejony kanoniczny modul drzwi (std-external-2); dekoracyjne: skala z szerokosci w prompcie (24 px/m).
Podglad na kaflu chodnika (miasto-kostka 32 px). Wynik: E:/ai/wyniki/krea_v2_diorama/"""
import glob, json, os, re
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
OUT = "E:/ai/wyniki/krea_v2_diorama"; os.makedirs(OUT, exist_ok=True)
PAL = np.array(json.load(open(r"E:\ai\skrzynka\odpowiedzi\world_palette.json", encoding="utf-8-sig")), np.int32)
K = "E:/ai/codex_paczki/budynki/wejsciowe-v2/"
MC = np.array(Image.open(K + "_drzwi-kanon-closed.png").convert("RGBA")); mh, mw = MC.shape[:2]; WYS_DRZWI = 58
tb = Image.new("RGBA", (mw, mh), (128, 128, 128, 255)); tb.alpha_composite(Image.fromarray(MC))
TPL = cv2.cvtColor(np.array(tb.convert("RGB")).astype(np.float32), cv2.COLOR_RGB2GRAY)
KAFEL = Image.open("E:/ai/wyniki/partia-22a/kafle/miasto-kostka/miasto-kostka_oryginal.png").convert("RGBA")
P = json.load(open("E:/ai/lora/prompty_podglad_10_v2.json", encoding="utf-8"))
SZER = [float(re.search(r"about ([\d.]+) m wide", p).group(1)) for p in P]
WYS = [float(re.search(r"m wide and ([\d.]+) m tall", p).group(1)) for p in P]
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia z domkiem", "szklarnia", "obserwatorium", "weterynarz", "kino"]
WEJ = {0, 1, 4, 6, 7, 8, 9}
ZRODLA = [("Krea 2 Turbo int8 + LoRA v2 (z Raw) · RTX 3080", "turbo",
           lambda j: glob.glob(f"E:/ai/runpod/wyniki/output/gen_v2lekkie_krea2turbo_512/samples/*__000002000_{j}.jpg")),
          ("Krea 2 Raw + LoRA v2 · podgląd z treningu", "raw",
           lambda j: glob.glob(f"E:/ai/runpod/wyniki/podglady/swiat2d_krea2raw_budynki_v2final_512/**/*__000002000_{j}.jpg", recursive=True)),
          ("Z-Image Turbo + LoRA v2 · podgląd z treningu", "zimage",
           lambda j: glob.glob(f"E:/ai/runpod/wyniki/podglady/swiat2d_zimageturbo_budynki_v2final_512/**/*__000002000_{j}.jpg", recursive=True))]
import sys   # python krea_v2_do_dioramy.py [kody po przecinku, np. zimage]
if len(sys.argv) > 1: ZRODLA = [z for z in ZRODLA if z[1] in sys.argv[1].split(",")]
SUF = "_".join(z[1] for z in ZRODLA)


def wytnij(im):
    a = np.array(im.convert("RGB")).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    tlo = (r > 150) & (b > 120) & (g < 120) & (r - g > 70) & (b - g > 50)
    fg = ndimage.binary_opening(~tlo, iterations=1)
    lab, n = ndimage.label(ndimage.binary_dilation(fg, iterations=2)); roz = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    m = ndimage.binary_erosion((lab == (np.argmax(roz) + 1)) & fg, iterations=2)   # bez rozowej obwodki z antyaliasingu modelu
    o = Image.fromarray(np.dstack([a, np.where(m, 255, 0)]).astype(np.uint8), "RGBA"); return o.crop(o.getchannel("A").getbbox())


def drzwi(im):
    g = cv2.cvtColor(np.array(im.convert("RGB")).astype(np.float32), cv2.COLOR_RGB2GRAY); H, W = g.shape; best = (-1, None)
    for s in np.arange(0.5, 4.01, 0.03):
        t = cv2.resize(TPL, (max(4, round(mw * s)), max(4, round(mh * s))), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= H * 0.7 or t.shape[1] >= W * 0.7: continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); r[:int(H * 0.4)] = -1
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]: best = (mx, (loc[0], loc[1], loc[0] + t.shape[1], loc[1] + t.shape[0]))
    return best


def paleta(img):
    a = np.array(img).astype(np.int32); al = a[..., 3] >= 128; rgb = a[..., :3][al]
    u, inv = np.unique(rgb, axis=0, return_inverse=True); m = PAL[((u[:, None] - PAL[None]) ** 2).sum(2).argmin(1)]
    o = np.zeros_like(a); o[..., :3][al] = m[inv.ravel()]; o[..., 3] = np.where(al, 255, 0); return o.astype(np.uint8)


def chodnik(w, h):
    t = Image.new("RGBA", (w, h))
    for y in range(0, h, KAFEL.height):
        for x in range(0, w, KAFEL.width): t.paste(KAFEL, (x, y))
    return t


wyn = []
for zn, kod, fn in ZRODLA:
    for j in range(10):
        f = fn(j)
        if not f: continue
        org = Image.open(f[0]).convert("RGB"); b = wytnij(org)
        info = {"zrodlo": zn, "kod": kod, "budynek": T[j], "plik": f[0], "szer_prompt_m": SZER[j], "wys_prompt_m": WYS[j]}
        if j in WEJ:
            sc, bb = drzwi(b); s = WYS_DRZWI / (bb[3] - bb[1]); info.update(pewnosc=round(sc, 2), metoda="skala wg drzwi")
        else:
            s = SZER[j] * 24 / b.width; bb = None; info.update(metoda="skala z promptu")
        gm = paleta(b.convert("RGBa").resize((max(1, round(b.width * s)), max(1, round(b.height * s))), Image.BOX).convert("RGBA"))
        if bb is not None:
            d = [round(v * s) for v in bb]; cx = (d[0] + d[2]) / 2
            px = max(0, min(gm.shape[1] - mw, int(round(cx - mw / 2)))); py = max(0, min(gm.shape[0], d[1] + WYS_DRZWI) - mh)
            gm[py:py + mh, px:px + mw] = np.where(MC[..., 3:4] > 0, MC, gm[py:py + mh, px:px + mw]); info["drzwi_xy"] = [px, py]
        for _ in range(3):   # fioletowe piksele na brzegu (resztki tla magenta) -> przezroczyste
            al = gm[..., 3] > 0; brzeg = al & ~ndimage.binary_erosion(al)
            c = gm[..., :3].astype(int); fio = (c[..., 0] - c[..., 1] > 15) & (c[..., 2] - c[..., 1] > 15)
            gm[brzeg & fio, 3] = 0
        gi = Image.fromarray(gm, "RGBA"); gi = gi.crop(gi.getchannel("A").getbbox())
        info.update(w_px=gi.width, h_px=gi.height, szer_m=round(gi.width / 24, 1), wys_m=round(gi.height / 24, 1))
        nm = f"{kod}_{j}_{T[j].replace(' ', '-')}"; gi.save(f"{OUT}/{nm}.png"); info["gra"] = f"{OUT}/{nm}.png"
        wyn.append((info, org))
        print(f"{nm:34} {info['metoda']:16} {gi.width:3}x{gi.height:3} px = {info['szer_m']:4} x {info['wys_m']:4} m (prompt {SZER[j]:g} x {WYS[j]:g} m)"
              + (f"  drzwi {info['pewnosc']}" if j in WEJ else ""))

F = ImageFont.truetype("arialbd.ttf", 20); FS = ImageFont.truetype("arial.ttf", 15)
WZ = [("apteka (gra)", K + "apteka-closed.png"), ("biblioteka (gra)", K + "biblioteka-closed.png")]
X = 2
for zn, kod, _ in ZRODLA:
    el = [(n, Image.open(p).convert("RGBA")) for n, p in WZ] + [(i["budynek"], Image.open(i["gra"])) for i, _ in wyn if i["kod"] == kod]
    W = sum(e.width for _, e in el) + 12 * (len(el) + 1); Hb = max(e.height for _, e in el); H = Hb + 40
    sc = chodnik(W, H); x = 12
    for n, e in el:
        sc.alpha_composite(e, (x, Hb - e.height + 10)); x += e.width + 12
    big = sc.resize((W * X, H * X), Image.NEAREST); sh = Image.new("RGB", (big.width, big.height + 70), (40, 48, 36)); sh.paste(big, (0, 70)); d = ImageDraw.Draw(sh)
    d.text((10, 8), f"MODEL: {zn} – format dioramy na chodniku (24 px = 1 m, powiększenie x{X}); po lewej 2 budynki z gry", font=F, fill=(255, 255, 255))
    x = 12
    for n, e in el:
        d.text((x * X, 42), n, font=FS, fill=(255, 230, 140)); x += e.width + 12
    sh.save(f"{OUT}/ulica_{kod}.png"); print("ulica", kod, sh.size)

X3 = 3; C = 300; pad = 16
maxw = max(i["w_px"] for i, _ in wyn) + 2 * pad; maxh = max(i["h_px"] for i, _ in wyn) + 2 * pad
RH = max(C, maxh * X3) + 30; CW = C + 16 + maxw * X3 + 30
sh = Image.new("RGB", (len(ZRODLA) * CW + 20, 70 + 10 * RH), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: " + " / ".join(z[0] for z in ZRODLA) + " – oryginał 512 px | po przeróbce do dioramy (x3) na chodniku. Wejściowe: skala wg drzwi + kanoniczne drzwi; dekoracyjne: skala z promptu",
       font=F, fill=(255, 255, 255))
for k, (zn, kod, _) in enumerate(ZRODLA):
    x0 = 10 + k * CW; d.text((x0, 40), zn, font=F, fill=(255, 230, 140))
    for r, (i, org) in enumerate([w for w in wyn if w[0]["kod"] == kod]):
        y = 70 + r * RH; sh.paste(org.resize((C, C), Image.LANCZOS), (x0, y))
        g = Image.open(i["gra"]); bg = chodnik(g.width + 2 * pad, g.height + 2 * pad); bg.alpha_composite(g, (pad, pad))
        big = bg.resize((bg.width * X3, bg.height * X3), Image.NEAREST); sh.paste(big.convert("RGB"), (x0 + C + 16, y + RH - 30 - big.height))
        d.text((x0, y + RH - 26), f"{i['budynek']}: {i['szer_m']:g} × {i['wys_m']:g} m w grze (prompt {i['szer_prompt_m']:g} × {i['wys_prompt_m']:g} m) · {i['metoda']}",
               font=FS, fill=(220, 225, 210))
sh.save(f"{OUT}/szczegoly_{SUF}.png"); print("szczegoly", sh.size)
json.dump([i for i, _ in wyn], open(f"{OUT}/lista_{SUF}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
