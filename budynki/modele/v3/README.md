# LoRA budynki v3 i v3-3000 (trening 2026-10-22)

Zbiór: [`../../zbiory/v3-final/`](../../zbiory/v3-final/) – 88 obiektów (58 z v2 + 30 nowych), tylko 512 px.
Stan: **wytrenowane**. Na Hugging Face jest jeden plik na LoRA (krok końcowy). v3-3000 to ten sam zbiór i te same ustawienia, tylko 3000 kroków.

| LoRA | model bazowy (trening) | używamy na | kroki | HF |
|---|---|---|---|---|
| v3 | Z-Image Turbo (+ adapter ostris v2) | Z-Image Turbo | 3000 | [v3/zimage-turbo-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3/zimage-turbo-512) |
| v3 | FLUX 3 Image Klein base | FLUX 3 Klein destylat | 2000 | [v3/flux3-klein-base-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3/flux3-klein-base-512) |
| v3 | MOSS-Image Base | MOSS-Image SFT | 2000 | [v3/moss-image-base-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3/moss-image-base-512) |
| v3 | Krea 2 Raw | Krea 2 Turbo | 2000 | [v3/krea2-raw-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3/krea2-raw-512) |
| v3-3000 | FLUX 3 Image Klein base | FLUX 3 Klein destylat | 3000 | [v3-3000/flux3-klein-base-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3-3000/flux3-klein-base-512) |
| v3-3000 | MOSS-Image Base | MOSS-Image SFT | 3000 | [v3-3000/moss-image-base-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3-3000/moss-image-base-512) |
| v3-3000 | Krea 2 Raw | Krea 2 Turbo | 3000 | [v3-3000/krea2-raw-512](https://huggingface.co/q3ok/dioramaonline-lora-models/tree/main/budynki/v3-3000/krea2-raw-512) |

Licencje i ustawienia ComfyUI (sampler, kroki, CFG) są takie jak dla tych samych modeli w v1: [`../v1/`](../v1/).

## Wyniki

Końcowy arkusz na modelach, których używamy do generowania (Z-Image Turbo z v3; FLUX 3 Klein destylat, MOSS-Image SFT i Krea 2 Turbo z v3-3000), prompt zwykły i uzdatniony K, 27 obiektów spoza zbioru:
[część 1](podglady/arkusz_koncowy_1.webp) · [część 2](podglady/arkusz_koncowy_2.webp) · [część 3](podglady/arkusz_koncowy_3.webp) (skrypt `finalny_v3_3000.py`).

Ocena właściciela: styl v3 przestał się podobać. v4 zmienia rzut wierzchu (½ głębi) i paletę (128 kolorów): [`../../../wspolne/KARTA_TECHNICZNA_V4.md`](../../../wspolne/KARTA_TECHNICZNA_V4.md) i [`../../../wspolne/SCHEMAT_OPISOW.md`](../../../wspolne/SCHEMAT_OPISOW.md).
Krea 2 Turbo z LoRA v3-3000 służy teraz do przerysowania dachów budynków ze zbioru na rzut ½ (inpainting tylko dachu).

## Trening

ai-toolkit (ostris), 512 px, bf16 bez kwantyzacji (`low_vram: false`), rank 16, alpha 16, lr 1e-4, adamw8bit, batch 1, podgląd co 250 kroków, krok 0 = model bez LoRA. Słowo wyzwalające: `swiat2d style`. Każdy model na osobnej maszynie, równolegle.

| model bazowy | kroki v3 | karta (RunPod) | dlaczego ta karta | do użycia też na |
|---|---|---|---|---|
| Z-Image Turbo (+ adapter ostris v2) | **3000** | RTX A5000 24 GB | model ok. 6B (12 GB) + koder Qwen3-4B mieszczą się w 24 GB | – |
| FLUX 3 Image Klein base | 2000 | RTX A5000 24 GB | ok. 5,8B (12 GB) + koder Qwen3-VL-4B | FLUX 3 Klein destylat |
| MOSS-Image Base | 2000 | A40 48 GB | duży koder Qwen3.5-9B (ok. 18 GB) + model ok. 5,4B | MOSS-Image SFT |
| Krea 2 Raw | 2000 | RTX A6000 48 GB | sam model ok. 13,5B (27 GB) | Krea 2 Turbo |

v3-3000 (FLUX 3, MOSS, Krea): te same karty, 3000 kroków.

Zasada doboru: najmniejsza karta, na której model i koder tekstu mieszczą się w VRAM bez zrzucania do RAM. A6000 48 GB kosztuje prawie tyle co RTX 4090 24 GB, więc większa karta tam, gdzie potrzebna, nie podnosi kosztu.

Konfiguracje: [`konfiguracje/`](konfiguracje/) (`swiat2d_<model>_budynki_v3_512.yaml`, generator [`zbuduj_v3.py`](konfiguracje/zbuduj_v3.py)).
Pody miały tylko token HF do odczytu.

## Podglądy (prompty testowe v3)

7 obiektów spoza zbioru v3, każdy zwykły i uzdatniony K („Semi-realistic pixel art game sprite” + opis materiałów), seed 42+i: [`../../testy/prompty_v3_nowe_obiekty.json`](../../testy/prompty_v3_nowe_obiekty.json), źródło: [`konfiguracje/prompty_test_v3.py`](konfiguracje/prompty_test_v3.py).

| obiekt | typ | rozmiar w prompcie | kamera |
|---|---|---|---|
| pawilon szklarniowy | wejściowy | 16 × 9 m | front, góra lekko z góry (dach dowolny) |
| średniowieczny zamek | dekoracyjny | 20 × 18 m | front, góra lekko z góry + okrągłe bryły |
| basen odkryty | obiekt | 18 × 5 m | front, góra lekko z góry |
| przystanek tramwajowy | obiekt | 9 × 4 m | front, góra lekko z góry |
| gospodarstwo rolne | dekoracyjny | 22 × 10 m | front, góra lekko z góry |
| gospodarstwo hodowlane | dekoracyjny | 24 × 10 m | front, góra lekko z góry + okrągłe bryły (silos) |
| samochód sedan (lata 2000, test) | obiekt | 5 × 2 m | bok do widza, przodem w prawo, góra lekko z góry |

Zasady promptów: bez zaprzeczeń, płaski dach w kamerze tylko gdy logiczny, bez dymu, parkingów, aut i torów przed obiektami.

