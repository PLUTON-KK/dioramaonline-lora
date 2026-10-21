"""Zestawienie wszystkich LoRA budynki v1: wiersz = model + LoRA + rozdzielczosc (ostatni dostepny krok), kolumna = budynek z promptu.
Lokalne treningi (RTX 3080) mialy tylko 4 pierwsze prompty - reszta kolumn pusta."""
import glob, os
from PIL import Image, ImageDraw, ImageFont

L = "E:/ai/lora/output"; R = "E:/ai/runpod/wyniki/podglady"
WIERSZE = [  # (model, lora, rozdzielczosc, katalog z samples, gdzie)
    ("Z-Image Turbo", "budynki v1", "512", f"{L}/swiat2d_zimage_budynki_v1final_512", "RTX 3080"),
    ("Z-Image Turbo", "budynki v1", "1024", f"{R}/swiat2d_zimage_budynki_v1final_1024_bf16", "RunPod L40"),
    ("Z-Image Base", "budynki v1", "512", f"{L}/swiat2d_zimagebase_budynki_v1final_512", "RTX 3080"),
    ("MOSS-Image Base", "budynki v1", "512", f"{L}/swiat2d_moss_base_budynki_v1final_512", "RTX 3080"),
    ("MOSS-Image SFT", "budynki v1 (z Base)", "512", f"{L}/zestawienie_moss_sft_lora_base512", "obraz: ComfyUI 3080"),
    ("MOSS-Image Base", "budynki v1", "1024", f"{R}/swiat2d_moss_budynki_v1final_1024_bf16", "RunPod L40"),
    ("FLUX 3 Klein base", "budynki v1", "512", f"{L}/swiat2d_flux3_base_budynki_v1final_512", "RTX 3080"),
    ("FLUX 3 Klein (destylat)", "budynki v1 (z base)", "512", f"{L}/zestawienie_flux3_destylat_lora_base512", "obraz: ComfyUI 3080"),
    ("FLUX 3 Klein base", "budynki v1", "1024", f"{R}/swiat2d_flux3_budynki_v1final_1024_bf16", "RunPod A40"),
    ("FLUX.2 Klein 4B", "budynki v1", "512", f"{L}/swiat2d_klein4b_budynki_v1final_512", "RTX 3080"),
    ("Qwen-Image 2512", "budynki v1", "512", f"{R}/swiat2d_qwenimage2512_budynki_v1final_512", "RunPod A100"),
    ("Qwen-Image-Edit 2511", "budynki v1", "512", f"{R}/swiat2d_qwenedit2511_budynki_v1final_512", "RunPod A100"),
    ("Krea 2 Raw", "budynki v1", "512", f"{R}/swiat2d_krea2raw_budynki_v1final_512", "RunPod A6000"),
    ("Krea 2 Turbo int8", "budynki v1 (z Raw)", "512", f"{L}/zestawienie_krea2turbo_lora_raw512", "obraz: ComfyUI 3080"),
    ("Qwen-Image Q4 (GGUF)", "budynki v1 (z 2512)", "512", f"{L}/zestawienie_qwenimage_q4_lora_2512", "obraz: ComfyUI 3080"),
    ("Qwen-Image-Edit 2511 Q4", "budynki v1", "512", f"{L}/zestawienie_qwenedit_q4_lora_2511", "obraz: ComfyUI 3080"),
    ("FLUX.2 Klein 4B (destylat)", "budynki v1 (z base)", "512", f"{L}/zestawienie_klein4b_destylat_lora_base512", "obraz: ComfyUI 3080"),
    ("MOSS-Image SFT", "budynki v1 (z Base)", "1024", f"{L}/zestawienie_moss_sft_lora_base1024", "obraz: ComfyUI 3080"),
    ("FLUX 3 Klein (destylat)", "budynki v1 (z base)", "1024", f"{L}/zestawienie_flux3_destylat_lora_base1024", "obraz: ComfyUI 3080"),
]
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia obok", "szklarnia", "obserwatorium", "weterynarz", "kino"]
C, LW, H = 260, 300, 70
import json
CZ = json.load(open("E:/ai/wyniki/zestawienie_comfy/czasy_3080.json", encoding="utf-8")) if os.path.exists("E:/ai/wyniki/zestawienie_comfy/czasy_3080.json") else {}
ZA_DUZY = {"swiat2d_qwenimage2512_budynki_v1final_512": "Qwen-Image 2512 bf16 ~41 GB", "swiat2d_qwenedit2511_budynki_v1final_512": "Qwen-Image-Edit bf16 ~41 GB",
           "swiat2d_krea2raw_budynki_v1final_512": "Krea 2 Raw bf16"}
