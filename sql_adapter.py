import psycopg2
import os

class SQL_adapter:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
        host="localhost",
        database="projekt",
        user="postgres",
        password="masloooo")
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def save_changes(self):
        self.conn.commit()

    def update_base(self):
        current_dir = os.getcwd()
        path = os.path.join(current_dir, 'databases/')
        self.cur.execute(f"""
            SELECT aktualizuj_baze('{path}');
            """)
        self.cur.fetchall()

    def _get_student_id(self, name, last_name):
        self.cur.execute(f"""
            SELECT "Id"
            FROM 
            Wyswietlani_Studenci
            WHERE "Imie" = '{name}' AND "Nazwisko" = '{last_name}';
            """)
        id_list = self.cur.fetchall()
        if self._count_students_named(name, last_name) == 1:
            return id_list[0][0]
        elif self._count_students_named(name, last_name) == 0:
            not_found=-1
            return not_found
        else:
            ids = self.take_column(id_list)
            print('Istnieje więcej osób o tym imienu:')
            for i, id in enumerate(ids):
                print(f"Id: {id}, wspólne przedmioty: {self._student_courses(id)}")
            return input("Wprowadz id osoby którą miałeś(aś) na myśli: ")

    def _count_students_named(self, name, last_name):
        self.cur.execute(f"""
            SELECT count(*) AS ilosc_osob
            FROM 
            Wyswietlani_Studenci
            WHERE "Imie" = '{name}' AND "Nazwisko" = '{last_name}';
            """)
        return self.cur.fetchall()[0][0]

    def get_student_courses(self, name, last_name):
        id = self._get_student_id(name, last_name)
        if id == -1:
            return ("","","")
        return self._student_courses(id)

    def _student_courses(self, students_id):
        self.cur.execute(f"""
            SELECT DISTINCT przedmiot
            FROM
            przedmioty_studentow
            WHERE
            "Id" = {students_id}
            """)
        return self.take_column(self.cur.fetchall())

    def find_groups(self, name, last_name):
        id = self._get_student_id(name, last_name)
        if id == -1:
            return ("","","","","","","","")
        return self._groups(id)

    def _groups(self, id):
        self.cur.execute(f"""
            SELECT g.*
            FROM 
            Wyswietlane_Grupy AS g
            JOIN
            "Studenci_do_Grup" AS sg
            ON g."Id" = sg."Id grupy"
            WHERE sg."Id studenta" = {id};
            """)
        return self.cur.fetchall()

    def find_students_on_course(self, course):
        self.cur.execute(f"""                
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
            """)
        return self.cur.fetchall()

    def add_friend(self, name, last_name):
        student_id = self._get_student_id(name, last_name)
        self.cur.execute(f"""    
            UPDATE 
            "Studenci"
            SET
            "Znajomy" = TRUE
            WHERE
            "Id" = {student_id}
            """)

    def last_update_info(self):
        self.cur.execute(f"""
            SELECT * from "Aktualizacje" 
            WHERE "Data" = (
            SELECT max("Data") FROM "Aktualizacje" 
            )
            """)
        return self.cur.fetchone()

    @classmethod
    def take_column(cls, table, column_index=0):
        return [row[column_index] for row in table]

if __name__=="__main__":
    test = SQL_adapter()
    print(test.last_update_info())
    print(test.update_base())
    print(test.get_student_courses("Kacper","Mazur"))
    test.close()