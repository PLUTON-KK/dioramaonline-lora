# LoRA: Krea 2 swiat2d budynki (Krea 2 Raw), budynki v1 final, 512

**Pliki LoRA (wszystkie zapisane kroki 250-2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki-v1-final/krea2-raw-512)**

- Trening: Krea 2 Raw (bf16), zbior `../../train_512`, rank 16, lr 1e-4, 2000 krokow, RunPod RTX A6000 48 GB, ok. 1 h treningu (2026-10-21).
- Licencja modelu bazowego: **Krea 2 Community License (komercyjnie tylko przy przychodzie firmy < 1 mln USD/rok; `LICENSE.pdf`, `NOTICE.txt`)**.
- Konfiguracja: `config_ai-toolkit.yaml`.
- Juz bez LoRA (krok 0) robi fronty i magente, ale wpisuje slowa z promptu w obraz; z LoRA od kroku 1000 bez napisow. Krea zaleca uzywac LoRA z Raw na Krea 2 Turbo.

## Podglady
`podglady/kroki_0-2000.png`: 10 budynkow spoza zbioru (prompty: `../../../lora-budynki-v2/narzedzia/prompty_podglad_10_v1.json`), kroki 0 (bez LoRA), 500, 1000, 1500, 2000. Sample ai-toolkit z treningu.
