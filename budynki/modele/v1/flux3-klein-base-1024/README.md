# LoRA: FLUX 3 Image Klein base, budynki v1 final, 1024

**Plik LoRA (krok końcowy 2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux3-klein-base-1024)**

- Trening: FLUX 3 Image Klein base (bf16), zbior [`budynki/zbiory/v1-final/train_1024`](../../../zbiory/v1-final/train_1024/), rank 16, lr 1e-4, 2000 krokow, RunPod A40 48 GB (2026-10-21).
- Licencja modelu bazowego: **FLUX Kommunity License (Black Forest Labs)**.
- Konfiguracja: `config_ai-toolkit.yaml`.
- Uczy sie najwolniej z modeli; napisy (np. u weterynarza) zostaja dlugo. Najlepiej uzywac na wersji destylowanej.

## Podglady
`podglady/kroki_0-2000.png`: 10 budynkow spoza zbioru (prompty: [`budynki/testy/prompty_v1.json`](../../../testy/prompty_v1.json)), kroki 0 (bez LoRA), 500, 1000, 1500, 2000. Sample ai-toolkit z treningu.
