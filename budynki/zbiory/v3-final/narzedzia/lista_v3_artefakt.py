"""Strona koncowej listy zbioru v3 (E:/ai/lora/lora-budynki-v3): obraz train_512 + opis + przycisk wykluczenia. db: v3/<nazwa> = {odrzucony}.
Wynik: E:/ai/runpod/lista_v3.html"""
import base64, io, json
from PIL import Image
D = "E:/ai/lora/lora-budynki-v3"
NM = {"krea": "Krea 2 Turbo", "flux3d": "FLUX 3 Klein destylat", "moss": "MOSS-Image SFT"}
dane = []
for l in open(f"{D}/metadata.jsonl", encoding="utf-8"):
    m = json.loads(l); b = io.BytesIO(); Image.open(f"{D}/train_512/{m['nazwa']}.png").convert("RGB").save(b, "PNG", optimize=True)
    zr = ""
    if m["zrodlo"] != "v2-final":
        mod, war, _ = m["zrodlo"][6:].split("__"); zr = f"{NM[mod]} · prompt {war if not war.startswith('Ks') else 'K, seed ' + war[2:]}"
    dane.append({"nazwa": m["nazwa"], "nowy": m["zrodlo"] != "v2-final", "typ": m["typ"], "szer": round(m["szer_m"]), "wys": round(m["wys_sprite_m"]), "zrodlo": zr,
                 "caption": m["caption"], "src": "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()})
html = open("E:/ai/runpod/lista_v3_szablon.html", encoding="utf-8").read().replace("/*DANE*/null", json.dumps(dane, ensure_ascii=False))
open("E:/ai/runpod/lista_v3.html", "w", encoding="utf-8").write(html)
import os; print(len(dane), round(os.path.getsize("E:/ai/runpod/lista_v3.html") / 1e6, 2), "MB")
