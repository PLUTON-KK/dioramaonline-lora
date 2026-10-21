"""TEST-V2: Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512), te same 38 obiektow co test-v1, poprawione prompty.
Zmiany wzgledem test-v1 (nowe_budynki_krea_v2.py):
- "flat rectangular roof visible from above" w kamerze TYLKO tam, gdzie plaski dach jest logiczny (hale, wiezowiec, szpital z ladowiskiem, supermarket,
  stacja, parking); reszta: kamera "wolna" - front do widza, gora widoczna lekko z gory, bez narzucania ksztaltu dachu;
- "front facade" tylko dla budynkow; obiekty, ktore nie sa budynkami (turbina, plac zabaw, autozlom...) = "decorative object";
- zdjete narzucone "dark grey flat roof" tam, gdzie dach moze byc dowolny (stodola, tartak, dworzec, komisariat, bank, budki obok obiektow);
- dopisek o okraglych (pionowe boki, gora jako splaszczona elipsa) bez wycinania frontu z kamery; foliak bez niego (polokragly tunel nie ma pionowych bokow).
Warianty: v2 (bez uzdatnienia), J ("realistic shading and volume"), K ("semi-realistic pixel art"); seed 42+i.
Wynik: E:/ai/wyniki/nowe_budynki_krea_lora_v2-test-v2/
Po test-v2 (prompty test-v2 sa w prompty.txt w folderach wynikow): supermarket bez parkingu i aut.
Zasady q3ok: bez dymu/pary (przemysl), bez parkingow i aut przed budynkiem - to robi diorama osobno."""
import os, sys
sys.path.insert(0, "E:/ai"); sys.path.insert(0, "E:/ai/lora")
OUT = "E:/ai/wyniki/nowe_budynki_krea_lora_v2-test-v2"; os.makedirs(OUT, exist_ok=True)
KAM = {"plaski": " Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above{okr}, isolated on solid magenta #FF00FF background.",
       "wolna": " Pixel art game sprite, fixed orthographic RPG 3/4 camera, the front facing the viewer and the top seen slightly from above{okr}, isolated on solid magenta #FF00FF background."}
