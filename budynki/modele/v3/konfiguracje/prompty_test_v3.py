"""Prompty testowe dla LoRA budynki v3 (podglady z treningu co 250 krokow + generowanie lokalne): 7 obiektow spoza zbioru v3,
kazdy w wersji zwyklej (styl v3) i uzdatnionej K (opis materialow + "Semi-realistic pixel art game sprite").
Zasady: bez zaprzeczen, kamera zgodna z bryla (plaski dach tylko gdy logiczny), bez dymu, bez parkingow/aut i torow przed obiektami.
Kolejnosc w ai-toolkit: 0-6 zwykle, 7-13 uzdatnione (seed 42+i przy walk_seed)."""
KAM = {"plaski": "front facade facing the viewer, flat rectangular roof visible from above", "wolna": "the front facing the viewer and the top seen slightly from above",
       "bok": "the side facing the viewer and the top seen slightly from above"}
OKR = ", round shapes drawn straight from the front with their tops visible as flattened ellipses"
DRZWI = ", and the standard entrance door in the middle of the front facade"
# (nazwa, typ, rodzaj, szer, wys, kamera, okragle, opis, materialy)
O = [
 ("pawilon szklarniowy", "enterable", "building", 16, 9, "wolna", False,
  "a glasshouse pavilion: large glass walls and a glass roof made of panes in a white metal frame, tall palms and green plants visible inside, a cream stone plinth along the bottom",
  "thin white painted metal frame, clear glass panes with reflections, lush leaves pressed against the glass"),
 ("średniowieczny zamek", "decorative", "building", 20, 18, "wolna", True,
  "a medieval stone castle: a square keep in the middle, round corner towers with battlements and pointed slate roofs, a curtain wall with a gatehouse and a wooden gate with a portcullis",
  "rough grey stone blocks with moss, dark slate roof tiles, heavy timber gate with iron straps"),
 ("basen odkryty", "decorative", "object", 18, 5, "wolna", False,
  "an outdoor swimming pool: a rectangular pool with blue water and lane ropes seen from slightly above, a diving board, white sun loungers with striped umbrellas and a small changing building",
  "blue water with ripples and light reflections, white ceramic tiles, painted metal ladders"),
 ("przystanek tramwajowy", "decorative", "object", 9, 4, "wolna", False,
  "a tram stop: a long shelter with glass panels and a thin flat roof on a raised concrete platform, a bench, a timetable board and a tram stop sign on a pole",
  "steel frame, glass panels with reflections, concrete platform edge with a yellow line"),
 ("gospodarstwo rolne", "decorative", "building", 22, 10, "wolna", False,
  "a farmstead: a small farmhouse with white walls, a red wooden barn with big double doors next to it, a vegetable garden with rows of plants, hay bales and a low wooden fence",
  "whitewashed plaster, red painted planks with wood grain, straw bales, dark soil rows"),
 ("gospodarstwo hodowlane", "decorative", "building", 24, 10, "wolna", True,
  "a livestock farm: a long cowshed with a row of small windows and a wide open door, a fenced paddock with black and white cows in front of it and a tall round metal feed silo at the side",
  "weathered timber and brick walls, corrugated metal roof sheets, wooden fence rails, galvanised silo"),
 ("samochód sedan", "decorative", "object", 5, 2, "bok", False,
  "a silver four-door sedan car from the 2000s seen from the side and facing right, with its roof, bonnet and windscreen visible slightly from above, black tyres and clear windows",
  "metallic silver paint with soft reflections, tinted glass, chrome door handles, dark rubber tyres"),
]


def prompt(o, uzd=False):
    n, typ, rodz, w, h, kam, okr, op, mat = o
    t = f"swiat2d style, {typ} {rodz}, about {w} m wide and {h} m tall, {op}"
    if uzd: t += f", realistic materials and proportions: {mat}"
    if typ == "enterable": t += DRZWI
    k = KAM[kam] if rodz == "building" else KAM[kam].replace("front facade facing", "front facing")
    styl = "Semi-realistic pixel art game sprite" if uzd else "Pixel art game sprite"
    return t + f". {styl}, fixed orthographic RPG 3/4 camera, {k}{OKR if okr else ''}, isolated on solid magenta #FF00FF background."


NAZWY = [o[0] for o in O] + [o[0] + " (K)" for o in O]
PROMPTY = [prompt(o) for o in O] + [prompt(o, True) for o in O]

if __name__ == "__main__":
    import re
    NEG = re.compile(r"\b(no|not|without|never|none|nothing|except|instead|only)\b", re.I)
    for n, p in zip(NAZWY, PROMPTY):
        bl = [x for x, c in (("zaprzeczenie", NEG.search(p)), ("plaski dach + spiczaste", "flat rectangular roof visible" in p and re.search(r"pointed|dome|conical|tent", p)),
                             ("parking/smoke", re.search(r"car park|parking|smoke|steam", p))) if c]
        print(f"[{n}] {'BLEDY: ' + str(bl) if bl else 'ok'}\n{p}\n")
