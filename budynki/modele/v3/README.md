# LoRA budynki v3 (trening 2026-10-22)

Zbiór: [`../../zbiory/v3-final/`](../../zbiory/v3-final/) – 88 obiektów (58 z v2 + 30 nowych), tylko 512 px.
Stan: **w treningu** (RunPod). Pliki LoRA trafią na Hugging Face `budynki/v3/<model>/` po zakończeniu; wyniki tutaj i w `../../porownania/`.

## Trening

ai-toolkit (ostris), 512 px, bf16 bez kwantyzacji (`low_vram: false`), rank 16, alpha 16, lr 1e-4, adamw8bit, batch 1, zapis i podgląd **co 250 kroków**, krok 0 = model bez LoRA. Słowo wyzwalające: `swiat2d style`. Każdy model na osobnej maszynie, równolegle.

| model bazowy | kroki | karta (RunPod) | dlaczego ta karta | do użycia też na |
|---|---|---|---|---|
| Z-Image Turbo (+ adapter ostris v2) | **3000** | RTX A5000 24 GB | model ok. 6B (12 GB) + koder Qwen3-4B mieszczą się w 24 GB | – |
| FLUX 3 Image Klein base | 2000 | RTX A5000 24 GB | ok. 5,8B (12 GB) + koder Qwen3-VL-4B | FLUX 3 Klein destylat |
| MOSS-Image Base | 2000 | A40 48 GB | duży koder Qwen3.5-9B (ok. 18 GB) + model ok. 5,4B | MOSS-Image SFT |
| Krea 2 Raw | 2000 | RTX A6000 48 GB | sam model ok. 13,5B (27 GB) | Krea 2 Turbo |

Zasada doboru: najmniejsza karta, na której model i koder tekstu mieszczą się w VRAM bez zrzucania do RAM. A6000 48 GB kosztuje prawie tyle co RTX 4090 24 GB, więc większa karta tam, gdzie potrzebna, nie podnosi kosztu.

Konfiguracje: [`konfiguracje/`](konfiguracje/) (`swiat2d_<model>_budynki_v3_512.yaml`, generator [`zbuduj_v3.py`](konfiguracje/zbuduj_v3.py)).
Zabezpieczenie: skrypt sterujący co ok. 2 min pobiera z poda każdy nowy checkpoint i podglądy na dysk lokalny (awaria poda nie traci zapisanych kroków). Pody mają tylko token HF do odczytu.

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

## Plan po treningu
- Siatka kroków dla każdego modelu (wiersz = krok, kolumna = prompt): [`konfiguracje/arkusz_krokow_v3.py`](konfiguracje/arkusz_krokow_v3.py).
- Końcowe LoRA z Krea 2 Raw i FLUX 3 Klein base uruchomione lokalnie (RTX 3080) na Krea 2 Turbo int8 i FLUX 3 Klein destylat: [`konfiguracje/v3_lzejsze.py`](konfiguracje/v3_lzejsze.py).
- Jeden arkusz zbiorczy wszystkich modeli.
