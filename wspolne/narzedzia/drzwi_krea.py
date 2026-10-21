"""Krea 2 Turbo: czy we WSZYSTKICH wygenerowanych budynkach wejsciowych da sie podmienic drzwi na kanoniczne (jak drzwi_v1_ocena.py).
Zestawy: LoRA v1 + prompty v1 (seed 42+i, int8 RTX 3080), nowe seedy 1001-5005, uzdatnione v1/J/K (seed 271828, RunPod bf16),
LoRA v1 + prompty v2 (RunPod bf16), LoRA v2 + prompty v2 (int8 RTX 3080). Skala wzorca szeroka (0.5-4x), bo w v2 budynek wypelnia kadr.
Wynik: wyniki/drzwi_krea.csv, wyniki/drzwi_krea_arkusz.png"""
import csv, glob, json, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
src = open("E:/ai/runpod/drzwi_v1_ocena.py", encoding="utf-8").read(); ns = {}
exec(src[:src.index("rows, kom = [], []")].replace('src = open("E:/ai/runpod/zestawienie_v1.py"', 'src = open("E:/ai/runpod/zestawienie_v1.py"'), ns)
TPL, WEJ, bbox_budynku = ns["TPL"], ns["WEJ"], ns["bbox_budynku"]
def znajdz(im):
    a = np.array(im.convert("RGB")); g = cv2.cvtColor(a.astype(np.float32), cv2.COLOR_RGB2GRAY); H, W = g.shape; ocz = H / 512; best = (-1, None, None)
    for s in np.arange(0.5, 4.01, 0.04) * ocz:
        t = cv2.resize(TPL, (max(4, round(TPL.shape[1] * s)), max(4, round(TPL.shape[0] * s))), interpolation=cv2.INTER_AREA)
        if t.shape[0] >= H * 0.6 or t.shape[1] >= W * 0.6: continue
        r = cv2.matchTemplate(g, t, cv2.TM_CCOEFF_NORMED); r[:int(H * 0.3)] = -1
        _, mx, _, loc = cv2.minMaxLoc(r)
        if mx > best[0]: best = (mx, (loc[0], loc[1], loc[0] + t.shape[1], loc[1] + t.shape[0]), s / ocz)
    return best, bbox_budynku(a)
G = "E:/ai/runpod/wyniki/output/"
def g(p): x = glob.glob(p); return x[0] if x else None
r = ns["ns"] if "ns" in ns else None
src2 = open("E:/ai/runpod/ranking_artefakt.py", encoding="utf-8").read(); n2 = {}; exec(src2[:src2.index("ZESTAWY = ")], n2); n2["b64"] = lambda f: f
v1 = [w for w in n2["zestaw_v1v1"]()["wiersze"] if w["id"] == "zestawienie_krea2turbo_lora_raw512"][0]["obrazy"]
ZEST = [("LoRA v1 · prompt v1 · seed 42+i", lambda j: v1.get(j))]
for s in (1001, 2002, 3003, 4004, 5005):
    ZEST.append((f"LoRA v1 · prompt v1 · seed {s}", lambda j, s=s: (lambda p: p if os.path.exists(p) else None)(f"E:/ai/wyniki/seedy_top3_v1/zestawienie_krea2turbo_lora_raw512_{j}_s{s}.png")))
for k, o in (("v1", 0), ("J", 10), ("K", 20)):
    ZEST.append((f"LoRA v1 · uzdatniony {k} · seed 271828" if k != "v1" else "LoRA v1 · prompt v1 · seed 271828", lambda j, o=o: g(f"{G}gen_uzd_krea2turbo_512/samples/*__000000000_{j + o}.jpg")))
