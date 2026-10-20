"""Lista wszystkich budynkow do zbioru LoRA (budynki) + opisy (caption) + strona oceny.
- dekoracyjne z paskow 10-11: wyciecie, skala jak budynki wejsciowe z tych samych paskow (srednia 0.575 px oryg. -> px gry), paleta swiata;
- wejsciowe: wejsciowe-v2\\<n>-closed.png (+open), dekoracyjne: gotowe\\ + dekoracyjne\\, z gry: 054-zrodla (B1-B4, townhall);
- caption wg TYPY-BUDYNKOW.md; zapis: E:\\ai\\codex_paczki\\budynki\\lora-lista.json + lora-lista.csv + przeglad (artefakt) html."""
import base64, csv, io, json, os
import numpy as np
from PIL import Image

B = r"E:\ai\codex_paczki\budynki"; os.makedirs(os.path.join(B, "dekoracyjne"), exist_ok=True)
PAL = np.array(json.load(open(r"E:\ai\skrzynka\odpowiedzi\world_palette.json", encoding="utf-8-sig")), np.int32)
src = open(r"E:\ai\lora\budynki_gotowe.py", encoding="utf-8").read(); ns = {}; exec(src[:src.index("def do_gry")], ns)
SKALA_STRIP = 0.575


def do_gry(im, s):
    g = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.BOX)
    a = np.array(g).astype(np.int32); al = a[..., 3] >= 128; rgb = a[..., :3][al]
    u, inv = np.unique(rgb, axis=0, return_inverse=True); m = PAL[((u[:, None] - PAL[None]) ** 2).sum(2).argmin(1)]
    o = np.zeros_like(a); o[..., :3][al] = m[inv.ravel()]; o[..., 3] = np.where(al, 255, 0)
    g = Image.fromarray(o.astype(np.uint8), "RGBA"); return g.crop(g.getchannel("A").getbbox())


DEK_NOWE = {"pasek10.png": ["kamienica-pierzeja-1", "kamienica-pierzeja-2", None, "kamienica-pierzeja-4"],
            "pasek11.png": ["zaplecze-dostaw", "magazyn-deptaku", "budka-pokazu", "hangar-portu"],
            "pasek14.png": [None, "stacja-trafo", None, "toaleta-parkowa"],   # garaze-szereg, zajezdnia -> pasek 19
            "pasek19.png": ["garaze-szereg", "zajezdnia", "remiza", "kotlownia"],
            "pasek15.png": ["dom-z-lokalem", "dom-z-panelami", "wartownia-portu", "piekarnia-dom"],
            "pasek18.png": ["magazyn-blacha", "wiata-rowerowa", "hala-sportowa", "warsztat-panele"]}
for plik, nazwy in DEK_NOWE.items():
    obs = ns["obiekty"](os.path.join(B, "wyniki-wejsciowe", plik))
    sk = SKALA_STRIP * 2172 / Image.open(os.path.join(B, "wyniki-wejsciowe", plik)).width   # pasek innej szerokosci = inna skala pikseli Codexa
    for n, im in zip(nazwy, obs):
        if n:
            do_gry(im, sk).save(os.path.join(B, "dekoracyjne", n + "_gra.png"))

