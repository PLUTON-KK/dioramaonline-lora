# LoRA budynki v1-final

Zbiór: [`../../zbiory/v1-final/`](../../zbiory/v1-final/) (72 budynki). 11 LoRA na 8 modelach bazowych, 2000 kroków, rank 16. Na Hugging Face jeden plik na LoRA (krok końcowy 2000).
W każdym folderze: README (jak uczona, jak używać w ComfyUI, licencja), `config_ai-toolkit.yaml`, `podglady/`.

| model | rozdz. | trening | opis i podglądy | pliki |
|---|---|---|---|---|
| Z-Image Turbo | 512 | RTX 3080 | [`zimage-turbo-512`](zimage-turbo-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-turbo-512) |
| Z-Image Turbo | 1024 | RunPod L40 | [`zimage-turbo-1024`](zimage-turbo-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-turbo-1024) |
| Z-Image Base (nie działa na Turbo) | 512 | RTX 3080 | [`zimage-base-512`](zimage-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/zimage-base-512) |
| MOSS-Image Base (najlepsza na SFT) | 512 | RTX 3080 | [`moss-image-base-512`](moss-image-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-512) |
| MOSS-Image Base (najlepsza na SFT) | 1024 | RunPod L40 | [`moss-image-base-1024`](moss-image-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/moss-image-base-1024) |
| FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 512 | RTX 3080 | [`flux3-klein-base-512`](flux3-klein-base-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux3-klein-base-512) |
| FLUX 3 Image Klein base (najlepsza na destylacie; FLUX Kommunity) | 1024 | RunPod A40 | [`flux3-klein-base-1024`](flux3-klein-base-1024/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux3-klein-base-1024) |
| FLUX.2 Klein 4B | 512 | RTX 3080 | [`flux2-klein-4b-512`](flux2-klein-4b-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/flux2-klein-4b-512) |
| Qwen-Image 2512 | 512 | RunPod A100 | [`qwen-image-2512-512`](qwen-image-2512-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-2512-512) |
| Qwen-Image-Edit 2511 (z obrazem wzoru) | 512 | RunPod A100 | [`qwen-image-edit-2511-512`](qwen-image-edit-2511-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/qwen-image-edit-2511-512) |
| Krea 2 Raw (do użycia na Krea 2 Turbo; Krea 2 Community License) | 512 | RunPod A6000 | [`krea2-raw-512`](krea2-raw-512/) | [HF](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v1/krea2-raw-512) |
