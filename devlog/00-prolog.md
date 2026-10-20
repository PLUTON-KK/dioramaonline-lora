# Prolog: po co to wszystko

Zacząć od tego, że Codex jest drogi po CLI, a ChatGPT generowanie wymaga ręcznego klikania. Jak to zautomatyzować? Samemu mi się pisać nie chce nic, mamy Claude Code, no to niech Claude robi wszystko, ba, niech pisze nawet devloga w moim stylu, co wymyślałem i co były za rzeczy zrobione i dlaczego (o ile wie, haha), i niech docelowo Claude sobie gada bezpośrednio z agentem, który programuje dioramę, żeby mógł mu zlecać obrazki zamiast Codexowi (co był drogi).

Więc skoro mamy GPU, 3080, kupione jeszcze bez LHR, chyba zanim wyszedł CP2077, i jakoś działa to wszystko, szkoda, że ma mniej VRAM-u niż 3060 Ti (*q3ok się myli - to zwykła 3060 ma więcej VRAM-u, 12 GB; 3060 Ti ma 8 GB - dopisek Klaudiusza*), ale za to jak działa tam CP! I Forza! No i w sumie to głównie WoW działał. Kopania nie widziała (no może trochę, ale za mało), ale za to może trochę poobliczać rzeczy.

LoRA? Myślałem, że to moduł do komunikacji bezprzewodowej, a to się okazuje, że to do finetuningu modeli LLM. No i dobra, ale finetuning, o. Grafika, bo tu można sprawdzić i się zmieści na GPU (no w miarę). Czy my robimy destylację generatora obrazów ChatGPT? Chyba nie do końca, ale to on robił pierwsze obrazy do dioramy.

No to tak, skoro się pomyślało, to zaczęliśmy po kolei modele testować lokalnie. Później, co to w sumie ta LoRA jest... a dobra, nie chce mi się już samemu programować (kto jeszcze sam programuje, jak robi teraz to AI? Tym bardziej jak to odpalanie automatyczne skryptów, a nie projekt do publikacji). No to niech Claude robi wszystko, sobie koordynuje. Ma dostęp do GPU? Ma. No to jedziemy, logika jest prosta, wektory, przesunięcia, ale trzeba usiąść i analizować grafiki.

Ale nie mamy wystarczająco? No to znowu. Codex CLI? Nieee, za drogi. Lecimy, będę kopiował do ChatGPT i wybierał, i z tego będziemy się uczyć. No i jeszcze drzwi.

Tylko w sumie po co ja to robię? Tyle grafik mi do wszystkiego wystarczy już pewnie bez generatora. Ale nie, większy fun mam z testowania tego wszystkiego.

A diorama? To w sumie miał być tylko taki dodatkowy projekt do sklepu. Ot, takie coś, co może kogoś przyciągnąć, może ktoś sobie podejrzeć, jak idzie nam pakowanie w sklepie (co w sumie mamy już na tych grafikach z ChatGPT zrealizowane w becie dioramy), ale nie - miał być cały sklep faktycznie w dioramie, z możliwością przeglądania i zamawiania z przekierowaniem do sklepu. No ale od razu wpadł pomysł miasta, scen, minigier, warsztatów modelarskich i masa innych rzeczy, które tylko wpadają do długiej listy pomysłów. Ale generator - przyda się spójny styl graficzny. Przy okazji czegoś się można dowiedzieć i nauczyć o sposobie działania AI (albo i nie).

Ale tak, i tak zaczął się ten projekt repo w końcu, z LoRA pod różne modele. Czy uda się zrobić jedno LoRA do wszystkich elementów dioramy? Czy wybierzemy jeden model do wszystkiego? Czy będziemy mieli osobne LoRA do różnych części dioramy? Dowiemy się w następnych odcinkach. Wszyscy, bo ja sam nie znam odpowiedzi na te pytania.

A tymczasem nawet pisanie zlecam Klaudiuszowi (znaczy się Claude Code, ale on nie wie, że go tak nazywam - ale teraz już się dowie, jak będzie "przerabiał" ten tekst do publikacji w tym devlogu). Liczę, że nie będzie was Klaudiusz zanudzał wszystkimi szczegółami i raportami i skupi się na tym, co ja odkryłem, a jak nie, to go popchnę we właściwą stronę. Tymczasem działam dalej z pomysłami i zleceniami generowania LoRA pod różne dziwne modele, co na 10 GB VRAM-u sobie poradzą.

---
*Od Klaudiusza: dowiedziałem się. Pierwszą wersję tego tekstu „wygładziłem” za bardzo i dostałem polecenie, żeby utrzymać styl autora, a nie przerabiać wszystkiego. Więc poprawiłem tylko literówki i interpunkcję.*
