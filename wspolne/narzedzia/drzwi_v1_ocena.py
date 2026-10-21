"""Czy w budynkach wejsciowych (LoRA v1, prompty v1) da sie podmienic drzwi na nasze kanoniczne (std-external-2, 59x58 px w skali gry)?
Dla kazdego z 19 wierszy x 7 budynkow wejsciowych: dopasowanie wzorca drzwi (cv2, skala 0.5-2.0 wzgledem oczekiwanej),
sprawdzenie: (1) wykryte (pewnosc >= 0.55), (2) polozenie zgodne z promptem (srodek / prawo), (3) rozmiar zgodny ze skala gry (0.8-1.25),
(4) dol drzwi na dole budynku (linia gruntu). Rozmiar = ile przeskalowac budynek, zeby drzwi mialy 58 px (informacja, nie blokuje). Wynik: wyniki/drzwi_v1_arkusz.png, wyniki/drzwi_v1.csv + podsumowanie."""
import csv, glob, json, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

kan = Image.open("E:/ai/codex_paczki/budynki/wejsciowe-v2/_drzwi-kanon-closed.png").convert("RGBA")
tb = Image.new("RGBA", kan.size, (128, 128, 128, 255)); tb.alpha_composite(kan)
TPL = cv2.cvtColor(np.array(tb.convert("RGB")).astype(np.float32), cv2.COLOR_RGB2GRAY)
WEJ = {0: ("kwiaciarnia", "prawo"), 1: ("hotel", "srodek"), 4: ("dom turkusowy", "srodek"), 6: ("szklarnia", "srodek"),
       7: ("obserwatorium", "srodek"), 8: ("weterynarz", "srodek"), 9: ("kino", "srodek")}
src = open("E:/ai/runpod/zestawienie_v1.py", encoding="utf-8").read(); ns = {}; exec(src[:src.index("\nT = [")], ns)
oceny = {}
for f in glob.glob("E:/ai/runpod/ranking_oceny/ocena/*.json"):
    _, w, b = os.path.basename(f)[:-5].split("__"); oceny[(w, int(b))] = json.load(open(f, encoding="utf-8")).get("ocena")


def bbox_budynku(a):
    m = ~((a[..., 0] > 150) & (a[..., 2] > 140) & (a[..., 1] < 140))           # nie-tlo (magenta / rozowe tlo)
    kol = np.where(m.mean(0) > 0.15)[0]; wie = np.where(m.mean(1) > 0.15)[0]  # kolumny/wiersze z istotna trescia (odporne na szum)
    return (kol.min(), wie.min(), kol.max(), wie.max()) if len(kol) and len(wie) else (0, 0, a.shape[1] - 1, a.shape[0] - 1)


def znajdz(im):
    a = np.array(im.convert("RGB")); g = cv2.cvtColor(a.astype(np.float32), cv2.COLOR_RGB2GRAY); H, W = g.shape
    ocz = H / 512   # oczekiwany mnoznik: zbior v1 512 = 1 px gry na px, 1024 = 2 px
    best = (-1, None, None)
    for s in np.arange(0.5, 2.01, 0.03) * ocz:
        t = cv2.resize(TPL, (max(4, round(TPL.shape[1] * s)), max(4, round(TPL.shape[0] * s))), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= H or t.shape[1] >= W: continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); r[:int(H * 0.3)] = -1
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]: best = (mx, (loc[0], loc[1], loc[0] + t.shape[1], loc[1] + t.shape[0]), s / ocz)
    return best, bbox_budynku(a)


