"""Pakiet uniwersalny v1-budynki-lora (niezalezny od modelu): E:\ai\lora\v1-budynki-lora\
- sprites\<nazwa>.png        format gry: 24 px/m, paleta swiata, twarda alfa (zrodlo prawdy); wejsciowe tez <nazwa>-open.png + .json gry
- train_1024\<nazwa>.png+.txt plotno 1024 magenta, sprite x2 NEAREST, dol na y=984, srodek poziomo (jedna skala dla wszystkich: 1 m = 48 px)
- metadata.jsonl              nazwa, typ, rozmiar w m, pozycja drzwi, caption, zrodlo, ocena
- README.md                   zasady
Filtr: [oceny.json] (ocena/bud__<nazwa>: decyzja 'nie' -> pomin); 'z gry (inne drzwi)' tylko z 'tak'."""
import json, os, shutil, sys
import numpy as np
from PIL import Image

B = r"E:\ai\codex_paczki\budynki"; OUT = r"E:\ai\lora\lora-budynki-v1-final"
L = json.load(open(os.path.join(B, "lora-lista.json"), encoding="utf-8"))
oceny = json.load(open(sys.argv[1], encoding="utf-8")) if len(sys.argv) > 1 else {}
for d in ("sprites", "train_1024"):
    shutil.rmtree(os.path.join(OUT, d), ignore_errors=True); os.makedirs(os.path.join(OUT, d))
