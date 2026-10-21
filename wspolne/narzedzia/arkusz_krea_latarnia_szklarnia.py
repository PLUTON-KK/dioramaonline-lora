"""Krea 2 Turbo int8 (LoRA z Krea 2 Raw, 512): wszystko co mamy dla latarni i szklarni na jednym arkuszu."""
import glob, re
from PIL import Image, ImageDraw, ImageFont
src = open("E:/ai/runpod/ranking_artefakt.py", encoding="utf-8").read(); ns = {}
exec(src[:src.index("ZESTAWY = ")], ns); ns["b64"] = lambda f: f
v1 = [w for w in ns["zestaw_v1v1"]()["wiersze"] if w["id"] == "zestawienie_krea2turbo_lora_raw512"][0]["obrazy"]
G = "E:/ai/runpod/wyniki/output/"; S = "E:/ai/wyniki/seedy_top3_v1/zestawienie_krea2turbo_lora_raw512_"
def g(p): x = glob.glob(p); return x[0] if x else None
KOL = [("LoRA v1 · prompt v1\nseed 42+i · ocena: średnie", lambda b: v1.get(b))] + \
      [(f"LoRA v1 · prompt v1\nseed {s}", lambda b, s=s: f"{S}{b}_s{s}.png") for s in (1001, 2002, 3003, 4004, 5005)] + \
      [("LoRA v1 · uzdatniony J\n(realistic shading) seed 271828", lambda b: g(f"{G}gen_uzd_krea2turbo_512/samples/*__000000000_{b+10}.jpg")),
       ("LoRA v1 · uzdatniony K\n(semi-realistic) seed 271828", lambda b: g(f"{G}gen_uzd_krea2turbo_512/samples/*__000000000_{b+20}.jpg")),
       ("LoRA v2 · prompt v2\nseed 42+i · ocena: średnie", lambda b: g(f"{G}gen_v2lekkie_krea2turbo_512/samples/*__000002000_{b}.jpg"))]
C, LW, H = 300, 170, 110; F = ImageFont.truetype("arialbd.ttf", 22); FS = ImageFont.truetype("arial.ttf", 16)
sh = Image.new("RGB", (LW + len(KOL) * (C + 6), H + 2 * (C + 6) + 10), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "MODEL: Krea 2 Turbo int8 + LoRA budynki (z Krea 2 Raw, 512 px) – latarnia i szklarnia, wszystkie wygenerowane warianty", font=ImageFont.truetype("arialbd.ttf", 26), fill=(255, 255, 255))
for j, (t, _) in enumerate(KOL): d.multiline_text((LW + j * (C + 6) + 4, 50), t, font=FS, fill=(255, 230, 140))
for r, (b, nz) in enumerate([(5, "latarnia\nz domkiem"), (6, "szklarnia")]):
    y = H + r * (C + 6); d.multiline_text((10, y + 10), nz, font=F, fill=(255, 255, 255))
    for j, (_, fn) in enumerate(KOL):
        f = fn(b); x = LW + j * (C + 6)
        if f: sh.paste(Image.open(f).convert("RGB").resize((C, C), Image.LANCZOS), (x, y))
sh.save("E:/ai/runpod/wyniki/krea2turbo_latarnia_szklarnia.png"); print(sh.size)
