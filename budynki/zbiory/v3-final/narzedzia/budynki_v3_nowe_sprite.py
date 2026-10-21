"""Zbior v3, krok 1: wybrane nowe obrazy (etap 1 wyboru, E:/ai/runpod/wybor_v3_final_kandydaci.json) -> sprite w formacie gry, jak budynki v1/v2:
wyciecie z tla magenta, skala gry 24 px = 1 m (wejsciowe: wg drzwi, drzwi = 58 px + wklejony kanoniczny modul std-external-2;
dekoracyjne: wg szerokosci z promptu), paleta swiata 64 kolory, twarda alfa. Do tego podglad do pisania opisow.
Wynik: E:/ai/lora/lora-budynki-v3-robocze/sprites/<nazwa>.png, nowe.json, podglad_opisy.png"""
import json, os, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, "E:/ai/lora"); sys.path.insert(0, "E:/ai/runpod")
import nowe_budynki_krea_v2_test2 as T2
src = open("E:/ai/runpod/krea_v2_do_dioramy.py", encoding="utf-8").read()
ns = {}; exec(src[:src.index("wyn = []")], ns)          # wytnij, drzwi, paleta, MC, WYS_DRZWI
OUT = "E:/ai/lora/lora-budynki-v3-robocze"; os.makedirs(f"{OUT}/sprites", exist_ok=True)
W = "E:/ai/wyniki/"
FOL = {"krea": "nowe_budynki_krea_lora_v2-test-v2", "flux3d": "nowe_budynki_flux3-klein-destylat_lora_v2-test-v2", "moss": "nowe_budynki_moss-image-sft_lora_v2-test-v2"}
NAZWY = {"elektrownia węglowa": "elektrownia-weglowa", "elektrownia atomowa": "elektrownia-atomowa", "turbina wiatrowa": "turbina-wiatrowa", "farma fotowoltaiczna": "farma-fotowoltaiczna",
         "rafineria": "rafineria", "tartak": "tartak", "oczyszczalnia ścieków": "oczyszczalnia-sciekow", "punkt skupu złomu": "skup-zlomu", "wieżowiec szklany": "wiezowiec-szklany",
         "wieża ciśnień": "wieza-cisnien", "maszt telekomunikacyjny": "maszt-telekomunikacyjny", "silos zbożowy": "silos-zbozowy", "cyrk": "cyrk", "meczet": "meczet",
         "wiatrak holenderski": "wiatrak", "zamek": "zamek", "piramida w wesołym miasteczku": "piramida-wesole-miasteczko", "szpital": "szpital", "bank": "bank",
         "stacja benzynowa": "stacja-benzynowa", "plac zabaw": "plac-zabaw", "kurnik": "kurnik", "szklarnia tunelowa": "szklarnia-tunelowa", "silos przy farmie": "silos-farma"}
ids = json.load(open("E:/ai/runpod/wybor_v3_final_kandydaci.json"))
licz, nowe = {}, []
for kid in ids:
    m, war, i = kid.split("__"); i = int(i); e = T2.L[i]
    f = f"{W}{FOL[m]}-seedy/K_{i}_s{war[2:]}.png" if war.startswith("Ks") else f"{W}{FOL[m]}/{war}_{i}.png"
    baza = NAZWY[e[1]]; licz[baza] = licz.get(baza, 0) + 1; nazwa = f"{baza}-{licz[baza]}"
    org = Image.open(f).convert("RGB"); b = ns["wytnij"](org); rec = {"nazwa": nazwa, "obiekt": e[1], "zrodlo_id": kid, "plik": f, "typ": "wejsciowy" if e[2] == "enterable" else "dekoracyjny"}
    if e[2] == "enterable":
        sc, bb = ns["drzwi"](b); s = ns["WYS_DRZWI"] / (bb[3] - bb[1]); rec["skala_wg"] = "drzwi"; rec["pewnosc_drzwi"] = round(sc, 2)
    else:
        s = e[4] * 24 / b.width; bb = None; rec["skala_wg"] = f"szerokosc z promptu {e[4]} m"
    gm = ns["paleta"](b.convert("RGBa").resize((max(1, round(b.width * s)), max(1, round(b.height * s))), Image.BOX).convert("RGBA"))
    from scipy import ndimage
    for _ in range(3):   # resztki magenty na brzegu -> przezroczyste
        al = gm[..., 3] > 0; brzeg = al & ~ndimage.binary_erosion(al); c = gm[..., :3].astype(int)
        gm[brzeg & (c[..., 0] - c[..., 1] > 15) & (c[..., 2] - c[..., 1] > 15), 3] = 0
    MC, mh, mw = ns["MC"], ns["MC"].shape[0], ns["MC"].shape[1]
    if bb is not None:
        d = [round(v * s) for v in bb]; cx = (d[0] + d[2]) / 2
        px = max(0, min(gm.shape[1] - mw, int(round(cx - mw / 2)))); py = max(0, min(gm.shape[0], d[1] + ns["WYS_DRZWI"]) - mh)
        gm[py:py + mh, px:px + mw] = np.where(MC[..., 3:4] > 0, MC, gm[py:py + mh, px:px + mw])
    gi = Image.fromarray(gm); bx = gi.getchannel("A").getbbox(); gi = gi.crop(bx)
    if bb is not None:
        px -= bx[0]; py -= bx[1]; rec["drzwi"] = {"x_px": px, "y_px": py, "w_px": mw, "h_px": mh}
        sr = (px + mw / 2) / gi.width; rec["drzwi_polozenie"] = "middle" if 0.35 <= sr <= 0.65 else ("left" if sr < 0.35 else "right")
    rec.update(w_px=gi.width, h_px=gi.height, szer_m=round(gi.width / 24, 2), wys_sprite_m=round(gi.height / 24, 2))
    gi.save(f"{OUT}/sprites/{nazwa}.png"); nowe.append(rec)
    print(f"{nazwa:30} {rec['typ']:11} {gi.width}x{gi.height} = {rec['szer_m']} x {rec['wys_sprite_m']} m  {rec.get('drzwi_polozenie', '')}")
json.dump(nowe, open(f"{OUT}/nowe.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# podglad do opisow: oryginal 512 obok sprite'a (x2), z nazwa
F = ImageFont.truetype("arialbd.ttf", 18); FS = ImageFont.truetype("arial.ttf", 15)
C = 380; sh = Image.new("RGB", (2 * (C * 2 + 30), (len(nowe) + 1) // 2 * (C + 40)), (40, 48, 36)); d = ImageDraw.Draw(sh)
for n, r in enumerate(nowe):
    x, y = (n % 2) * (C * 2 + 30), (n // 2) * (C + 40)
    sh.paste(Image.open(r["plik"]).convert("RGB").resize((C, C)), (x, y))
    g = Image.open(f"{OUT}/sprites/{r['nazwa']}.png"); k = min(C / g.width, C / g.height); g2 = g.resize((max(1, int(g.width * k)), max(1, int(g.height * k))), Image.NEAREST)
    bg = Image.new("RGBA", (C, C), (255, 0, 255, 255)); bg.alpha_composite(g2, ((C - g2.width) // 2, C - g2.height)); sh.paste(bg.convert("RGB"), (x + C + 4, y))
    d.text((x, y + C + 4), f"{r['nazwa']} · {r['szer_m']:.1f} x {r['wys_sprite_m']:.1f} m · {r['typ']} {r.get('drzwi_polozenie', '')}", font=F, fill=(255, 230, 140))
sh.save(f"{OUT}/podglad_opisy.png"); print(sh.size)
