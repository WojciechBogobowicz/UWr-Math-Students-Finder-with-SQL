# UWrMathStudentsFinder
Program umożliwa studentom matematyki na Uwr wyszukiwanie osób z którymi są zapisani na przedmioty.  
Korzystanie z programu wymaga konta na portalu usosweb.uni.wroc.pl  
W pliku SQL_code.txt zamieszczono wszystkie instrukcje zapisane w języku PostgreSQL.

Program dzieli się na cztery głowne części:  
- Bazy danych znormalizowanej do postaći BCNF napisanej w PostgreSQL. Zawierającą poza tabelami, funckje pozwalające aktualizować bazę na podstawie pliku txt, oraz triggery unifikujace dane przed wprowadzeniem do bazy.
- Adaptera pozwalającego połączyć się z bazą danych oraz wykonywać SQLowe kwerendy z poziomu pythona. Napisanego z wykorzystaniem biblioteki psycopg2.
- Downloadera który na podstawie biblioteki request jest w stanie pobrać dane z portalu usos, oraz przetworzyć je do użytecznej formy z pomocą biblioteki bs4.
- Prosteg GUI napisanego w PySimpeGUI, do komunikacji z użytkownikiem.
