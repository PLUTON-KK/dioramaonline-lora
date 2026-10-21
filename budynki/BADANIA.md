# Budynki: badania w skrócie (stan 2026-10-21)

Ku pamięci: co sprawdzaliśmy, jak i co wyszło. Szczegóły, obrazy i oceny są w podlinkowanych folderach.

## Cel
LoRA, która rysuje budynki do dioramy w stylu gry: pixel art, rzut RPG 3/4 (front prosto, płaski prostokątny dach widoczny z góry, bez perspektywy), kanoniczne drzwi, tło magenta. Najlepiej model szybki, uczony i uruchamiany lokalnie (RTX 3080, 10 GB).

## Jak badaliśmy

**Zbiory** (oba zamrożone, obrazy z ChatGPT + nasza obróbka):
- [v1-final](zbiory/v1-final/): 72 budynki w skali gry (24 px = 1 m), budynki zajmują 100–200 px z 512.
- [v2-final](zbiory/v2-final/): te same 72, ciasny kadr (88% płótna), rozmiar w metrach w opisie, poprawione „side door” i zaprzeczenie w budce. Skalę gry przywraca skrypt. Lista zmian: [ZMIANY_V1_V2.md](zbiory/v2-final/ZMIANY_V1_V2.md).

**Trening:** ai-toolkit, rank 16, lr 1e-4, 2000 kroków, bf16. Lokalnie (RTX 3080) lub RunPod (karty 48 GB, Qwen na A100), po jednej maszynie na model, równolegle.
- v1: 11 LoRA na 8 modelach (512 i część 1024).
- v2: 7 LoRA (512).

**Zestaw testowy:** [10 budynków spoza zbioru](testy/) (kwiaciarnia, hotel, stacja karetek, budka z lodami, dom turkusowy, latarnia z domkiem, szklarnia, obserwatorium, weterynarz, kino). Prompty v1 i v2, seed 42+i, krok 2000. LoRA uczona na wersji base działa też na lżejszych wersjach (destylat, SFT, Turbo int8) – te generowane w ComfyUI na RTX 3080.

**Ocena:** zawsze właściciela projektu, na stronie z obrazami.
1. **Dobre / średnie / słabe** dla każdego obrazu → punkty (2/1/0, maks. 20 na wiersz).
2. **Pojedynki** (od 2026-10-21): dwa dobre obrazy tego samego budynku, ukryte nazwy, wybór lepszego → ranking Bradley-Terry z niepewnością.

## Przebieg i wyniki

| # | badanie | wynik | folder |
|---|---|---|---|
| 1 | Modele bez LoRA | Żaden nie trzyma frontu (izometria, dachy dwuspadowe, różowe tło). LoRA konieczna. | [devlog](../devlog/) |
| 2 | LoRA v1, prompty v1 (19 wierszy) | Czołówka po 15 pkt: Z-Image Turbo 512, MOSS SFT 1024, Krea 2 Turbo int8. Krea 2 Raw 14. Qwen Q4 0 (niepasujący GGUF). Latarnia: 0 dobrych na 19 modeli. | [lora-v1_prompty-v1](porownania/2026-10-21_lora-v1_prompty-v1/) |
| 3 | Podmiana drzwi | W 133 obrazach wejściowych: 101 drzwi na miejscu (podmiana na kanoniczne możliwa), 11 do poprawy, 21 brak. | jw. |
| 4 | Nowe seedy dla słabszych budynków (top 3) | 10 dobrych z 65. Latarnia, szklarnia, kwiaciarnia bez poprawy – problem w prompcie/zbiorze, nie w seedzie. | [nowe-seedy](porownania/2026-10-21_lora-v1_prompty-v1/nowe-seedy/) |
| 5 | Latarnia i szklarnia (Z-Image Turbo) | Opis kamery „dla okrągłych” nic nie daje. Działa opis materiałów + hasło stylu: J „realistic shading and volume”, K „semi-realistic pixel art”. Szklany dach tylko po opisie „flat rectangular glass roof made of glass panels”. | [latarnia-i-realizm](porownania/2026-10-21_lora-v1_prompty-v1/latarnia-i-realizm/) |
| 6 | LoRA v1, prompty v2 (17 wierszy) | Suma spada 165 → 139: LoRA v1 nie zna rozmiarów w metrach. Nie jest to miarodajne porównanie zbiorów. | [lora-v1_prompty-v2](porownania/2026-10-21_lora-v1_prompty-v2/) |
| 7 | Uzdatnione prompty J/K na 5 modelach + siła LoRA | Siła 1.5 przywraca front przy „realistic”. MOSS SFT: złe drzwi i skośne dachy; FLUX 3: dach zwęża się do tyłu; Krea: latarnia dobra już bez uzdatnienia, szklany dach tylko z J/K. | [uzdatnione-prompty](porownania/2026-10-21_uzdatnione-prompty/) |
| 8 | Modele zewnętrzne (ChatGPT, Gemini) | Wzór stylu + prompt paskowy, bez treningu. Punkt odniesienia, nie do użycia lokalnie. | [modele-zewnetrzne](porownania/2026-10-21_modele-zewnetrzne/) |
| 9 | LoRA v2, prompty v2 (11 wierszy) | 108 pkt vs 106 dla v1/v1 na tych samych modelach – remis. Najlepsze: FLUX 3 destylat 16, Z-Image Turbo 15, Krea 2 Turbo 14. Zyskały stacja karetek i hotel, straciła latarnia. MOSS SFT spada (3). | [lora-v2_prompty-v2](porownania/2026-10-21_lora-v2_prompty-v2/) |
| 10 | Pojedynki v1/v1 vs v2/v2 (dobre obrazy) | v1 vs v2 bezpośrednio 29 : 28. Krea 2 (Raw i Turbo) w czołówce niezależnie od LoRA. Z-Image Base i MOSS Base 1024 na dole. | [pojedynki](porownania/2026-10-21_pojedynki/) |

