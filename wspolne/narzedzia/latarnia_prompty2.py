"""Z-Image Turbo + LoRA v1 (512): latarnia - runda 2. Baza: wariant C (walec, gora elipsa, domek z plaskim dachem, kamera dla okraglych),
dochodzi bryla/realizm: cieniowanie walca, materialy, proporcje - nadal pixel art w naszym rzucie. Seedy 47, 5005, 777.
Wynik: E:/ai/wyniki/latarnia_prompty2/arkusz.png + prompty.txt"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import zestawienie_wf_bazowe as B

OUT = "E:/ai/wyniki/latarnia_prompty2"; os.makedirs(OUT, exist_ok=True)
KAM = (" Pixel art game sprite, fixed orthographic RPG 3/4 camera seen from the south and slightly from above, round shapes drawn straight from the front "
       "with vertical sides and their tops visible as flattened ellipses, isolated on solid magenta #FF00FF background.")
WIEZA = ("swiat2d style, decorative building, a tall round lighthouse tower drawn as a straight vertical cylinder with white and red horizontal stripes, "
         "a round gallery with a railing and a glass lantern room with a bright light on top, the top of the tower seen from above as a flattened ellipse")
DOM = ", and a small cream keeper's house with a dark grey flat roof standing next to the tower on its right side"
CIEN = ", the round tower shaded like a real cylinder: lit from the top-left, gradually darker towards its right edge, so it clearly looks round and solid"
REAL = ", realistic materials and proportions: painted stone tower with visible stone blocks and weathered paint, a stone base with a small entrance door at the bottom of the tower, small windows going up the tower"
WARIANTY = [
    ("C", "runda 1 wariant C\n(punkt odniesienia)", WIEZA + DOM + "." + KAM),
    ("H", "C + cieniowanie walca\n(światło z lewej, cień z prawej)", WIEZA + CIEN + DOM + "." + KAM),
    ("I", "H + realistyczne materiały\ni proporcje (kamień, drzwi, okienka)", WIEZA + CIEN + REAL + DOM + "." + KAM),
    ("J", "I + „realistic shading,\ndetailed” w opisie stylu", WIEZA + CIEN + REAL + DOM + "." + KAM.replace("Pixel art game sprite,", "Detailed pixel art game sprite with realistic shading and volume,")),
    ("K", "I + „semi-realistic pixel art”\nzamiast „pixel art”", WIEZA + CIEN + REAL + DOM + "." + KAM.replace("Pixel art game sprite,", "Semi-realistic pixel art game sprite,")),
    ("L", "J bez domku\n(sama wieża)", WIEZA + CIEN + REAL + "." + KAM.replace("Pixel art game sprite,", "Detailed pixel art game sprite with realistic shading and volume,")),
]
SEEDY = [47, 5005, 777]; B.RES = 512; M = B.MOD["swiat2d_zimage_budynki_v1final_512"]
with open(f"{OUT}/prompty.txt", "w", encoding="utf-8") as f:
    for k, et, p in WARIANTY: f.write(f"{k}: {et.replace(chr(10), ' ')}\n{p}\n\n")
for k, et, p in WARIANTY:
    for s in SEEDY:
        png = f"{OUT}/{k}_s{s}.png"
        if not os.path.exists(png): silnik.generuj(B.wf(M, p, s), png); print(k, s, flush=True)
C, LW = 280, 120; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 14)
sh = Image.new("RGB", (LW + len(WARIANTY) * (C + 4), 110 + len(SEEDY) * (C + 4) + 20), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: Z-Image Turbo + LoRA budynki v1 (512) – latarnia, runda 2: bryła i realizm w naszym rzucie (pełne prompty: prompty.txt)", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
for j, (k, et, p) in enumerate(WARIANTY): d.multiline_text((LW + j * (C + 4) + 4, 44), f"{k}: {et}", font=FS, fill=(255, 230, 140))
for i, s in enumerate(SEEDY):
    y = 110 + i * (C + 4); d.text((10, y + 10), f"seed {s}", font=F, fill=(255, 255, 255))
    for j, (k, et, p) in enumerate(WARIANTY): sh.paste(Image.open(f"{OUT}/{k}_s{s}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + j * (C + 4), y))
sh.save(f"{OUT}/arkusz.png"); print("KONIEC")
