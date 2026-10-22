# Budynki

Fronty budynków do dioramy: pixel art, stała kamera RPG 3/4, płaski prostokątny dach, tło magenta. Dwa typy: `enterable building` (z kanonicznymi drzwiami gry) i `decorative building`.
Pochodzenie obrazów: v1 i v2 wygenerował ChatGPT, a my przerobiliśmy je na format gry (kadr, skala 24 px = 1 m, jedne kanoniczne drzwi, paleta świata, opisy). W v3 doszło 30 obiektów wygenerowanych z naszymi LoRA v2 i wybranych przez właściciela.

**Badania w skrócie: [BADANIA.md](BADANIA.md)** (metoda, wyniki, wnioski).

## Stan (2026-10-22)

| wersja | zbiór | LoRA | stan |
|---|---|---|---|
| v1 | [v1-final](zbiory/v1-final/) – 72 budynki, skala gry w obrazie | [modele/v1](modele/v1/) – 11 LoRA, 8 modeli bazowych | zamrożona |
| v2 | [v2-final](zbiory/v2-final/) – te same 72, ciasny kadr, rozmiar w metrach w opisie ([zmiany](zbiory/v2-final/ZMIANY_V1_V2.md)) | [modele/v2](modele/v2/) – 7 LoRA, 512 | zamrożona |
| v3 | [v3-final](zbiory/v3-final/) – 88 obiektów, 512 ([zmiany](zbiory/v3-final/ZMIANY_V2_V3.md)) | [modele/v3](modele/v3/) – v3 (4 LoRA) i v3-3000 (3 LoRA) | wytrenowana, styl odrzucony |
| v4 | w przygotowaniu: budynki z v3 z dachem przerysowanym na rzut ½, nowe propsy, opisy wg schematu v4 | – | zasady: [KARTA_TECHNICZNA_V4](../wspolne/KARTA_TECHNICZNA_V4.md), [SCHEMAT_OPISOW](../wspolne/SCHEMAT_OPISOW.md), paleta [paleta128](../wspolne/paleta128.png) |

Pliki LoRA: Hugging Face [q3ok/dioramaonline-lora-models](https://huggingface.co/q3ok/dioramaonline-lora-models), folder `budynki/<wersja>/<model>/` – jeden plik na LoRA (krok końcowy). Słowo wyzwalające: `swiat2d style`.

Porównania (nasze LoRA i ChatGPT / Gemini na tych samych budynkach testowych): [`porownania/`](porownania/).

## Katalogi
| katalog | co jest w środku |
|---|---|
| [`zbiory/`](zbiory/) | zbiory treningowe: `train_512/` (v1 też `train_1024/`), `sprites/` (format gry), `metadata.jsonl`, `captions.csv`, lista zmian względem poprzedniej wersji |
| [`modele/`](modele/) | opis każdej wersji LoRA: trening, konfiguracje, podglądy, linki do HF |
| [`testy/`](testy/) | zestaw testowy: budynki spoza zbioru, prompty, wzory stylu i drzwi |
| [`porownania/`](porownania/) | zestawienia wyników, każde w osobnym folderze z datą |
