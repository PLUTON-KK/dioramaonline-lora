"""Opisy (caption) 32 nowych obrazow zbioru v3 - napisane recznie wg tego, co jest na obrazie (nie wg promptu generowania).
Zasady v2 -> v3: rozmiar w metrach z gotowego sprite'a (szerokosc / wysokosc z widocznym dachem, 24 px = 1 m), bez zaprzeczen,
"building" tylko dla budynkow, "object" dla reszty; kamera: plaski dach tylko gdy obiekt ma plaski prostokatny dach, inaczej kamera "wolna";
dopisek o okraglych bryłach tylko przy obiektach z okraglymi czesciami. Wejsciowe: kanoniczne drzwi wklejone w sprite, polozenie z detekcji."""
# nazwa: (rodzaj, kamera, okragle, opis)
OPISY = {
 "elektrownia-weglowa-1": ("building", "plaski", True, "a coal power plant: a red brick turbine hall with a dark grey flat roof, a wide grey roller door and small windows, two tall round brick chimneys with red and white bands behind the hall, a steel conveyor bridge running to a black coal heap on the right and small trees at the sides"),
 "elektrownia-atomowa-1": ("building", "wolna", True, "a nuclear power plant: a tall grey concrete cooling tower shaped like a hyperboloid with an open round top, a round reactor building with a white dome on the right and a low dark grey turbine hall with a flat roof in front, on a grassy base"),
 "elektrownia-atomowa-2": ("building", "wolna", True, "a nuclear power plant: a round reactor building with a white dome on the left, a tall grey concrete cooling tower shaped like a hyperboloid behind it and a low dark grey turbine hall with a flat roof on the right, on a grassy base"),
 "turbina-wiatrowa-1": ("object", "wolna", True, "a white wind turbine: a slim round white tower on a small concrete base, a nacelle on top and three long white blades"),
 "turbina-wiatrowa-2": ("object", "wolna", True, "a white wind turbine: a slim round white tower on a small concrete base, a nacelle on top and three long white blades with red tips"),
 "farma-fotowoltaiczna-1": ("object", "wolna", False, "a solar farm: a large tilted field of dark blue solar panels in a grid on metal stands, a small grey inverter box at the bottom and a low wire fence"),
 "rafineria-1": ("object", "wolna", True, "an oil refinery: white round storage tanks, tall steel distillation columns with ladders and platforms, a web of grey pipes on a concrete base and a thin red and white flare stack"),
 "tartak-1": ("building", "wolna", False, "a sawmill: an open wooden shed on posts with a dark grey plank roof, a big circular saw on a timber frame inside, stacks of logs on both sides and piles of sawn planks in front on sandy ground"),
 "tartak-2": ("building", "wolna", False, "a sawmill: an open wooden shed on posts with a weathered grey plank roof, a big circular saw on a timber frame inside, stacks of logs on both sides and piles of sawn planks in front on sandy ground"),
 "oczyszczalnia-sciekow-1": ("object", "wolna", True, "a sewage treatment plant: two large round open concrete tanks with dark water and rotating bridges, joined by a small grey control building in the middle"),
 "oczyszczalnia-sciekow-2": ("object", "wolna", True, "a sewage treatment plant: one large round concrete tank seen from slightly above with dark water, a rotating bridge with radial arms and a railing around the rim, a small door in the front wall and a small control tower behind it"),
 "skup-zlomu-1": ("object", "wolna", False, "a scrap metal yard: a small cream office cabin with a dark grey flat roof and a double door, piles of rusty scrap metal, a truck scale in the middle and a blue steel container on the right, on a concrete yard"),
 "skup-zlomu-2": ("object", "wolna", False, "a scrap metal yard: a small wooden office cabin with a dark grey flat roof and a dark double door in the middle, surrounded by piles of rusty scrap, old radiators, pipes and gas cylinders behind a metal fence"),
 "wiezowiec-szklany-1": ("building", "plaski", False, "a tall glass office building with blue reflective windows in a grid, a dark grey flat roof with two antennas and planters along the front"),
 "wieza-cisnien-1": ("building", "wolna", True, "a brick water tower: a round red brick shaft with small arched windows and a small arched door at the bottom, and a wide round dark grey metal water tank on top with a low conical roof"),
 "maszt-telekomunikacyjny-1": ("object", "wolna", False, "a tall red and white steel lattice telecom mast with round white dish antennas and a small grey equipment cabin at its foot"),
 "silos-zbozowy-1": ("building", "wolna", True, "a grain elevator: a row of three tall round concrete silos, a tall square concrete elevator tower behind them on the right and rusty metal loading chutes"),
 "silos-zbozowy-2": ("building", "wolna", True, "a grain elevator: three tall round grey silos on a stone base with small doors, a tall square elevator tower behind them and rusty chutes running from the tower to the tops of the silos"),
 "cyrk-1": ("object", "wolna", True, "a circus big top: a round tent with red and white stripes rising to a pointed top with a flag, an open entrance with red curtains in the middle and guy ropes on poles at the sides"),
 "meczet-1": ("building", "wolna", True, "a mosque with cream stone walls, a large green ribbed dome on a round drum with arched windows, a tall slim white minaret with a balcony and a green pointed top on the left, an arched entrance with a dark double door and planters along the front"),
 "wiatrak-1": ("building", "wolna", True, "a Dutch windmill: a round tapering red brick tower on a stone base, a thatched cap on top, four large canvas sails on wooden frames facing the viewer and a small wooden door at the bottom"),
 "wiatrak-2": ("building", "wolna", True, "a Dutch windmill: a round tapering brown brick tower, a straw cap on top, four large lattice sails facing the viewer and a small wooden door at the bottom"),
 "zamek-1": ("building", "wolna", True, "a small grey stone castle with two round towers with battlements, a battlemented wall between them, a wooden double gate with iron straps in the middle, a wooden drawbridge in front and ivy on the walls"),
 "piramida-wesole-miasteczko-1": ("object", "wolna", False, "a funfair attraction shaped like a golden pyramid with a pointed top, rows of colourful light bulbs along its edges, a decorated sign board and an entrance with a red and white striped awning between two potted shrubs"),
 "szpital-1": ("building", "plaski", False, "a four-storey hospital with white walls, rows of blue windows, a large red cross pictogram above an entrance canopy, a dark grey flat roof with a helicopter landing pad marked with H and an air conditioning unit, planters along the front"),
 "bank-1": ("building", "plaski", False, "a bank with a cream stone facade, four columns at the front, a sign board with a coin pictogram, wall lamps, planters and a dark grey flat roof"),
 "bank-2": ("building", "plaski", False, "a bank with a beige stone facade, four columns, a round coin emblem above the entrance, tall narrow windows and a dark grey flat roof"),
 "stacja-benzynowa-1": ("building", "plaski", False, "a petrol station: a small shop with cream walls, a shop window, a wall lamp, the standard entrance door in the middle of the shop front and a dark grey flat roof with an air conditioning unit, and on its right a flat rectangular canopy on posts over two fuel pumps"),
 "plac-zabaw-1": ("object", "wolna", False, "a playground on green grass with a small slide with a blue roof, two swings, a climbing frame and a sandpit, surrounded by a low hedge with flowers"),
 "kurnik-1": ("building", "wolna", False, "a small wooden chicken coop with a dark grey plank roof, nest boxes with straw and a small ramp, and next to it a wire mesh run with white hens"),
 "szklarnia-tunelowa-1": ("building", "wolna", False, "a polytunnel greenhouse seen from its open end: a tall half-round tunnel covered with translucent milky plastic film on metal hoops, with rows of green plants visible through the open doorway"),
 "silos-farma-1": ("building", "wolna", True, "a tall round grey metal farm silo with a domed top and a ladder, and on its right a small wooden farm shed with a gable roof and a wide opening"),
}
DRZWI_TXT = {"middle": "in the middle of the front facade", "left": "on the left side of the front facade", "right": "on the right side of the front facade"}
DRZWI_W_OPISIE = {"stacja-benzynowa-1"}   # drzwi opisane w tresci (polozenie wzgledem sklepu, nie calego obiektu)
KAM = {"plaski": "front facade facing the viewer, flat rectangular roof visible from above", "wolna": "the front facing the viewer and the top seen slightly from above"}
OKR = ", round shapes drawn straight from the front with their tops visible as flattened ellipses"


def caption(r):
    rodz, kam, okr, op = OPISY[r["nazwa"]]
    wej = r["typ"] == "wejsciowy"
    t = f"swiat2d style, {'enterable' if wej else 'decorative'} {rodz}, about {round(r['szer_m'])} m wide and {round(r['wys_sprite_m'])} m tall, {op}"
    if wej and r['nazwa'] not in DRZWI_W_OPISIE: t += f", and the standard entrance door {DRZWI_TXT[r['drzwi_polozenie']]}"
    k = KAM[kam] if rodz == "building" else KAM[kam].replace("front facade facing", "front facing")
    return t + f". Pixel art game sprite, fixed orthographic RPG 3/4 camera, {k}{OKR if okr else ''}, isolated on solid magenta #FF00FF background."
