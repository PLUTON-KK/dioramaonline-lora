"""Arkusz podgladow z RunPod: wiersz = krok (0, 500, ...), kolumna = prompt. python arkusz_podgladow.py <nazwa_runa> [kroki,...]"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
nm = sys.argv[1]; MODEL = {"qwenimage2512": "Qwen-Image 2512", "qwenedit2511": "Qwen-Image-Edit 2511", "zimage": "Z-Image Turbo", "moss": "MOSS-Image Base", "flux3": "FLUX 3 Image Klein base", "krea2raw": "Krea 2 Raw"}
mn = next((v for k, v in MODEL.items() if k in nm), nm); D = os.path.join(r"E:\ai\runpod\wyniki\podglady", nm)
fs = glob.glob(os.path.join(D, "**", "*.jpg"), recursive=True)
kroki = sorted({int(os.path.basename(f).split("__")[1].split("_")[0]) for f in fs})
if len(sys.argv) > 2: kroki = [k for k in kroki if str(k) in sys.argv[2].split(",")]
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia obok", "szklarnia", "obserwatorium", "weterynarz", "kino"]
F = ImageFont.truetype("arialbd.ttf", 18); C = 300
sh = Image.new("RGB", (10 * (C + 6) + 110, len(kroki) * (C + 6) + 80), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 8), "MODEL: " + mn + " + LoRA budynki (" + ("1024" if "1024" in nm else "512") + ")", font=ImageFont.truetype("arialbd.ttf", 26), fill=(255, 255, 255))
for i, t in enumerate(T): d.text((112 + i * (C + 6), 50), t, font=F, fill=(255, 230, 140))
for r, k in enumerate(kroki):
    d.text((8, 80 + r * (C + 6) + 10), "krok\n" + str(k) + ("\n(bez\nLoRA)" if k == 0 else ""), font=F, fill=(255, 255, 255))
    for f in fs:
        b = os.path.basename(f)
        if int(b.split("__")[1].split("_")[0]) == k:
            i = int(b.split("_")[-1][:-4]); sh.paste(Image.open(f).convert("RGB").resize((C, C)), (110 + i * (C + 6), 80 + r * (C + 6)))
out = os.path.join(r"E:\ai\runpod\wyniki", f"{nm}_podglad.png"); sh.save(out); print(out, kroki)
