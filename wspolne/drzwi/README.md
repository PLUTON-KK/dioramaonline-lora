# Drzwi kanoniczne (v5, od 2026-10-23)

Jedyne drzwi, których używamy w budynkach Świata 2D. Wszystkie wcześniejsze wersje (w tym v4 59×57 px) są nieużywane.

| moduł | plik | rozmiar | wymiar | doorway / changedRegion (x, y, w, h) |
|---|---|---|---|---|
| `std-external-2` (dwuskrzydłowe) | `drzwi-2skrz-closed.png`, `drzwi-2skrz-open.png` | 59 × 59 px | 2,4 × 2,4 m, **kwadrat** | 10, 3, 41, 56 / 10, 3, 41, 56 |
| `std-external-1` (jednoskrzydłowe) | `drzwi-1skrz-closed.png`, `drzwi-1skrz-open.png` | 29 × 59 px | 1,2 × 2,4 m | 4, 4, 21, 55 / 2, 2, 25, 57 |

Skala gry 24 px/m (59 px = 2,4 m, zaokrąglenie przyjęte dla drzwi). Tło przezroczyste, otwarte = przezroczysty otwór w `changedRegion`. Dane maszynowe: [`drzwi_kanon_v5.json`](drzwi_kanon_v5.json).

Pochodzenie: v4 (59 × 57) + zdublowane wiersze 17 i 44 (szyba nad i pod klamką), żeby drzwi dwuskrzydłowe były idealnym kwadratem – generatorom łatwiej trzymać proporcję kwadratu. Rama i klamki bez zmian.

Wzór do generatorów (GPT itp.): tylko drzwi zamknięte, z informacją, że mają 2,4 × 2,4 m / 59 × 59 px i w obrazie też muszą być kwadratowe.

![v4 obok v5](podglad.png)
