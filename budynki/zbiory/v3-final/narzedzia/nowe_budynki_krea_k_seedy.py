"""Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512), prompt K (test-v2) dla obiektow, ktore w etapie 1 wyboru do v3 nie zostawily zadnego obrazu,
5 nowych seedow (1001-5005). Wynik: E:/ai/wyniki/nowe_budynki_krea_lora_v2-test-v2-seedy/K_<i>_s<seed>.png + arkusz.png"""
import json, os, sys
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
import nowe_budynki_krea_v2_test2 as T2
OUT = "E:/ai/wyniki/nowe_budynki_krea_lora_v2-test-v2-seedy"; os.makedirs(OUT, exist_ok=True)
SEEDY = [1001, 2002, 3003, 4004, 5005]
zost = json.load(open("E:/ai/runpod/wybor_v3_etap1_zostaje.json"))
majace = {int(i.split("__")[2]) for i in zost}
IDX = [i for i in range(len(T2.L)) if i not in majace]
# q3ok 2026-10-21: elektrownie i przemysl BEZ dymu i pary (dym, jesli potrzebny, generuje diorama)
BEZ_DYMU = {"elektrownia atomowa": (" with a white plume of steam,", ","), "rafineria": ("a thin flare stack with a small flame", "a thin flare stack")}
L = []
for e in T2.L:
    e = list(e)
    if e[1] in BEZ_DYMU: e[8] = e[8].replace(*BEZ_DYMU[e[1]])
    if e[0] == "przemysł": e[8] += ", no smoke and no steam"
    L.append(tuple(e))
T2.L = L
if __name__ == "__main__":
    assert not T2.sprawdz()
    from PIL import Image, ImageDraw, ImageFont
    import silnik
    import dogeneruj_zestawienie_v1_lekkie as LK
    with open(f"{OUT}/prompty.txt", "w", encoding="utf-8") as f:
        f.write(f"Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512), prompt K, seedy {SEEDY}\n\n")
        for i in IDX: f.write(f"[K] {T2.L[i][1]}\n{T2.uzd(T2.L[i], 'K')}\n\n")
    for i in IDX:
        for s in SEEDY:
            png = f"{OUT}/K_{i}_s{s}.png"
            if os.path.exists(png): continue
            LK.P = {i: T2.uzd(T2.L[i], "K")}
            w = LK.wf("zestawienie_krea2turbo_lora_raw512", i); w["lora"]["inputs"]["lora_name"] = "swiat2d_v2f512_krea2raw_2000.safetensors"
            w["ks"]["inputs"]["seed"] = s
            silnik.generuj(w, png); print(i, s, T2.L[i][1], flush=True)
    C, LW = 240, 260; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 15)
    sh = Image.new("RGB", (LW + 5 * (C + 4), 76 + len(IDX) * (C + 4)), (40, 48, 36)); d = ImageDraw.Draw(sh)
    d.text((10, 10), "MODEL: Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512) – prompt K (semi-realistic), 5 nowych seedów, obiekty bez wyboru w etapie 1",
           font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
    for j, s in enumerate(SEEDY): d.text((LW + j * (C + 4) + 4, 48), f"seed {s}", font=F, fill=(255, 230, 140))
    for r, i in enumerate(IDX):
        y = 76 + r * (C + 4); d.text((10, y + 10), T2.L[i][1], font=F, fill=(255, 255, 255)); d.text((10, y + 36), T2.L[i][0], font=FS, fill=(200, 210, 190))
        for j, s in enumerate(SEEDY): sh.paste(Image.open(f"{OUT}/K_{i}_s{s}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + j * (C + 4), y))
    sh.save(f"{OUT}/arkusz.png"); print("KONIEC")
