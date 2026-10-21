"""Zestawienie wynikow modeli zewnetrznych: dwie sekcje (pasek wejsciowe, pasek dekoracyjne), wiersz = model (folder w wyniki/), kolumny v1 | v2.
Pliki rozpoznawane po nazwie: 'wejsciowe'/'dekoracyjne' + 'v1'/'v2'; kilka czesci (part1, part2...) skladane pionowo. Nowy model = nowy folder w wyniki/.
Wynik: wyniki/zestawienie_modele_zewnetrzne.png"""
import glob, os, time
from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__)); W = f"{D}/wyniki"
C, LW, PAD = 1100, 260, 14
F = ImageFont.truetype("arialbd.ttf", 26); FS = ImageFont.truetype("arial.ttf", 20); FT = ImageFont.truetype("arialbd.ttf", 34)
modele = sorted(d for d in os.listdir(W) if os.path.isdir(f"{W}/{d}"))


def obraz(model, typ, wer):
    fs = sorted(f for f in glob.glob(f"{W}/{model}/*") if typ in os.path.basename(f) and wer in os.path.basename(f))
    if not fs: return None
    ims = [Image.open(f).convert("RGB") for f in fs]
    im = Image.new("RGB", (max(i.width for i in ims), sum(i.height for i in ims) + 6 * (len(ims) - 1)), (40, 48, 36)); y = 0
    for i in ims: im.paste(i, (0, y)); y += i.height + 6
    return im


def dopasuj(im, w, h):
    s = min(w / im.width, h / im.height); return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


sekcje = [("Pasek: budynki z wejściem (7)", "wejsciowe", ["wzory/wzor_wejsciowe.png", "wzory/wzor_drzwi.png"]),
          ("Pasek: budynki dekoracyjne (3)", "dekoracyjne", ["wzory/wzor_dekoracyjne.png"])]
wiersze = []   # (etykieta, [obraz v1, obraz v2], wysokosc)
for tyt, typ, wz in sekcje:
    wiersze.append(("SEKCJA", tyt, None))
    wzory = [Image.open(f"{D}/{p}").convert("RGB") for p in wz]
    wiersze.append(("wzór (załączony)\nlewo: styl\nprawo: drzwi" if typ == "wejsciowe" else "wzór (załączony)", [dopasuj(wzory[0], C, 600), dopasuj(wzory[1], C, 600) if len(wzory) > 1 else None], None))
    for m in modele:
        ims = [obraz(m, typ, v) for v in ("v1", "v2")]
        if any(ims): wiersze.append((m, [dopasuj(i, C, 900) if i else None for i in ims], None))
H = 70 + sum(90 if e == "SEKCJA" else max((i.height for i in ims if i), default=200) + PAD for e, ims, _ in wiersze) + 40
sh = Image.new("RGB", (LW + 2 * (C + PAD) + PAD, H), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((14, 14), "Modele zewnętrzne: te same budynki co nasze LoRA (prompty v1 i v2)", font=FT, fill=(255, 255, 255)); y = 70
for e, ims, _ in wiersze:
    if e == "SEKCJA":
        d.text((14, y + 6), ims, font=FT, fill=(255, 230, 140))
        for k, v in enumerate(("prompty v1", "prompty v2")): d.text((LW + k * (C + PAD) + 6, y + 52), v, font=F, fill=(200, 210, 190))
        y += 90; continue
    h = max((i.height for i in ims if i), default=200)
    d.multiline_text((14, y + 10), e, font=F, fill=(255, 255, 255))
    for k, im in enumerate(ims):
        x = LW + k * (C + PAD)
        if im: sh.paste(im, (x, y))
        elif not e.startswith("wzór"): d.rectangle([x, y, x + C, y + h], fill=(30, 34, 28)); d.text((x + C // 2 - 40, y + h // 2), "brak", font=FS, fill=(120, 120, 110))
    y += h + PAD
d.text((14, H - 32), "Prompty: prompty/pasek_*_v1.txt i _v2.txt. Wzory: wzory/. Każdy model dostał te same wzory i prompty.", font=FS, fill=(180, 180, 170))
out = f"{W}/zestawienie_modele_zewnetrzne.png"
try: sh.save(out)
except OSError: out = time.strftime(f"{W}/zestawienie_modele_zewnetrzne_%H%M.png"); sh.save(out)
print(out, sh.size, modele)
