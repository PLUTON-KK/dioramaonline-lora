# LoRA: MOSS-Image Base, budynki v1 final, 1024

**Pliki LoRA (wszystkie zapisane kroki 250-2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-1024)**

- Trening: MOSS-Image Base (bf16), zbior [`budynki/zbiory/v1-final/train_1024`](../../../zbiory/v1-final/train_1024/), rank 16, lr 1e-4, 2000 krokow, RunPod L40 48 GB (2026-10-21).
- Licencja modelu bazowego: **Apache 2.0**.
- Konfiguracja: `config_ai-toolkit.yaml`.
- Od kroku 1000 fronty, plaskie dachy, magenta; skala zmienia sie miedzy krokami. Najlepiej uzywac na MOSS-Image SFT.

## Podglady
`podglady/kroki_0-2000.png`: 10 budynkow spoza zbioru (prompty: [`budynki/testy/prompty_v1.json`](../../../testy/prompty_v1.json)), kroki 0 (bez LoRA), 500, 1000, 1500, 2000. Sample ai-toolkit z treningu.
