import os


class Database:
    def __init__(self, colnames, name, pkey_column=0, have_pkey=True):    
        self.have_pkey = have_pkey
        self.name = name
        self.colnames = colnames
        self.pkey_column = pkey_column
        self.pkeys = set()
        self.rows = []

    def add_row(self, *row):    
        pkey_already_in_database = row[self.pkey_column] in self.pkeys
        if not self.have_pkey or not pkey_already_in_database:
            self.rows.append(row)
            if self.have_pkey:
                self.pkeys.add(row[self.pkey_column])
    
    def save_to_file(self, format='csv'):
        dir = 'databases'
        path = os.path.join(dir, self.name + '.' + format)
        with open(path, 'w') as f:
            f.write(','.join(self.colnames)+'\n')
            for row in self.rows:
                f.write(','.join(row)+'\n')

    def add_to_file(self, format='csv'):
        dir = 'databases'
        path = os.path.join(dir, self.name + '.' + format)
        with open(path, 'a') as f:
            for row in self.rows:
                f.write(','.join(row)+'\n')

    def count_elements(self):
        return len(self.rows)

            


if __name__=="__main__":
    dom = Database(("id", "imie"), 'moj_dom', have_pkey=False)
    dom.add_row('1', 'Mama')
    dom.add_row('2', 'Piotrek')
    dom.add_row('3', 'Niunia')
    dom.add_row(*('3', 'NiuniaPrzezPrzypadek'))
    dom.save_to_file()