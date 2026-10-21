# dioramaonline-lora

Zbiory treningowe LoRA i gotowe LoRA do gry Świat 2D (dioramaonline), pixel art.

## 📓 [Devlog: jak to powstaje](devlog/00-prolog.md)
Skąd ten projekt, co testowaliśmy, co nie wyszło i dlaczego. Zaczyna się od [prologu](devlog/00-prolog.md), a [tu jest spis wpisów](devlog/README.md).

> Sorry, że po polsku, ale mi tak łatwiej. Jesteśmy w dobie AI (serio!), więc można sobie automatycznie przetłumaczyć. - q3ok
>
> *Sorry it's in Polish, it's just easier for me. We live in the age of AI (seriously!), so feel free to auto-translate it.*

## Jak to jest poukładane

Repo dzielimy **po tematach** (budynki, potem natura, auta, produkty…). Każdy temat ma ten sam układ:

```
<temat>/
  README.md     ← stan tematu: aktualny zbiór, LoRA, ostatnie porównania
  zbiory/       ← zbiory treningowe (v1-final, v2, …): train_512/, train_1024/, sprites/, opisy
  modele/       ← opisy wytrenowanych LoRA (konfiguracja, podglądy kroków); same pliki LoRA są na Hugging Face
  testy/        ← zestaw testowy tematu: budynki spoza zbioru, prompty, wzory stylu
  porownania/   ← zestawienia wyników: nasze LoRA i modele zewnętrzne (ChatGPT, Gemini) na tym samym zestawie testowym
wspolne/        ← rzeczy wspólne dla tematów (skrypty do zestawień)
devlog/         ← dziennik projektu
```

Pliki LoRA (`.safetensors`) leżą na Hugging Face: **[q3ok/dioramaonline-lora-models](https://huggingface.co/q3ok/dioramaonline-lora-models)**, w tym samym podziale (`budynki/v1/<model>/`).

## Tematy

| temat | zbiory | LoRA | porównania | status |
|---|---|---|---|---|
| [**budynki**](budynki/) | [v1-final](budynki/zbiory/v1-final/) (72, zamrożony), [v2-final](budynki/zbiory/v2-final/) (te same 72, ciasny kadr, zamrożony) | [11 LoRA v1](budynki/modele/v1/) (8 modeli bazowych, 512/1024) | [budynki/porownania](budynki/porownania/) | v1 wytrenowane, v2 w treningu |
| natura | – | – | – | plan |
| produkty (zdjęcie produktu → diorama) | – | – | – | później, modele z edycją obrazu (tabela niżej) |

## Modele: generowanie czy też edycja obrazu

Ściąga, którym modelem da się tylko generować z tekstu, a którym także przerabiać istniejący obraz (np. zdjęcie produktu ze sklepu → wersja do dioramy). Stan: 2026-10-21, wg kart modeli na Hugging Face.

| model | tekst → obraz | edycja / obraz wejściowy | lokalnie (RTX 3080, 10 GB) | licencja | nasza LoRA budynków |
|---|---|---|---|---|---|
| Z-Image Turbo | ✅ | ❌ (Tongyi zapowiada osobne Z-Image-Edit i Z-Image-Omni-Base, jeszcze niewydane) | ✅ bf16 | Apache 2.0 | v1 512, 1024 |
| Z-Image Base | ✅ | ❌ | ✅ bf16 | Apache 2.0 | v1 512 |
| MOSS-Image Base / SFT | ✅ | ❌ | ✅ int8 | Apache 2.0 | v1 512, 1024 (uczona na Base) |
| FLUX 3 Image Klein (base i destylat) | ✅ | ✅ edycja i kilka obrazów referencyjnych | ✅ int8 | FLUX Kommunity | v1 512, 1024 (uczona na base) |
| FLUX.2 Klein 4B (base i destylat) | ✅ | ✅ edycja i kilka obrazów referencyjnych | ✅ bf16 | Apache 2.0 | v1 512 (uczona na base) |
| Qwen-Image 2512 | ✅ | ❌ (do edycji jest osobny Qwen-Image-Edit) | ⚠️ tylko GGUF Q4 (bf16 ~41 GB za duży) | Apache 2.0 | v1 512 |
| Qwen-Image-Edit 2511 | ✅ | ✅ edycja instrukcją, do 3 obrazów wejściowych | ⚠️ tylko GGUF Q4 | Apache 2.0 | v1 512 (uczona z wzorem stylu jako obrazem wejściowym) |
| Krea 2 Raw / Turbo | ✅ | ⚠️ tylko referencja stylu przez LoRA `krea2_style_reference` (bez edycji treści) | ⚠️ Turbo int8; Raw za duży | Krea 2 Community (komercyjnie < 1 mln USD/rok) | v1 512 (uczona na Raw) |
| PixelDiT 1300M | ✅ | ❌ | ✅ bf16 | – | brak |
| Krea 3, Nano Banana, Imagen, ChatGPT (obrazy) | ✅ | ✅ | ❌ tylko API, wag nie ma | zamknięte | nie da się (brak wag) |

Do przerabiania zdjęć produktów na styl dioramy kandydaci to modele z edycją: **Qwen-Image-Edit 2511**, **FLUX 3 Klein**, **FLUX.2 Klein 4B** (lokalnie), z naszą LoRA budynków albo przyszłą LoRA przedmiotów.
