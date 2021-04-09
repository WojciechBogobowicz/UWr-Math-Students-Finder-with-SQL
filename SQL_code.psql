
--KOD:
----------------Grupy:----------------------
ALTER TABLE 
"Grupy"
ALTER COLUMN "Godz. Zakończ." TYPE TIME (4)
USING "Godz. Zakończ."::TIME(4) without time zone;

ALTER TABLE 
"Grupy"
ALTER COLUMN "Godz. Rozp." TYPE TIME (4)
USING "Godz. Rozp."::TIME(4) without time zone;


----------------CHECK:-----------------------
ALTER TABLE
"Grupy"
ADD CHECK ("Godz. Zakończ." > "Godz. Rozp.");

ALTER TABLE
"Studenci"
ADD CHECK ("Status" IN ('aktywny','nieaktywny'));

ALTER TABLE
"Grupy"
ADD CHECK ("Dzien" SIMILAR TO '%(poniedziałek|wtorek|środa|czwartek|piątek|sobota|niedziela)%');

ALTER TABLE
"Aktualizacje"
ADD CHECK ("Ilość wierszy" >=0);
----------------TRIGGER:---------------------


CREATE OR REPLACE FUNCTION unifikuj_sale_zd() RETURNS TRIGGER AS $$
BEGIN
	IF (NEW."Miejsce" = 'sala wirtualna') THEN
		NEW."Miejsce" = 'sala zd';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

DROP TRIGGER unifikuj_sale_zd ON "Grupy" CASCADE;
CREATE TRIGGER unifikuj_sale_zd BEFORE INSERT ON "Grupy"
	FOR EACH ROW EXECUTE PROCEDURE unifikuj_sale_zd();


CREATE OR REPLACE FUNCTION wez_pierwsze_imie() RETURNS TRIGGER AS $$
BEGIN
    NEW."Imie" = split_part(NEW."Imie", ' ', 1);
	RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

DROP TRIGGER wez_pierwsze_imie ON "Studenci" CASCADE;
CREATE TRIGGER wez_pierwsze_imie BEFORE INSERT ON "Studenci"
	FOR EACH ROW EXECUTE PROCEDURE wez_pierwsze_imie();

-----------------FUNCTION:-----------------------------

CREATE OR REPLACE FUNCTION aktualizuj_baze(sciezka TEXT) RETURNS VOID AS $$
DECLARE
	ilosc_wierszy INTEGER;
	Aktualizacje_sciezka TEXT;
	nauczyciele_sciezka TEXT;
	typy_grup_sciezka TEXT;
	przedmioty_sciezka TEXT;
	Studenci_sciezka TEXT;
	Grupy_sciezka TEXT;
	Studenci_do_Grup_sciezka TEXT;
BEGIN
	DELETE FROM "Aktualizacje";
	SELECT concat (sciezka, 'Aktualizacje.csv') INTO Aktualizacje_sciezka;
	execute format('copy "Aktualizacje" from %L delimiter '','' CSV HEADER;', Aktualizacje_sciezka);

	SELECT "Ilość wierszy" from "Aktualizacje" 
	WHERE "Data" = (
		SELECT max("Data") FROM "Aktualizacje" 
	) INTO ilosc_wierszy;

	IF (ilosc_wierszy = 0) THEN
		RAISE 'Nie ma co aktualizować';
    END IF;

	DELETE FROM "Studenci_do_Grup";
	DELETE FROM "Grupy";
	DELETE FROM "Studenci";
	DELETE FROM "Przedmioty";
	DELETE FROM "Nauczyciele";
	DELETE FROM "Typy_Grup";

	SELECT concat (sciezka, 'Nauczyciele.csv') INTO nauczyciele_sciezka;
	execute format('copy "Nauczyciele" from %L delimiter '','' CSV HEADER;', nauczyciele_sciezka);

	SELECT concat (sciezka, 'Typy_Grup.csv') INTO typy_grup_sciezka;
	execute format('copy "Typy_Grup" from %L delimiter '','' CSV HEADER;', typy_grup_sciezka);

	SELECT concat (sciezka, 'Przedmioty.csv') INTO przedmioty_sciezka;
	execute format('copy "Przedmioty" from %L delimiter '','' CSV HEADER;', przedmioty_sciezka);

	SELECT concat (sciezka, 'Studenci.csv') INTO Studenci_sciezka;
	execute format('copy "Studenci" from %L delimiter '','' CSV HEADER;', Studenci_sciezka);

	SELECT concat (sciezka, 'Grupy.csv') INTO Grupy_sciezka;
	execute format('copy "Grupy" from %L delimiter '','' CSV HEADER;', Grupy_sciezka);

	SELECT concat (sciezka, 'Studenci_do_Grup.csv') INTO Studenci_do_Grup_sciezka;
	execute format('copy "Studenci_do_Grup" from %L delimiter '','' CSV HEADER;', Studenci_do_Grup_sciezka);
END;
$$ LANGUAGE 'plpgsql';

'/home/w/Dokumenty/kody/projekt_BD/databases/'



-----------------------------VIEWS:------------------------------------------------------

CREATE VIEW Wyswietlani_Studenci AS
SELECT "Imie", "Nazwisko", "Id"
FROM "Studenci"
WHERE "Status"='aktywny' 
ORDER BY "Znajomy" DESC, "Nazwisko" ASC;

CREATE VIEW Wyswietlane_Grupy AS
SELECT p."Nazwa Przedmiotu", g."Typ", g."Nr. grupy", 
g."Dzien", g."Godz. Rozp.", g."Godz. Zakończ.", n."Nazwisko" AS Nauczyciel, g."Id"
FROM
"Grupy" AS g
JOIN
"Przedmioty" AS p ON g."Kod kursu" = p."Id"
JOIN
"Nauczyciele" AS n ON g."Id nauczyciela" = n."Id"; 

CREATE VIEW przedmioty_studentow AS
SELECT g."Nazwa Przedmiotu" AS Przedmiot, s.*
FROM
Wyswietlani_Studenci AS s
JOIN
"Studenci_do_Grup" AS sg
ON s."Id" = sg."Id studenta"
JOIN
Wyswietlane_Grupy AS g
ON g."Id" = sg."Id grupy";


-----------------------------QUERIES:----------------------------------

--Wspólne grupy ze studentem o konkretnym Id

SELECT g.*
FROM 
Wyswietlane_Grupy AS g
JOIN
"Studenci_do_Grup" AS sg
ON g."Id" = sg."Id grupy"
WHERE sg."Id studenta" = 202086;

--Studenci chodzacy na dany przedmiot:

SELECT "Imie", "Nazwisko", s."Id"
FROM 
"Studenci" AS s
JOIN
"Studenci_do_Grup" AS sg
ON s."Id" = sg."Id studenta"
JOIN
Wyswietlane_Grupy AS g
ON g."Id" = sg."Id grupy"
WHERE g."Nazwa Przedmiotu" = '{course}'
AND
"Status"='aktywny' 
GROUP BY s."Id"
ORDER BY "Znajomy" DESC, "Nazwisko" ASC;

--Id studenta:

SELECT count(*) AS ilosc_osob
FROM 
Wyswietlani_Studenci
WHERE "Imie" = 'Magdalena' AND "Nazwisko" = 'Buszka';

SELECT "Id"
FROM 
Wyswietlani_Studenci
WHERE "Imie" = 'Magdalena' AND "Nazwisko" = 'Buszka';

--Przedmioty studenta:

SELECT DISTINCT przedmiot
FROM
przedmioty_studentow
WHERE
"Id" = 202086;


