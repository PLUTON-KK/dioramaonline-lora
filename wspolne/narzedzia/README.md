# Wspólne narzędzia

Skrypty do składania zestawień. Ścieżki w środku są lokalne (E:/ai/...) – do uruchomienia u siebie trzeba je zmienić.

| skrypt | co robi |
|---|---|
| `arkusz_podgladow.py` | arkusz jednej LoRA: wiersz = krok treningu (0, 500, …, 2000), kolumna = budynek testowy, nagłówek z nazwą modelu |
| `zestawienie_v1.py` | tabela wszystkich LoRA: wiersz = model + LoRA + rozdzielczość, kolumna = budynek, czas na RTX 3080 |
| `wytnij_i_zestaw.py` | wycina budynki z obrazów modeli zewnętrznych (tło magenta) i składa tabelę jak dla LoRA |
| `zestawienie_paski_zewnetrzne.py` | oryginalne paski modeli zewnętrznych obok załączonych wzorów |
| `ranking_artefakt.py` + `ranking_szablon.html` | strona oceny dobre / średnie / słabe (zakładki: zestawy LoRA × prompty), oceny w bazie strony |
| `v2_lzejsze.py` | LoRA v2 na lżejszych wersjach modeli (MOSS SFT, destylaty FLUX, Krea 2 Turbo int8) w ComfyUI na RTX 3080 |
| `ranking_v2_vs_v1.py` | punkty LoRA v2 vs v1 na tych samych promptach, per model i per budynek |
| `v2_do_repo.py` | zestawienie v2 z ramkami ocen, `oceny.csv` i tabele do README |
| `elo_artefakt.py` + `elo_szablon.html` | strona pojedynków (dwa obrazy tego samego budynku, ukryte nazwy) z rankingiem Bradley-Terry |
| `elo_analiza.py` | analiza głosów: liczba porównań, zgodność z ocenami, przedziały niepewności (bootstrap) |
| `arkusz_krea_latarnia_szklarnia.py` | wszystkie warianty latarni i szklarni z Krea 2 Turbo na jednym arkuszu |
| `drzwi_krea.py` + `drzwi_krea_zoom.py` | dopasowanie kanonicznych drzwi we wszystkich budynkach wejściowych Krea 2 Turbo + powiększenia do ręcznej weryfikacji |
