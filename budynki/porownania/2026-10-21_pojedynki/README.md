# Pojedynki obrazów: v1/v1 vs v2/v2 (2026-10-21)

Druga metoda oceny, obok dobre / średnie / słabe. Ocena punktowa dobrze odsiewa słabe obrazy, ale nie mówi, który z dwóch dobrych jest lepszy.

## Jak
- Strona pokazuje dwa obrazy **tego samego budynku** z dwóch różnych wierszy (model + LoRA). Nazwy modeli ukryte do momentu wyboru.
- Odpowiedzi: lewy lepszy / prawy lepszy / remis / oba słabe.
- Pula: tylko obrazy ocenione wcześniej jako **dobre**, z LoRA v1 na promptach v1 i LoRA v2 na promptach v2 – 90 obrazów z 25 wierszy. LoRA v1 na promptach v2 pominięta (w zbiorze v1 nie było rozmiarów w metrach). Bez Qwen-Edit 2511 i Qwen Q4.
- Wynik: model **Bradley-Terry** (każdy wiersz ma „siłę” p, szansa wygranej A z B = pA / (pA + pB), dopasowane do wszystkich głosów naraz, niezależnie od kolejności). Remis = pół wygranej dla obu, „oba słabe” nie wchodzi do wyniku. Skala jak Elo (1500 = przeciętny), ± = 90% niepewności.

Pierwsza wersja (Elo, 430 obrazów z wszystkich zestawów, także słabych) nie dała wyniku: 176 głosów, każdy obraz średnio 0,8 porównania, 48% głosów „oba słabe”, wszystkie wiersze w przedziale 1484–1513. Wniosek: przy losowych parach pulę trzeba najpierw zawęzić do obrazów, które w ogóle wchodzą w grę.

## Wynik (195 głosów w puli)

| # | model | LoRA · prompty | wynik | ± | pojedynki | wygr. / przegr. / remis | oba słabe |
|---|---|---|---|---|---|---|---|
| 1 | Krea 2 Raw 512 | v2 · v2 | 1834 | 228 | 10 | 8 / 1 / 1 | 0 |
| 2 | Krea 2 Turbo int8 512 | v1 · v1 | 1722 | 160 | 16 | 9 / 2 / 5 | 1 |
| 3 | FLUX 3 Klein base 512 | v2 · v2 | 1707 | 130 | 27 | 21 / 6 / 0 | 10 |
| 4 | MOSS-Image Base 512 | v2 · v2 | 1700 | 222 | 8 | 5 / 1 / 2 | 0 |
| 5 | Qwen-Image 2512 512 | v1 · v1 | 1665 | 264 | 5 | 3 / 1 / 1 | 3 |
| 6 | FLUX.2 Klein 4B destylat 512 | v2 · v2 | 1637 | 167 | 13 | 8 / 5 / 0 | 5 |
| 7 | Krea 2 Raw 512 | v1 · v1 | 1637 | 151 | 20 | 11 / 2 / 7 | 1 |
| 8 | Z-Image Turbo 1024 | v1 · v1 | 1625 | 138 | 19 | 12 / 7 / 0 | 5 |
| 9 | MOSS-Image SFT 1024 | v1 · v1 | 1604 | 136 | 20 | 11 / 8 / 1 | 4 |
| 10 | Qwen-Image 2512 512 | v2 · v2 | 1602 | 339 | 2 | 1 / 1 / 0 | 0 |
| 11 | Krea 2 Turbo int8 512 | v2 · v2 | 1590 | 147 | 18 | 8 / 5 / 5 | 1 |
| 12 | FLUX 3 Klein destylat 512 | v1 · v1 | 1524 | 161 | 14 | 6 / 5 / 3 | 2 |
| 13 | Z-Image Turbo 512 | v1 · v1 | 1507 | 146 | 20 | 8 / 7 / 5 | 2 |
| 14 | FLUX 3 Klein destylat 512 | v2 · v2 | 1475 | 95 | 47 | 14 / 30 / 3 | 2 |
| 15 | MOSS-Image SFT 512 | v1 · v1 | 1463 | 156 | 15 | 6 / 9 / 0 | 1 |
| 16 | FLUX 3 Klein base 512 | v1 · v1 | 1458 | 170 | 12 | 5 / 6 / 1 | 1 |
| 17 | FLUX.2 Klein 4B 512 | v1 · v1 | 1445 | 286 | 4 | 2 / 2 / 0 | 0 |
| 18 | FLUX.2 Klein 4B 512 | v2 · v2 | 1438 | 352 | 2 | 0 / 1 / 1 | 0 |
| 19 | Z-Image Turbo 512 | v2 · v2 | 1408 | 141 | 20 | 6 / 10 / 4 | 0 |
| 20 | MOSS-Image SFT 512 | v2 · v2 | 1367 | 276 | 5 | 1 / 4 / 0 | 3 |
| 21 | Z-Image Base 512 | v1 · v1 | 1339 | 181 | 13 | 2 / 9 / 2 | 1 |
| 22 | FLUX.2 Klein 4B destylat 512 | v1 · v1 | 1337 | 453 | 2 | 0 / 2 / 0 | 3 |
| 23 | MOSS-Image Base 1024 | v1 · v1 | 1272 | 185 | 15 | 2 / 12 / 1 | 3 |
| 24 | FLUX 3 Klein destylat 1024 | v1 · v1 | 1151 | 428 | 4 | 0 / 4 / 0 | 0 |
| 25 | Z-Image Base 512 | v2 · v2 | 992 | 417 | 9 | 0 / 9 / 0 | 2 |

Głosy: [`glosy.csv`](glosy.csv) (wszystkie 360, także z pierwszej wersji; wiersz = `<zestaw>__<id wiersza>`, budynek = numer 0–9 z zestawu testowego).

## Co z tego wynika
- Niepewność jest duża (±95–450), pewne są tylko grupy, nie kolejność.
- **Krea 2** (Raw i Turbo, v1 i v2) jest w czołówce niezależnie od LoRA – najpewniejszy sygnał.
- **v1 vs v2 bezpośrednio:** 29 : 28 wygranych (4 remisy, 9 „oba słabe”). Dobre obrazy z obu LoRA są tak samo dobre; v2 nie poprawiła wyglądu najlepszych obrazów (zysk v2 to skala i drzwi, których pojedynki nie mierzą).
- **Z-Image Turbo** w ocenie punktowej w czołówce, w pojedynkach w środku – często daje obraz „wystarczająco dobry”, ale przegrywa bezpośrednio z Krea.
- **Z-Image Base** i **MOSS Base 1024** na dole.
- Błąd doboru par: latarnia miała tylko 2 dobre obrazy (oba FLUX 3 v2) i trafiła 19 razy – destylat przegrywał tam z base, więc FLUX 3 destylat v2 jest zaniżony.