ZEST.append(("LoRA v1 · prompt v2 · seed 42+i", lambda j: g(f"{G}gen_v1lora_v2prompty_krea2turbo_512/samples/*__000000000_{j}.jpg")))
ZEST.append(("LoRA v2 · prompt v2 · seed 42+i", lambda j: g(f"{G}gen_v2lekkie_krea2turbo_512/samples/*__000002000_{j}.jpg")))
rows, kom = [], []
for zn, fn in ZEST:
    for j, (bud, ocz_poz) in WEJ.items():
        f = fn(j)
        if not f: continue
        im = Image.open(f).convert("RGB"); (sc, bb, skala), (bx0, by0, bx1, by1) = znajdz(im)
        cx = ((bb[0] + bb[2]) / 2 - bx0) / max(1, bx1 - bx0); poz = "srodek" if 0.35 <= cx <= 0.65 else ("lewo" if cx < 0.35 else "prawo")
        dol = abs(bb[3] - by1) / max(1, by1 - by0); wyk = sc >= 0.55; poz_ok = poz == ocz_poz; dol_ok = dol <= 0.12
        wer = ("brak drzwi" if not wyk else "podmiana OK" if (poz_ok and dol_ok) else
               "do poprawy: " + ", ".join(x for x, ok in (("położenie", poz_ok), ("nie na ziemi", dol_ok)) if not ok))
        rows.append({"zestaw": zn, "budynek": bud, "pewnosc": round(sc, 2), "polozenie": poz, "oczekiwane": ocz_poz, "skala": round(skala, 2), "dol_odstep": round(dol, 2), "werdykt": wer, "plik": os.path.basename(f)})
        kom.append((zn, bud, im, bb, wer))
with open("E:/ai/runpod/wyniki/drzwi_krea.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter=";"); w.writeheader(); w.writerows(rows)
C, LW = 210, 330; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 15)
zs = [z for z, _ in ZEST if any(k[0] == z for k in kom)]
sh = Image.new("RGB", (LW + 7 * (C + 4), 70 + len(zs) * (C + 26) + 10), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: Krea 2 Turbo + LoRA budynki (z Krea 2 Raw, 512) – drzwi w budynkach wejściowych: ramka = znalezione drzwi", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
for j, (bud, ozp) in enumerate(WEJ.values()): d.text((LW + j * (C + 4) + 4, 46), f"{bud} ({ozp})", font=F, fill=(255, 230, 140))
KOL = {"podmiana OK": (90, 220, 110), "brak drzwi": (240, 80, 70)}
for zn, bud, im, bb, wer in kom:
    i = zs.index(zn); j = [v[0] for v in WEJ.values()].index(bud); y = 70 + i * (C + 26); x = LW + j * (C + 4)
    if j == 0 or not any(k[0] == zn and k[1] == list(WEJ.values())[0][0] for k in kom):
        d.multiline_text((10, y + 10), zn.replace(" · ", "\n"), font=FS, fill=(230, 235, 220))
    v = im.copy(); kol = KOL.get(wer, (240, 190, 60)); ImageDraw.Draw(v).rectangle(bb, outline=kol, width=max(3, im.width // 120))
    sh.paste(v.resize((C, C), Image.LANCZOS), (x, y)); d.text((x + 2, y + C + 3), wer[:30], font=FS, fill=kol)
sh.save("E:/ai/runpod/wyniki/drzwi_krea_arkusz.png")
from collections import Counter
print("lacznie", len(rows), Counter(r["werdykt"].split(":")[0] for r in rows))
for z in zs:
    rr = [r for r in rows if r["zestaw"] == z]
    print(f"{z:42s} OK {sum(r['werdykt'] == 'podmiana OK' for r in rr)}/{len(rr)}  do poprawy {sum(r['werdykt'].startswith('do') for r in rr)}  brak {sum(r['werdykt'] == 'brak drzwi' for r in rr)}")
for r in rows:
    if r["werdykt"] != "podmiana OK": print(" ", r["zestaw"], "|", r["budynek"], "|", r["werdykt"], r["pewnosc"], r["polozenie"])
