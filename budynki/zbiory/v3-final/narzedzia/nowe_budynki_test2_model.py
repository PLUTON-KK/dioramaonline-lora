"""Ten sam zestaw TEST-V2 (38 nowych obiektow x v2/J/K, prompty z nowe_budynki_krea_v2_test2.py, seed 42+i) na innym modelu z LoRA budynki v2 (512), ComfyUI RTX 3080.
python nowe_budynki_test2_model.py zimage|moss|flux3d
zimage: Z-Image Turbo bf16 + LoRA v2 Z-Image Turbo -> E:/ai/wyniki/nowe_budynki_zimage-turbo_lora_v2-test-v2/
moss:   MOSS-Image SFT int8 + LoRA v2 z MOSS-Image Base -> E:/ai/wyniki/nowe_budynki_moss-image-sft_lora_v2-test-v2/"""
import os, sys
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import nowe_budynki_krea_v2_test2 as T2
MODELE = {"zimage": ("swiat2d_zimage_budynki_v1final_512", "swiat2d_v2f512_zimageturbo_2000.safetensors", "nowe_budynki_zimage-turbo_lora_v2-test-v2",
                     "Z-Image Turbo bf16 + LoRA budynki v2 (512)"),
          "flux3d": ("zestawienie_flux3_destylat_lora_base512", "swiat2d_v2f512_flux3base_2000.safetensors", "nowe_budynki_flux3-klein-destylat_lora_v2-test-v2",
                     "FLUX 3 Klein destylat int8 + LoRA budynki v2 (z FLUX 3 Klein base, 512)"),
          "moss": ("zestawienie_moss_sft_lora_base512", "swiat2d_v2f512_mossbase_2000.safetensors", "nowe_budynki_moss-image-sft_lora_v2-test-v2",
                   "MOSS-Image SFT int8 + LoRA budynki v2 (z MOSS-Image Base, 512)")}
kod = sys.argv[1]; klucz, lora, fol, opis = MODELE[kod]
OUT = f"E:/ai/wyniki/{fol}"; os.makedirs(OUT, exist_ok=True)
assert not T2.sprawdz(), T2.sprawdz()
from PIL import Image, ImageDraw, ImageFont
import silnik
import zestawienie_wf_bazowe as B
B.RES = 512; M = list(B.MOD[klucz]); M[4] = lora; M = tuple(M)
with open(f"{OUT}/prompty.txt", "w", encoding="utf-8") as f:
    f.write(f"TEST-V2 · Model: {opis}, seed 42+i (prompty jak Krea test-v2)\n\n")
    for k, et, fn in T2.WAR:
        for i, e in enumerate(T2.L): f.write(f"[{k}] {e[1]}\n{fn(e)}\n\n")
for i, e in enumerate(T2.L):
    for k, et, fn in T2.WAR:
        png = f"{OUT}/{k}_{i}.png"
        if os.path.exists(png): continue
        silnik.generuj(B.wf(M, fn(e), 42 + i), png); print(k, i, e[1], flush=True)
C, LW = 240, 250; F = ImageFont.truetype("arialbd.ttf", 17); FS = ImageFont.truetype("arial.ttf", 15)
grupy = []
[grupy.append(e[0]) for e in T2.L if e[0] not in grupy]
for g in grupy:
    idx = [i for i, e in enumerate(T2.L) if e[0] == g]
    sh = Image.new("RGB", (LW + len(idx) * (C + 4), 76 + 3 * (C + 4)), (40, 48, 36)); d = ImageDraw.Draw(sh)
    d.text((10, 10), f"TEST-V2 · MODEL: {opis} – nowe obiekty spoza zbioru: {g}, seed 42+i", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
    for c, i in enumerate(idx): d.text((LW + c * (C + 4) + 4, 48), T2.L[i][1], font=F, fill=(255, 230, 140))
    for r, (k, et, fn) in enumerate(T2.WAR):
        y = 76 + r * (C + 4); d.multiline_text((10, y + 10), et.replace(" (", "\n("), font=FS, fill=(255, 255, 255))
        for c, i in enumerate(idx): sh.paste(Image.open(f"{OUT}/{k}_{i}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + c * (C + 4), y))
    sh.save(f"{OUT}/arkusz_{g}.png")
print("KONIEC")
