import PySimpleGUI as sg   
from logic import Logic
from windows import Windows

"DarkPurple"
'Topanga'
sg.theme('DarkTeal2')
l = Logic()
w = Windows()


layout = [
          [sg.Button('   Aktualizuj baze   '), sg.Button('Sprawdz aktualizacje ')],
          [sg.Button('Znajdź wspólne grupy '), sg.Button('Zapisani na przedmiot')],
          [sg.Button('   Dodaj znajomego   '), sg.Button('         Exit        ')],
          ]      

window = sg.Window('Baza studentów', layout)    

while True:
    event, values = window.read()    
    print(event, values)
    if event in (None, '         Exit        '):
        break
    if event == '   Aktualizuj baze   ':
        login = sg.popup_get_text('Wprowadż login do USOSa:', 'Logowanie')
        password = sg.popup_get_text('Wprowadż hasło do USOSa:', 'Logowanie', password_char='*')
        sg.popup_ok("Baza jest aktualizowana, powiadomi, jak skonczy.", auto_close_duration=3, auto_close=True)
        #sg.popup_auto_close
        l.update_base(login, password)
        sg.popup_ok("Aktualizowanie bazy zakończone!")
    if event == 'Sprawdz aktualizacje ':
        sg.popup_ok(l.update_message())
    if event == 'Znajdź wspólne grupy ':
        student_names = sg.popup_get_text("Podaj imię studenta", default_text="Jan Kowalski")
        name, last_name = student_names.split(' ')
        headers, table = l.find_student_table(name, last_name)
        w.shared_groups(table, headers, name, last_name)
    if event == 'Zapisani na przedmiot':
        course_name = sg.popup_get_text("Wprowadź nazwę przedmiotu")
        headers, table = l.find_course_table(course_name)
        w.signed_for_course(table,headers,course_name)
    if event == '   Dodaj znajomego   ':
        student_names = sg.popup_get_text("Podaj imię studenta", default_text="Jan Kowalski")
        name, last_name = student_names.split(' ')
        l.add_friend(name, last_name)

window.close()
l.close()

