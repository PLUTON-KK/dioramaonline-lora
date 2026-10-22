# LoRA: Qwen-Image-Edit 2511, budynki v1 final, 512

**Plik LoRA (krok końcowy 2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-edit-2511-512)**

- Trening: Qwen-Image-Edit 2511 (bf16), zbior [`budynki/zbiory/v1-final/train_512`](../../../zbiory/v1-final/train_512/) z obrazem kontrolnym = wzor stylu (`wzor_wejsciowe` / `wzor_dekoracyjne`), rank 16, lr 1e-4, 2000 krokow, RunPod A100 80 GB, ok. 2,5 h (2026-10-21).
- Licencja modelu bazowego: **Apache 2.0**.
- Konfiguracja: `config_ai-toolkit.yaml`.
- Model edycji: przy generowaniu podaje sie obraz wejsciowy (tu wzor stylu). Fronty od kroku 500; budynki wypelniaja kadr, czesc elementow kopiuje ze wzoru/zbioru (np. krzyz zamiast lapy u weterynarza na krokach 500-1000).

## Podglady
`podglady/kroki_0-2000.png`: 10 budynkow spoza zbioru (prompty: [`budynki/testy/prompty_v1.json`](../../../testy/prompty_v1.json)), kroki 0 (bez LoRA), 500, 1000, 1500, 2000. Sample ai-toolkit z treningu.
