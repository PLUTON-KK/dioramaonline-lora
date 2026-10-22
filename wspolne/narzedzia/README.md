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
| `sprawdz_opis.py` | walidator opisów i promptów wg `wspolne/schemat_opisow.json` (obowiązuje od v4) |
| `sprawdz_grafike.py` | walidator grafik bez AI (numpy + OpenCV), kryteria wspólne ze stroną gry: P1–P6 piksele, K1–K4 kamera i dach (heurystyki, SKIP gdy niepewne), D1–D9 drzwi, B1 dekoracyjne, M metadane, P4b fioletowa obwódka po magencie (>5% brzegu = FAIL); wynik PASS / FAIL / SKIP |
| `waliduj_zbior_v3.py` | uruchomienie walidatora na zbiorze budynki v3-final: CSV, podsumowanie, arkusz obiektów do obejrzenia |
| `v4_obrobka.py` | obróbka sprite'ów v4 bez AI: `despill()` usuwa fioletowe zabarwienie brzegów po magencie, `mapuj()` mapuje na paletę 128 w przestrzeni Lab i czyści pojedyncze piksele, `fioletowa_obwodka()` – miara dla walidatora (P4b) |
| `paleta128.py` | generator palety świata 128 (`wspolne/paleta128.json`, `paleta128.png`): 16 ramp materiałów × 8 jasności; opis w `wspolne/KARTA_TECHNICZNA_V4.md` |
