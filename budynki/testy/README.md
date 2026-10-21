# Budynki: zestaw testowy

10 budynków **spoza zbioru treningowego**, na których porównujemy wszystkie LoRA i modele zewnętrzne. Model nie widział ich podczas nauki, więc wynik pokazuje, czy nauczył się stylu, a nie zapamiętał obrazków.

| # | budynek | typ | wzór (dla modeli z obrazem wejściowym) |
|---|---|---|---|
| 1 | kwiaciarnia | enterable | `wzor_wejsciowe` |
| 2 | hotel | enterable | `wzor_wejsciowe` |
| 3 | stacja karetek | decorative | `wzor_dekoracyjne` |
| 4 | budka z lodami | decorative | `wzor_dekoracyjne` |
| 5 | dom turkusowy | enterable | `wzor_wejsciowe` |
| 6 | latarnia z domkiem | decorative | `wzor_dekoracyjne` |
| 7 | szklarnia | enterable | `wzor_wejsciowe` |
| 8 | obserwatorium | enterable | `wzor_wejsciowe` |
| 9 | weterynarz | enterable | `wzor_wejsciowe` |
| 10 | kino | enterable | `wzor_wejsciowe` |

## Pliki
| plik | co to |
|---|---|
| [`prompty_v1.json`](prompty_v1.json) | prompty z podglądów treningu v1 (zbiór v1-final) |
| [`prompty_v2.json`](prompty_v2.json) | prompty v2: rozmiar w metrach, drzwi stacji karetek opisane na froncie (zamiast „side door”), budka bez zaprzeczenia – szczegóły w [`ZMIANY_V1_V2.md`](../zbiory/v2-final/ZMIANY_V1_V2.md) |
| [`pasek_wejsciowe_v1.txt`](pasek_wejsciowe_v1.txt), [`_v2`](pasek_wejsciowe_v2.txt) | jeden prompt na 7 budynków z wejściem w jednym obrazku – dla modeli zewnętrznych (ChatGPT, Gemini) |
| [`pasek_dekoracyjne_v1.txt`](pasek_dekoracyjne_v1.txt), [`_v2`](pasek_dekoracyjne_v2.txt) | to samo dla 3 budynków dekoracyjnych |
| [`wzory/wzor_wejsciowe.png`](wzory/wzor_wejsciowe.png) | wzór stylu: 7 budynków z wejściem ze zbioru v1-final, różne dachy, skala ×2 (48 px = 1 m), miarka 2 m |
| [`wzory/wzor_dekoracyjne.png`](wzory/wzor_dekoracyjne.png) | wzór stylu: 7 budynków dekoracyjnych, różne dachy |
| [`wzory/wzor_drzwi.png`](wzory/wzor_drzwi.png) | kanoniczne drzwi wejściowe gry (z miarką) |
| [`wzory/stare/`](wzory/stare/) | pierwsze wzory (wszystkie dachy jednakowe) – tych używał trening Qwen-Image-Edit 2511 v1 |

Modele zewnętrzne dostają: wzór stylu (+ wzór drzwi przy budynkach z wejściem) i prompt paskowy. Nasze LoRA dostają pojedyncze prompty z `prompty_v*.json`, bez wzoru (wyjątek: Qwen-Image-Edit, który ma wzór jako obraz wejściowy).
