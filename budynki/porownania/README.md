# Budynki: porównania

Wszystkie porównania używają [zestawu testowego](../testy/) (10 budynków spoza zbioru). Każde porównanie to osobny folder z datą: zestawienie (PNG) + README z legendą i uwagami. Ocena wizualna należy do właściciela projektu; w README są tylko fakty o tym, jak obrazy powstały.

| porównanie | co pokazuje |
|---|---|
| [`2026-10-21_lora-v1_prompty-v1/`](2026-10-21_lora-v1_prompty-v1/) | wszystkie LoRA v1 (20 wierszy: model × rozdzielczość, także LoRA na lżejszych wersjach modeli do RTX 3080) na promptach v1, z czasem generowania na RTX 3080 |
| [`2026-10-21_modele-zewnetrzne/`](2026-10-21_modele-zewnetrzne/) | ChatGPT, Gemini, Gemini Banana: wzór stylu + prompt paskowy, v1 i v2, budynki wycięte do ramek |
| `2026-10-21_lora-v1_prompty-v2/` | *(w przygotowaniu)* te same LoRA v1 na promptach v2 – czy sama poprawka promptów coś zmienia |
| `…_lora-vs-zewnetrzne/` | *(w przygotowaniu)* najlepsze nasze LoRA obok modeli zewnętrznych w jednej tabeli |

## Jak czytać tabele
- **kolumna** = budynek z zestawu testowego, **wiersz** = model (+ LoRA, rozdzielczość, wersja promptów),
- każdy obraz jest dopasowany do swojej ramki osobno – wielkości między ramkami nie są porównywalne (skalę gry widać w samych podglądach treningu, `../modele/v1/*/podglady/`),
- **modele zewnętrzne vs nasze LoRA:** ChatGPT/Gemini dostają nasz wzór jako obraz i nie są trenowane; nasze LoRA są wytrenowane na zbiorze, działają bez wzoru i lokalnie (część na RTX 3080).
