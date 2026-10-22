# Schemat opisów i promptów (obowiązuje od v4)

Ustalone 2026-10-22. **Wszystkie zbiory treningowe i prompty do generowania od v4 trzymają się tego schematu sztywno**, we wszystkich tematach (budynki, pojazdy, wnętrza, natura…). Cel: jedna LoRA do wszystkiego, w której stałe słowo na stałym miejscu przełącza rodzaj obiektu.

Wersja maszynowa: [`schemat_opisow.json`](schemat_opisow.json). Walidator: [`narzedzia/sprawdz_opis.py`](narzedzia/sprawdz_opis.py) – każdy opis i prompt przechodzi przez niego przed treningiem lub generowaniem.

## Szablon

```
swiat2d style, <kategoria>, <podtyp>, <rozmiar>, <opis>. <końcówka>
```

1. `swiat2d style` – słowo-klucz LoRA, zawsze pierwsze.
2. **kategoria** – jedna z listy niżej, zawsze trzeci wyraz.
3. **podtyp** – jeden z listy dla danej kategorii.
4. **rozmiar** – wzór przypisany do kategorii (metry; produkty w centymetrach).
5. **opis** – co widać na obrazie: bryła, materiały, kolory, elementy. Pisany z obrazu, nie z promptu.
6. **końcówka** – jedna z gotowych końcówek przypisanych do kategorii (kamera + tło), słowo w słowo.

## Kategorie i podtypy

| kategoria | co to jest | podtypy | rozmiar | końcówki |
|---|---|---|---|---|
| `building` | budynek z dachem | `enterable`, `decorative` | `about W m wide and H m tall` | `front_plaski` (płaski prostokątny dach), `front` (kopuły, wieże, dachy spadziste) |
| `structure` | konstrukcja, która nie jest budynkiem | `energy`, `industrial`, `infrastructure`, `agricultural`, `attraction` | `about W m wide and H m tall` | `front` |
| `vehicle` | pojazd | `car`, `van`, `truck`, `bus`, `tram`, `train`, `emergency`, `motorcycle`, `bicycle`, `boat` | `about L m long and H m tall` | `bok_prawo`, `bok_lewo`, `przod`, `tyl` |
| `outdoor prop` | element stojący na zewnątrz | `street furniture`, `sign`, `fence`, `lighting`, `playground`, `sports`, `market stall`, `garden`, `container` | `about W m wide and H m tall` | `front` |
| `nature` | roślinność i natura | `tree`, `bush`, `flower bed`, `rock`, `water` | `about W m wide and H m tall` | `front` |
| `interior object` | wyposażenie wnętrza (sklep, dom) | `shelf`, `counter`, `display case`, `table`, `seating`, `appliance`, `lighting`, `decoration`, `storage` | `about W m wide and H m tall` | `front` |
| `product` | towar, przedmiot do ręki | `box`, `bottle`, `can`, `food`, `toy`, `tool`, `electronics`, `clothing`, `other` | `about W cm wide and H cm tall` | `front` |
| `character` | postać, zwierzę (zarezerwowane) | `person`, `animal` | `about W m wide and H m tall` | `bok_prawo`, `bok_lewo`, `przod`, `tyl` |
| `terrain tile` | bezszwowy kafel podłoża | `grass`, `pavement`, `road`, `dirt`, `gravel`, `sand`, `water`, `floor` | `one ground tile of W by W m` | `kafel` |
| `overlay` | nakładka na podłoże | `path`, `puddle`, `crack`, `stain`, `tyre tracks`, `leaves`, `flowers`, `stones` | `about W m wide and D m deep` | `nakladka` |

Nowa kategoria albo podtyp: tylko decyzją właściciela, dopisana tutaj i w JSON-ie, zanim pojawi się w zbiorze.

## Końcówki (słowo w słowo)