# bez "vertical sides": klocilo sie z chlodnia (hiperboloida), wiatrakiem (zweza sie ku gorze) i namiotem cyrku
OKR = ", round shapes drawn straight from the front with their tops visible as flattened ellipses"
STYL = {"J": "Detailed pixel art game sprite with realistic shading and volume,", "K": "Semi-realistic pixel art game sprite,"}
DRZWI = "and the standard entrance door in the middle of the front facade"
# (grupa, nazwa, typ, rodzaj, szer m, wys m, kamera, okragly, opis, materialy)
L = [
 ("przemysł", "elektrownia węglowa", "decorative", "building", 24, 20, "plaski", True,
  "a coal power plant: a brick turbine hall with a dark grey flat roof, two tall round brick chimneys with red and white bands behind it, a conveyor belt bridge and a black coal heap next to it",
  "red brick walls with visible bricks, sooty chimney tops, a steel truss conveyor, coal heap with lumps"),
 ("przemysł", "elektrownia atomowa", "decorative", "building", 26, 22, "wolna", True,
  "a nuclear power plant: a large concrete cooling tower shaped like a hyperboloid with a white plume of steam, a round reactor building with a dome and a low turbine hall with a dark grey flat roof",
  "weathered grey concrete with formwork lines, a smooth white reactor dome, metal pipes and fences"),
 ("przemysł", "turbina wiatrowa", "decorative", "object", 8, 22, "wolna", True,
  "a tall white wind turbine with a slim round tower, a nacelle on top and three long blades facing the viewer, standing on a small concrete base",
  "smooth white painted steel tower, slightly shaded blades, a concrete foundation"),
 ("przemysł", "farma fotowoltaiczna", "decorative", "object", 16, 4, "wolna", False,
  "a solar farm: three rows of dark blue solar panels on metal stands tilted towards the viewer, a small grey inverter box and a low wire fence",
  "dark blue photovoltaic cells in a grid with light reflections, aluminium frames, galvanised steel stands"),
 ("przemysł", "huta", "decorative", "building", 24, 18, "wolna", True,
  "a steelworks: a tall blast furnace tower, round hot stoves, large rusty pipes and a long hall with a dark grey flat roof, glowing orange light from an open gate in the hall",
  "rusty steel plates with rivets, soot stains, corrugated metal hall walls, hot orange glow"),
 ("przemysł", "rafineria", "decorative", "object", 24, 16, "wolna", True,
  "an oil refinery: white round storage tanks, tall distillation columns with ladders, a web of pipes and a thin flare stack with a small flame",
  "white painted steel tanks with weld seams, metal ladders and railings, grey pipes with valves"),
 ("przemysł", "tartak", "decorative", "building", 18, 8, "wolna", False,
  "a sawmill: an open wooden shed on posts with a big circular saw inside, stacks of logs and piles of sawn planks in front of it",
  "weathered timber posts and planks with wood grain, log ends with rings, sawdust on the ground"),
 ("odpady", "wysypisko śmieci", "decorative", "object", 18, 6, "wolna", False,
  "a landfill: a large mound of mixed rubbish bags and junk, a small grey site office container and a yellow bulldozer on the heap, a wire fence in front",
  "colourful plastic bags, broken boxes, scrap pieces, dusty ground"),
 ("odpady", "autozłom", "decorative", "object", 18, 7, "wolna", False,
  "a car scrapyard: stacks of old crushed cars piled three high, a yellow crane with a magnet, a small office shed and a corrugated metal fence",
  "rusty car bodies with faded paint, broken windows, corrugated steel fence sheets"),
 ("odpady", "oczyszczalnia ścieków", "decorative", "object", 20, 6, "wolna", True,
  "a sewage treatment plant: two large round open concrete tanks with grey water and rotating bridges, their water surface visible from above, and a small control building",
  "weathered concrete tank walls, metal walkway railings, murky water surface"),
 ("odpady", "punkt skupu złomu", "decorative", "object", 14, 6, "wolna", False,
  "a scrap metal yard: a small office cabin, piles of scrap metal, old radiators and pipes, a truck scale and a container",
  "rusty iron scraps, dented metal sheets, a blue steel container with ribs"),
 ("transport", "dworzec kolejowy z peronem", "enterable", "building", 22, 10, "wolna", False,
  "a small railway station building with cream walls and a clock on the front, a long platform with a canopy on posts next to it and rail tracks along the bottom",
  "plastered walls with stone corners, a metal platform canopy, rails with sleepers"),
 ("transport", "przystanek autobusowy", "decorative", "object", 6, 3, "wolna", False,
  "a bus stop shelter with a glass back wall and a thin flat roof, a bench and a bus stop sign on a pole",
  "steel frame, glass panels with reflections, a painted metal sign"),
 ("transport", "parking wielopoziomowy", "decorative", "building", 18, 12, "plaski", False,
  "a multi-storey car park: an open concrete frame with four levels, parked cars visible on each level, a ramp at the side and cars parked on the open top deck",
  "bare concrete slabs and columns, painted parking lines, metal railings"),
 ("transport", "myjnia samochodowa", "decorative", "building", 12, 5, "wolna", False,
  "a car wash with two open washing bays under a canopy, blue brushes, a car inside one bay and a sign with a water drop pictogram",
  "white metal panels, blue rotating brushes, wet floor with puddles"),
 ("transport", "lotnisko", "enterable", "building", 20, 18, "wolna", True,
  "a small airport: a low terminal building with large glass windows, and a tall control tower with a round glass cabin on top standing next to the terminal",
  "concrete and glass facade, tinted tower windows, antennas on the tower"),
 ("transport", "port z dźwigiem", "decorative", "object", 20, 16, "wolna", False,
  "a small harbour quay with a tall blue gantry crane, stacked shipping containers in red, blue and green, and a strip of water with a bollard",
  "painted steel crane girders, ribbed container walls, concrete quay edge"),
 ("wysokie", "wieżowiec szklany", "enterable", "building", 12, 30, "plaski", False,
  "a tall glass office skyscraper with blue reflective windows in a grid and antennas on its roof", "glass curtain wall with reflections, thin metal mullions"),
 ("wysokie", "wieża ciśnień", "decorative", "building", 8, 18, "wolna", True,
  "a brick water tower: a round brick shaft with small windows and a wide round water tank on top with a low conical roof", "red brick with visible courses, a riveted metal tank"),
 ("wysokie", "maszt telekomunikacyjny", "decorative", "object", 6, 24, "wolna", False,
  "a tall red and white steel lattice telecom mast with dish antennas and a small grey equipment cabin at its foot", "thin steel lattice beams, white dish antennas, a metal cabin"),
 ("wysokie", "silos zbożowy", "decorative", "building", 14, 20, "wolna", True,
  "a grain elevator: a row of three tall round concrete silos with a tall square elevator tower above them and a loading chute", "weathered concrete with vertical streaks, rusty metal chutes"),
 ("bryły", "stadion", "decorative", "building", 24, 10, "wolna", True,
  "a small oval football stadium: curved stands with coloured seats, floodlight masts at the corners and an entrance gate in the middle of the front", "concrete stands, plastic seats in rows, steel floodlight masts"),
 ("bryły", "cyrk", "decorative", "object", 16, 12, "wolna", True,
  "a circus big top: a round tent with red and white stripes rising to a pointed top with a flag, an entrance with curtains in the middle", "striped canvas with folds, ropes and poles"),
 ("bryły", "meczet", "decorative", "building", 16, 18, "wolna", True,
  "a mosque with a large round dome, a tall slim minaret with a balcony next to it, arched windows and an arched entrance", "white stone walls, a green dome with ribs, carved arches"),
 ("bryły", "wiatrak holenderski", "decorative", "building", 10, 16, "wolna", True,
  "a Dutch windmill: a round tapering brick tower with a small cap on top and four large sails facing the viewer, a small wooden door at the bottom", "brick tower, wooden sail frames with canvas, a thatched cap"),
 ("bryły", "zamek", "decorative", "building", 18, 16, "wolna", True,
  "a small stone castle with two round towers with battlements, a wall with a gate and a wooden drawbridge in the middle", "grey stone blocks with moss, wooden gate with iron straps"),
 ("bryły", "piramida w wesołym miasteczku", "decorative", "object", 12, 10, "wolna", False,
  "a funfair attraction shaped like a golden pyramid with a pointed top, colourful lights along its edges and an entrance with a ticket booth at the front", "painted plywood panels, light bulbs, a striped ticket booth"),
 ("usługi", "szpital", "enterable", "building", 22, 16, "plaski", False,
  "a large hospital with white walls, a red cross pictogram, rows of windows, an ambulance entrance canopy and a helicopter landing pad marked with H on the roof", "white render, blue tinted windows, a painted helipad"),
 ("usługi", "komisariat", "enterable", "building", 14, 9, "wolna", False,
  "a police station with white walls, a dark blue stripe, a badge pictogram and a blue lamp above the entrance", "white render, dark blue painted band, glass entrance"),
 ("usługi", "bank", "enterable", "building", 12, 10, "wolna", False,
  "a bank with a stone facade, four columns at the front and a coin pictogram sign", "light stone blocks, fluted columns, polished brass details"),
 ("usługi", "supermarket", "enterable", "building", 22, 7, "plaski", False,   # po test-v2: bez parkingu (q3ok: parking i auta robimy osobno w dioramie)
  "a supermarket with a wide glass front, a shopping cart pictogram sign and a few shopping trolleys by the entrance", "metal cladding panels, large glass windows"),
 ("usługi", "stacja benzynowa", "enterable", "building", 18, 7, "plaski", False,
  "a petrol station: a small shop and next to it a flat rectangular canopy on posts over two fuel pumps", "white metal canopy with a coloured stripe, glass shop front, fuel pumps with hoses"),
 ("usługi", "plac zabaw", "decorative", "object", 12, 5, "wolna", False,
  "a playground with a slide, swings, a small climbing frame and a sandpit, surrounded by a low fence", "painted wooden and metal play equipment, rubber safety ground"),
 ("usługi", "basen odkryty", "decorative", "object", 18, 5, "wolna", False,
  "an outdoor swimming pool with blue water seen from slightly above, a diving board, sun loungers with umbrellas and a small changing building", "blue water with ripples, white tiles, striped umbrellas"),
 ("wiejskie", "stodoła", "decorative", "building", 14, 9, "wolna", False,
  "a red wooden barn with big double barn doors with white cross braces and hay bales in front", "red painted vertical planks with wood grain, straw bales"),
 ("wiejskie", "kurnik", "decorative", "building", 7, 4, "wolna", False,
  "a small wooden chicken coop with a ramp, nest boxes, a wire mesh run and a few white hens", "weathered wooden planks, chicken wire, straw"),
 ("wiejskie", "szklarnia tunelowa", "decorative", "building", 14, 5, "wolna", False,
  "a polytunnel greenhouse seen from its open end: a long half-round tunnel covered with translucent plastic film on metal hoops, rows of plants visible inside", "milky translucent foil stretched on metal hoops, green vegetable rows"),
 ("wiejskie", "silos przy farmie", "decorative", "building", 10, 14, "wolna", True,
  "a single tall round metal farm silo with a domed top and a ladder, next to a small wooden farm shed", "corrugated galvanised steel, a metal ladder, a wooden shed"),
]