# opisy obiektow (bez stylu i kamery)
OPIS = {
 "blok-z-balkonami": "a three-storey apartment block with balconies", "piekarnia": "a small bakery with striped awnings and a bread pictogram sign board",
 "apteka": "a pharmacy with glass shop windows and a green cross pictogram sign board", "biurowiec": "a two-storey office building with large glass windows",
 "szkola": "a primary school, a two-storey block with a clock above the entrance", "dom-wiejski": "a rural single-storey house with cream walls and wooden shutters",
 "dom-nowoczesny": "a modern detached family house with white render and wooden cladding", "dom-ceglany": "a modern two-storey family house with grey brick and a balcony above the entrance",
 "bungalow": "a small modern bungalow with large windows", "kamienica-nowa": "a four-storey modern apartment house with cream render, orange wooden cladding and flower boxes",
 "house-3n": "a low cream building with orange facade panels and tall blue windows", "house-4n": "a narrow cream building with orange cladding and a dark entrance canopy",
 "house-12n": "a low cream and orange building with a bench beside the entrance", "house-7n": "a narrow two-storey cream building with green vertical wall panels",
  "house-10n": "a narrow two-storey cream and orange building with an upstairs flower box", "house-11n": "a two-storey cream and orange building with a garage door on the right",
 "pavilion-2n": "a small cream and timber pavilion with a green awning and a glazed front", "pavilion-4n": "a tall narrow glazed pavilion",
 "pavilion-6n": "a wide cream and timber pavilion with glazed shop windows on both sides",
 "sklep-modelarski": "a hobby model shop with wide glass shop windows and a model airplane pictogram sign board", "hala-wystawowa": "a large exhibition hall with tall glass panels",
 "pracownia-klubowa": "a modelling club workshop with large windows and timber cladding", "sala-gieldy": "a collectors fair hall with display windows and a trading cards pictogram sign board",
 "pawilon-maly": "a small exhibitor pavilion with a glass front and a striped awning", "pawilon-sredni": "a medium exhibitor pavilion with display windows on both sides",
 "pawilon-szeroki": "a wide exhibitor pavilion with three display windows", "stacja-kolejki-dolna": "a cable car valley station, a stone and timber building with an opening for the cable cabin",
 "stacja-kolejki-gorna": "a small cable car mountain station, a stone and timber building", "dom-gracza-1": "a single-storey player house with cream render and timber cladding",
 "dom-gracza-2": "a two-storey player house with grey brick and a small balcony", "dom-gracza-3": "a two-storey player house with white render and a garage door on one side",
 "warsztat": ("a car repair workshop with a large roller door", "with a large roller door and a small side door"),
 "magazyn": ("a brick warehouse with a loading dock", "with a roller loading door and a small side door"),
 "garaz": ("a single garage", "with a metal up-and-over garage door"), "kosciol": ("a small church with a bell tower", "with an arched wooden double door"),
 "kamienica-pierzeja-1": ("a narrow three-storey town house with ground-floor shop windows", "with a small side door"),
 "kamienica-pierzeja-2": ("a four-storey town house with balconies", "with a small side door"), "kamienica-pierzeja-4": ("a three-storey brick town house with arched windows", "with a small side door"),
 "zaplecze-dostaw": ("a shop delivery backyard building", "with a roller loading door and a small service door"), "magazyn-deptaku": ("a promenade storage building", "with two roller doors"),
 "budka-pokazu": ("a lakeside show service booth with a serving window and a small awning", "with a small service door"), "hangar-portu": ("a harbour boathouse for model boats", "with a wide wooden door"),
 "garaze-szereg": ("a row of three neighbourhood garages with a flat roof covered with grey ribbed metal sheets", "with three closed metal roller garage doors"),
 "stacja-trafo": ("a small electrical transformer station with a warning pictogram", "with a metal service door"),
 "zajezdnia": ("a red brick tram depot with tram tracks and a flat roof covered with grey gravel", "with two tall closed green sliding doors and a small side door"),
 "remiza": ("a small fire station with a fire pictogram and a flat roof covered with grey ribbed metal sheets", "with two closed red roller doors and a small red side door"),
 "kotlownia": ("a small brick boiler house with a short metal chimney and a flat roof covered with grey gravel", "with a metal service door"),
 "toaleta-parkowa": ("a small public park toilet with man and woman pictograms", "with two small doors"),
 "dom-z-lokalem": ("a narrow four-storey apartment house with cream render, orange wooden cladding, balconies and a small shop window on the ground floor", "with a small side door"),
 "dom-z-panelami": ("a three-storey apartment house with cream render, grey wall panels and flower boxes", "with a small side door"),
 "wartownia-portu": ("a small harbour gatehouse with a barrier and a serving window", "with a small door"),
 "piekarnia-dom": ("a two-storey building with orange wooden cladding, a striped awning over a bakery window and a bread pictogram sign board", "with a small side door"),
 "magazyn-blacha": ("a storage warehouse with grey corrugated metal walls, a loading dock and a flat roof covered with grey corrugated metal sheets", "with a roller loading door and a small side door"),
 "wiata-rowerowa": ("a small bicycle shelter with timber walls, parked bicycles and a flat green roof planted with grass", "with a wide open front"),
 "hala-sportowa": ("a sports hall with orange timber cladding, high windows and a flat roof covered with light gravel and a row of skylights", "with a small side door"),
 "warsztat-panele": ("a small workshop with cream walls and a flat roof covered with dark blue solar panels", "with a roller door and a small side door"),
 "sklep-hobby": "a wide hobby shop with blue storefront glazing, a plain empty sign board and a flat roof covered with grey ribbed metal sheets",
 "sklep-blacha": "a wide cream shop with a striped awning over the shop windows and a flat roof covered with orange metal sheets with two roof vents",
 "sklep-drewno": "a cream shop with orange timber trim, a wide plant shop window and a flat roof covered with orange ribbed metal sheets",
 "sklep-zielony-dach": "a cream shop with a wide plant shop window and a flat green roof planted with grass and low plants",
 "ratusz": "a wide two-storey town hall with cream and orange walls, a clock on a raised middle part of the facade and a flat roof covered with grey gravel",
 "biblioteka": "a two-storey town library with tall windows showing bookshelves and a flat roof covered with light gravel and three square skylights",
 "dom-panele": "a modern two-storey family house with white render, a glass balcony and a flat roof covered with dark blue solar panels",
 "restauracja-taras": "a small restaurant with large windows and a flat roof terrace with wooden decking, potted trees, a table and a closed parasol",
 "sklep-narozny": "a corner shop with a striped awning over a wide shop window", "dom-rodzinny": "a two-storey family house with a large living room window",
 "kawiarnia": "a small cafe with outdoor tables and a coffee cup pictogram sign board", "fryzjer": "a hairdresser salon with a scissors pictogram sign board and a big window",
 "kiosk-gazet": "a small newspaper kiosk with a green striped awning over a serving window", "kasa-biletowa": "a ticket booth with a ticket pictogram sign board and two notice board windows",
 "kamienica-waska": "a narrow three-storey building with orange cladding, large windows and flower boxes", "poczta": "a post office with an envelope pictogram sign board and a red post box",
 "B1": ("a wide cream shop with blue storefront glazing and a dark ribbed metal roof", "with a sliding glass entrance door"),
 "B2": ("a wide cream shop with blue storefront glazing and vents on the flat roof", "with a sliding glass entrance door"),
 "B3": ("a wide cream shop with timber trim and blue storefront glazing", "with a sliding glass entrance door"),
 "B4": ("a wide cream shop with blue storefront glazing and a green planted roof", "with a sliding glass entrance door"),
 "townhall": ("a wide cream and timber town hall with a clock tower", "with glazed double doors"),
}
KAM = ("Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, "
       "isolated on solid magenta #FF00FF background.")
