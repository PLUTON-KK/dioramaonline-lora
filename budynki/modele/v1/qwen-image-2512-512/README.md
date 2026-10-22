# LoRA: Qwen-Image 2512, budynki v1 final, 512

**Plik LoRA (krok końcowy 2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-2512-512)**

- Trening: Qwen-Image 2512 (bf16, bez kwantyzacji), zbior [`budynki/zbiory/v1-final/train_512`](../../../zbiory/v1-final/train_512/), ai-toolkit (arch qwen_image), rank 16, lr 1e-4, 2000 krokow, RunPod A100 SXM 80 GB, ok. 1 h treningu (2026-10-21).
- Konfiguracja: `config_ai-toolkit.yaml`.
- Model bazowy na licencji Apache 2.0. Skala budynkow skacze miedzy krokami (1000: male, 1500: waskie, 2000: najblizej zbioru).

## Podglady
`podglady/kroki_0-2000.png: 10 promptow spoza zbioru, kroki 0 (bez LoRA), 500, 1000, 1500, 2000 (sample ai-toolkit, 25 krokow, guidance 4).`
