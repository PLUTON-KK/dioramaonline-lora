# Budynki: porównania

Wszystkie porównania używają [zestawu testowego](../testy/) (10 budynków spoza zbioru). Każde porównanie to osobny folder z datą: zestawienie (PNG) + README z legendą i uwagami. Rankingi pochodzą z ocen właściciela projektu (dobre / średnie / słabe dla każdego obrazu, a od 2026-10-21 także pojedynki parami); README opisują tylko, jak obrazy powstały i co wynika z ocen.

| porównanie | co pokazuje |
|---|---|
| [`2026-10-21_lora-v1_prompty-v1/`](2026-10-21_lora-v1_prompty-v1/) | wszystkie LoRA v1 (19 wierszy: model × rozdzielczość, także LoRA na lżejszych wersjach modeli do RTX 3080) na promptach v1: ranking z ocen, najlepsze modele per budynek, czas na RTX 3080, test podmiany drzwi |
| [`2026-10-21_modele-zewnetrzne/`](2026-10-21_modele-zewnetrzne/) | ChatGPT, Gemini, Gemini Banana: wzór stylu + prompt paskowy, v1 i v2, budynki wycięte do ramek |
| [`2026-10-21_lora-v1_prompty-v2/`](2026-10-21_lora-v1_prompty-v2/) | te same LoRA v1 na promptach v2 (17 wierszy): ranking z ocen, zmiana względem promptów v1 |
| [`2026-10-21_uzdatnione-prompty/`](2026-10-21_uzdatnione-prompty/) | prompty z opisem materiałów i hasłem „realistic shading” / „semi-realistic” na 5 modelach, siła LoRA 1.0–1.5, Krea 2 Turbo: latarnia i szklarnia |
| [`2026-10-21_lora-v2_prompty-v2/`](2026-10-21_lora-v2_prompty-v2/) | LoRA v2-final na promptach v2 (11 wierszy): ranking z ocen, porównanie z v1 |
| [`2026-10-21_pojedynki/`](2026-10-21_pojedynki/) | ślepe pojedynki dobrych obrazów v1/v1 vs v2/v2, ranking Bradley-Terry |
| [`2026-10-21_drzwi-krea2-turbo/`](2026-10-21_drzwi-krea2-turbo/) | czy w budynkach wejściowych z Krea 2 Turbo da się podmienić drzwi na kanoniczne (52 obrazy, sprawdzone ręcznie) |
| `…_lora-vs-zewnetrzne/` | *(w przygotowaniu)* najlepsze nasze LoRA obok modeli zewnętrznych w jednej tabeli |

## Jak czytać tabele
- **kolumna** = budynek z zestawu testowego, **wiersz** = model (+ LoRA, rozdzielczość, wersja promptów),
- każdy obraz jest dopasowany do swojej ramki osobno – wielkości między ramkami nie są porównywalne (skalę gry widać w samych podglądach treningu, `../modele/v1/*/podglady/`),
- **modele zewnętrzne vs nasze LoRA:** ChatGPT/Gemini dostają nasz wzór jako obraz i nie są trenowane; nasze LoRA są wytrenowane na zbiorze, działają bez wzoru i lokalnie (część na RTX 3080).
