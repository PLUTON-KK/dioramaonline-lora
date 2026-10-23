# Drzwi kanoniczne (v7, od 2026-10-23)

Jedyne drzwi, których używamy w budynkach Świata 2D. Ten sam projekt co v6 (dwuskrzydłowe 60 × 60 px = 2,5 × 2,5 m, kwadrat; jednoskrzydłowe 30 × 60 px = 1,25 × 2,5 m), ale przerysowany w pełnym kolorze, żeby dało się go mapować na dowolną paletę. Wcześniejsze wersje (v4–v6) są nieużywane.

Pliki (`<typ>` = `2skrz` / `1skrz`, `<stan>` = `closed` / `open`):

| plik | co to jest |
|---|---|
| `drzwi-<typ>-<stan>_pelny.png` | rozmiar gry (60×60 / 30×60), pełny kolor – źródło do dowolnej palety |
| `drzwi-<typ>-<stan>_p1024.png` | rozmiar gry, paleta 1024 (128 + kolory pośrednie) |
| `drzwi-<typ>-<stan>_master_pelny.png` | bez zmniejszenia: wycinek z gpt-image-2 (2-skrz 468×516, 1-skrz 221×516), pełny kolor |
| `drzwi-<typ>-<stan>_master_p1024.png` | bez zmniejszenia, paleta 1024 |

`doorway` / `changedRegion` i maska otwarcia bez zmian względem v6 (`drzwi_kanon_v7.json`). Master nie jest dokładnym kwadratem (GPT narysował drzwi ok. 10% wyższe), rozmiar gry jest skalowany do dokładnie 60×60 / 30×60.

Pochodzenie: gpt-image-2 (quality high) przerysował drzwi v6 ×8 w pełnym kolorze, prompt: zachowaj projekt, szare szkło z plamami, kwadrat 1:1.

![v7](podglad.png)
