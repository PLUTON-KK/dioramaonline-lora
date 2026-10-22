# Karta techniczna v4: głębia wierzchu i paleta

Zatwierdzone przez właściciela (q3ok) 2026-10-22. Obowiązuje dla zbioru v4 i wszystkich nowych grafik.

## 1. Głębia wierzchu: ½ rzeczywistej głębokości

Rzut ortogonalny frontem do widza. Szerokość i wysokość: 24 px/m. Głębokość (wszystko, co biegnie w głąb): **12 px/m**, czyli ½ rzeczywistej głębokości. To pełna formuła `D × 12` z `docs/KAMERA.md` gry, **bez** dodatkowego skracania o 50%.

Jedna liczba dla każdej poziomej powierzchni:

| Element | Zasada |
|---|---|
| płaski dach | pas dachu = `depth_m × 12` px (budynek 8 m w głąb → 96 px) |
| okrągły wierzch (kosz, misa fontanny, zbiornik, wieża) | elipsa o wysokości ½ szerokości |
| siedzisko ławki, blat, wierzch skrzyni | głębokość × 12 px |
| krawędzie biegnące w głąb | równoległe, bez punktu zbiegu; tylne nogi i krawędzie dokładnie za przednimi |

Front zawsze w pełnej wysokości (24 px/m). Płytkie budynki mają wąski dach, głębokie szeroki: głębokość wynika z rzeczywistej bryły (`metric.depth_m`).

Wzorce geometryczne z kodu: `wyniki/wzorce_geometria` (budynek, walec, misa, ławka, namiot; poprawnie i typowe błędy).

Zmiana względem wcześniejszego zapisu w kryteriach dioramy (059, K2): tam „dachy na ok. 50% formuły D × 12” — to było nieporozumienie; właściwa wartość to pełna formuła D × 12 (½ rzeczywistości). Dotyczy reguł K2 i D8.

## 2. Paleta świata 128

Plik: [`paleta128.json`](paleta128.json), próbnik: [`paleta128.png`](paleta128.png), generator: [`narzedzia/paleta128.py`](narzedzia/paleta128.py). Zastępuje dla grafik v4 dotychczasową paletę świata 64 (`world_palette.json` gry).

Budowa (narzucona od góry, blisko rzeczywistości, praktyka palet pixel art):
- **16 ramp × 8 stopni jasności = 128 kolorów.** Każda rampa zbudowana wokół typowego, rzeczywistego koloru materiału (wzorzec w pliku), stopnie jasności L* od cienia do światła.
- Rampy: asfalt/beton (szarości od czerni `#0B0B10` do bieli `#FFFFFF`), ciepła szarość (kamień, tynk kremowy), tynk brzoskwiniowy, cegła, dachówka, drewno (dąb), piasek/ochra, trawa, liście, błękit (woda → niebo/szkło), łupek/stal niebieska, czerwień farby, żółć znaków, pomarańcz, granat, kwiaty/fiolet.
- Przesunięcie barwy jak w grach: cienie chłodniejsze, światła cieplejsze; nasycenie łagodnie spada ku skrajom.
- Kolory wyraźnie różne: najmniejsza różnica ΔE 4,6 (dwie pary poniżej 5), mediana najbliższego sąsiada ΔE 9,8. Magenta tła (`#FF00FF`) daleko od palety (ΔE ≥ 71).

Użycie: każdy piksel sprite'a mapowany na najbliższy kolor palety (odległość RGB), bez ditheringu, twarda alfa. Kolejność kolorów w pliku nie ma znaczenia dla mapowania.
