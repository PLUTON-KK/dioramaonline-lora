# Wspólne narzędzia

Skrypty do składania zestawień. Ścieżki w środku są lokalne (E:/ai/...) – do uruchomienia u siebie trzeba je zmienić.

| skrypt | co robi |
|---|---|
| `arkusz_podgladow.py` | arkusz jednej LoRA: wiersz = krok treningu (0, 500, …, 2000), kolumna = budynek testowy, nagłówek z nazwą modelu |
| `zestawienie_v1.py` | tabela wszystkich LoRA: wiersz = model + LoRA + rozdzielczość, kolumna = budynek, czas na RTX 3080 |
| `wytnij_i_zestaw.py` | wycina budynki z obrazów modeli zewnętrznych (tło magenta) i składa tabelę jak dla LoRA |
| `zestawienie_paski_zewnetrzne.py` | oryginalne paski modeli zewnętrznych obok załączonych wzorów |
