# Budynki: zbiór v2

(dawniej katalog `lora-budynki-v2`)

Te same 72 budynki co [zbiór v1-final](../v1-final/) (25 dekoracyjnych, 47 wejsciowych), inaczej podane do nauki.
Generator: `E:/ai/lora/budynki_pakiet_v2.py`.

## Czym rozni sie od v1
- **Skali nie uczymy w obrazie.** Kazdy budynek kadrowany ciasno: dluzszy bok = 88% plotna, wysrodkowany poziomo, dol 6% nad dolna krawedzia. Maly garaz i ratusz zajmuja podobnie duzo kadru, wiec model ma cala rozdzielczosc na detal.
- **Rozmiar jest w opisie:** zaraz po typie `about <szer> m wide and <wys> m tall` (wysokosc sprite'a z widocznym dachem, jak w grze).
- **Skale gry przywraca skrypt po generacji:** szerokosc budynku na wyniku -> `szer_m * 24` px, potem paleta swiata i wyciecie magenty.
- Poprawiony opis `budka-pokazu` (budka z lodami): bez zaprzeczenia "with no visible door".
- "side door" (13 opisow) zamienione na polozenie drzwi na froncie (`on the right/left of the front facade`) - modele czytaly to jako drzwi w scianie bocznej i obracaly budynek do izometrii.

**Pelna lista zmian i powody: [ZMIANY_V1_V2.md](ZMIANY_V1_V2.md).**

## Zawartosc
| folder / plik | co to jest |
|---|---|
| `train_512/`, `train_1024/` | `<nazwa>.png` (magenta #FF00FF) + `<nazwa>.txt` (opis) |
| `sprites/` | zrodlo prawdy w formacie gry (24 px = 1 m), kopia z v1 |
| `metadata.jsonl` | jak v1 + `kadr`: skala, px na metr i bbox budynku dla 512 i 1024 |
| `captions.csv` | wszystkie opisy |
| `podglad.png` | wszystkie budynki z train_512 |

## Skalowanie obrazow
Skala niecalkowita (od x1 do ~x4,8 przy 512), wiec: NEAREST x8, potem BOX do rozmiaru docelowego na kolorach premultiplikowanych, alfa progowana -> brak magentowej obwodki, piksele lekko miekkie na krawedziach. Po generacji i tak zmniejszamy do skali gry.
Trening: bez bucketow i bez dodatkowego skalowania (obrazy juz w docelowej rozdzielczosci).