rows, kom = [], []
for m, lora, res, kat, gdzie in ns["WIERSZE"]:
    w = os.path.basename(kat); fs = glob.glob(f"{kat}/**/*.jpg", recursive=True)
    kroki = {int(os.path.basename(f).split("__")[1].split("_")[0]) for f in fs}
    k = max(x for x in kroki if sum(1 for f in fs if f"__{x:09d}_" in f) >= 4)
    for j, (bud, ocz_poz) in WEJ.items():
        f = [x for x in fs if f"__{k:09d}_{j}." in x]
        if not f: continue
        im = Image.open(f[0]).convert("RGB"); (sc, bb, skala), (bx0, by0, bx1, by1) = znajdz(im)
        cx = ((bb[0] + bb[2]) / 2 - bx0) / max(1, bx1 - bx0)
        poz = "srodek" if 0.35 <= cx <= 0.65 else ("lewo" if cx < 0.35 else "prawo")
        dol = abs(bb[3] - by1) / max(1, by1 - by0)          # odleglosc dolu drzwi od dolu budynku (czesc wysokosci budynku)
        wyk = sc >= 0.55; poz_ok = poz == ocz_poz; skala_ok = 0.8 <= skala <= 1.25; dol_ok = dol <= 0.12
        # rozmiar nie blokuje podmiany: budynek i tak skalujemy tak, by drzwi mialy 58 px (skala gry) - podajemy tylko potrzebna skale
        werdykt = ("brak drzwi" if not wyk else "podmiana OK" if (poz_ok and dol_ok) else
                   "do poprawy: " + ", ".join(x for x, ok in (("położenie", poz_ok), ("nie na ziemi", dol_ok)) if not ok))
        rows.append({"model": m, "wariant": f"{lora} {res}", "wiersz": w, "budynek": bud, "ocena": oceny.get((w, j)) or "", "pewnosc": round(sc, 2),
                     "polozenie": poz, "oczekiwane": ocz_poz, "skala": round(skala, 2), "dol_odstep": round(dol, 2), "werdykt": werdykt})
        kom.append((m, f"{lora} {res}", bud, im, bb, werdykt))
with open("E:/ai/runpod/wyniki/drzwi_v1.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter=";"); wr.writeheader(); wr.writerows(rows)
# arkusz: wiersz = model, kolumna = budynek wejsciowy, ramka drzwi + werdykt
C = 220; LW = 300; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 15)
modele = []; [modele.append((a, b)) for a, b, *_ in kom if (a, b) not in modele]
sh = Image.new("RGB", (LW + 7 * (C + 4), 70 + len(modele) * (C + 44) + 30), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "Drzwi w budynkach wejściowych (LoRA v1, prompty v1): czy da się podmienić na nasze kanoniczne?", font=ImageFont.truetype("arialbd.ttf", 24), fill=(255, 255, 255))
for j, (bud, ocz) in enumerate(WEJ.values()): d.text((LW + j * (C + 4) + 4, 46), f"{bud} ({ocz})", font=F, fill=(255, 230, 140))
KOL = {"podmiana OK": (90, 220, 110), "brak drzwi": (240, 80, 70)}
for (m, war, bud, im, bb, wer) in kom:
    i = modele.index((m, war)); j = [v[0] for v in WEJ.values()].index(bud); y = 70 + i * (C + 44); x = LW + j * (C + 4)
    if j == 0: d.text((10, y + 10), m, font=F, fill=(255, 255, 255)); d.text((10, y + 36), war, font=FS, fill=(200, 210, 190))
    v = im.copy(); kol = KOL.get(wer, (240, 190, 60)); ImageDraw.Draw(v).rectangle(bb, outline=kol, width=max(3, im.width // 120))
    sh.paste(v.resize((C, C), Image.LANCZOS), (x, y)); r_ = [r for r in rows if r["model"] == m and r["wariant"] == war and r["budynek"] == bud][0]
    d.text((x + 2, y + C + 3), (wer[:22] + (f"  skala x{1 / r_['skala']:.2f}" if wer != "brak drzwi" else ""))[:34], font=FS, fill=kol)
sh.save("E:/ai/runpod/wyniki/drzwi_v1_arkusz.png")
from collections import Counter
print(Counter(r["werdykt"].split(":")[0] for r in rows))
for (m, war) in modele:
    rr = [r for r in rows if r["model"] == m and r["wariant"] == war]
    print(f"{m:28s} {war:30s} OK {sum(r['werdykt'] == 'podmiana OK' for r in rr)}/7  brak {sum(r['werdykt'] == 'brak drzwi' for r in rr)}  "
          f"do poprawy {sum(r['werdykt'].startswith('do') for r in rr)}")
