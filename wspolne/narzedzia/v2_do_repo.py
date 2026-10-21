"""Wyniki LoRA v2 -> repo: zestawienie z ocenami (11 wierszy), oceny.csv, tabele do README (ranking v2, porownanie z v1)."""
import json, os, csv, glob
from PIL import Image, ImageDraw, ImageFont
src = open("E:/ai/runpod/ranking_artefakt.py", encoding="utf-8").read(); ns = {}
exec(src[:src.index("ZESTAWY = ")], ns); ns["b64"] = lambda f: f
R = "E:/ai/dioramaonline-lora/budynki/porownania/2026-10-21_lora-v2_prompty-v2"; os.makedirs(R, exist_ok=True)
D = "E:/ai/runpod/ranking_oceny_akt/ocena"; PKT = {"dobre": 2, "srednie": 1, "slabe": 0}; PL = {"dobre": "dobre", "srednie": "średnie", "slabe": "słabe", None: "–"}
T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia z domkiem", "szklarnia", "obserwatorium", "weterynarz", "kino"]
def oc(z, w, j):
    f = f"{D}/{z}__{w}__{j}.json"; return json.load(open(f, encoding="utf-8")).get("ocena") if os.path.exists(f) else None
# odpowiedniki: wiersz v2 -> (wiersz v1 prompty v1, wiersz v1 prompty v2), czas RTX 3080
ODP = {"v2_zimageturbo": ("swiat2d_zimage_budynki_v1final_512", "zimageturbo_512", "15 s"), "v2_zimagebase": ("swiat2d_zimagebase_budynki_v1final_512", "zimagebase_512", "33 s"),
       "v2_mossbase": ("swiat2d_moss_base_budynki_v1final_512", "mossbase_512", "7.8 s"), "v2_flux3base": ("swiat2d_flux3_base_budynki_v1final_512", "flux3base_512", "8.7 s"),
       "v2_klein4b": ("swiat2d_klein4b_budynki_v1final_512", "klein4bbase_512", "16 s"), "v2_qwenimage2512": ("swiat2d_qwenimage2512_budynki_v1final_512", "qwenimage2512_512", "za duży"),
       "v2_krea2raw": ("swiat2d_krea2raw_budynki_v1final_512", "krea2raw_512", "za duży"), "v2l_mosssft_512": ("zestawienie_moss_sft_lora_base512", "mosssft_512", "7.7 s"),
       "v2l_flux3destylat_512": ("zestawienie_flux3_destylat_lora_base512", "flux3destylat_512", "2.6 s"), "v2l_klein4bdestylat_512": ("zestawienie_klein4b_destylat_lora_base512", "klein4bdestylat_512", "3.1 s"),
       "v2l_krea2turbo_512": ("zestawienie_krea2turbo_lora_raw512", "krea2turbo_512", "8.2 s")}
W = ns["zestaw_v2v2"]()["wiersze"]
wiersze = []
for w in W:
    o = [oc("v2v2", w["id"], j) for j in range(10)]; a, b, czas = ODP[w["id"]]
    p1 = sum(PKT.get(oc("v1v1", a, j), 0) for j in range(10)); p12 = sum(PKT.get(oc("v1v2", b, j), 0) for j in range(10))
    gdzie = "podgląd z treningu (RunPod)" if w["id"].startswith("v2_") else "ComfyUI RTX 3080"
    wiersze.append(dict(w=w, o=o, p=sum(PKT.get(x, 0) for x in o), d=o.count("dobre"), s=o.count("srednie"), sl=o.count("slabe"), n=o.count(None), p1=p1, p12=p12, czas=czas, gdzie=gdzie))
wiersze.sort(key=lambda x: -x["p"])
# zestawienie
KOL = {"dobre": (70, 200, 90), "srednie": (235, 185, 50), "slabe": (225, 70, 60)}
C, LW = 230, 360; F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 15)
sh = Image.new("RGB", (LW + 10 * (C + 4), 80 + len(wiersze) * (C + 4) + 10), (40, 48, 36)); d = ImageDraw.Draw(sh)
d.text((10, 10), "LoRA budynki v2-final (512 px) na promptach v2, seed 42+i, krok 2000 – ramka = ocena właściciela (zielona dobre, żółta średnie, czerwona słabe)", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
for j, t in enumerate(T): d.text((LW + j * (C + 4) + 4, 52), t, font=F, fill=(255, 230, 140))
for i, x in enumerate(wiersze):
    y = 80 + i * (C + 4); w = x["w"]
    d.text((10, y + 8), w["model"], font=ImageFont.truetype("arialbd.ttf", 20), fill=(255, 255, 255))
    d.multiline_text((10, y + 36), w["opis"].replace(" · ", "\n"), font=FS, fill=(200, 210, 190))
    d.text((10, y + C - 30), f"{x['p']} pkt (v1 na promptach v1: {x['p1']})", font=F, fill=(255, 230, 140))
    for j in range(10):
        xx = LW + j * (C + 4); f = w["obrazy"].get(j)
        if f: sh.paste(Image.open(f).convert("RGB").resize((C, C), Image.LANCZOS), (xx, y))
        if x["o"][j]: d.rectangle([xx, y, xx + C - 1, y + C - 1], outline=KOL[x["o"][j]], width=5)
sh.save(f"{R}/zestawienie.png"); print(sh.size)
with open(f"{R}/oceny.csv", "w", newline="", encoding="utf-8") as fh:
    c = csv.writer(fh); c.writerow(["model", "lora", "budynek", "ocena"])
    for x in wiersze:
        for j in range(10): c.writerow([x["w"]["model"], x["w"]["opis"].split(" · ")[0], T[j], PL[x["o"][j]]])
# tabele
print("| # | model | LoRA | obraz | punkty | dobre | średnie | słabe | v1 · prompty v1 | v1 · prompty v2 | RTX 3080 / obraz |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for i, x in enumerate(wiersze, 1):
    w = x["w"]; lora = w["opis"].split(" · ")[0].replace("LoRA ", "")
    print(f"| {i} | {w['model']} | {lora} | {x['gdzie']} | **{x['p']}**{'*' if x['n'] else ''} | {x['d']} | {x['s']} | {x['sl']} | {x['p1']} | {x['p12']} | {x['czas']} |")
print("SUMA v2", sum(x["p"] for x in wiersze), "v1v1", sum(x["p1"] for x in wiersze), "v1v2", sum(x["p12"] for x in wiersze))
print("\n| budynek | dobre | średnie | słabe | oceniony jako „dobre” u |\n|---|---|---|---|---|")
for j, t in enumerate(T):
    o = [x["o"][j] for x in wiersze]
    print(f"| {t} | {o.count('dobre')} | {o.count('srednie')} | {o.count('slabe')} | {', '.join(x['w']['model'] for x in wiersze if x['o'][j] == 'dobre') or '–'} |")
