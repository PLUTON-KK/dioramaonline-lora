# Zasady (stan na 2026-10-22)

## Grafika gry
- Skala: 24 px = 1 m. Paleta świata: 64 kolory. Twarda przezroczystość (alfa 0 albo 255).
- Kamera: stała, RPG 3/4 z południa. Front do widza, pionowe krawędzie, bez skosów i perspektywy.
- Budynki: płaski, prostokątny dach o szerokości frontu. Jego wysokość na sprite'cie to połowa głębokości budynku.
- Budynek z wejściem ma **jedne** drzwi: kanoniczny moduł `std-external-2` (59×58 px = 2,46 × 2,42 m), w dowolnym miejscu frontu. Renderer animuje tylko jedne drzwi.
- Budynek dekoracyjny ma własne drzwi i bramy, rysowane jako zamknięte.
- Zero napisów w języku, tylko piktogramy. Szyldy z logo dodaje gra.

## Generowanie pasków (ChatGPT/Codex)
- Szablon promptu jest stały, zmienia się tylko lista obiektów z wymiarami w metrach. Dopisywanie „własnych reguł” do szablonu psuło wyniki.
- Wzór zawiera tylko zaakceptowane grafiki tej kategorii. Jeden zły przykład we wzorze wraca w wynikach.
- Jeden pasek = jedna nowa rozmowa. Poprawka (np. dach trapezem) to edycja w tej samej rozmowie, zapisywana jako `pasekNN_edit1.png`.
- Opisy obiektów pisane naszymi materiałami (krem, pomarańczowe drewno, szare panele). Słowa typu „town house”, „brick”, „shutters” ciągną w stronę starówki.

## Opisy i prompty od v4 (obowiązuje sztywno)
- Jeden schemat dla wszystkich tematów: `swiat2d style, <kategoria>, <podtyp>, <rozmiar>, <opis>. <końcówka>`.
- Kategoria zawsze trzecim wyrazem, ze stałej listy: `building`, `structure`, `vehicle`, `outdoor prop`, `nature`, `interior object`, `product`, `character`, `terrain tile`, `overlay`. Podtypy i końcówki kamery przypisane do kategorii.
- Szczegóły, lista podtypów, końcówki słowo w słowo: [`wspolne/SCHEMAT_OPISOW.md`](../wspolne/SCHEMAT_OPISOW.md). Każdy opis i prompt przechodzi przez walidator [`wspolne/narzedzia/sprawdz_opis.py`](../wspolne/narzedzia/sprawdz_opis.py).
- Bez dymu i pary, bez parkingów i aut przed budynkami, bez podłoża pod obiektem i dookoła (perony, płyty, chodniki, trawniki) – to robi diorama osobnymi assetami. Płaski dach w kamerze tylko przy płaskim dachu.
- Zbiory v1–v3 zostają w starym zapisie (`enterable building` / `decorative building` / `decorative object`); przy budowie v4 przepisujemy je wg tabeli przejścia.

## Zbiory LoRA
- Obrazy treningowe: płótno w jednej skali dla wszystkich obiektów (`train_512`: piksele gry ×1, linia gruntu y=492; `train_1024`: ×2, y=984), tło magenta #FF00FF, bez automatycznego skalowania w trenerze.
- Opisy pisane **z obrazków**, nie z promptów. Jeden schemat:
  `swiat2d style, <enterable building | decorative building>, <co, kondygnacje, ściany, elementy, dach>, <drzwi>. <stała końcówka o kamerze i tle>`.
- **Zero zaprzeczeń** w opisach i promptach testowych („no door”, „without”). Modele słabo je rozumieją, a samo słowo „door” przyciąga drzwi.
- Elementów stylu, które model ma dobierać sam (donice, krzaki), nie opisujemy.
- Właściciel akceptuje listę i opisy przed zbudowaniem pakietu. Pakiet trafia do repo.

## Trening
- Trening tylko na wyraźne polecenie właściciela, domyślnie w nocy.
- Podgląd co 500 kroków na obiektach **spoza** zbioru. Zapis LoRA co 250 kroków, bo najlepszy bywa etap pośredni.
- Ocena końcowa: w ComfyUI, w PNG, kilka seedów. Podglądy z ai-toolkit są w JPG.
