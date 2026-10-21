"""Strona porownan parami (Bradley-Terry): dwa obrazy TEGO SAMEGO budynku z roznych wierszy. Pula: LoRA v1 + prompty v1 oraz LoRA v2 + prompty v2,
tylko obrazy ocenione wczesniej jako dobre (v1 na promptach v2 pominiete - w zbiorze v1 nie bylo rozmiarow).
Obrazy: te same co w ranking_artefakt.py, w pelnej rozdzielczosci jako arkusze 10 kafli (elo_arkusze/<id>.jpg).
Pominiete: Qwen-Edit 2511 (wykluczony) i Qwen Q4 GGUF (niepasujacy model). db: glosy/<sesja>_<n> = {v: [[a, b, wynik, czas], ...]}
Wynik: E:/ai/runpod/elo_lora.html + E:/ai/runpod/elo_arkusze/"""
import json, os, re
from PIL import Image
src = open("E:/ai/runpod/ranking_artefakt.py", encoding="utf-8").read(); ns = {}
exec(src[:src.index("ZESTAWY = ")], ns); ns["b64"] = lambda f: f   # sciezki zamiast base64
OUT = "E:/ai/runpod/elo_arkusze"; os.makedirs(OUT, exist_ok=True); S = 512
def ocena(z, w, j):
    f = f"E:/ai/runpod/ranking_oceny_akt/ocena/{z}__{w}__{j}.json"
    return json.load(open(f, encoding="utf-8")).get("ocena") if os.path.exists(f) else None
KROTKO = {"v1v1": "LoRA v1 · prompty v1", "v1v2": "LoRA v1 · prompty v2", "v2v2": "LoRA v2 · prompty v2"}
wiersze = []
for z in ("v1v1", "v2v2"):
    for w in ns["zestaw_" + z]()["wiersze"]:
        if re.search(r"2511|qwenimage_q4", w["id"]): continue
        dobre = [j for j in w["obrazy"] if ocena(z, w["id"], j) == "dobre"]   # tylko obrazy ocenione jako dobre
        if not dobre: continue
        rid = f"{z}__{w['id']}"; ark = Image.new("RGB", (S * 10, S), (0, 0, 0))
        for j, f in w["obrazy"].items(): ark.paste(Image.open(f).convert("RGB").resize((S, S), Image.LANCZOS), (j * S, 0))
        ark.save(f"{OUT}/{rid}.jpg", quality=86)
        res = re.search(r"(\d{3,4}) px", w["opis"]); 
        wiersze.append({"id": rid, "zestaw": KROTKO[z], "model": w["model"], "opis": w["opis"], "px": res.group(1) if res else "", "j": sorted(dobre)})
dane = {"budynki": ns["T"], "wiersze": wiersze}
html = open("E:/ai/runpod/elo_szablon.html", encoding="utf-8").read().replace("/*DANE*/null", json.dumps(dane, ensure_ascii=False))
open("E:/ai/runpod/elo_lora.html", "w", encoding="utf-8").write(html)
tot = sum(os.path.getsize(f"{OUT}/{w['id']}.jpg") for w in wiersze)
print(len(wiersze), "wierszy,", sum(len(w["j"]) for w in wiersze), "obrazow, arkusze", round(tot / 1e6, 1), "MB")
for w in wiersze: print(w["id"], "|", w["model"], "|", w["zestaw"], w["px"])
