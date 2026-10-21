"""Zestawienie: LoRA v1 (bez zmian) na promptach v2. Wiersz = model + LoRA + rozdzielczosc, kolumna = budynek testowy.
Obrazy: RunPod (ai-toolkit, bf16, LoRA wczytana, krok 0 = bez uczenia) albo ComfyUI RTX 3080 dla destylatow, ktorych ai-toolkit nie wczytuje."""
import glob, os, time
from PIL import Image, ImageDraw, ImageFont

G = "E:/ai/runpod/wyniki/output/gen_v1lora_v2prompty_"
WIERSZE = [  # (model, lora, rozdz, klucz, skad)
    ("Z-Image Turbo", "budynki v1", "512", "zimageturbo_512", "RunPod bf16"),
    ("Z-Image Turbo", "budynki v1", "1024", "zimageturbo_1024", "RunPod bf16"),
    ("Z-Image Base", "budynki v1", "512", "zimagebase_512", "RunPod bf16"),
    ("MOSS-Image Base", "budynki v1", "512", "mossbase_512", "RunPod bf16"),
    ("MOSS-Image SFT", "budynki v1 (z Base)", "512", "mosssft_512", "RunPod bf16"),
    ("MOSS-Image Base", "budynki v1", "1024", "mossbase_1024", "RunPod bf16"),
    ("MOSS-Image SFT", "budynki v1 (z Base)", "1024", "mosssft_1024", "RunPod bf16"),
    ("FLUX 3 Klein base", "budynki v1", "512", "flux3base_512", "RunPod bf16"),
    ("FLUX 3 Klein (destylat)", "budynki v1 (z base)", "512", "flux3destylat_512", "ComfyUI int8, RTX 3080"),
    ("FLUX 3 Klein base", "budynki v1", "1024", "flux3base_1024", "RunPod bf16"),
    ("FLUX 3 Klein (destylat)", "budynki v1 (z base)", "1024", "flux3destylat_1024", "ComfyUI int8, RTX 3080"),
    ("FLUX.2 Klein 4B base", "budynki v1", "512", "klein4bbase_512", "RunPod bf16"),
    ("FLUX.2 Klein 4B (destylat)", "budynki v1 (z base)", "512", "klein4bdestylat_512", "ComfyUI bf16, RTX 3080"),
    ("Qwen-Image 2512", "budynki v1", "512", "qwenimage2512_512", "RunPod bf16"),
    ("Qwen-Image-Edit 2511", "budynki v1", "512", "qwenedit2511_512", "RunPod bf16, wzór jako obraz"),
    ("Krea 2 Raw", "budynki v1", "512", "krea2raw_512", "RunPod bf16"),
    ("Krea 2 Turbo", "budynki v1 (z Raw)", "512", "krea2turbo_512", "RunPod bf16"),
]
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia obok", "szklarnia", "obserwatorium", "weterynarz", "kino"]
C, LW, H = 260, 300, 70
F = ImageFont.truetype("arialbd.ttf", 20); FS = ImageFont.truetype("arial.ttf", 17)
sh = Image.new("RGB", (LW + len(T) * (C + 4), H + len(WIERSZE) * (C + 4) + 40), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "LoRA budynki v1 na PROMPTACH v2 (rozmiar w metrach, drzwi na froncie, budka bez zaprzeczenia)", font=ImageFont.truetype("arialbd.ttf", 26), fill=(255, 255, 255))
for j, t in enumerate(T): d.text((LW + j * (C + 4) + 6, H - 26), t, font=F, fill=(255, 230, 140))
for i, (m, lora, res, k, skad) in enumerate(WIERSZE):
    y = H + i * (C + 4); fs = glob.glob(f"{G}{k}/samples/*__000000000_*.jpg")
    for n, s in enumerate([m, f"+ LoRA {lora}", f"{res} px", skad]):
        d.text((10, y + 10 + n * 26), s, font=F if n == 0 else FS, fill=(255, 255, 255) if n == 0 else (200, 210, 190))
    for j in range(10):
        f = [x for x in fs if x.endswith(f"__000000000_{j}.jpg")]; x0 = LW + j * (C + 4)
        if f: sh.paste(Image.open(f[0]).convert("RGB").resize((C, C), Image.LANCZOS), (x0, y))
        else: d.rectangle([x0, y, x0 + C, y + C], fill=(30, 34, 28)); d.text((x0 + 90, y + C // 2 - 10), "w kolejce", font=FS, fill=(120, 120, 110))
d.text((10, sh.height - 32), "Te same LoRA, seedy (42+i), kroki i guidance co w zestawieniu v1; zmieniony tylko tekst promptów (budynki/testy/prompty_v2.json).", font=FS, fill=(180, 180, 170))
out = "E:/ai/runpod/wyniki/zestawienie_v1lora_prompty_v2.png"
try: sh.save(out)
except OSError: out = time.strftime("E:/ai/runpod/wyniki/zestawienie_v1lora_prompty_v2_%H%M.png"); sh.save(out)
print(out, sh.size)
