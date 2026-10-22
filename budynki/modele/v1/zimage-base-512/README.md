# LoRA: Z-Image Base, budynki v1 final, 512

**Plik LoRA (krok końcowy 2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-base-512)**

- Trening: Z-Image Base (bf16), zbior [`budynki/zbiory/v1-final/train_512`](../../../zbiory/v1-final/train_512/), ai-toolkit, rank 16, lr 1e-4, 2000 krokow, RTX 3080 (2026-10-21).
- Konfiguracja: `config_ai-toolkit.yaml`.
- Na Z-Image Turbo ta LoRA nie dziala (porownanie Base vs Turbo w devlogu). Uzywac na Z-Image Base.

## Podglady
`podglady/zimagebase_kroki.png: podglady z treningu po krokach.`
