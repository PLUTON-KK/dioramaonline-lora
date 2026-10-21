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

## Gotowe LoRA

Pliki LoRA (`.safetensors`, wszystkie zapisane kroki) są na Hugging Face: **[q3ok/dioramaonline-lora-models](https://huggingface.co/q3ok/dioramaonline-lora-models)**. Tutaj zostają opisy, konfiguracje i podglądy.

| LoRA | model | trening | opis i podglądy | pliki |
|---|---|---|---|---|
| budynki v1 final, 512 | Z-Image Turbo | RTX 3080 | [`zimage-turbo-512`](lora-budynki-v1-final/modele/zimage-turbo-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/zimage-turbo-512) |
| budynki v1 final, 512 | Z-Image Base (nie działa na Turbo) | RTX 3080 | [`zimage-base-512`](lora-budynki-v1-final/modele/zimage-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/zimage-base-512) |
| budynki v1 final, 512 | MOSS-Image (trening na Base, najlepsza na SFT) | RTX 3080 | [`moss-image-base-512`](lora-budynki-v1-final/modele/moss-image-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/moss-image-base-512) |
| budynki v1 final, 512 | FLUX 3 Image Klein (trening na base, najlepsza na destylacie; licencja FLUX Kommunity) | RTX 3080 | [`flux3-klein-base-512`](lora-budynki-v1-final/modele/flux3-klein-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/flux3-klein-base-512) |
| budynki v1 final, 512 | FLUX.2 Klein 4B | RTX 3080 | [`flux2-klein-4b-512`](lora-budynki-v1-final/modele/flux2-klein-4b-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/flux2-klein-4b-512) |
| budynki v1 final, 512 | Qwen-Image 2512 (bf16) | RunPod A100 | [`qwen-image-2512-512`](lora-budynki-v1-final/modele/qwen-image-2512-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/qwen-image-2512-512) |

W treningu na RunPod (2026-10-21): Qwen-Image-Edit 2511 (512), Krea 2 Raw (512), Z-Image Turbo / MOSS / FLUX 3 w 1024 bf16. Dopisuję, gdy skończą.
