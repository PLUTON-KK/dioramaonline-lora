"""Pakiet lora-budynki-v2 (niezalezny od modelu): E:/ai/lora/lora-budynki-v2/
Roznica wzgledem v1: skali NIE uczymy w obrazie. Kazdy budynek kadrowany ciasno (wypelnia ~88% dluzszego boku plotna),
a jego prawdziwy rozmiar jest w opisie ("about 10 m wide and 8 m tall"). Skale gry (24 px/m) przywraca skrypt po generacji:
szerokosc budynku na wyniku -> szer_m * 24 px.
Zrodlo: sprites/ i opisy z lora-budynki-v1-final (te same 72 budynki), z poprawka budki (bez zaprzeczenia)."""
import csv, json, os, re, shutil
import numpy as np
from PIL import Image

V1 = "E:/ai/lora/lora-budynki-v1-final"; OUT = "E:/ai/lora/lora-budynki-v2"
WYPELN = 0.88                      # dluzszy bok budynku wzgledem plotna (margines 6% z kazdej strony)
MAGENTA = (255, 0, 255)
# "side door" modele bazowe rozumieja jako drzwi w scianie bocznej -> pokazuja bok budynku (izometria).
# Na obrazkach to zawsze dodatkowe drzwi NA FRONCIE - opisujemy ich polozenie (sprawdzone recznie na kazdym sprite, 2026-10-21).
DRZWI_BOCZNE = {n: "right" for n in "dom-z-lokalem dom-z-panelami hala-sportowa kamienica-pierzeja-1 kamienica-pierzeja-2 kamienica-pierzeja-4 magazyn-blacha magazyn piekarnia-dom remiza warsztat-panele zajezdnia".split()}
DRZWI_BOCZNE["warsztat"] = "left"
POPRAWKI = {   # zaprzeczenia w opisach v1 -> opis pozytywny
    "budka-pokazu": (", with no visible door.", ", the serving window being the only opening in the front."),
}


def skaluj(im, s):
    """sprite pixel art (twarda alfa) -> rozmiar *s: NEAREST x8, potem BOX na kolorach premultiplikowanych (bez magentowej obwodki), alfa progowana"""
    w, h = round(im.width * s), round(im.height * s)
    big = im.resize((im.width * 8, im.height * 8), Image.NEAREST).convert("RGBa").resize((w, h), Image.BOX).convert("RGBA")
    a = np.array(big); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0); return Image.fromarray(a)


def opis(n, cap, szer_m, wys_m):
    if n in POPRAWKI:
        stare, nowe = POPRAWKI[n]; assert stare in cap, n; cap = cap.replace(stare, nowe)
    if n in DRZWI_BOCZNE:
        cap, k = re.subn(r"((?:a|an) [^,.]*?)side door( with steps)?", lambda m: f"{m.group(1)}door{m.group(2) or ''} on the {DRZWI_BOCZNE[n]} of the front facade", cap)
        assert k == 1, (n, k)
    assert "side door" not in cap, n
    typ = "enterable building" if "enterable building" in cap else "decorative building"
    return cap.replace(typ + ", ", f"{typ}, about {round(szer_m)} m wide and {round(wys_m)} m tall, ", 1)


meta_v1 = [json.loads(l) for l in open(f"{V1}/metadata.jsonl", encoding="utf-8")]
for d in ("train_512", "train_1024", "sprites"): shutil.rmtree(f"{OUT}/{d}", ignore_errors=True); os.makedirs(f"{OUT}/{d}")
meta = []
for m in meta_v1:
    n = m["nazwa"]; im = Image.open(f"{V1}/sprites/{n}.png").convert("RGBA")
    for f in os.listdir(f"{V1}/sprites"):
        if f.split(".")[0] in (n, n + "-open"): shutil.copy(f"{V1}/sprites/{f}", f"{OUT}/sprites/{f}")
    cap = opis(n, open(f"{V1}/train_512/{n}.txt", encoding="utf-8").read().strip(), m["szer_m"], m["wys_sprite_m"])
    rec = dict(m, caption=cap, kadr={})
    for P in (512, 1024):
        s = WYPELN * P / max(im.width, im.height); b = skaluj(im, s)
        x, y = (P - b.width) // 2, P - round((1 - WYPELN) / 2 * P) - b.height   # srodek poziomo, dol 6% nad krawedzia
        c = Image.new("RGBA", (P, P), MAGENTA + (255,)); c.alpha_composite(b, (x, y))
        c.convert("RGB").save(f"{OUT}/train_{P}/{n}.png"); open(f"{OUT}/train_{P}/{n}.txt", "w", encoding="utf-8").write(cap)
        rec["kadr"][str(P)] = {"skala": round(s, 4), "px_na_m": round(24 * s, 2), "bbox": [x, y, b.width, b.height]}
    meta.append(rec)
with open(f"{OUT}/metadata.jsonl", "w", encoding="utf-8") as f:
    for r in meta: f.write(json.dumps(r, ensure_ascii=False) + "\n")
with open(f"{OUT}/captions.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(["nazwa", "typ", "szer_m", "wys_sprite_m", "caption"])
    for r in meta: w.writerow([r["nazwa"], r["typ"], r["szer_m"], r["wys_sprite_m"], r["caption"]])

# podglad: wszystkie train_512 w siatce 9 x 8, miniatury 160 px
K, T = 9, 160; ark = Image.new("RGB", (K * T, -(-len(meta) // K) * T), (40, 40, 40))
for i, r in enumerate(meta):
    ark.paste(Image.open(f"{OUT}/train_512/{r['nazwa']}.png").resize((T - 4, T - 4), Image.BOX), ((i % K) * T + 2, (i // K) * T + 2))
ark.save(f"{OUT}/podglad.png")
print(len(meta), "budynkow;", "px/m (512):", min(r["kadr"]["512"]["px_na_m"] for r in meta), "-", max(r["kadr"]["512"]["px_na_m"] for r in meta))
