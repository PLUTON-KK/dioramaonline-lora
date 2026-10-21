"""LoRA budynki v3: siatka krokow per model - wiersz = krok (0, 250, ...), kolumna = prompt testowy v3 (7 zwyklych + 7 uzdatnionych K).
python arkusz_krokow_v3.py <kod>  -> wyniki/v3_kroki_<kod>.png; wypisuje gotowe kroki"""
import glob, os, sys, time
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai/lora")
import prompty_test_v3 as PT
D = "E:/ai/runpod/wyniki/podglady"; W = "E:/ai/runpod/wyniki"
NM = {"zimageturbo": "Z-Image Turbo", "flux3base": "FLUX 3 Klein base", "mossbase": "MOSS-Image Base", "krea2raw": "Krea 2 Raw"}


def pliki(kod):
    fs = glob.glob(f"{D}/swiat2d_{kod}_budynki_v3_512/**/*.jpg", recursive=True); o = {}
    for f in fs:
        b = os.path.basename(f)[:-4].split("__")[-1]; k, j = b.split("_"); o.setdefault(int(k), {})[int(j)] = f
    return o


def arkusz(kod):
    o = pliki(kod); kroki = sorted(o)
    if not kroki: return None, []
    C, LW, H = 200, 150, 96; n = len(PT.NAZWY); F = ImageFont.truetype("arialbd.ttf", 15); FS = ImageFont.truetype("arial.ttf", 13)
    sh = Image.new("RGB", (LW + n * (C + 3) + 12, H + len(kroki) * (C + 3)), (40, 48, 36)); d = ImageDraw.Draw(sh)
    d.text((10, 8), f"MODEL: {NM[kod]} + LoRA budynki v3 (512) – podglądy z treningu (ai-toolkit, bf16, seed 42+i); krok 0 = bez LoRA", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
    for j, t in enumerate(PT.NAZWY):
        x = LW + j * (C + 3) + (12 if j >= 7 else 0)
        d.multiline_text((x + 3, 40), t.replace(" (K)", "\n(uzdatniony K)").replace("gospodarstwo ", "gospodarstwo\n"), font=FS, fill=(255, 230, 140) if j < 7 else (180, 220, 255))
    for r, k in enumerate(kroki):
        y = H + r * (C + 3); d.text((10, y + 10), f"krok {k}", font=F, fill=(255, 255, 255)); d.text((10, y + 32), f"{len(o[k])}/{n}", font=FS, fill=(200, 210, 190))
        for j in range(n):
            x = LW + j * (C + 3) + (12 if j >= 7 else 0)
            if j in o[k]: sh.paste(Image.open(o[k][j]).convert("RGB").resize((C, C), Image.LANCZOS), (x, y))
            else: d.rectangle([x, y, x + C, y + C], fill=(30, 34, 28))
    out = f"{W}/v3_kroki_{kod}.png"
    try: sh.save(out)
    except OSError: out = out.replace(".png", time.strftime("_%H%M.png")); sh.save(out)
    return out, [k for k in kroki if len(o[k]) >= n]


if __name__ == "__main__":
    print(arkusz(sys.argv[1]))
