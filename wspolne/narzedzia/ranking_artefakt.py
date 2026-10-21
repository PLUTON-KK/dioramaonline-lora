"""Strona oceny dobre/slabe + ranking modeli. Zestawy (zakladki): v1 na promptach v1; pozniej v1 na promptach v2, v2-final...
Obrazy: te same co w zestawieniach (zestawienie_v1.py / zestawienie_v1_prompty_v2.py). db: ocena/<zestaw>__<wiersz>__<budynek> = {ocena: dobre|slabe|null}.
python ranking_artefakt.py [v1v1,v1v2,...]  -> E:/ai/runpod/ranking_lora.html"""
import base64, glob, io, json, os, re, sys
from PIL import Image

T = ["kwiaciarnia", "hotel", "stacja karetek", "budka z lodami", "dom turkusowy", "latarnia obok", "szklarnia", "obserwatorium", "weterynarz", "kino"]


def wiersze_z(skrypt):
    src = open(skrypt, encoding="utf-8").read(); ns = {}
    exec(src[:src.index("\nT = [")], ns); return ns


def b64(f):
    im = Image.open(f).convert("RGB"); im.thumbnail((320, 320), Image.LANCZOS); b = io.BytesIO(); im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def zestaw_v1v1():
    ns = wiersze_z("E:/ai/runpod/zestawienie_v1.py"); out = []
    for m, lora, res, kat, gdzie in ns["WIERSZE"]:
        fs = glob.glob(f"{kat}/**/*.jpg", recursive=True)
        kroki = {int(os.path.basename(f).split("__")[1].split("_")[0]) for f in fs}
        pelne = [k for k in kroki if sum(1 for f in fs if f"__{k:09d}_" in f) >= 4]; k = max(pelne)
        obr = {}
        for j in range(10):
            f = [x for x in fs if f"__{k:09d}_{j}." in x]
            if f: obr[j] = b64(f[0])
        out.append({"id": re.sub(r"[^A-Za-z0-9_\-.]", "_", os.path.basename(kat)), "model": m, "opis": f"LoRA {lora} · {res} px · {gdzie}", "obrazy": obr})
    return {"id": "v1v1", "nazwa": "LoRA v1 · prompty v1", "opis": "Wszystkie LoRA wytrenowane na zbiorze v1-final, generowane promptami testowymi v1 (krok 2000).", "wiersze": out}


def zestaw_v1v2():
    ns = wiersze_z("E:/ai/runpod/zestawienie_v1_prompty_v2.py"); out = []
    for m, lora, res, k, skad in ns["WIERSZE"]:
        obr = {}
        for j in range(10):
            f = glob.glob(f"{ns['G']}{k}/samples/*__000000000_{j}.jpg")
            if f: obr[j] = b64(f[0])
        out.append({"id": k, "model": m, "opis": f"LoRA {lora} · {res} px · {skad}", "obrazy": obr})
    return {"id": "v1v2", "nazwa": "LoRA v1 · prompty v2", "opis": "Te same LoRA v1, ten sam seed i ustawienia; zmieniony tylko tekst promptów (rozmiar w metrach, drzwi na froncie, budka bez zaprzeczenia).", "wiersze": out}


ZESTAWY = {"v1v1": zestaw_v1v1, "v1v2": zestaw_v1v2}
wybrane = sys.argv[1].split(",") if len(sys.argv) > 1 else ["v1v1"]
dane = {"budynki": T, "zestawy": [ZESTAWY[z]() for z in wybrane]}
html = open("E:/ai/runpod/ranking_szablon.html", encoding="utf-8").read().replace("/*DANE*/null", json.dumps(dane, ensure_ascii=False))
open("E:/ai/runpod/ranking_lora.html", "w", encoding="utf-8").write(html)
print(round(os.path.getsize("E:/ai/runpod/ranking_lora.html") / 1e6, 2), "MB;", [(z["id"], len(z["wiersze"]), sum(len(w["obrazy"]) for w in z["wiersze"])) for z in dane["zestawy"]])