items = []
def pozycja_drzwi(nazwa):
    j = json.load(open(os.path.join(B, "wejsciowe-v2", nazwa + "-closed.json"), encoding="utf-8"))
    r = (j["doors"][0]["placement"]["x"] + 29.5) / j["image"]["w"]
    return "in the middle of" if 0.4 <= r <= 0.6 else ("on the left side of" if r < 0.4 else "on the right side of")
import importlib.util as _iu
_sp = _iu.spec_from_file_location("opisy_v2", os.path.join(B, "opisy_v2", "opisy.py")); OPV2 = _iu.module_from_spec(_sp); _sp.loader.exec_module(OPV2)
def dodaj(nazwa, typ, plik, plik_open=None):
    # opisy v2 (z obrazkow, 2026-10-20): znacznik typu zaraz po slowie wyzwalajacym
    if typ == "wejsciowy":
        cap = f"swiat2d style, enterable building, {OPV2.WEJ[nazwa]}, and the standard entrance door {pozycja_drzwi(nazwa)} the front facade. {KAM}"
    else:
        o = OPV2.DEK[nazwa]; cap = f"swiat2d style, decorative building, {o[0]}, {o[1]}. {KAM}"
    items.append({"nazwa": nazwa, "typ": typ, "plik": plik, "plik_open": plik_open, "caption": cap})
WEJ = [f[:-11] for f in sorted(os.listdir(os.path.join(B, "wejsciowe-v2"))) if f.endswith("-closed.png") and not f.startswith("_")]
for n in WEJ:
    dodaj(n, "wejsciowy", os.path.join(B, "wejsciowe-v2", n + "-closed.png"), os.path.join(B, "wejsciowe-v2", n + "-open.png"))
for n in ("warsztat", "magazyn", "garaz", "kosciol"):
    dodaj(n, "dekoracyjny", os.path.join(B, "gotowe", n + "_gra.png"))
DO_POPRAWY = set()   # 2026-10-20 wlasciciel: zly dach / wnetrze za uchylonymi drzwiami -> pasek 19
for n in [x for v in DEK_NOWE.values() for x in v if x and x not in DO_POPRAWY]:
    dodaj(n, "dekoracyjny", os.path.join(B, "dekoracyjne", n + "_gra.png"))
for n in ():   # B1-B4, townhall: usuniete 2026-10-20, przerysowanie w pasku 16-17 (prompty-dachy.md)
    dodaj(n, "z gry (inne drzwi)", rf"E:\ai\skrzynka\odpowiedzi\054-zrodla\budynki\{n}-closed-native.png")
