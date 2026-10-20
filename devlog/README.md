# Devlog: grafiki do Świata 2D

**Zacznij od [prologu](00-prolog.md).**

Dziennik prac nad grafikami do gry Świat 2D (dioramaonline): pixel art, generowanie lokalne i własne LoRA.
Zapisujemy tu decyzje, eksperymenty i to, co nie zadziałało, razem z powodami. Wnioski bez kontekstu szybko się dezaktualizują, więc przy każdej decyzji jest jej uzasadnienie.

- [ZASADY.md](ZASADY.md): obowiązujące reguły zbiorów i promptów. Krótko i zawsze aktualnie.
- [Prolog: po co to wszystko](00-prolog.md)
- Wpisy, od najnowszego:
  - [2026-10-21: zanim zaczęliśmy generować lokalnie (gościnnie: agent dioramy)](2026-10-21-diorama-zanim-zaczelismy.md)
  - [2026-10-20: budynki, od pasków w ChatGPT do pierwszych LoRA](2026-10-20-budynki-lora.md)

## Konwencje
- Jeden wpis na etap pracy, nazwa `RRRR-MM-DD-temat.md`, obrazki w `img/RRRR-MM-DD/`.
- Każdy wpis: kontekst, co zrobiliśmy, wyniki z obrazkami, decyzje (i dlaczego), błędy, następne kroki.
- Liczby podajemy zmierzone (czas, kroki, rozmiary), a przypuszczenia oznaczamy jako przypuszczenia.
- Głos: właściciel projektu, pierwsza osoba. Najważniejsze są jego pomysły, decyzje i odkrycia. Szczegóły techniczne tylko tam, gdzie wyjaśniają decyzję.
- Grafiki dioramy są nasze i mogą być publikowane. Nie publikujemy kluczy, tokenów ani danych prywatnych.

## Sprzęt i narzędzia
RTX 3080 10 GB, 32 GB RAM, Windows. ComfyUI (generowanie), ai-toolkit (trening LoRA), ChatGPT/Codex z obrazkiem-wzorem (paski z nowymi obiektami).
