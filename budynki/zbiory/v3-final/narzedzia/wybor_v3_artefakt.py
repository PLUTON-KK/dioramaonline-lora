"""Strona etapu 1 wyboru do zbioru v3: wszystkie obrazy test-v2 (Krea 2 Turbo, FLUX 3 Klein destylat, MOSS-Image SFT, Z-Image Turbo; v2/J/K),
bez budynkow wejsciowych odrzuconych przy dopasowaniu drzwi (E:/ai/wyniki/nowe_budynki_drzwi_odrzucone.json). db: etap1/<model>__<war>__<i> = {odrzucony}.
Wynik: E:/ai/runpod/wybor_v3.html"""
import base64, io, json, os, sys
from PIL import Image
sys.path.insert(0, "E:/ai/lora")
import nowe_budynki_krea_v2_test2 as T2
W = "E:/ai/wyniki/"
MODELE = [("krea", "Krea 2 Turbo", W + "nowe_budynki_krea_lora_v2-test-v2"), ("flux3d", "FLUX 3 Klein destylat", W + "nowe_budynki_flux3-klein-destylat_lora_v2-test-v2"),
          ("moss", "MOSS-Image SFT", W + "nowe_budynki_moss-image-sft_lora_v2-test-v2"), ("zimage", "Z-Image Turbo", W + "nowe_budynki_zimage-turbo_lora_v2-test-v2")]
ODRZ = json.load(open(W + "nowe_budynki_drzwi_odrzucone.json", encoding="utf-8"))


def b64(f):
    im = Image.open(f).convert("RGB"); im.thumbnail((300, 300), Image.LANCZOS); b = io.BytesIO(); im.save(b, "JPEG", quality=84)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


obiekty, grupy, brak = [], [], 0
POMIN = {30}   # supermarket test-v2 mial parking w prompcie - q3ok: zawsze odpada (parking robimy osobno assetami podlogi i aut)
for i, e in enumerate(T2.L):
    if i in POMIN: continue
    if e[0] not in grupy: grupy.append(e[0])
    ob = []
    for kod, nazwa, d in MODELE:
        for war in ("v2", "J", "K"):
            f = f"{d}/{war}_{i}.png"
            if not os.path.exists(f): brak += 1; continue
            if f"{kod}|{war}|{i}" in ODRZ: continue
            ob.append({"id": f"{kod}__{war}__{i}", "m": kod, "w": war, "src": b64(f)})
    for s in (1001, 2002, 3003, 4004, 5005):   # dogenerowane: Krea, prompt K, nowe seedy (obiekty bez wyboru w etapie 1)
        f = f"{W}nowe_budynki_krea_lora_v2-test-v2-seedy/K_{i}_s{s}.png"
        if os.path.exists(f) and f"krea|Ks{s}|{i}" not in ODRZ: ob.append({"id": f"krea__Ks{s}__{i}", "m": "krea", "w": f"Ks{s}", "src": b64(f)})
    obiekty.append({"nazwa": e[1], "grupa": e[0], "typ": e[2], "obrazy": ob})
dane = {"modele": [{"kod": k, "nazwa": n} for k, n, _ in MODELE], "grupy": grupy, "obiekty": obiekty, "odrzuconeDrzwi": len(ODRZ)}
html = open("E:/ai/runpod/wybor_v3_szablon.html", encoding="utf-8").read().replace("/*DANE*/null", json.dumps(dane, ensure_ascii=False))
open("E:/ai/runpod/wybor_v3.html", "w", encoding="utf-8").write(html)
print(round(os.path.getsize("E:/ai/runpod/wybor_v3.html") / 1e6, 2), "MB;", sum(len(o["obrazy"]) for o in obiekty), "obrazow; brak plikow:", brak, "; odrzucone drzwi:", len(ODRZ))
