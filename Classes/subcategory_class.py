import pandas as pd
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *
from Classes.entry_class import Entry

#############################################################
## CLASSES                                                 ##
#############################################################
class Subcategory_report:    
    ## CLASS CONSTRUCTORS
    def __init__(self, name, cat):
        if name not in CATEGORIES[cat]:
            CATEGORIES[cat].append(name)
        self.Name = name
        self.Entries = []
        self.Subtotal_revenue = 0.0
        self.Subtotal_expense = 0.0
        self.Subtotal = 0.0
    
    ## CLASS DISPLAYS
    def display(self, depth=9):
        if (depth >= 0):
            if (len(self.Entries) == 0):
                print(colored(f"\t• {self.Name} {LANGUAGE_DICT['no_entries']}", attrs=['bold']))
            else:
                print(colored(f"\t• {self.Name} : +{self.Subtotal_revenue:.2f}{LANGUAGE_DICT['currency']} | -{self.Subtotal_expense:.2f}{LANGUAGE_DICT['currency']} | {LANGUAGE_DICT['total']}: {self.Subtotal:.2f}{LANGUAGE_DICT['currency']}", attrs=['bold']))
                for entry in self.Entries:
                    entry.display(depth - 1)
    
    ## CLASS FUNCTIONS
    def add_entry(self, name, data:pd.DataFrame, row, col):
        entry = Entry(name)
        entry.build(data, row, col)
        self.Entries.append(entry)

    def build(self, data:pd.DataFrame, i, j):
        self.Subtotal_revenue = 0.0
        self.Subtotal_expense = 0.0
        self.Subtotal = 0.0
        row = i+1
        col = j+1
        details = str(data.iloc[row].iloc[col])
        while details != LANGUAGE_DICT['total']:
            if (details != "nan"):
                self.add_entry(details, data, row, col)
                self.Subtotal_revenue += self.Entries[-1].get_revenue()
                self.Subtotal_expense += self.Entries[-1].get_expense()
                self.Subtotal += self.Entries[-1].get_total()
            row += 1
            details = str(data.iloc[row].iloc[col])
    
    def get_name(self):
        return self.Name
    
    def get_nb_entries(self):
        return len(self.Entries)

    def get_revenue(self):
        return self.Subtotal_revenue

    def get_expense(self):
        return self.Subtotal_expense

    def get_total(self):
        return self.Subtotal