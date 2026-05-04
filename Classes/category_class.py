import pandas as pd
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *
from Classes.subcategory_class import Subcategory_report

#############################################################
## CLASSES                                                 ##
#############################################################
class Category_report:    
    ## CLASS CONSTRUCTORS
    def __init__(self, name):
        if name not in CATEGORIES:
            CATEGORIES[name] = []
        self.Name = name
        self.Subcategories = {}
        self.Category_Revenues = 0.0
        self.Category_Expenses = 0.0
        self.Category_Total = 0.0
    
    ## CLASS DISPLAYS
    def display(self, depth=9):
        if (depth >= 0):
            print(colored(f"■ {self.Name}: +{self.Category_Revenues:.2f}{LANGUAGE_DICT['currency']} | -{self.Category_Expenses:.2f}{LANGUAGE_DICT['currency']} | {self.Category_Total:.2f}{LANGUAGE_DICT['currency']}", color='green', attrs=['bold']))
            for sub in self.Subcategories.keys():
                self.Subcategories[sub].display(depth - 1)
    
    ## CLASS FUNCTIONS
    def add_subcategory(self, name):
        subcategory = Subcategory_report(name, self.Name)
        self.Subcategories[name] = subcategory
    
    def build(self, data:pd.DataFrame):
        self.Category_Revenues = 0.0
        self.Category_Expenses = 0.0
        self.Category_Total = 0.0
        for i in range(data.__len__()):
            for j in range(1, data.iloc[i].__len__(), 6):
                Sub = str(data.iloc[i].iloc[j]).capitalize()
                if (Sub != "Nan"):
                    self.add_subcategory(Sub)
                    self.Subcategories[Sub].build(data, i, j)
                    self.Category_Revenues += self.Subcategories[Sub].get_revenue()
                    self.Category_Expenses += self.Subcategories[Sub].get_expense()
                    self.Category_Total += self.Subcategories[Sub].get_total()
    
    def fulfill_worksheet(self, data, remove_null=True):
        len_table = 1
        for sub in self.Subcategories.keys():
            sub_list = []
            sub_list.append(sub)
            sub_list.append(self.Subcategories[sub].get_revenue())
            sub_list.append(self.Subcategories[sub].get_expense())
            if (sub_list[1] == 0.0 and sub_list[2] == 0.0 and remove_null):
                pass
            else:
                len_table += 1
                data.append(sub_list)
        return len_table
    
    def get_name(self):
        return self.Name
    
    def get_nb_entries(self):
        return len(self.Subcategories.keys())

    def get_revenue(self):
        return self.Category_Revenues

    def get_expense(self):
        return self.Category_Expenses

    def get_total(self):
        return self.Category_Total