"""Pakiet lora-budynki-v3 (tylko 512): 72 budynki v2-final + nowe obiekty wybrane przez q3ok (etap 1, 2026-10-21/22).
Format jak v2: kadr ciasny (dluzszy bok 88% plotna, dol 6% nad krawedzia), skalowanie NEAREST x8 + BOX premultiplikowany, tlo magenta,
rozmiar w metrach w opisie. Zmiany opisow v2 -> v3: budka-pokazu bez "the serving window being the only opening in the front".
Kontrola opisow: brak zaprzeczen, brak sprzecznosci kamery (plaski dach vs spiczaste/kopuly), rozmiar zgodny ze sprite'em.
python budynki_pakiet_v3.py [lista nazw do pominiecia po przecinku]  -> E:/ai/lora/lora-budynki-v3/"""
import csv, json, os, re, shutil, sys
from PIL import Image
sys.path.insert(0, "E:/ai/lora")
import numpy as np
WYPELN, MAGENTA = 0.88, (255, 0, 255)   # jak budynki_pakiet_v2.py (nie importowac - ten skrypt przy imporcie przebudowuje pakiet v2)


def skaluj(im, s):
    """jak w v2: NEAREST x8, potem BOX na kolorach premultiplikowanych, alfa progowana"""
    w, h = round(im.width * s), round(im.height * s)
    big = im.resize((im.width * 8, im.height * 8), Image.NEAREST).convert("RGBa").resize((w, h), Image.BOX).convert("RGBA")
    a = np.array(big); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0); return Image.fromarray(a)
import budynki_v3_opisy_nowe as ON
V2 = "E:/ai/dioramaonline-lora/budynki/zbiory/v2-final"; ROB = "E:/ai/lora/lora-budynki-v3-robocze"; OUT = "E:/ai/lora/lora-budynki-v3"
POMIN = set(sys.argv[1].split(",")) if len(sys.argv) > 1 and sys.argv[1] else set()
POPRAWKI_V3 = {"budka-pokazu": (", the serving window being the only opening in the front.", ".")}
NEG = re.compile(r"\b(no|not|without|never|none|nothing|except|instead|only)\b", re.I)
SPICZ = re.compile(r"(pointed|dome|conical|half-round|tent|pyramid|gable)", re.I)


def sprawdz(n, cap, szer_m, wys_m):
    bl = []
    if NEG.search(cap): bl.append("zaprzeczenie: " + NEG.search(cap).group(0))
    tresc = cap.split(". Pixel art")[0]
    if "flat rectangular roof visible" in cap and SPICZ.search(tresc) and not re.search(r"(rising above|tower part|bell tower)", tresc): bl.append("plaski dach w kamerze + " + SPICZ.search(tresc).group(0))
    m = re.search(r"about (\d+) m wide and (\d+) m tall", cap)
    if not m or int(m.group(1)) != round(szer_m) or int(m.group(2)) != round(wys_m): bl.append("rozmiar")
    if cap.count("swiat2d style") != 1 or not cap.endswith("#FF00FF background."): bl.append("trigger/tlo")
    if "side door" in cap: bl.append("side door")
    return bl


rekordy = []
for l in open(f"{V2}/metadata.jsonl", encoding="utf-8"):
    m = json.loads(l); cap = m["caption"]
    if m["nazwa"] in POPRAWKI_V3: a, b = POPRAWKI_V3[m["nazwa"]]; assert a in cap; cap = cap.replace(a, b)
    rekordy.append({"nazwa": m["nazwa"], "zrodlo": "v2-final", "typ": m["typ"], "w_px": m["w_px"], "h_px": m["h_px"], "szer_m": m["szer_m"], "wys_sprite_m": m["wys_sprite_m"],
                    "drzwi": m.get("drzwi"), "caption": cap, "sprite": f"{V2}/sprites/{m['nazwa']}.png", "sprite_open": f"{V2}/sprites/{m['nazwa']}-open.png"})
for r in json.load(open(f"{ROB}/nowe.json", encoding="utf-8")):
    rekordy.append({"nazwa": r["nazwa"], "zrodlo": "nowe: " + r["zrodlo_id"], "typ": r["typ"], "w_px": r["w_px"], "h_px": r["h_px"], "szer_m": r["szer_m"], "wys_sprite_m": r["wys_sprite_m"],
                    "drzwi": r.get("drzwi"), "caption": ON.caption(r), "sprite": f"{ROB}/sprites/{r['nazwa']}.png", "obraz_wygenerowany": r["plik"]})
bledy = {r["nazwa"]: sprawdz(r["nazwa"], r["caption"], r["szer_m"], r["wys_sprite_m"]) for r in rekordy}
bledy = {k: v for k, v in bledy.items() if v}
if bledy: print("BLEDY OPISOW:", bledy); sys.exit(1)
rekordy = [r for r in rekordy if r["nazwa"] not in POMIN]
for d in ("train_512", "sprites"): shutil.rmtree(f"{OUT}/{d}", ignore_errors=True); os.makedirs(f"{OUT}/{d}")
P = 512
for r in rekordy:
    im = Image.open(r["sprite"]).convert("RGBA"); shutil.copy(r["sprite"], f"{OUT}/sprites/{r['nazwa']}.png")
    if os.path.exists(r.get("sprite_open", "")): shutil.copy(r["sprite_open"], f"{OUT}/sprites/{r['nazwa']}-open.png")
    s = WYPELN * P / max(im.width, im.height); b = skaluj(im, s)
    x, y = (P - b.width) // 2, P - round((1 - WYPELN) / 2 * P) - b.height
    c = Image.new("RGBA", (P, P), MAGENTA + (255,)); c.alpha_composite(b, (x, y))
    c.convert("RGB").save(f"{OUT}/train_512/{r['nazwa']}.png"); open(f"{OUT}/train_512/{r['nazwa']}.txt", "w", encoding="utf-8").write(r["caption"])
    r["kadr_512"] = {"skala": round(s, 4), "px_na_m": round(24 * s, 2), "bbox": [x, y, b.width, b.height]}
with open(f"{OUT}/metadata.jsonl", "w", encoding="utf-8") as f:
    for r in rekordy: f.write(json.dumps({k: v for k, v in r.items() if k not in ("sprite", "sprite_open")}, ensure_ascii=False) + "\n")
with open(f"{OUT}/captions.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(["nazwa", "zrodlo", "typ", "szer_m", "wys_sprite_m", "caption"])
    for r in rekordy: w.writerow([r["nazwa"], r["zrodlo"], r["typ"], r["szer_m"], r["wys_sprite_m"], r["caption"]])
K, T = 10, 160; ark = Image.new("RGB", (K * T, -(-len(rekordy) // K) * T), (40, 40, 40))
for i, r in enumerate(rekordy): ark.paste(Image.open(f"{OUT}/train_512/{r['nazwa']}.png").resize((T - 4, T - 4), Image.BOX), ((i % K) * T + 2, (i // K) * T + 2))
ark.save(f"{OUT}/podglad.png")
print(len(rekordy), "obiektow (v2:", sum(r["zrodlo"] == "v2-final" for r in rekordy), ", nowe:", sum(r["zrodlo"] != "v2-final" for r in rekordy), "), pominiete:", sorted(POMIN))
