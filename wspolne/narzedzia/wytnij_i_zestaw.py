"""Wycina pojedyncze budynki z obrazow modeli zewnetrznych i sklada tabele jak dla naszych LoRA:
kolumny = 10 budynkow testowych, wiersze = model + wersja promptow (+ wariant, gdy model narysowal budynek kilka razy).
Ramki: wyniki/_wycinki/_podglad/ramki.json (wykryte automatycznie, podglady z numerami w _podglad/), przypisanie budynkow RECZNIE w PRZYPISANIE
(modele rysuja siatki/duplikaty, wiec automat sie myli). Gdy budynki sie stykaja: zakresy x w ZAKRESY_X.
Wynik: wyniki/zestawienie_modele_zewnetrzne_budynki.png + wycinki w wyniki/_wycinki/."""
import json, os, time
import numpy as np
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__)); W = f"{D}/wyniki"; WY = f"{W}/_wycinki"
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia z domkiem", "szklarnia", "obserwatorium", "weterynarz", "kino"]
RAMKI = {k.replace("\\", "/"): v for k, v in json.load(open(f"{WY}/_podglad/ramki.json")).items()}
# (model, wersja, wariant): [(plik, {kolumna: nr ramki})]
PRZYPISANIE = {
    ("chatgpt", "v1", 1): [("chatgpt/pasek_wejsciowe_v1.png", {0: 0, 1: 1, 4: 2, 6: 3, 7: 4, 8: 5, 9: 6}), ("chatgpt/paski_dekoracyjne_v1.png", {2: 1, 3: 2, 5: 0})],
    ("chatgpt", "v2", 1): [("chatgpt/paski_wejsciowe_v2.png", {0: "x0", 1: "x1", 4: "x2", 6: "x3", 7: "x4", 8: "x5", 9: "x6"}), ("chatgpt/paski_dekoracyjne_v2.png", {2: 1, 3: 2, 5: 0})],
    ("gemini", "v1", 1): [("gemini/pasek_wejsciowe_v1.jfif", {0: 0, 1: 5, 4: 1, 6: 6, 7: 2, 8: 3, 9: 8}), ("gemini/pasek_dekoracyjne_v1.jfif", {2: 0, 3: 1, 5: 4})],
    ("gemini", "v1", 2): [("gemini/pasek_wejsciowe_v1.jfif", {0: 4, 8: 7}), ("gemini/pasek_dekoracyjne_v1.jfif", {2: 2, 3: 3})],
    ("gemini", "v2", 1): [("gemini/pasek_wejsciowe_v2.jfif", {0: 0, 1: 1, 4: 2, 6: 3, 7: 5, 8: 6, 9: 7}), ("gemini/pasek_dekoracyjne_v2.jfif", {2: 0, 3: 1, 5: 2})],
    ("gemini", "v2", 2): [("gemini/pasek_wejsciowe_v2.jfif", {0: 4}), ("gemini/pasek_dekoracyjne_v2.jfif", {2: 3, 3: 4})],
    ("gemini-banana", "v1", 1): [("gemini-banana/pasek_wejsciowe_v1_part1.jfif", {0: 0, 1: 6, 4: 7, 6: 2, 7: 3, 8: 4, 9: 9})],
    ("gemini-banana", "v1", 2): [("gemini-banana/pasek_wejsciowe_v1_part1.jfif", {0: 5, 8: 8})],
    ("gemini-banana", "v1", 3): [("gemini-banana/paski_wejsciowe_v1_part2.jfif", {0: 0, 1: 6, 4: 7, 6: 2, 7: 3, 8: 4, 9: 9})],
    ("gemini-banana", "v1", 4): [("gemini-banana/paski_wejsciowe_v1_part2.jfif", {0: 5, 8: 8})],
}
ZAKRESY_X = {"chatgpt/paski_wejsciowe_v2.png": [(20, 299), (302, 601), (603, 853), (856, 1197), (1200, 1504), (1507, 1772), (1773, 2156)]}
OPIS = {("gemini-banana", "v1", 3): "druga generacja", ("gemini-banana", "v1", 4): "druga generacja"}


def maska(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return ~((r > 170) & (b > 170) & (g < 110))


def wycinek(plik, nr):
    im = Image.open(f"{W}/{plik}").convert("RGB")
    if isinstance(nr, str): x0, x1 = ZAKRESY_X[plik][int(nr[1:])]; box = [x0, 0, x1, im.height]
    else: box = RAMKI[f"wyniki/{plik}"][nr]
    c = im.crop(box); m = maska(np.array(c)); ys, xs = np.where(m)
    return c.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


wiersze = {}
for k, lista in PRZYPISANIE.items():
    for plik, mapa in lista:
        for kol, nr in mapa.items():
            im = wycinek(plik, nr); wiersze.setdefault(k, {})[kol] = im
            im.save(f"{WY}/{k[0]}_{k[1]}_w{k[2]}_{T[kol].replace(' ', '_')}.png")

C, LW = 260, 300; F = ImageFont.truetype("arialbd.ttf", 20); FS = ImageFont.truetype("arial.ttf", 17)
klucze = list(PRZYPISANIE)
sh = Image.new("RGB", (LW + 10 * (C + 4), 70 + len(klucze) * (C + 4) + 40), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "Modele zewnętrzne: budynki wycięte z wyników (wzór stylu + prompt v1/v2)", font=ImageFont.truetype("arialbd.ttf", 26), fill=(255, 255, 255))
for j, t in enumerate(T): d.text((LW + j * (C + 4) + 6, 44), t, font=F, fill=(255, 230, 140))
for i, k in enumerate(klucze):
    y = 70 + i * (C + 4); m, v, war = k
    linie = [m, f"prompty {v}"] + ([f"wariant {war}" + (f" ({OPIS[k]})" if k in OPIS else "")] if war > 1 or (m, v, 2) in PRZYPISANIE else [])
    for n_, s in enumerate(linie): d.text((10, y + 10 + n_ * 26), s, font=F if n_ == 0 else FS, fill=(255, 255, 255) if n_ == 0 else (200, 210, 190))
    for j in range(10):
        x0 = LW + j * (C + 4); im = wiersze[k].get(j)
        d.rectangle([x0, y, x0 + C, y + C], fill=(255, 0, 255) if im else (30, 34, 28))
        if im:
            s_ = min((C - 8) / im.width, (C - 8) / im.height); r = im.resize((max(1, round(im.width * s_)), max(1, round(im.height * s_))), Image.LANCZOS)
            sh.paste(r, (x0 + (C - r.width) // 2, y + C - 4 - r.height))
        else: d.text((x0 + 100, y + C // 2 - 10), "brak", font=FS, fill=(120, 120, 110))
d.text((10, sh.height - 32), "Każdy budynek dopasowany do ramki osobno (rozmiary między ramkami nie są porównywalne). Wariant = model narysował budynek kilka razy. Gemini Banana: tylko prompty v1, budynki z wejściem.", font=FS, fill=(180, 180, 170))
out = f"{W}/zestawienie_modele_zewnetrzne_budynki.png"
try: sh.save(out)
except OSError: out = time.strftime(f"{W}/zestawienie_modele_zewnetrzne_budynki_%H%M.png"); sh.save(out)
print(out, sh.size)
