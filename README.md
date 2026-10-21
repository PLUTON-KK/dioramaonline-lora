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

Każdy zbiór ma `train_512/` i `train_1024/` (PNG + TXT, gotowe do ai-toolkit / kohya / KohakuMossTrainer), `sprites/` (format gry) i README z zasadami.

## Gotowe LoRA

| LoRA | model | gdzie |
|---|---|---|
| budynki v1 final, 512 | Z-Image Turbo | [`lora-budynki-v1-final/modele/zimage-turbo-512`](lora-budynki-v1-final/modele/zimage-turbo-512/) |
| budynki v1 final, 512 | MOSS-Image (trening na Base, najlepsza na SFT) | [`lora-budynki-v1-final/modele/moss-image-base-512`](lora-budynki-v1-final/modele/moss-image-base-512/) |
| budynki v1 final, 512 | FLUX 3 Image Klein (trening na base, najlepsza na destylacie; licencja FLUX Kommunity) | [`lora-budynki-v1-final/modele/flux3-klein-base-512`](lora-budynki-v1-final/modele/flux3-klein-base-512/) |
