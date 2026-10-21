# LoRA v1 na promptach v1 (2026-10-21)

![zestawienie](zestawienie.png)

- **Wiersz:** model bazowy + LoRA budynki v1 + rozdzielczość; opis modelu: [`../../modele/v1/`](../../modele/v1/).
- **Obrazy:** podglądy z treningu (ai-toolkit, krok 2000, seed 42+i) albo – gdzie podgląd nie istniał – wygenerowane w ComfyUI na RTX 3080 tymi samymi promptami i seedem.
- **Wiersze „na lżejszej wersji”:** LoRA uczona na jednym modelu użyta na wersji, która mieści się na RTX 3080 (MOSS SFT, FLUX 3 / FLUX.2 Klein destylat, Krea 2 Turbo int8, Qwen GGUF Q4).
- **Czas RTX 3080:** jeden obraz po wczytaniu modelu (ComfyUI, ten sam sampler i liczba kroków co w podglądzie). „Za duży” = model w pełnej precyzji nie zmieści się w 10 GB VRAM + 32 GB RAM.
- **Prompty:** [`../../testy/prompty_v1.json`](../../testy/prompty_v1.json). Uwaga: prompt stacji karetek ma „a small side door” (prawdopodobnie ciągnie do widoku z boku), budka z lodami ma zaprzeczenie „with no visible door” – poprawione w promptach v2.
