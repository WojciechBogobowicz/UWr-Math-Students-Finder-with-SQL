from database import Database
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys




########################################## MAIN #########################################

#login, password = get_login_data(test=True)


def download_from_usos(login, password):

    def create_soup(url):
        r = s.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        return soup

    def login_to_usos(username, password):
        login_data = {
            'username':	username,
            'password': password,
            '_eventId': "submit",
            'submit'  : "ZALOGUJ"
        }

        url = 'https://login.uni.wroc.pl/cas/login?service=https%3A%2F%2Fusosweb.uni.wroc.pl%3A443%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl'
        r = s.get(url)     
                                                                            #żądanie logowania - tworzy ciastka, ciastka sa potrzebne
        soup = BeautifulSoup(r.content, 'html5lib')                                            #piekna zupa porządkuje info ze strony czyli r.content - deklarujemy ja tu
        login_data['lt'] = soup.find('input', attrs={'name' : 'lt'})['value']                  #w slowniuk z danymi logowania te rzeczy ponizej sie zmieniaja przy kazdym logowaniu, wiec znajdujemy je zupą 
        login_data['execution'] = soup.find('input', attrs={'name' : 'execution'})['value']     
        r = s.post(url, data=login_data)                                                       #post to rządanie odpowiadające wypisaniu formularza - u nas wpisanie danych do logowania i zalogowanie sie
        

    def groups_iter(test=False):
        groups_page_url = 'https://usosweb.uni.wroc.pl/kontroler.php?_action=home/grupy'
        soup = create_soup(groups_page_url)
        for url in find_hrefs_by_substr(soup, 'pokazZajecia'):
            gr_soup = create_soup(url)
            gr_url_without_student_limit = find_hrefs_by_substr(gr_soup, "limit=500")[0]
            yield gr_url_without_student_limit
            if test == True:
                break


    def download_students_list_from_group_page(file_name, soup, format="csv"):
        test_url = find_hrefs_by_substr(soup, format)[0]
        save_file(test_url, file_name)


    def find_hrefs_by_substr(soup, substring):
        found_hriefs = []
        for a in soup.find_all('a', href=True):
            if substring in a['href']:
                found_hriefs.append(a['href'])
        return found_hriefs


    def save_file(file_url, name):
        o_file = name  
        r = s.get(file_url)
        with open(o_file, 'wb') as output:
            output.write(r.content)


    def get_group_species(soup):
        page_title = soup.find('title').string
        gr_name = page_title[0:page_title.find(' -')]
        gr_type, gr_nr = split_group_name(gr_name)
        return gr_type, gr_nr

    def split_group_name(gr_name):
        split_index = gr_name.find(" gr.")
        gr_type = gr_name[:split_index]
        gr_nr = gr_name[split_index:]
        return gr_type, extract_nr(gr_nr)

    def extract_nr(text):
        return ''.join([i for i in text if i.isnumeric()])

    def get_teacher_name(soup):
        return find_first_hrief_match(soup, 'pokazOsobe').split()[::-1]


    def find_first_hrief_match(soup, part_of_hrief):
        finded_string = ''
        for a in soup.find_all('a', href=True):
            if  part_of_hrief in a['href']:
                finded_string = a.string
                break
        return finded_string


    def get_course_name(soup):
        return find_first_hrief_match(soup, 'pokazPrzedmiot')


    def get_course_code(soup):
        return soup.find('span', attrs={'class':'note'}).string


    def get_group_term(soup):
        """
        Return: Tuple with day of the week, hours, and place
        """
        table_body = extract_table_from_soup(soup, 1, {'class':'grey', 'cellspacing': '1'})
        table = convert_html_table_to_list(table_body)
        for row in table:
            if row[0] == 'Termin i miejsce:':
                try:
                    time, place = convert_cell_text_into_tuple(row[1])[0:2]
                    day, hours = split_date(time)
                    start_hours, end_hours = split_hours(hours)
                    return day, start_hours, end_hours, place
                except:
                    break
        return '','','',''


    def convert_cell_text_into_tuple(text):
        raw_info = text.split("   ")
        info = [i.strip("\n") for i in raw_info if i]
        return info


    def split_date(time):
        day, hour =  [i.strip() for i in time.split(',')]
        return day, hour


    def split_hours(hours):
        return [h.strip() for h in hours.split('-')]


    def extract_table_from_soup(soup, table_index_in_page, table_html_attrs):
        all_tables = soup.find_all('table', attrs=table_html_attrs)
        table = all_tables[table_index_in_page]
        table_body = table.find('tbody')
        return table_body


    def convert_html_table_to_list(table_body):
        table = []
        rows = table_body.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            cells = [cell.text.strip() for cell in cells if cell.text.strip()]
            table.append(cells)
        return table


    def extract_id_from_url(url):
        id_index = url.find('id=')
        assert not id_index == -1, f"Nie znaleziono id w url: {url}"
        number_index = url.find('id=')+3
        number = ''
        for i in url[number_index:]:
            if i.isdigit():
                number+=i
            else:
                break
        return number


    def get_student_info(soup):
        students_info = []
        students_list = get_students_names_list(soup)
        students_ids = get_students_ids(soup)
        assert len(students_ids) == len(students_list), "liczba studentów i id jest rozna"
        for i in range(len(students_list)):
            student = [students_ids[i]] + students_list[i]
            students_info.append(student)
        return students_info

    def get_students_names_list(soup):
        html_table = extract_table_from_soup(soup, 0, 
                        {'class': "wrnav", 
                        'style': "margin-top: 15px",
                        'cellspacing': "1px"})
        raw_student_list = convert_html_table_to_list(html_table)
        student_list = raw_student_list[raw_student_list.index(['Stan'])+1:-2]
        return student_list


    def get_students_ids(soup):
        ids = []
        for url in find_hrefs_by_substr(soup, 'pokazOsobe')[1:]:
            ids.append(extract_id_from_url(url))
        return ids


    def get_teacher_id(soup):
        url = find_hrefs_by_substr(soup, 'pokazOsobe')[0]
        return extract_id_from_url(url)


    def get_curr_date_and_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    courses = Database(('Id', 'Nazwa przedmiotu'), 'Przedmioty')
    groups = Database(('Id', 'Typ', 'Dzień', 'Godz. Rozp.', 'Godz. Zakończ.', 'Miejsce', 'Id nauczyciela', 'Kod kursu', 'Nr. grupy'), 'Grupy')
    teachers = Database(('Id', 'Nazwisko', 'Imię'), 'Nauczyciele')
    students = Database(('Id', 'Na, ''zwisko', 'Imiona', 'Status', 'Znajomy'), 'Studenci')
    students_to_groups = Database(('Id studenta', 'Id grupy'), 'Studenci_do_Grup', have_pkey=False) # ∞<->∞
    groups_types = Database(('Typ',), "Typy_Grup")
    updates = Database(("Login","Data","Ilość wierszy"), "Aktualizacje", have_pkey=False)


    with requests.Session() as s:
        login_to_usos(login, password)
        for gr_url in groups_iter(test=False):
            try:
                gr_soup = create_soup(gr_url)

                course_name = get_course_name(gr_soup)
                course_code = get_course_code(gr_soup)
                
                teacher_id = get_teacher_id(gr_soup)
                teacher_last_name, teacher_name = get_teacher_name(gr_soup)
                
                gr_id = extract_id_from_url(gr_url)
                gr_type, gr_nr = get_group_species(gr_soup)
                day, start_hour, end_hour, place = get_group_term(gr_soup)
                
                for student_info in get_student_info(gr_soup):
                    student_id = student_info[0]
                    students.add_row(*student_info, 'FALSE')
                    students_to_groups.add_row(student_id, gr_id)
            except:
                print("Nie udało się pobrać danych:", sys.exc_info()[1])
                continue
            courses.add_row(course_code, course_name)
            groups.add_row(gr_id, gr_type, day, start_hour, end_hour, place, teacher_id, course_code, gr_nr)
            teachers.add_row(teacher_id, teacher_last_name, teacher_name)
            groups_types.add_row(gr_type)
            print("Sprawdziłem grupę:", course_name, gr_type, "gr.", gr_nr)
            #groups_in_courses.add_row(group_id, course_code)
            #teachers_in_groups.add_row(group_id, teacher_id)

        
        all_datablases = (updates, courses, groups, teachers, students, students_to_groups, groups_types)
        row_count_total = sum([database.count_elements() for database in all_datablases[1:]])
        updates.add_row(login, get_curr_date_and_time(), str(row_count_total))
        updates.add_to_file()
        
        if row_count_total > 0:
            download_message = f"Pobrano {row_count_total} wierszy"    
            for database in all_datablases[1:]:
                database.save_to_file()
        else:
            download_message="Nie udało się zaktualizować bazy, prawdopodobnie trwa migracja danych"
            
            
            
            #file_name = f"{course_name}-{group_name}.csv"
            #download_students_list_from_group_page(file_name, soup)
        return download_message











    
