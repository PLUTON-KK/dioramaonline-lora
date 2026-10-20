# LoRA: Z-Image Turbo, budynki v1 final, 512

- Plik: `swiat2d_zimage_budynki_v1final_512.safetensors` (krok 2000, rank 16, ~85 MB).
- Model bazowy: Z-Image Turbo (`z_image_turbo_bf16.safetensors`), trening z adapterem ostris `zimage_turbo_training_adapter_v2`.
- Zbior: `../../train_512` (72 budynki, 512x512, piksele gry x1), ai-toolkit, 2000 krokow, lr 1e-4, batch 1. Czas: 59 min na RTX 3080 10 GB (2026-10-20).
- Konfiguracja: `config_ai-toolkit.yaml`.

## Uzycie (ComfyUI)
- LoraLoaderModelOnly, sila 1.0; Z-Image Turbo: 8 krokow, cfg 1, sampler res_multistep, shift 3, rozdzielczosc 512x512.
- Prompt wg schematu opisow zbioru: `swiat2d style, enterable building, ... , and the standard entrance door in the middle of the front facade. Pixel art game sprite, fixed orthographic RPG 3/4 camera, front facade facing the viewer, flat rectangular roof visible from above, isolated on solid magenta #FF00FF background.`
- Wynik: wyciac magente, paleta swiata -> sprite gry (piksele 1:1, bez zmniejszania).

## Podglady
`podglady/`: budynki spoza zbioru po krokach 500-2000 (JPG z ai-toolkit). Krok 2000: wspolna linia gruntu, kanoniczne drzwi, pokrycia dachow z opisu, czysta magenta.
Uwaga: prompt budki z lodami w podgladach zawieral zaprzeczenie ("no visible door") - ten test nie jest miarodajny.
Pozostale zapisy (500-1750) lokalnie: `E:\ai\lora\output\swiat2d_zimage_budynki_v1final_512\`.
