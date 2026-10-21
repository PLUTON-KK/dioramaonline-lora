# Zmiany: zbiór budynków v2-final → v3-final

## 1. Skład
- **Usunięte z v2 (14), decyzja właściciela:** biurowiec, dom-gracza-1, dom-nowoczesny, dom-z-panelami, house-10n, house-12n, kamienica-pierzeja-2, kamienica-waska, kiosk-gazet, pavilion-2n, pawilon-maly, sklep-modelarski, wiata-rowerowa, zajezdnia.
- **Dodane (30):** obiekty spoza v1/v2, z których LoRA v2 robiła najsłabsze rzeczy albo których w zbiorze nie było wcale: obiekty okrągłe (chłodnia, wieża ciśnień, silosy, wiatraki, cyrk), wysokie i smukłe (turbiny, wieżowiec), nietypowe bryły (meczet z kopułą, zamek, piramida, foliak), przemysł i infrastruktura (elektrownie, tartak, oczyszczalnia, skup złomu, fotowoltaika), usługi (szpital, banki, stacja benzynowa), plac zabaw, kurnik. Tabela w [README](README.md).
- Odrzucone w końcowym wyborze spośród nowych: maszt telekomunikacyjny, rafineria.
- Razem 88: 42 wejściowe (37 z v2 + 5 nowych), 46 dekoracyjnych (21 + 25).

## 2. Jak powstały nowe obiekty
1. 38 obiektów spoza zbioru, prompty w stylu v2 (rozmiar w metrach) + uzdatnione J („realistic shading and volume”) i K („semi-realistic pixel art”) z opisem materiałów.
   - Test-v1 promptów odrzucony: kamera z „flat rectangular roof” dla wszystkiego dawała płaski prostokąt za cyrkiem, piramidą, zamkiem. W test-v2 płaski dach tylko tam, gdzie logiczny; reszta „the front facing the viewer and the top seen slightly from above”.
2. Generowanie: Krea 2 Turbo int8, FLUX 3 Klein destylat, MOSS-Image SFT, Z-Image Turbo (część) z LoRA v2 512, ComfyUI RTX 3080; obiekty bez dobrego wyniku – Krea + prompt K na 5 seedach (przemysł bez dymu i pary).
3. Budynki wejściowe: dopasowanie kanonicznych drzwi; odrzucone te w izometrii i bez kanonicznych drzwi (sprawdzone ręcznie).
4. Etap 1 (właściciel): z ~460 obrazów zostały 32. Etap 2 (lista końcowa): zostało 30.
5. Przeróbka jak budynki gry: wycięcie z magenty, skala gry (wejściowe: drzwi = 58 px, dekoracyjne: szerokość z promptu), paleta świata 64 kolory, czyszczenie fioletowej obwódki, wklejone drzwi std-external-2, kadr v2 (NEAREST ×8 + BOX premultiplikowany).

## 3. Opisy
- **Nowe opisy napisane według obrazu**, nie według promptu, którym obraz powstał.
- **Bez zaprzeczeń** (no / not / without / only…). Poprawiony jedyny taki opis z v2: `budka-pokazu` – usunięte „, the serving window being the only opening in the front” (okno sprzedaży jest już opisane wprost).
- **Kamera zgodna z bryłą:** „front facade facing the viewer, flat rectangular roof visible from above” tylko dla budynków z płaskim prostokątnym dachem (wszystkie z v2 + 6 nowych). Pozostałe: „the front facing the viewer and the top seen slightly from above”.
- **Okrągłe bryły:** dopisek „round shapes drawn straight from the front with their tops visible as flattened ellipses” tylko przy obiektach z okrągłymi częściami.
- **„building” / „object”:** obiekty, które nie są budynkami (turbina, fotowoltaika, oczyszczalnia, skup złomu, cyrk, piramida, plac zabaw), mają „decorative object”.
- Bez dymu i bez parkingów/aut przed budynkami (te rzeczy robi diorama osobno).
- Rozmiar `about W m wide and H m tall` z gotowego sprite'a (szerokość / wysokość z widocznym dachem, 24 px = 1 m), jak w v2.
- Automatyczna kontrola w generatorze: zaprzeczenia, płaski dach przy spiczastych/kopułach, zgodność rozmiaru ze sprite'em, słowo `swiat2d style`, tło magenta, „side door”.

## 4. Inne
- Tylko 512 px (bez 1024).
- Zestaw testowy (10 budynków z `budynki/testy/`) bez zmian i poza zbiorem.
