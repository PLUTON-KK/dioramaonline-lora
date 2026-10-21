# Zmiany: lora-budynki-v1-final → lora-budynki-v2

Te same 72 budynki (25 dekoracyjnych, 47 wejściowych), te same sprite'y źródłowe. Zmienia się tylko sposób podania ich do nauki i część opisów. Każda zmiana ma powód z wyników v1.

## 1. Kadr i skala

| | v1 | v2 |
|---|---|---|
| skala w obrazie | wspólna dla wszystkich: 512 → 1 m = 24 px (×1), 1024 → 1 m = 48 px (×2) | brak wspólnej skali: każdy budynek kadrowany ciasno, dłuższy bok = 88% płótna |
| położenie | dół na stałej linii gruntu (y=492 / y=984), środek poziomo | dół 6% nad dolną krawędzią, środek poziomo |
| mały budynek (garaż 4 m) w 512 | ok. 94 px z 512 | ok. 450 px z 512 |
| skalowanie sprite'a | NEAREST ×1 / ×2 (całkowite) | niecałkowite: NEAREST ×8, potem BOX, kolory premultiplikowane, alfa progowana (bez magentowej obwódki, krawędzie pikseli lekko miękkie) |
| skala gry | uczona przez model | przywracana skryptem po generacji: szerokość budynku → `szer_m × 24` px |

**Dlaczego:** w v1 budynki zajmowały 100–200 px z 512, model miał mało miejsca na detal (VAE 8×8 → domek to ok. 15 komórek). Podglądy v1 pokazały też, że żaden model nie trzyma skali stabilnie: Qwen-Image 2512 na krokach 1000 / 1500 / 2000 dawał budynki małe / wąskie / średnie, Krea 2 i MOSS podobnie.

## 2. Opisy (caption)

| zmiana | v1 | v2 | dotyczy |
|---|---|---|---|
| rozmiar w metrach | brak | po typie: `about 10 m wide and 8 m tall, ...` (wysokość sprite'a z widocznym dachem) | wszystkie 72 |
| zaprzeczenie w budce | `..., with no visible door.` | `..., the serving window being the only opening in the front.` | `budka-pokazu` |
| „side door” | `a small dark grey side door` | `a small dark grey door on the right of the front facade` (lub `on the left`) | 13 opisów, niżej |

**Dlaczego „side door”:** modele bazowe czytają *side door* jako drzwi w ścianie bocznej, a żeby je pokazać, obracają budynek do widoku 3/4. W podglądach v1 stacja karetek (prompt z `a small side door`) najdłużej zostawała w izometrii: Z-Image Turbo 1024 na wszystkich krokach do 2000, FLUX 3 1024 do kroku 1000, MOSS 1024 na kroku 500. Na naszych obrazkach te drzwi zawsze są na froncie, więc opisujemy ich położenie na froncie. Położenie sprawdzone ręcznie na każdym sprite:

| budynek | drzwi |
|---|---|
| dom-z-lokalem, dom-z-panelami, hala-sportowa, kamienica-pierzeja-1, kamienica-pierzeja-2, kamienica-pierzeja-4, magazyn-blacha, magazyn, piekarnia-dom, remiza, warsztat-panele, zajezdnia | `on the right of the front facade` |
| warsztat | `on the left of the front facade` |

Reszta opisów bez zmian (te same co v1, zaakceptowane przez właściciela 2026-10-20).

## 3. Prompty testowe (podglądy z treningu)

Te same 10 budynków spoza zbioru co w v1, z tymi samymi poprawkami co w opisach:
- rozmiar w metrach (kwiaciarnia 10×8, hotel 13×13, stacja karetek 12×8, budka z lodami 7×6, dom turkusowy 10×10, latarnia z domkiem 14×18, szklarnia 14×8, obserwatorium 12×12, weterynarz 10×8, kino 15×11, dobrane do podobnych budynków ze zbioru),
- stacja karetek: `a small side door` → `a small door on the right of the front facade`,
- budka z lodami: bez `with no visible door`.

Plik: [`narzedzia/prompty_podglad_10_v2.json`](narzedzia/prompty_podglad_10_v2.json) (v1: [`narzedzia/prompty_podglad_10_v1.json`](narzedzia/prompty_podglad_10_v1.json)).

**Uwaga do porównań v1 ↔ v2:** różnią się i zbiór, i prompty testowe. Lepszy wynik v2 na stacji karetek może wynikać z samej zmiany promptu, nie z kadrowania.

## 4. Trening (plan)

- Tylko 512 (w v1 Z-Image Turbo 1024 wypadł gorzej niż 512, a w v2 budynek i tak wypełnia kadr).
- RunPod: Qwen-Image 2512, Krea 2 Raw (+ ewentualnie Qwen-Image-Edit 2511); lokalnie na RTX 3080, w nocy: Z-Image Turbo, Z-Image Base, MOSS-Image Base, FLUX 3 Klein base, FLUX.2 Klein 4B. Decyzja po wynikach v1.
- Parametry jak w v1 (rank 16, lr 1e-4, 2000 kroków, zapis co 250, podgląd co 500).
