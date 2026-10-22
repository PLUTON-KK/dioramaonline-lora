"""Paleta 128 narzucona od gory, BLISKO RZECZYWISTOSCI (q3ok 2026-10-22): 16 ramp x 8 stopni jasnosci.
Kazda rampa zbudowana wokol typowego, rzeczywistego koloru materialu (wzorzec sRGB): odcien i nasycenie z wzorca (LCh),
stopnie jasnosci L* od cienia do swiatla; wzorzec trafia dokladnie w najblizszy mu stopien. Hue shift jak w pixel arcie
(cienie chlodniejsze, swiatla cieplejsze, slabszy dla ramp naturalnych), nasycenie maleje ku skrajom.
Rampa szarosci zaczyna sie gleboka czernia #0B0B10 i konczy czystym bialym #FFFFFF. Magenta tla daleko od palety.
Wynik: E:/ai/dioramaonline-lora/wspolne/paleta128.json, paleta128.png"""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
PL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paleta128.json")

def lab(rgb):
    c = np.asarray(rgb, float) / 255; c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    xyz = c @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)



L_ST = [10, 21, 32, 43, 54, 65, 77, 90]
# (nazwa, wzorzec rzeczywisty sRGB, sila hue shift)
RAMPY = [("asfalt / beton (szarość)", (154, 154, 150), 0.3), ("ciepła szarość: kamień / tynk kremowy", (200, 188, 165), 0.5),
         ("tynk brzoskwiniowy", (227, 176, 143), 0.6), ("cegła", (139, 58, 43), 0.8), ("dachówka / terakota", (181, 86, 47), 0.8),
         ("drewno (dąb)", (160, 112, 63), 0.8), ("piasek / ochra", (216, 192, 138), 0.6), ("trawa", (94, 154, 50), 0.6),
         ("liście / ciemna zieleń", (47, 93, 42), 0.6), ("błękit: woda → niebo / szkło", (88, 150, 190), 0.5),
         ("łupek / stal niebieska", (74, 85, 96), 0.4), ("czerwień farby / znaki", (200, 48, 42), 1.0), ("żółć znaków / światła", (242, 194, 0), 1.0),
         ("pomarańcz (pachołki, ostrzeżenia, jesień)", (232, 130, 40), 1.0), ("granat (farby, markizy, tkaniny)", (45, 55, 120), 0.8),
         ("kwiaty / fiolet", (150, 90, 160), 1.0)]


def lch2rgb(L, C, h):
    a, b = C * np.cos(np.radians(h)), C * np.sin(np.radians(h))
    fy = (L + 16) / 116; fx, fz = fy + a / 500, fy - b / 200
    t = np.array([fx, fy, fz]); xyz = np.where(t ** 3 > 0.008856, t ** 3, (t - 16 / 116) / 7.787) * np.array([0.95047, 1.0, 1.08883])
    lin = np.linalg.solve(np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]), xyz)
    return np.where(lin > 0.0031308, 1.055 * np.abs(lin) ** (1 / 2.4) * np.sign(lin) - 0.055, 12.92 * lin) * 255


def kolor(L, C, h):
    for _ in range(80):
        rgb = lch2rgb(L, C, h)
        if (rgb >= -0.5).all() and (rgb <= 255.5).all(): return np.clip(np.round(rgb), 0, 255).astype(int)
        C *= 0.94
    return np.clip(np.round(lch2rgb(L, 0, h)), 0, 255).astype(int)


L_KOL = [16, 26, 36, 46, 56, 66, 77, 88]   # rampy kolorowe: bez skrajnej czerni i bieli (tylko szarosci maja pelny zakres)


def rampa(wz, sila, Lst=L_KOL):
    Lw, a, b = lab(np.array([wz], float))[0]; C0, h0 = np.hypot(a, b), np.degrees(np.arctan2(b, a))
    kw = int(np.argmin([abs(L - Lw) for L in Lst])); Ls = list(Lst); Ls[kw] = Lw             # wzorzec trafia w najblizszy stopien
    out = []
    for n, L in enumerate(Ls):
        if n == kw: out.append(np.array(wz)); continue
        dL = (L - Lw) / 80
        h = h0 + sila * (12 * dL if dL > 0 else 16 * dL)                                       # swiatla cieplej, cienie chlodniej
        C = max(C0 * max(0.55, 1 - 0.7 * abs(dL)), min(C0, 10)) * (1 + 0.15 * sila * (dL < 0))   # nasycenie spada lagodnie - rampa trzyma charakter
        out.append(kolor(L, C, h))
    return out


if __name__ == "__main__":
    P = []
    CIEPLE = {"cegła", "dachówka / terakota", "czerwień farby / znaki", "pomarańcz (pachołki, ostrzeżenia, jesień)", "drewno (dąb)"}
    L_CIEP = [16, 26, 36, 46, 56, 65, 73, 81]   # ciepłe rampy: najjaśniejszy stopień niżej, żeby nie dublowały bladej brzoskwini tynku
    for r, (nazwa, wz, sila) in enumerate(RAMPY): P += rampa(wz, sila, L_ST if r == 0 else (L_CIEP if nazwa in CIEPLE else L_KOL))
    P = np.array(P); P[0] = [11, 11, 16]; P[7] = [255, 255, 255]                                 # szarosci: od czerni do bieli
    Lp = lab(P); d = np.sqrt(((Lp[:, None] - Lp[None]) ** 2).sum(-1)); np.fill_diagonal(d, 1e9)
    mag = float(np.sqrt(((Lp - lab(np.array([[255, 0, 255]]))) ** 2).sum(-1)).min())
    stat = {"min_dE_miedzy_kolorami": round(float(d.min()), 1), "mediana_min_dE": round(float(np.median(d.min(1))), 1), "par_ponizej_dE5": int((d < 5).sum() // 2),
            "min_dE_do_magenty_tla": round(mag, 1)}
    json.dump({"opis": "Paleta swiata 128 (q3ok 2026-10-22), narzucona od gory, blisko rzeczywistosci: 16 ramp x 8 stopni jasnosci wokol rzeczywistych kolorow materialow; "
               "rampa szarosci od czerni #0B0B10 do bieli #FFFFFF. Kolejnosc: rampa po rampie, od ciemnego do jasnego.",
               "rampy": [{"nazwa": r[0], "wzorzec": list(r[1])} for r in RAMPY], "statystyka": stat, "kolory": P.tolist()}, open(PL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    C_ = 36; F = ImageFont.truetype("arial.ttf", 14)
    im = Image.new("RGB", (8 * C_ + 360, len(RAMPY) * C_ + 20), (236, 233, 224)); dr = ImageDraw.Draw(im)
    for r, (nazwa, wz, _) in enumerate(RAMPY):
        for n in range(8):
            x, y = 10 + n * C_, 10 + r * C_; c = tuple(int(v) for v in P[r * 8 + n]); dr.rectangle([x, y, x + C_ - 2, y + C_ - 2], fill=c)
            if c == tuple(wz): dr.rectangle([x + 2, y + 2, x + C_ - 4, y + C_ - 4], outline=(255, 255, 255) if sum(c) < 380 else (0, 0, 0))
        dr.text((20 + 8 * C_, 10 + r * C_ + 10), nazwa, font=F, fill=(30, 30, 30))
    im.save(os.path.join(os.path.dirname(PL), "paleta128.png")); print(stat)
