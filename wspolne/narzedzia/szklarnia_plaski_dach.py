"""Z-Image Turbo + LoRA v1 (512): szklarnia z promptem v1 vs prompt z wyraznym plaskim szklanym dachem. 6 seedow (48 = oryginal, 1001-5005).
Wynik: E:/ai/wyniki/szklarnia_plaski_dach/arkusz.png"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import zestawienie_wf_bazowe as B

OUT = "E:/ai/wyniki/szklarnia_plaski_dach"; os.makedirs(OUT, exist_ok=True)
STARY = json.load(open("E:/ai/lora/prompty_podglad_10.json", encoding="utf-8"))[6]
NOWY = STARY.replace("a garden centre greenhouse with large glass walls and a glass roof, green plants visible inside,",
                     "a garden centre greenhouse with large glass walls and a flat rectangular glass roof made of glass panels in a metal frame, seen from above like the flat roofs of the other buildings, green plants visible through the glass walls and the glass roof,")
assert NOWY != STARY
open(f"{OUT}/prompty.txt", "w", encoding="utf-8").write(f"STARY (v1):\n{STARY}\n\nNOWY:\n{NOWY}\n")
SEEDY = [48, 1001, 2002, 3003, 4004, 5005]; B.RES = 512; M = B.MOD["swiat2d_zimage_budynki_v1final_512"]
for nazwa, p in (("stary", STARY), ("nowy", NOWY)):
    for s in SEEDY:
        f = f"{OUT}/{nazwa}_s{s}.png"
        if not os.path.exists(f): silnik.generuj(B.wf(M, p, s), f); print(nazwa, s, flush=True)
C, LW = 300, 250; F = ImageFont.truetype("arialbd.ttf", 20); FS = ImageFont.truetype("arial.ttf", 16)
sh = Image.new("RGB", (LW + 6 * (C + 4), 70 + 2 * (C + 4) + 20), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: Z-Image Turbo + LoRA budynki v1 (512) – szklarnia: prompt v1 vs „płaski szklany dach”", font=ImageFont.truetype("arialbd.ttf", 24), fill=(255, 255, 255))
for j, s in enumerate(SEEDY): d.text((LW + j * (C + 4) + 4, 44), f"seed {s}" + (" (oryginał)" if s == 48 else ""), font=F, fill=(255, 230, 140))
for i, (nazwa, et) in enumerate((("stary", "prompt v1\n„glass roof”"), ("nowy", "nowy prompt\n„flat rectangular\nglass roof…”"))):
    y = 70 + i * (C + 4); d.multiline_text((10, y + 10), et, font=F, fill=(255, 255, 255))
    for j, s in enumerate(SEEDY): sh.paste(Image.open(f"{OUT}/{nazwa}_s{s}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + j * (C + 4), y))
sh.save(f"{OUT}/arkusz.png"); print("KONIEC")