def kam(e):
    return KAM[e[6]].format(okr=OKR if e[7] else "").replace("front facade facing", "front facade facing" if e[3] == "building" else "front facing")


def tresc(e, mat=False):
    g, n, typ, rodz, w, h, k, okr, op, m = e
    t = f"swiat2d style, {typ} {rodz}, about {w} m wide and {h} m tall, {op}"
    if mat: t += f", realistic materials and proportions: {m}"
    return t + (f", {DRZWI}." if typ == "enterable" else ".")


def v2(e): return tresc(e) + kam(e)
def uzd(e, st): return tresc(e, True) + kam(e).replace("Pixel art game sprite,", STYL[st])


WAR = [("v2", "prompt v2 (bez uzdatnienia)", v2), ("J", "uzdatniony J (realistic shading)", lambda e: uzd(e, "J")), ("K", "uzdatniony K (semi-realistic)", lambda e: uzd(e, "K"))]


def sprawdz():
    """sprzecznosci: plaski dach w kamerze przy spiczastych/okraglych/kopulach; 'facade' przy obiektach; 'building' przy obiektach."""
    bl = []
    for e in L:
        p = v2(e); op = e[8]
        if "flat rectangular roof" in p and any(s in op for s in ("pointed", "dome", "conical", "half-round", "tent", "cap on top", "pyramid")): bl.append((e[1], "plaski dach + spiczasty/kopula"))
        if e[3] == "object" and "facade facing" in p: bl.append((e[1], "obiekt z 'facade'"))
        if e[2] == "enterable" and e[3] != "building": bl.append((e[1], "wejsciowy obiekt"))
        if p.count("swiat2d style") != 1 or "#FF00FF" not in p: bl.append((e[1], "brak trigger/tla"))
    return bl


