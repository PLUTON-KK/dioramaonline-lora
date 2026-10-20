# lora-budynki-v1-final

Zbior treningowy LoRA: budynki do gry Swiat 2D (diorama), pixel art, fronty. Niezalezny od modelu (Z-Image, MOSS-Image, FLUX.2 klein, ...).
Zaakceptowany przez wlasciciela 2026-10-20: 72 obrazow (25 dekoracyjny, 47 wejsciowy).

## Zawartosc
| folder / plik | co to jest |
|---|---|
| `train_512/` | to samo w 512x512: sprite x1 (natywne piksele gry, 1 m = 24 px), dol na linii y=492, te same opisy. Do treningu w rozdzielczosci 512 (szybciej, ~1 s/krok na RTX 3080 vs ~7,5 s w 1024) |
| `train_1024/` | gotowe do treningu: `<nazwa>.png` (1024x1024) + `<nazwa>.txt` (opis). Format kohya / ai-toolkit / KohakuMossTrainer (folder obrazow z opisami) |
| `sprites/` | zrodlo prawdy w formacie gry: 24 px = 1 m, paleta swiata (64 kolory), przezroczyste tlo. Wejsciowe takze `<nazwa>-open.png` i `<nazwa>.json` (drzwi dla gry) |
| `metadata.jsonl` | jedna linia na budynek: typ, rozmiar w px i m, pozycja drzwi, opis |
| `captions.csv` | wszystkie opisy w jednej tabeli |
| `podglad.png` | wszystkie budynki w jednej skali |

## Obrazy treningowe
- Plotno 1024x1024, tlo jednolita magenta #FF00FF.
- Sprite powiekszony x2 metoda NEAREST (bez rozmycia): 1 m = 48 px. Ta sama skala dla wszystkich, wiec model uczy sie prawdziwych roznic wielkosci (garaz ~4 m, ratusz ~19 m).
- Dol budynku zawsze na linii y=984, wysrodkowany poziomo.
- Trening: rozdzielczosc 1024, BEZ bucketow / skalowania obrazow (inaczej znika wspolna skala).
- Wynik generowania: zmniejszyc /2 (NEAREST/BOX), paleta swiata, wyciac magente -> sprite gry.

## Opisy (caption)
Schemat:
`swiat2d style, <enterable building | decorative building>, <co to jest, kondygnacje, sciany i kolory, elementy, dach>, <drzwi>. Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background.`
- `swiat2d style` - slowo wyzwalajace styl.
- `enterable building` - budynek z wejsciem: jedne kanoniczne drzwi std-external-2 (59x58 px = 2,46 x 2,42 m), opis konczy sie `the standard entrance door in the middle of / on the left side of / on the right side of the front facade`.
- `decorative building` - bez wejscia, wlasne drzwi / bramy opisane slowami.
- Dach zawsze plaski prostokat; domyslnie `a dark grey flat roof with an air conditioning unit`, inne pokrycia opisane (zwir, swietliki, blacha, zielony dach, panele, taras).
- Bez napisow w jezyku, tylko piktogramy. Elementow typu donice nie opisujemy (styl).
- Opisy pisane z obrazkow (nie z promptow), zaakceptowane przez wlasciciela.

## Zasady stylu
Tylko fronty (tyl/bok - osobny zbior pozniej). Kamera RPG 3/4 z poludnia, pionowe krawedzie, plaski prostokatny dach (wysokosc na sprite = pol glebokosci budynku). Bez skosow i perspektywy.

## Dodatkowo
- `sprites/_drzwi-kanon-closed.png`, `_drzwi-kanon-open.png`, `_drzwi-kanon.json` - kanoniczny modul drzwi std-external-2 (59x58 px).
- `narzedzia/trening_budynki_zimage*.yaml` - konfiguracje ai-toolkit (Z-Image Turbo, adapter v2) dla 1024 i 512.
- `narzedzia/` - skrypty, ktorymi zbior powstal (sciezki lokalne E:\ai\...): `drzwi_kanon.py` (podmiana drzwi i skala wg drzwi), `budynki_lista_lora.py` (lista i opisy), `opisy.py` (tresc opisow), `budynki_pakiet.py` (ten pakiet).