## Wnioski
1. **LoRA uczy stylu, nie kopiuje zbioru.** Front, płaski dach, drzwi, paleta i donice przenoszą się na nowe budynki. Kolory z promptu zostają (turkusowy dom). Kosztem jest to, że nietypowe dachy (szkło, kopuła, skosy) LoRA ściąga do płaskiego prostokąta.
2. **Zbiór v2 nie poprawił jakości najlepszych obrazów**, ale też nie zaszkodził: v2/v2 i v1/v1 dają tyle samo punktów i remis w pojedynkach. Zysk v2 to większy budynek w kadrze, skala z opisu i drzwi na froncie.
3. **Modele:**
   - **Krea 2 Turbo int8** (LoRA z Krea 2 Raw): najlepszy kompromis – czołówka w ocenach i pojedynkach, ok. 8 s na obraz na RTX 3080, latarnię rysuje poprawnie. Licencja: komercyjnie do 1 mln USD przychodu rocznie.
   - **FLUX 3 Klein destylat** (LoRA z base): najszybszy (ok. 3 s), najlepszy w v2. Wada: dach zwęża się do tyłu.
   - **Z-Image Turbo:** równy, często „wystarczająco dobry”, ale w pojedynkach przegrywa z Krea.
   - **Odpadają:** Qwen-Image-Edit 2511 (za drogi: ok. 3 h treningu na A100, 5,5 min na obraz lokalnie, wynik średni), Qwen Q4 (niepasujący model), Z-Image Base (dół obu rankingów), MOSS SFT z LoRA z Base (w v2 źle się przenosi).
4. **Prompty:** opisywać wprost to, czego zbiór nie ma.
   - Dach budynku towarzyszącego: „with a dark grey flat roof”.
   - Szklany dach: „flat rectangular glass roof made of glass panels in a metal frame”.
   - Położenie drzwi na froncie zamiast „side door”.
   - Dla obiektów spoza zbioru: opis materiałów + „realistic shading” albo „semi-realistic”.
   - Unikać nazw, które model zamienia w napis (np. „veterinary clinic”).
5. **Metoda oceny:**
   - Punkty dobre/średnie/słabe dobrze odsiewają słabe obrazy.
   - Pojedynki działają tylko na zawężonej puli. Na wszystkich obrazach połowa głosów to „oba słabe” i ranking jest szumem.
   - Przy kilkuset głosach pewne są grupy, nie kolejność.

## Otwarte pomysły
- **v3:** obiekty okrągłe (latarnia, wieża ciśnień, silos, kiosk) narysowane wg zasad rzutu 3/4: walec z pionowymi bokami, góra jako elipsa o wysokości 0,5 szerokości, paski jako łuki. Do tego szklane dachy. Najpierw wzorce do akceptacji.
- Dłuższy trening (2500–3000 kroków) albo wyższa siła LoRA dla MOSS SFT i FLUX 3 – przeciw izometrii i zwężaniu dachu.
- Uzdatnione prompty J/K z LoRA v2 (dotąd tylko z v1).
- Pojedynki: dobierać pary bez nadreprezentacji budynków z 2 obrazami.
