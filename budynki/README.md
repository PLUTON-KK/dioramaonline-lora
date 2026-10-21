# Budynki

Fronty budynków do dioramy: pixel art, stała kamera RPG 3/4, płaski prostokątny dach, tło magenta. Dwa typy: `enterable building` (z kanonicznymi drzwiami gry) i `decorative building`.
Obrazy zbioru wygenerował ChatGPT, a my przerobiliśmy je na format gry (kadr, skala 24 px = 1 m, jedne kanoniczne drzwi, paleta świata, opisy).

## Stan (2026-10-21)
- **Zbiór v1-final** (72 budynki, skala gry w obrazie): wytrenowane 11 LoRA na 8 modelach bazowych → [`modele/v1/`](modele/v1/).
- **Zbiór v2-final** (zamrożony 2026-10-21; te same budynki, ciasny kadr, rozmiar w metrach w opisie, poprawione opisy) → [`zbiory/v2-final/`](zbiory/v2-final/), lista zmian: [`ZMIANY_V1_V2.md`](zbiory/v2-final/ZMIANY_V1_V2.md). Trening LoRA v2 (512) na RunPod: 2026-10-21.
- **Porównania** (nasze LoRA i ChatGPT / Gemini na tych samych 10 budynkach testowych) → [`porownania/`](porownania/).

## Katalogi
| katalog | co jest w środku |
|---|---|
| [`zbiory/v1-final/`](zbiory/v1-final/) | zbiór treningowy v1 (zamrożony): `train_512/`, `train_1024/`, `sprites/` (format gry), `metadata.jsonl`, `captions.csv`, skrypty |
| [`zbiory/v2-final/`](zbiory/v2-final/) | zbiór v2-final (zamrożony) + [`ZMIANY_V1_V2.md`](zbiory/v2-final/ZMIANY_V1_V2.md) |
| [`modele/v1/`](modele/v1/) | po jednym folderze na LoRA: README (jak uczona, jak używać, licencja), `config_ai-toolkit.yaml`, `podglady/` (kroki 0–2000) |
| [`testy/`](testy/) | zestaw testowy: 10 budynków spoza zbioru, prompty v1/v2, wzory stylu i drzwi, prompty „paskowe” dla modeli zewnętrznych |
| [`porownania/`](porownania/) | zestawienia wyników, każde w osobnym folderze z datą |

## LoRA

Pliki: Hugging Face [`budynki/v1/`](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1). Słowo wyzwalające: `swiat2d style`.

| zbiór | model | rozdz. | trening | opis i podglądy | pliki |
|---|---|---|---|---|---|
| v1-final | Z-Image Turbo | 512 | RTX 3080 | [`zimage-turbo-512`](modele/v1/zimage-turbo-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-turbo-512) |
| v1-final | Z-Image Turbo | 1024 | RunPod L40 | [`zimage-turbo-1024`](modele/v1/zimage-turbo-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-turbo-1024) |
| v1-final | Z-Image Base (nie działa na Turbo) | 512 | RTX 3080 | [`zimage-base-512`](modele/v1/zimage-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-base-512) |
| v1-final | MOSS-Image Base (najlepsza na SFT) | 512 | RTX 3080 | [`moss-image-base-512`](modele/v1/moss-image-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-512) |
| v1-final | MOSS-Image Base (najlepsza na SFT) | 1024 | RunPod L40 | [`moss-image-base-1024`](modele/v1/moss-image-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-1024) |
| v1-final | FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 512 | RTX 3080 | [`flux3-klein-base-512`](modele/v1/flux3-klein-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux3-klein-base-512) |
| v1-final | FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 1024 | RunPod A40 | [`flux3-klein-base-1024`](modele/v1/flux3-klein-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux3-klein-base-1024) |
| v1-final | FLUX.2 Klein 4B | 512 | RTX 3080 | [`flux2-klein-4b-512`](modele/v1/flux2-klein-4b-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux2-klein-4b-512) |
| v1-final | Qwen-Image 2512 | 512 | RunPod A100 | [`qwen-image-2512-512`](modele/v1/qwen-image-2512-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-2512-512) |
| v1-final | Qwen-Image-Edit 2511 (z obrazem wzoru) | 512 | RunPod A100 | [`qwen-image-edit-2511-512`](modele/v1/qwen-image-edit-2511-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-edit-2511-512) |
| v1-final | Krea 2 Raw (do użycia na Krea 2 Turbo; Krea 2 Community License) | 512 | RunPod A6000 | [`krea2-raw-512`](modele/v1/krea2-raw-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/krea2-raw-512) |
