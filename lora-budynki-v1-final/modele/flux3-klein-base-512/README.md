# LoRA: FLUX 3 Image Klein, budynki v1 final, 512

Wytrenowana na **FLUX 3 Image Klein base** (int8 convrot, koder Qwen3-VL-4B fp8), zbiór `../../train_512` (72 budynki), ai-toolkit (moduł `flux3`), rank 16, lr 1e-4, 2000 kroków, 47 min na RTX 3080 10 GB (2026-10-21).

**Licencja modelu bazowego: FLUX Kommunity** (darmowa także komercyjnie przy przychodzie poniżej 5 mln USD, z warunkami Black Forest Labs). Inne nasze LoRA (Z-Image, MOSS) są na modelach Apache 2.0.

| plik | krok |
|---|---|
| `swiat2d_flux3_base_budynki_v1final_512_000002000.safetensors` | 2000 |

## Użycie (ComfyUI)
- **Zalecane: na wersji destylowanej** `flux3-image-klein-int8-convrot.safetensors` (choć LoRA była trenowana na base, działa też na destylacie): LoraLoaderModelOnly z siłą 1.0, CLIPLoader `qwen3vl_4b_int8_convrot.safetensors` typu `flux3`, VAE `flux2-vae`, EmptyFlux2LatentImage 512×512, KSampler er_sde/simple, 15 kroków, cfg 1.
- Na base (`flux3-image-klein-base-int8-convrot`) przy 15 krokach wyniki są nierówne. Podgląd z treningu liczył się na 50 krokach z guidance 3.5.
- Prompt według schematu opisów zbioru (`swiat2d style, enterable building, ...`). ComfyUI wczytuje tę LoRA bez ostrzeżeń.

## Wyniki (podglady/)
- `trening_krok2000_vs_inne.png`: podgląd z treningu (JPG z ai-toolkit) obok Z-Image i MOSS.
- `comfyui_zimage_vs_flux3_base_i_destyl.png`: PNG z ComfyUI, 2 seedy. Na destylacie: front, kanoniczne drzwi, równa skala. Na base: nierówno.
- `wykrywanie_drzwi.png`: czy da się wykryć nasze drzwi do podmiany. Destylat 4/4, ale drzwi są 1,24–1,54 raza większe od szablonu.

Prompt budki z lodami zawiera zaprzeczenie („no visible door”), więc ten test nie jest miarodajny.