X, P, BAZA = 2, 1024, 984
meta = []; pomin = []
for it in L:
    n = it["nazwa"]; dec = oceny.get("bud__" + n, {}).get("decyzja")
    if dec == "nie" or (it["typ"].startswith("z gry") and dec != "tak"):
        pomin.append(n); continue
    im = Image.open(it["plik"]).convert("RGBA"); im = im.crop(im.getchannel("A").getbbox())
    a = np.array(im); a[..., 3] = np.where(a[..., 3] >= 128, 255, 0); im = Image.fromarray(a)
    im.save(os.path.join(OUT, "sprites", n + ".png"))
    drzwi = None
    if it.get("plik_open"):
        shutil.copy(it["plik_open"], os.path.join(OUT, "sprites", n + "-open.png"))
        js = it["plik"][:-4] + ".json"; shutil.copy(js, os.path.join(OUT, "sprites", n + ".json"))
        d = json.load(open(js, encoding="utf-8"))["doors"][0]; drzwi = {"x_px": d["placement"]["x"], "y_px": d["placement"]["y"], "w_px": 59, "h_px": 58}
    big = im.resize((im.width * X, im.height * X), Image.NEAREST)
    assert big.width <= P - 40 and big.height <= BAZA - 20, (n, big.size)
    c = Image.new("RGBA", (P, P), (255, 0, 255, 255)); c.alpha_composite(big, ((P - big.width) // 2, BAZA - big.height))
    c.convert("RGB").save(os.path.join(OUT, "train_1024", n + ".png"))
    open(os.path.join(OUT, "train_1024", n + ".txt"), "w", encoding="utf-8").write(it["caption"])
    meta.append({"nazwa": n, "typ": it["typ"], "w_px": im.width, "h_px": im.height, "szer_m": round(im.width / 24, 2), "wys_sprite_m": round(im.height / 24, 2),
                 "drzwi": drzwi, "caption": it["caption"], "zrodlo": it["plik"], "ocena": dec or "brak"})
with open(os.path.join(OUT, "metadata.jsonl"), "w", encoding="utf-8") as f:
    for m in meta: f.write(json.dumps(m, ensure_ascii=False) + "\n")
typy = {t: sum(1 for m in meta if m["typ"] == t) for t in sorted({m["typ"] for m in meta})}
KAM = "Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background."
open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(f"""# lora-budynki-v1-final

Zbior treningowy LoRA: budynki do gry Swiat 2D (diorama), pixel art, fronty. Niezalezny od modelu (Z-Image, MOSS-Image, FLUX.2 klein, ...).
Zaakceptowany przez wlasciciela 2026-10-20: {len(meta)} obrazow ({", ".join(f"{v} {k}" for k, v in typy.items())}).

## Zawartosc
| folder / plik | co to jest |
|---|---|
| `train_1024/` | gotowe do treningu: `<nazwa>.png` (1024x1024) + `<nazwa>.txt` (opis). Format kohya / ai-toolkit / KohakuMossTrainer (folder obrazow z opisami) |
| `sprites/` | zrodlo prawdy w formacie gry: 24 px = 1 m, paleta swiata (64 kolory), przezroczyste tlo. Wejsciowe takze `<nazwa>-open.png` i `<nazwa>.json` (drzwi dla gry) |
| `metadata.jsonl` | jedna linia na budynek: typ, rozmiar w px i m, pozycja drzwi, opis |
| `captions.csv` | wszystkie opisy w jednej tabeli |
| `podglad.png` | wszystkie budynki w jednej skali |

## Obrazy treningowe
- Plotno 1024x1024, tlo jednolita magenta #FF00FF.
- Sprite powiekszony x2 metoda NEAREST (bez rozmycia): 1 m = 48 px. Ta sama skala dla wszystkich, wiec model uczy sie prawdziwych roznic wielkosci (garaz ~4 m, ratusz ~19 m).
- Dol budynku zawsze na linii y=984, wysrodkowany poziomo.
- Trening: rozdzielczosc 1024, BEZ bucketow / skalowania obrazow (inaczej znika wspolna skala).
- Wynik generowania: zmniejszyc /2 (NEAREST/BOX), paleta swiata, wyciac magente -> sprite gry.

## Opisy (caption)
Schemat:
`swiat2d style, <enterable building | decorative building>, <co to jest, kondygnacje, sciany i kolory, elementy, dach>, <drzwi>. {KAM}`
- `swiat2d style` - slowo wyzwalajace styl.
- `enterable building` - budynek z wejsciem: jedne kanoniczne drzwi std-external-2 (59x58 px = 2,46 x 2,42 m), opis konczy sie `the standard entrance door in the middle of / on the left side of / on the right side of the front facade`.
- `decorative building` - bez wejscia, wlasne drzwi / bramy opisane slowami.
- Dach zawsze plaski prostokat; domyslnie `a dark grey flat roof with an air conditioning unit`, inne pokrycia opisane (zwir, swietliki, blacha, zielony dach, panele, taras).
- Bez napisow w jezyku, tylko piktogramy. Elementow typu donice nie opisujemy (styl).
- Opisy pisane z obrazkow (nie z promptow), zaakceptowane przez wlasciciela.

## Zasady stylu
Tylko fronty (tyl/bok - osobny zbior pozniej). Kamera RPG 3/4 z poludnia, pionowe krawedzie, plaski prostokatny dach (wysokosc na sprite = pol glebokosci budynku). Bez skosow i perspektywy.
""")
import csv as _csv
with open(os.path.join(OUT, "captions.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = _csv.writer(f, delimiter=";"); w.writerow(["nr", "nazwa", "typ", "szer_m", "caption"])
    for i, m in enumerate(meta, 1): w.writerow([i, m["nazwa"], m["typ"], m["szer_m"], m["caption"]])
# podglad: wszystkie w jednej skali (x1), rzedy na wspolnej linii gruntu
from PIL import ImageDraw, ImageFont
F = ImageFont.truetype("arialbd.ttf", 14); MAXW = 2400; rows = []; row = []; w = 0
for m in meta:
    im = Image.open(os.path.join(OUT, "sprites", m["nazwa"] + ".png")).convert("RGBA")
    if row and w + im.width + 20 > MAXW: rows.append(row); row, w = [], 0
    row.append((m["nazwa"], im)); w += im.width + 20
rows.append(row)
H = sum(max(i.height for _, i in r) + 30 for r in rows) + 10
pv = Image.new("RGB", (MAXW + 20, H), (255, 0, 255)); d = ImageDraw.Draw(pv); y = 10
for r in rows:
    h = max(i.height for _, i in r); x = 10
    for n, i in r:
        pv.paste(i, (x, y + h - i.height), i); d.text((x, y + h + 4), n, font=F, fill=(255, 255, 255)); x += i.width + 20
    y += h + 30
pv.save(os.path.join(OUT, "podglad.png"))
print(len(meta), "obrazow", typy, "pominiete:", pomin)
