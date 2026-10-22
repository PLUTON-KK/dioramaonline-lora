# LoRA: MOSS-Image, budynki v1 final, 512

**Plik LoRA (krok końcowy 2000): [Hugging Face](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-512)**

Wytrenowana na **MOSS-Image Base** (int8 convrot), zbior [`budynki/zbiory/v1-final/train_512`](../../../zbiory/v1-final/train_512/) (72 budynki), ai-toolkit, rank 16, lr 1e-4, 2000 krokow, 48 min na RTX 3080 10 GB (2026-10-20).

| plik | krok | zalecane uzycie |
|---|---|---|
| `swiat2d_moss_base_budynki_v1final_512_000002000.safetensors` | 2000 | **na MOSS-Image SFT** - najlepszy wynik: prosty front, prostokatne dachy, dobra skala, duzo detali |

## Uzycie (ComfyUI)
UNETLoader `moss_image_sft_int8_convrot.safetensors` -> LoraLoaderModelOnly sila 1.0; CLIPLoader `qwen3.5_9b_int8_convrot.safetensors` typ `moss_image`; VAE `flux2-vae`; KSampler euler/simple, 30 krokow, cfg 4, 512x512.
Prompt wg schematu opisow zbioru (`swiat2d style, enterable building, ...`). ComfyUI wczytuje te LoRA bez ostrzezen o kluczach.

Krok 1500 (lepszy na MOSS-Image Base) usuniety - uzywamy tylko SFT z krokiem 2000.

## Podglady
`podglady/`: porownanie z Z-Image (JPG z treningu), SFT bez LoRA vs z LoRA, SFT z LoRA 1500 vs 2000 (PNG z ComfyUI).
Prompt budki z lodami zawiera zaprzeczenie ("no visible door") - ten test nie jest miarodajny.
