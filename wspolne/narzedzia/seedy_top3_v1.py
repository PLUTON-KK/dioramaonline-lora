"""LoRA v1 + prompty v1: budynki ocenione jako srednie/slabe w 3 najlepszych wierszach rankingu (po 15 pkt), po 5 nowych seedach.
Seedy oryginalne: 42+i (42-51). Nowe: 1001, 2002, 3003, 4004, 5005. ComfyUI (RTX 3080), te same workflow co w zestawieniu v1.
Wynik: E:/ai/wyniki/seedy_top3_v1/<wiersz>_<budynek>_s<seed>.png + arkusz.png"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import silnik
import zestawienie_wf_bazowe as B
import dogeneruj_zestawienie_v1_lekkie as LK

OUT = "E:/ai/wyniki/seedy_top3_v1"; os.makedirs(OUT, exist_ok=True)
SEEDY = [1001, 2002, 3003, 4004, 5005]
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia z domkiem", "szklarnia", "obserwatorium", "weterynarz", "kino"]
OC = "E:/ai/runpod/ranking_oceny_akt/ocena"


def z_seedem(wf, seed):
    wf["ks"]["inputs"]["seed"] = seed; return wf


WIERSZE = [  # (id oceny, nazwa, funkcja workflow(i, seed))
    ("swiat2d_zimage_budynki_v1final_512", "Z-Image Turbo + LoRA v1, 512 px",
     lambda i, s: (setattr(B, "RES", 512), z_seedem(B.wf(B.MOD["swiat2d_zimage_budynki_v1final_512"], B.P[i], s), s))[1]),
    ("zestawienie_moss_sft_lora_base1024", "MOSS-Image SFT + LoRA v1 (z Base), 1024 px", lambda i, s: z_seedem(LK.wf("zestawienie_moss_sft_lora_base1024", i), s)),
    ("zestawienie_krea2turbo_lora_raw512", "Krea 2 Turbo int8 + LoRA v1 (z Raw), 512 px", lambda i, s: z_seedem(LK.wf("zestawienie_krea2turbo_lora_raw512", i), s)),
]
plan = []
for w, nazwa, f in WIERSZE:
    for b in range(10):
        o = json.load(open(f"{OC}/v1v1__{w}__{b}.json", encoding="utf-8")).get("ocena")
        if o in ("srednie", "slabe"): plan.append((w, nazwa, f, b, o))
print(len(plan), "budynkow x", len(SEEDY), "seedow", flush=True)
for w, nazwa, f, b, o in plan:
    for s in SEEDY:
        png = f"{OUT}/{w}_{b}_s{s}.png"
        if not os.path.exists(png): silnik.generuj(f(b, s), png); print(nazwa, T[b], s, flush=True)
# arkusz: wiersz = model + budynek, kolumny = oryginal (seed 42+i, z ocena) + 5 nowych seedow
C, LW = 240, 330; F = ImageFont.truetype("arialbd.ttf", 19); FS = ImageFont.truetype("arial.ttf", 16)
sh = Image.new("RGB", (LW + 6 * (C + 4), 70 + len(plan) * (C + 4) + 30), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "LoRA v1, prompty v1: budynki ocenione jako średnie/słabe – 5 nowych seedów", font=ImageFont.truetype("arialbd.ttf", 24), fill=(255, 255, 255))
for j, t in enumerate(["oryginał (seed 42+i)"] + [f"seed {s}" for s in SEEDY]): d.text((LW + j * (C + 4) + 4, 44), t, font=F, fill=(255, 230, 140))
import glob
for i, (w, nazwa, f, b, o) in enumerate(plan):
    y = 70 + i * (C + 4)
    d.text((10, y + 10), T[b], font=F, fill=(255, 255, 255)); d.text((10, y + 36), nazwa, font=FS, fill=(200, 210, 190))
    d.text((10, y + 60), "ocena oryginału: " + {"srednie": "średnie", "slabe": "słabe"}[o], font=FS, fill=(240, 190, 60) if o == "srednie" else (240, 110, 90))
    org = glob.glob(f"E:/ai/lora/output/{w}/samples/*__000002000_{b}.jpg")
    if org: sh.paste(Image.open(org[0]).convert("RGB").resize((C, C), Image.LANCZOS), (LW, y))
    for j, s in enumerate(SEEDY): sh.paste(Image.open(f"{OUT}/{w}_{b}_s{s}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + (j + 1) * (C + 4), y))
sh.save(f"{OUT}/arkusz.png"); print("KONIEC", sh.size)
