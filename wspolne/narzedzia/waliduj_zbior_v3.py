"""Walidator grafik (sprawdz_grafike.py) na zbiorze budynki v3-final.
v2 (58): para gry closed/open + metadane z codex_paczki (zrodlo z metadata v2-final); nowe (30): sprite z przerobki + obraz generatora (P2).
Wynik: E:/ai/wyniki/walidacja_v3/wyniki.csv, podsumowanie.txt, arkusz_fail.png"""
import csv, json, os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sprawdz_grafike as S
from PIL import Image, ImageDraw, ImageFont
V3 = "E:/ai/lora/lora-budynki-v3"; V2 = "E:/ai/dioramaonline-lora/budynki/zbiory/v2-final"; ROB = "E:/ai/lora/lora-budynki-v3-robocze"
OUT = "E:/ai/wyniki/walidacja_v3"; os.makedirs(OUT, exist_ok=True)
DRZWI = json.load(open("E:/ai/codex_paczki/budynki/wejsciowe-v2/_drzwi-kanon.json", encoding="utf-8"))
m2 = {json.loads(l)["nazwa"]: json.loads(l) for l in open(f"{V2}/metadata.jsonl", encoding="utf-8")}
nowe = {r["nazwa"]: r for r in json.load(open(f"{ROB}/nowe.json", encoding="utf-8"))}
wyn, IDS = [], ["P1", "P2", "P3", "P4", "P5", "P6", "K1", "K2", "K3", "K4", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "B1", "M"]
for l in open(f"{V3}/metadata.jsonl", encoding="utf-8"):
    r = json.loads(l); n = r["nazwa"]; typ = r["typ"]
    if r["zrodlo"] == "v2-final":
        z = m2[n]["zrodlo"].replace("\\", "/"); closed = z if os.path.exists(z) else f"{V3}/sprites/{n}.png"
        op = closed.replace("-closed.png", "-open.png") if "-closed" in closed else None
        mj = closed.replace(".png", ".json"); meta = json.load(open(mj, encoding="utf-8")) if os.path.exists(mj) else None
        if meta is None: meta = {"image": {"w": r["w_px"], "h": r["h_px"]}, "metric": {"width_m": r["szer_m"]}}
        zrodlo = None
    else:
        nn = nowe[n]; closed = f"{ROB}/sprites/{n}.png"; op = None; zrodlo = nn["plik"]
        meta = {"image": {"w": nn["w_px"], "h": nn["h_px"]}, "anchor": {"x": nn["w_px"] / 2, "y": nn["h_px"]}, "metric": {"width_m": nn["szer_m"]}}
        if typ == "wejsciowy" and nn.get("drzwi"):
            d = nn["drzwi"]; dw = DRZWI["doorwayInModule"]
            meta["doors"] = [{"module": "std-external-2", "placement": {"x": d["x_px"], "y": d["y_px"]},
                              "doorway": {"x": d["x_px"] + dw["x"], "y": d["y_px"] + dw["y"], "w": dw["w"], "h": dw["h"]},
                              "changedRegion": {"x": d["x_px"] + dw["x"], "y": d["y_px"] + dw["y"], "w": dw["w"], "h": dw["h"]}}]
    w = S.sprawdz(closed, op, meta, typ, zrodlo, opis=r["caption"])
    wyn.append({"nazwa": n, "zrodlo": "v2" if r["zrodlo"] == "v2-final" else "nowy", "typ": typ, "plik": closed, **{k: w.get(k, ("", ""))[0] for k in IDS}, "profil": "plaski dach" if S.profil(r["caption"])["plaski"] else ("budynek inny" if S.profil(r["caption"])["budynek"] else "obiekt"),
                "uwagi": " | ".join(f"{k}: {v[1]}" for k, v in w.items() if v[0] != "PASS" and v[1])})
with open(f"{OUT}/wyniki.csv", "w", newline="", encoding="utf-8") as f:
    c = csv.DictWriter(f, fieldnames=list(wyn[0])); c.writeheader(); c.writerows(wyn)
lin = [f"Walidacja zbioru v3-final ({len(wyn)} obiektow): PASS / FAIL / SKIP / brak"]
for k in IDS:
    cnt = collections.Counter(r[k] or "-" for r in wyn); lin.append(f"{k:3} PASS {cnt['PASS']:3}  FAIL {cnt['FAIL']:3}  SKIP {cnt['SKIP']:3}  nie dotyczy {cnt['-'] + cnt['ND']:3}")
open(f"{OUT}/podsumowanie.txt", "w", encoding="utf-8").write("\n".join(lin)); print("\n".join(lin))
# arkusz: obiekty z FAIL w K3/K4/P3/P6-podejrzenie
zle = [r for r in wyn if r["K3"] == "FAIL" or r["K4"] == "FAIL" or r["K2"] == "FAIL" or "PODEJRZENIE" in r["uwagi"]]
C = 220; F = ImageFont.truetype("arial.ttf", 13); FB = ImageFont.truetype("arialbd.ttf", 14); kol = 6
sh = Image.new("RGB", (kol * (C + 6), max(1, (len(zle) + kol - 1) // kol) * (C + 64) + 10), (40, 48, 36)); d = ImageDraw.Draw(sh)
for i, r in enumerate(zle):
    im = Image.open(r["plik"]).convert("RGBA"); k = min(C / im.width, C / im.height); im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.NEAREST)
    bg = Image.new("RGBA", (C, C), (255, 0, 255, 255)); bg.alpha_composite(im, ((C - im.width) // 2, C - im.height))
    x, y = (i % kol) * (C + 6), (i // kol) * (C + 64); sh.paste(bg.convert("RGB"), (x, y))
    d.text((x + 2, y + C + 2), f"{r['nazwa']} ({r['zrodlo']})", font=FB, fill=(255, 230, 140))
    fails = [k for k in ("K2", "K3", "K4") if r[k] == "FAIL"] + (["P6?"] if "PODEJRZENIE" in r["uwagi"] else [])
    d.text((x + 2, y + C + 20), "FAIL: " + ", ".join(fails), font=F, fill=(255, 120, 100))
sh.save(f"{OUT}/arkusz_geometria.png"); print("arkusz:", len(zle))