json.dump(items, open(os.path.join(B, "lora-lista.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.join(B, "lora-lista.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["nr", "nazwa", "typ", "plik", "caption"])
    for i, it in enumerate(items, 1):
        w.writerow([i, it["nazwa"], it["typ"], it["plik"], it["caption"]])
print(len(items), "pozycji:", {t: sum(1 for i in items if i["typ"] == t) for t in {i["typ"] for i in items}})

# strona oceny (szablon przegladu wzorcow): obraz zamkniety, pod nim otwarty (wejsciowe); opis = caption
def b64(p):
    """miniatura = sprite 1:1 (natywne piksele gry, bez przeskalowania); skale robi strona (wspolna dla wszystkich)"""
    im = Image.open(p).convert("RGBA"); im = im.crop(im.getchannel("A").getbbox())
    bf = io.BytesIO(); im.save(bf, "PNG", optimize=True); return "data:image/png;base64," + base64.b64encode(bf.getvalue()).decode()
dane = []
for k, it in enumerate(items, 1):
    im = Image.open(it["plik"]); bb = im.getchannel("A").getbbox() if im.mode == "RGBA" else None
    w, h = (bb[2] - bb[0], bb[3] - bb[1]) if bb else im.size
    dane.append({"id": "bud__" + it["nazwa"], "nazwa": it["nazwa"], "kat": it["typ"], "opis": it["caption"], "kierunek": "front", "rodzaj": "sprite",
                 "wym": f"{w}x{h} px = {w/24:.1f} m", "nr": k, "uwaga": "drzwi gry innego typu (przesuwne/podwojne) - do decyzji" if it["typ"].startswith("z gry") else "",
                 "img": b64(it["plik"]), "pw": w, "ph": h, "pelny": "", "aranz": ""})
html = open(r"E:\ai\lora\przeglad_wzorce_szablon.html", encoding="utf-8").read()
html = html.replace("<title>Wzorce 054 do oceny</title>", "<title>Budynki do LoRA</title>").replace("<h1>Wzorce 054</h1>", "<h1>Budynki do LoRA</h1>")
html = html.replace("Zestaw od dioramy: grafiki gry sprzed generowania amd, w natywnych pikselach na przezroczystym tle (szachownica).",
                    "Wszystkie budynki do zbioru LoRA, w formacie gry (24 px = 1 m). Pod obrazkiem: opis do nauki (caption).")
html = html.replace("w aranżacji (przykład ułożenia)", "drzwi otwarte (wersja dla gry)")
# wspolna skala: okienko = 470 px gry (najszerszy budynek), budynek stoi na dole; przelacznik "Powieksz" = kazdy dopasowany do okienka
html = html.replace(".thumb img { image-rendering: pixelated; width: 92%; height: 92%; object-fit: contain; }",
  ".thumb { align-items: end; } .thumb img { image-rendering: auto; width: calc(var(--pw) / 470 * 100%); height: auto; margin-bottom: 3%; }"
  " body.powieksz .thumb { align-items: center; } body.powieksz .thumb img { image-rendering: pixelated; width: 94%; height: 94%; object-fit: contain; margin: 0; }"
  " .skala { margin: 0 0 12px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; font-size: 12px; color: var(--muted); }")
html = html.replace("img.src = it.img; img.alt = it.nazwa;", "img.src = it.img; img.alt = it.nazwa; img.style.setProperty('--pw', it.pw);")
PRZEL = """<div class="skala"><button type="button" id="przel" aria-pressed="false" onclick="const on=document.body.classList.toggle('powieksz');this.setAttribute('aria-pressed',on);this.textContent=on?'Wspólna skala':'Powiększ każdy';">Powiększ każdy</button><span>Domyślnie wszystkie budynki w tej samej skali (okienko = 19,6 m szerokości), stoją na dolnej krawędzi.</span></div>"""
html = html.replace('<div class="grid"', PRZEL + '<div class="grid"', 1)
html = html.replace("/*DANE*/[]", json.dumps(dane, ensure_ascii=False)).replace("/*KATEGORIE*/[]", json.dumps(["wejsciowy", "dekoracyjny", "z gry (inne drzwi)"], ensure_ascii=False))
open(os.path.join(B, "przeglad_budynki_lora.html"), "w", encoding="utf-8").write(html); print("html", round(os.path.getsize(os.path.join(B, "przeglad_budynki_lora.html")) / 1e6, 2), "MB")
