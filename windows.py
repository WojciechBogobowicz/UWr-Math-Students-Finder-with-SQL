import PySimpleGUI as sg   


class Windows:
    def __init__(self) -> None:
        pass

    def signed_for_course(self, table, headers, course_name):
        result_layout =[ [sg.Table(values=table, headings=headers,num_rows=10)]]
        result_window = sg.Window(f'Zapisani na przedmiot {course_name}', layout=result_layout)
        result_window.read()

    def shared_groups(self,table, headers, name, last_name):
        result_layout =[ [sg.Table(values=table, headings=headers,num_rows=5)]]
        result_window = sg.Window(f'Wspólne zajęcia z {name} {last_name}', layout=result_layout)
        result_window.read()

    def updating_prompt(self, message, function, *args):
        result_layout =[ [sg.Text(message)]]
        result_window = sg.Window(f'Jeszcze chwilkę', layout=result_layout)
        result_window.read()
        function(*args)
        result_window.close()
