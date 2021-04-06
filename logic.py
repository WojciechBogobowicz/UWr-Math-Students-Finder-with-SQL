from sql_adapter import SQL_adapter
from downloader import download_from_usos
from tabulate import tabulate 


class Logic:
    def __init__(self) -> None:
        self.sql = SQL_adapter()
    
    def update_base(self, login, password):
        msg = download_from_usos(login, password)
        self.sql.update_base()
        self.sql.save_changes()
        return msg, login

    def update_message(self):
        info = self.sql.last_update_info()
        return """Ostatnia aktualizacja dla użytkownika {}. \nWykonana {}, dodała {} krotek do tabel.""".format(*info)

    def close(self):
        self.sql.close()

    def find_student_table(self, name, last_name):
        headers = ("Przedmiot", "Typ", "Nr grupy", 'Dzień', 'Godz. Rozp.', 'Godz. Zakończ.', 'Nauczyciel','Id')
        table = self.sql.find_groups(name, last_name)
        return headers, table
    
    def find_course_table(self, course_name):
        headers = ("Imie", 'Nazwisko', 'Id')
        table = self.sql.find_students_on_course(course_name)
        return headers, table
    
    def add_friend(self, name, last_name):
        self.sql.add_friend(name, last_name)
        self.sql.save_changes()
        

    