# dioramaonline-lora

Zbiory treningowe LoRA i gotowe LoRA do gry Świat 2D (dioramaonline), pixel art.

## 📓 [Devlog: jak to powstaje](devlog/00-prolog.md)
Skąd ten projekt, co testowaliśmy, co nie wyszło i dlaczego. Zaczyna się od [prologu](devlog/00-prolog.md), a [tu jest spis wpisów](devlog/README.md).

> Sorry, że po polsku, ale mi tak łatwiej. Jesteśmy w dobie AI (serio!), więc można sobie automatycznie przetłumaczyć. - q3ok
>
> *Sorry it's in Polish, it's just easier for me. We live in the age of AI (seriously!), so feel free to auto-translate it.*

## Zbiory

| zbiór | co | obrazy | status |
|---|---|---|---|
| [`lora-budynki-v1-final`](lora-budynki-v1-final/) | budynki, fronty, `enterable` / `decorative` | 72 (47 + 25) | zaakceptowany 2026-10-20 |
| [`lora-budynki-v2`](lora-budynki-v2/) | te same budynki, kadrowane ciasno, rozmiar w metrach w opisie (skala gry przywracana po generacji) | 72 (47 + 25) | 2026-10-21, w treningu |

Każdy zbiór ma `train_512/` i `train_1024/` (PNG + TXT, gotowe do ai-toolkit / kohya / KohakuMossTrainer), `sprites/` (format gry) i README z zasadami.

## Modele: generowanie czy też edycja obrazu

Ściąga, którym modelem da się tylko generować z tekstu, a którym także przerabiać istniejący obraz (np. zdjęcie produktu ze sklepu → wersja do dioramy). Stan: 2026-10-21, wg kart modeli na Hugging Face.

| model | tekst → obraz | edycja / obraz wejściowy | lokalnie (RTX 3080, 10 GB) | licencja | nasza LoRA budynków |
|---|---|---|---|---|---|
| Z-Image Turbo | ✅ | ❌ (Tongyi zapowiada osobne Z-Image-Edit i Z-Image-Omni-Base, jeszcze niewydane) | ✅ bf16 | Apache 2.0 | v1 512, 1024 |
| Z-Image Base | ✅ | ❌ | ✅ bf16 | Apache 2.0 | v1 512 |
| MOSS-Image Base / SFT | ✅ | ❌ | ✅ int8 | Apache 2.0 | v1 512, 1024 (uczona na Base) |
| FLUX 3 Image Klein (base i destylat) | ✅ | ✅ edycja i kilka obrazów referencyjnych | ✅ int8 | FLUX Kommunity | v1 512, 1024 (uczona na base) |
| FLUX.2 Klein 4B (base i destylat) | ✅ | ✅ edycja i kilka obrazów referencyjnych | ✅ bf16 | Apache 2.0 | v1 512 (uczona na base) |
| Qwen-Image 2512 | ✅ | ❌ (do edycji jest osobny Qwen-Image-Edit) | ⚠️ tylko GGUF Q4 (bf16 ~41 GB za duży) | Apache 2.0 | v1 512 |
| Qwen-Image-Edit 2511 | ✅ | ✅ edycja instrukcją, do 3 obrazów wejściowych | ⚠️ tylko GGUF Q4 | Apache 2.0 | v1 512 (uczona z wzorem stylu jako obrazem wejściowym) |
| Krea 2 Raw / Turbo | ✅ | ⚠️ tylko referencja stylu przez LoRA `krea2_style_reference` (bez edycji treści) | ⚠️ Turbo int8; Raw za duży | Krea 2 Community (komercyjnie < 1 mln USD/rok) | v1 512 (uczona na Raw) |
| PixelDiT 1300M | ✅ | ❌ | ✅ bf16 | – | brak |
| Krea 3, Nano Banana, Imagen, ChatGPT (obrazy) | ✅ | ✅ | ❌ tylko API, wag nie ma | zamknięte | nie da się (brak wag) |

Do przerabiania zdjęć produktów na styl dioramy kandydaci to modele z edycją: **Qwen-Image-Edit 2511**, **FLUX 3 Klein**, **FLUX.2 Klein 4B** (lokalnie), z naszą LoRA budynków albo przyszłą LoRA przedmiotów.

## Gotowe LoRA

Pliki LoRA (`.safetensors`, wszystkie zapisane kroki) są na Hugging Face: **[q3ok/dioramaonline-lora-models](https://huggingface.co/q3ok/dioramaonline-lora-models)**. Tutaj zostają opisy, konfiguracje i podglądy.

| LoRA | model | rozdz. | trening | opis i podglądy | pliki |
|---|---|---|---|---|---|
| budynki v1 final | Z-Image Turbo | 512 | RTX 3080 | [`zimage-turbo-512`](lora-budynki-v1-final/modele/zimage-turbo-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/zimage-turbo-512) |
| budynki v1 final | Z-Image Turbo | 1024 | RunPod L40 | [`zimage-turbo-1024`](lora-budynki-v1-final/modele/zimage-turbo-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/zimage-turbo-1024) |
| budynki v1 final | Z-Image Base (nie działa na Turbo) | 512 | RTX 3080 | [`zimage-base-512`](lora-budynki-v1-final/modele/zimage-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/zimage-base-512) |
| budynki v1 final | MOSS-Image Base (najlepsza na SFT) | 512 | RTX 3080 | [`moss-image-base-512`](lora-budynki-v1-final/modele/moss-image-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/moss-image-base-512) |
| budynki v1 final | MOSS-Image Base (najlepsza na SFT) | 1024 | RunPod L40 | [`moss-image-base-1024`](lora-budynki-v1-final/modele/moss-image-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/moss-image-base-1024) |
| budynki v1 final | FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 512 | RTX 3080 | [`flux3-klein-base-512`](lora-budynki-v1-final/modele/flux3-klein-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/flux3-klein-base-512) |
| budynki v1 final | FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 1024 | RunPod A40 | [`flux3-klein-base-1024`](lora-budynki-v1-final/modele/flux3-klein-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/flux3-klein-base-1024) |
| budynki v1 final | FLUX.2 Klein 4B | 512 | RTX 3080 | [`flux2-klein-4b-512`](lora-budynki-v1-final/modele/flux2-klein-4b-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/flux2-klein-4b-512) |
| budynki v1 final | Qwen-Image 2512 | 512 | RunPod A100 | [`qwen-image-2512-512`](lora-budynki-v1-final/modele/qwen-image-2512-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/qwen-image-2512-512) |
| budynki v1 final | Qwen-Image-Edit 2511 (z obrazem wzoru) | 512 | RunPod A100 | [`qwen-image-edit-2511-512`](lora-budynki-v1-final/modele/qwen-image-edit-2511-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/qwen-image-edit-2511-512) |
| budynki v1 final | Krea 2 Raw (do użycia na Krea 2 Turbo; Krea 2 Community License) | 512 | RunPod A6000 | [`krea2-raw-512`](lora-budynki-v1-final/modele/krea2-raw-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/krea2-raw-512) |