if __name__ == "__main__":
    bl = sprawdz()
    if bl: print("SPRZECZNOSCI:", bl); sys.exit(1)
    if len(sys.argv) > 1 and sys.argv[1] == "sprawdz":
        for e in L: print(f"[{e[6]}{'+okr' if e[7] else ''}] {e[1]}\n{v2(e)}\n")
        sys.exit(0)
    from PIL import Image, ImageDraw, ImageFont
    import silnik
    import dogeneruj_zestawienie_v1_lekkie as LK
    with open(f"{OUT}/prompty.txt", "w", encoding="utf-8") as f:
        f.write("TEST-V2 · Model: Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512), seed 42+i\n\n")
        for k, et, fn in WAR:
            for i, e in enumerate(L): f.write(f"[{k}] {e[1]}\n{fn(e)}\n\n")
    for i, e in enumerate(L):
        for k, et, fn in WAR:
            png = f"{OUT}/{k}_{i}.png"
            if os.path.exists(png): continue
            LK.P = {i: fn(e)}
            w = LK.wf("zestawienie_krea2turbo_lora_raw512", i); w["lora"]["inputs"]["lora_name"] = "swiat2d_v2f512_krea2raw_2000.safetensors"
            silnik.generuj(w, png); print(k, i, e[1], flush=True)
    C, LW = 240, 250; F = ImageFont.truetype("arialbd.ttf", 17); FS = ImageFont.truetype("arial.ttf", 15)
    grupy = []
    [grupy.append(e[0]) for e in L if e[0] not in grupy]
    for g in grupy:
        idx = [i for i, e in enumerate(L) if e[0] == g]
        sh = Image.new("RGB", (LW + len(idx) * (C + 4), 76 + 3 * (C + 4)), (40, 48, 36)); d = ImageDraw.Draw(sh)
        d.text((10, 10), f"TEST-V2 · MODEL: Krea 2 Turbo int8 + LoRA budynki v2 (z Krea 2 Raw, 512) – nowe obiekty spoza zbioru: {g}, seed 42+i", font=ImageFont.truetype("arialbd.ttf", 22), fill=(255, 255, 255))
        for c, i in enumerate(idx): d.text((LW + c * (C + 4) + 4, 48), L[i][1], font=F, fill=(255, 230, 140))
        for r, (k, et, fn) in enumerate(WAR):
            y = 76 + r * (C + 4); d.multiline_text((10, y + 10), et.replace(" (", "\n("), font=FS, fill=(255, 255, 255))
            for c, i in enumerate(idx): sh.paste(Image.open(f"{OUT}/{k}_{i}.png").convert("RGB").resize((C, C), Image.LANCZOS), (LW + c * (C + 4), y))
        sh.save(f"{OUT}/arkusz_{g}.png")
    print("KONIEC")
