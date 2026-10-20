# Prolog: po co to wszystko

Zaczęło się od tego, że Codex z CLI jest drogi, a generowanie w ChatGPT wymaga ręcznego klikania. Jak to zautomatyzować? Samemu pisać mi się nic nie chce, a mamy Claude Code. No to niech Claude robi wszystko. Niech nawet pisze ten devlog, w moim stylu: co wymyśliłem, co zostało zrobione i dlaczego (o ile wie, haha). A docelowo niech sam gada z agentem, który programuje dioramę, i przyjmuje od niego zlecenia na obrazki zamiast Codexa, który był drogi.

Skoro mamy GPU, to czemu nie. RTX 3080, kupiona jeszcze w wersji bez LHR, chyba zanim wyszedł Cyberpunk 2077. Szkoda, że ma tylko 10 GB VRAM-u, mniej niż zwykła 3060. Ale za to jak działał na niej Cyberpunk! I Forza! No i w sumie głównie WoW. Kopania nie widziała (no, może trochę, ale za mało), więc niech teraz trochę poobliczą.

LoRA? Myślałem, że to moduł do komunikacji bezprzewodowej. Okazuje się, że to coś innego: sposób na douczanie dużych modeli, bez ruszania ich samych. Najpierw kojarzyło mi się z modelami językowymi, ale to samo działa z grafiką. A grafika jest wdzięczna: wynik widać od razu, no i mieści się na GPU (no, w miarę).

Czy my robimy destylację generatora obrazów ChatGPT? Chyba nie do końca. Ale to on narysował pierwsze grafiki do dioramy, a teraz na tych obrazkach uczymy własne modele, więc trochę tak.

No to po kolei zaczęliśmy testować modele lokalnie. Potem: czym ta LoRA w ogóle jest... A dobra, sam programować już nie chcę. Kto jeszcze sam programuje, skoro robi to teraz AI? Tym bardziej że to odpalanie skryptów, a nie projekt do publikacji. Niech Claude wszystko koordynuje. Ma dostęp do GPU? Ma. No to jedziemy. Logika jest prosta: wektory, przesunięcia. Ale trzeba usiąść i analizować grafiki.

Nie mamy ich wystarczająco? No to znowu: Codex CLI? Nieee, za drogi. Lecimy ręcznie: będę kopiował prompty do ChatGPT, wybierał wyniki i na tym będziemy się uczyć. No i jeszcze drzwi.

Tylko w sumie po co ja to robię? Tyle grafik pewnie już mi do wszystkiego wystarczy, nawet bez generatora. Ale nie, większy fun mam z testowania tego wszystkiego.

A diorama? Miała być tylko dodatkowym projektem do sklepu. Takim czymś, co może kogoś przyciągnąć, gdzie można podejrzeć, jak idzie pakowanie zamówień. To w sumie mamy już zrobione na grafikach z ChatGPT, w becie dioramy. Ale nie: miał być cały sklep w dioramie, z przeglądaniem i zamawianiem, z przekierowaniem do sklepu. A potem od razu wpadł pomysł miasta, scen, minigier, warsztatów modelarskich i masy innych rzeczy, które lądują na długiej liście pomysłów.

Do tego przyda się spójny styl graficzny, czyli generator. Przy okazji można się czegoś dowiedzieć o tym, jak działa AI (albo i nie). I tak w końcu zaczęło się to repo: LoRA pod różne modele.

Czy uda się zrobić jedną LoRA do wszystkich elementów dioramy? Czy wybierzemy jeden model do wszystkiego? Czy będziemy mieli osobne LoRA do różnych części dioramy? Dowiemy się w następnych odcinkach. Wszyscy, bo sam nie znam odpowiedzi na te pytania.

A tymczasem nawet pisanie zlecam Klaudiuszowi (znaczy się Claude Code, ale on nie wie, że tak go nazywam; teraz już się dowie, jak będzie przerabiał ten tekst do publikacji). Liczę, że Klaudiusz nie będzie was zanudzał wszystkimi szczegółami i raportami, tylko skupi się na tym, co odkryłem. A jak nie, to go popchnę we właściwą stronę.

Ja w tym czasie działam dalej z pomysłami i zleceniami trenowania LoRA pod różne dziwne modele, które poradzą sobie na 10 GB VRAM-u.

---
*Od Klaudiusza: dowiedziałem się. Tekst przerobiłem tylko redakcyjnie. Poprawiłem jeden fakt: zwykła RTX 3060 ma 12 GB, a 3060 Ti ma 8 GB, czyli mniej niż nasza 3080.*