F = ImageFont.truetype("arialbd.ttf", 20); FS = ImageFont.truetype("arial.ttf", 17)
sh = Image.new("RGB", (LW + len(T) * (C + 4), H + len(WIERSZE) * (C + 4) + 40), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "LoRA budynki v1 - wszystkie modele, ostatni krok", font=ImageFont.truetype("arialbd.ttf", 26), fill=(255, 255, 255))
for j, t in enumerate(T): d.text((LW + j * (C + 4) + 6, H - 26), t, font=F, fill=(255, 230, 140))
for i, (m, lora, res, kat, gdzie) in enumerate(WIERSZE):
    fs = glob.glob(f"{kat}/**/*.jpg", recursive=True)
    kroki = {int(os.path.basename(f).split("__")[1].split("_")[0]) for f in fs}
    pelne = [k for k in kroki if sum(1 for f in fs if f"__{k:09d}_" in f) >= 4]
    k = max(pelne) if pelne else None; y = H + i * (C + 4)
    b = os.path.basename(kat)
    rtx = (f"RTX 3080: {CZ[b]:.0f} s / obraz" if b in CZ else ("RTX 3080: za duzy" if b in ZA_DUZY else "RTX 3080: pomiar w toku"))
    for n, s in enumerate([m, f"+ LoRA {lora}", f"{res} px, " + (gdzie if gdzie.startswith("obraz") else "trening: " + gdzie), (f"krok {k}" + (" (trwa)" if k < 2000 else "")) if k else "krok 2000"]):
        d.text((10, y + 10 + n * 26), s, font=F if n == 0 else FS, fill=(255, 255, 255) if n == 0 else (200, 210, 190))
    d.text((10, y + 10 + 4 * 26 + 6), rtx, font=F, fill=(255, 200, 120) if b in ZA_DUZY else (140, 230, 140))
    if b in ZA_DUZY: d.text((10, y + 10 + 5 * 26 + 10), "(" + ZA_DUZY[b] + ";", font=FS, fill=(255, 200, 120)); d.text((10, y + 10 + 6 * 26 + 10), " lokalnie wersja Q4/int8 nizej)", font=FS, fill=(255, 200, 120))
    for j in range(len(T)):
        f = [x for x in fs if f"__{k:09d}_{j}." in x] if k is not None else []
        x0 = LW + j * (C + 4)
        if f: sh.paste(Image.open(f[0]).convert("RGB").resize((C, C), Image.LANCZOS), (x0, y))
        else: d.rectangle([x0, y, x0 + C, y + C], fill=(30, 34, 28)); d.text((x0 + 80, y + C // 2 - 10), "w kolejce", font=FS, fill=(120, 120, 110))
d.text((10, sh.height - 32), "Obrazy: sample ai-toolkit z treningu; wiersze ComfyUI i brakujace budynki lokalnych treningow dogenerowane na RTX 3080 (te same prompty, seed 42+i). Czas: 1 obraz po wczytaniu modelu.", font=FS, fill=(180, 180, 170))
import time
try: sh.save("E:/ai/runpod/wyniki/zestawienie_v1_wszystkie.png"); print("zapisano zestawienie_v1_wszystkie.png", sh.size)
except OSError: f = time.strftime("E:/ai/runpod/wyniki/zestawienie_v1_wszystkie_%H%M.png"); sh.save(f); print("plik zablokowany (otwarty w przegladarce?), zapisano", f)
