# Drzwi kanoniczne (v6, od 2026-10-23)

Jedyne drzwi, których używamy w budynkach Świata 2D. Wszystkie wcześniejsze wersje (v4 59×57, v5 59×59) są nieużywane.

| moduł | plik | rozmiar | wymiar | doorway / changedRegion (x, y, w, h) |
|---|---|---|---|---|
| `std-external-2` (dwuskrzydłowe) | `drzwi-2skrz-closed.png`, `drzwi-2skrz-open.png` | 60 × 60 px | 2,5 × 2,5 m, **kwadrat** | 10, 3, 42, 57 / 10, 3, 42, 57 |
| `std-external-1` (jednoskrzydłowe) | `drzwi-1skrz-closed.png`, `drzwi-1skrz-open.png` | 30 × 60 px | 1,25 × 2,5 m | 4, 4, 22, 56 / 2, 2, 26, 58 |

Skala gry 24 px/m, więc 2,5 m = dokładnie 60 px (bez zaokrągleń). Tło przezroczyste, otwarte = przezroczysty otwór w `changedRegion`. Dane maszynowe: [`drzwi_kanon_v6.json`](drzwi_kanon_v6.json).

Pochodzenie: v4 (59 × 57) → v5 (zdublowane wiersze szyby 17 i 44 → kwadrat 59 × 59) → v6 (zdublowany środkowy słupek x 29 / szyba skrzydła x 10 oraz wiersz szyby y 50 → 60 × 60). Rama i klamki bez zmian.

Wzór do generatorów (GPT itp.): tylko drzwi zamknięte, z informacją, że mają 2,5 × 2,5 m / 60 × 60 px i w obrazie też muszą być kwadratowe.

![v5 obok v6](podglad.png)
