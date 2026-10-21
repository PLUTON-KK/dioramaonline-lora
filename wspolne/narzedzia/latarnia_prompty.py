"""Z-Image Turbo + LoRA v1 (512): latarnia morska - rozne prompty, ten sam seed (47 = seed z rankingu; drugi wiersz 5005 dla kontroli).
Podejrzenie: koncowka KAM ("front facade facing the viewer, flat rectangular roof visible from above") nie pasuje do okraglej wiezy,
a zbior v1 nie ma zadnego okraglego obiektu. Zasada wlasciciela: okragle rzeczy widziane z gory jako splaszczona elipsa.
Wynik: E:/ai/wyniki/latarnia_prompty/arkusz.png + prompty.txt"""
import json, os, sys, textwrap
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import zestawienie_wf_bazowe as B

OUT = "E:/ai/wyniki/latarnia_prompty"; os.makedirs(OUT, exist_ok=True)
P1 = json.load(open("E:/ai/lora/prompty_podglad_10.json", encoding="utf-8"))[5]
KAM = " Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background."
assert P1.endswith(KAM)
TRESC = P1[:-len(KAM)]
KAM_OKR = " Pixel art game sprite, fixed orthographic RPG 3/4 camera seen from the south and slightly from above, round shapes drawn straight from the front with vertical sides and their tops visible as flattened ellipses, isolated on solid magenta #FF00FF background."
WIEZA = ("swiat2d style, decorative building, a tall round lighthouse tower drawn as a straight vertical cylinder with white and red horizontal stripes, "
         "a round gallery with a railing and a glass lantern room with a bright light on top, the top of the tower seen from above as a flattened ellipse")
DOM = ", and a small cream keeper's house with a dark grey flat roof standing next to the tower on its right side."
WARIANTY = [
    ("A", "prompt v1 (bez zmian)", P1),
    ("B", "v1, kamera dla okrągłych\n(zamiast „flat rectangular roof”)", TRESC + KAM_OKR),
    ("C", "wieża = pionowy walec,\ngóra jako elipsa + kamera okrągła", WIEZA + DOM + KAM_OKR),
    ("D", "jak C, domek bez dachu\nopisanego (tylko „small house”)", WIEZA + ", and a small cream keeper's house next to the tower on its right side." + KAM_OKR),
    ("E", "jak C, sama wieża\n(bez domku)", WIEZA + "." + KAM_OKR),
    ("F", "jak C + rozmiary\n(wieża 18 m, domek 4 m)", WIEZA.replace("a tall round lighthouse tower", "a tall round lighthouse tower about 18 m tall") + DOM.replace("a small cream keeper's house", "a small cream keeper's house about 4 m tall") + KAM_OKR),
    ("G", "jak C, kamera v1\n(„front facade… flat rectangular roof”)", WIEZA + DOM + KAM),
]
SEEDY = [47, 5005]; B.RES = 512; M = B.MOD["swiat2d_zimage_budynki_v1final_512"]
with open(f"{OUT}/prompty.txt", "w", encoding="utf-8") as f:
    for k, et, p in WARIANTY: f.write(f"{k}: {et.replace(chr(10), ' ')}\n{p}\n\n")
for k, et, p in WARIANTY:
    for s in SEEDY:
        png = f"{OUT}/{k}_s{s}.png"
        if not os.path.exists(png): silnik.generuj(B.wf(M, p, s), png); print(k, s, flush=True)
C, LW = 260, 140; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 14)
sh = Image.new("RGB", (LW + len(WARIANTY) * (C + 4), 130 + len(SEEDY) * (C + 4) + 20), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: Z-Image Turbo + LoRA budynki v1 (512) – latarnia morska: różne prompty, te same seedy (pełne prompty: prompty.txt)", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
for j, (k, et, p) in enumerate(WARIANTY): d.multiline_text((LW + j * (C + 4) + 4, 44), f"{k}: {et}", font=FS, fill=(255, 230, 140))
for i, s in enumerate(SEEDY):
    y = 130 + i * (C + 4); d.text((10, y + 10), f"seed {s}" + ("\n(ranking)" if s == 47 else ""), font=F, fill=(255, 255, 255))
    for j, (k, et, p) in enumerate(WARIANTY): sh.paste(Image.open(f"{OUT}/{k}_s{s}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + j * (C + 4), y))
sh.save(f"{OUT}/arkusz.png"); print("KONIEC")
