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


def zestaw_seedy():
    import json as _j
    S = "E:/ai/wyniki/seedy_top3_v1"; SEEDY = [1001, 2002, 3003, 4004, 5005]
    W = [("swiat2d_zimage_budynki_v1final_512", "Z-Image Turbo", "LoRA v1, 512 px"), ("zestawienie_moss_sft_lora_base1024", "MOSS-Image SFT", "LoRA v1 (z Base), 1024 px"),
         ("zestawienie_krea2turbo_lora_raw512", "Krea 2 Turbo int8", "LoRA v1 (z Raw), 512 px")]
    out = []
    for w, m, war in W:
        for b in range(10):
            o = _j.load(open(f"E:/ai/runpod/ranking_oceny_akt/ocena/v1v1__{w}__{b}.json", encoding="utf-8")).get("ocena")
            if o not in ("srednie", "slabe"): continue
            obr = {}
            org = glob.glob(f"E:/ai/lora/output/{w}/samples/*__000002000_{b}.jpg")
            if org: obr[0] = b64(org[0])
            for j, sd in enumerate(SEEDY, 1): obr[j] = b64(f"{S}/{w}_{b}_s{sd}.png")
            out.append({"id": f"{w}_b{b}", "model": f"{m} · {T[b]}", "opis": f"{war} · oryginał oceniony jako {'średnie' if o == 'srednie' else 'słabe'}", "obrazy": obr})
    return {"id": "seedy", "nazwa": "LoRA v1 · prompty v1 · nowe seedy", "kolumny": ["oryginał (seed 42+i)"] + [f"seed {s}" for s in SEEDY],
            "opis": "Budynki ocenione jako średnie/słabe w 3 najlepszych wierszach rankingu v1, po 5 nowych seedów (ten sam prompt v1 i LoRA). Pierwsza kolumna: obraz z rankingu (możesz ocenić ponownie).", "wiersze": out}


def zestaw_v2v2():
    MOD = [("zimageturbo", "Z-Image Turbo"), ("zimagebase", "Z-Image Base"), ("mossbase", "MOSS-Image Base"), ("flux3base", "FLUX 3 Klein base"),
           ("klein4b", "FLUX.2 Klein 4B"), ("qwenimage2512", "Qwen-Image 2512"), ("krea2raw", "Krea 2 Raw")]
    out = []
    for k, m in MOD:
        obr = {}
        for j in range(10):
            f = glob.glob(f"E:/ai/runpod/wyniki/podglady/swiat2d_{k}_budynki_v2final_512/**/*__000002000_{j}.jpg", recursive=True)
            if f: obr[j] = b64(f[0])
        out.append({"id": f"v2_{k}", "model": m, "opis": "LoRA v2-final · 512 px · podgląd z treningu (ai-toolkit, krok 2000, bf16, seed 42+i)", "obrazy": obr})
    for k, m, op in [("mosssft_512", "MOSS-Image SFT", "LoRA v2-final (z Base) · 512 px · ComfyUI RTX 3080"),
                     ("flux3destylat_512", "FLUX 3 Klein (destylat)", "LoRA v2-final (z base) · 512 px · ComfyUI RTX 3080"),
                     ("klein4bdestylat_512", "FLUX.2 Klein 4B (destylat)", "LoRA v2-final (z base) · 512 px · ComfyUI RTX 3080"),
                     ("krea2turbo_512", "Krea 2 Turbo int8", "LoRA v2-final (z Raw) · 512 px · ComfyUI RTX 3080")]:
        obr = {}
        for j in range(10):
            f = glob.glob(f"E:/ai/runpod/wyniki/output/gen_v2lekkie_{k}/samples/*__000002000_{j}.jpg")
            if f: obr[j] = b64(f[0])
        if obr: out.append({"id": f"v2l_{k}", "model": m, "opis": op + " (seed 42+i)", "obrazy": obr})
    return {"id": "v2v2", "nazwa": "LoRA v2 · prompty v2", "opis": "LoRA wytrenowane na zbiorze v2-final (ciasny kadr, rozmiar w metrach w opisie), prompty testowe v2, krok 2000. Porównuj z zakładką „LoRA v1 · prompty v2” (te same prompty, stara LoRA).", "wiersze": out}


ZESTAWY = {"v1v1": zestaw_v1v1, "v1v2": zestaw_v1v2, "seedy": zestaw_seedy, "v2v2": zestaw_v2v2}
wybrane = sys.argv[1].split(",") if len(sys.argv) > 1 else ["v1v1"]
dane = {"budynki": T, "zestawy": [ZESTAWY[z]() for z in wybrane]}
html = open("E:/ai/runpod/ranking_szablon.html", encoding="utf-8").read().replace("/*DANE*/null", json.dumps(dane, ensure_ascii=False))
open("E:/ai/runpod/ranking_lora.html", "w", encoding="utf-8").write(html)
print(round(os.path.getsize("E:/ai/runpod/ranking_lora.html") / 1e6, 2), "MB;", [(z["id"], len(z["wiersze"]), sum(len(w["obrazy"]) for w in z["wiersze"])) for z in dane["zestawy"]])