| nazwa | tekst |
|---|---|
| `front_plaski` | `Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background.` |
| `front` | `Pixel art game sprite, fixed orthographic RPG 3/4 camera, the front facing the viewer and the top seen slightly from above, isolated on solid magenta #FF00FF background.` |
| `bok_prawo` | `… the side facing the viewer and the top seen slightly from above, facing right, isolated on solid magenta #FF00FF background.` |
| `bok_lewo` | jak wyżej, `facing left` |
| `przod` | `… the front facing the viewer and the top seen slightly from above, facing the viewer, …` |
| `tyl` | `… the back facing the viewer and the top seen slightly from above, facing away from the viewer, …` |
| `kafel` | `Pixel art game texture, fixed orthographic RPG 3/4 camera, flat ground seen from above, seamless square tile filling the whole image.` |
| `nakladka` | `Pixel art game sprite, fixed orthographic RPG 3/4 camera, lying flat on the ground seen from above, isolated on solid magenta #FF00FF background.` |

Pełne teksty: `schemat_opisow.json`. Dopiski:
- **okrągłe bryły** (tylko `front_plaski` i `front`, tylko gdy obiekt ma okrągłe części): `round shapes drawn straight from the front with their tops visible as flattened ellipses` przed `, isolated on`.
- **styl uzdatniony K** (tylko w promptach do generowania): `Pixel art game sprite` → `Semi-realistic pixel art game sprite` + w opisie `realistic materials and proportions: <materiały>`. Zbiory treningowe mają zwykłą końcówkę.

## Reguły treści
- **Zero zaprzeczeń**: `no`, `not`, `without`, `never`, `none`, `nothing`, `except`, `instead`, `only`. Opisujemy to, co jest.
- **Budynek wejściowy** kończy opis jednym z: `and the standard entrance door in the middle / on the left side / on the right side of the front facade`. Inne drzwi opisujemy położeniem na froncie, nigdy `side door`.
- `front facade` tylko w kategorii `building`.
- Płaski dach w końcówce tylko przy płaskim prostokątnym dachu; przy kopułach, namiotach, szpicach, dachach spadzistych – końcówka `front`.
- **Bez dymu i pary** (dym robi diorama), **bez parkingów i aut przed budynkami** (parking to osobne kafle i pojazdy).
- **Bez podłoża pod obiektem i dookoła niego**: żadnych peronów, płyt, chodników, trawników, torów ani wody terenu (jezioro, rzeka, morze, kanał – woda to też podłoże dioramy) pod spodem i obok. Woda będąca częścią obiektu (misa fontanny, niecka basenu) zostaje. Obiekt stoi bezpośrednio na tle; podłoże to osobne assety dioramy (`terrain tile`, `overlay`). Dotyczy też promptów do generowania.
- Bez napisów w języku; szyldy jako piktogramy.
- Rozmiar z gotowego sprite'a w skali gry (24 px = 1 m): szerokość × wysokość z widocznym dachem.

## Przykłady

```
swiat2d style, building, enterable, about 10 m wide and 8 m tall, a single-storey flower shop with cream walls and orange timber corners, a sign board with a flower pictogram, a wide window with bouquets and a dark grey flat roof with an air conditioning unit, and the standard entrance door on the right side of the front facade. Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background.

swiat2d style, structure, energy, about 8 m wide and 15 m tall, a white wind turbine with a slim round tower on a small concrete base, a nacelle and three long white blades. Pixel art game sprite, fixed orthographic RPG 3/4 camera, the front facing the viewer and the top seen slightly from above, round shapes drawn straight from the front with their tops visible as flattened ellipses, isolated on solid magenta #FF00FF background.

swiat2d style, vehicle, car, about 5 m long and 2 m tall, a silver four-door sedan from the 2000s with tinted windows and chrome door handles. Pixel art game sprite, fixed orthographic RPG 3/4 camera, the side facing the viewer and the top seen slightly from above, facing right, isolated on solid magenta #FF00FF background.

swiat2d style, interior object, shelf, about 2 m wide and 2 m tall, a white metal shop shelf with four levels of colourful boxed goods. Pixel art game sprite, fixed orthographic RPG 3/4 camera, the front facing the viewer and the top seen slightly from above, isolated on solid magenta #FF00FF background.
```

## Przejście ze zbiorów v1–v3
| v1–v3 | od v4 |
|---|---|
| `enterable building` | `building, enterable` |
| `decorative building` | `building, decorative` |
| `decorative object` | `structure, <podtyp>` albo `outdoor prop, <podtyp>` – ręcznie według obiektu |
| końcówka „the front facing … top seen slightly from above” przy budynkach | bez zmian (`front`) |
