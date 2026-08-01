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
        self.Forecast = 0.0
        self.Difference = 0.0
    
    ## CLASS DISPLAYS
    def display(self, depth=9):
        if (depth >= 0):
            print(colored(f"■ {self.Name}: +{self.Category_Revenues:.2f}{LANGUAGE_DICT['currency']} | -{self.Category_Expenses:.2f}{LANGUAGE_DICT['currency']} | {self.Category_Total:.2f}{LANGUAGE_DICT['currency']} | {self.Forecast:.2f}{LANGUAGE_DICT['currency']}", color='green', attrs=['bold']))
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
    
    def build_forecast_category(self, data:pd.DataFrame, i, j):
        row = i+1
        col = j+1
        details = str(data.iloc[row].iloc[col])
        while details != LANGUAGE_DICT['total']:
            if (details != "nan" and details in self.Subcategories.keys()):
                if (str(data.iloc[row].iloc[col+1]) != "nan"):
                    self.Subcategories[details].set_forecast(float(data.iloc[row].iloc[col+1]))
                    self.Forecast += self.Subcategories[details].get_forecast()
            row += 1
            details = str(data.iloc[row].iloc[col])
        self.Difference = 0.0
        if self.Forecast != 0.0 and self.Category_Total != 0.0:
            self.Difference = ((self.Category_Total - self.Forecast) / abs(self.Forecast))
    
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

    def fulfill_worksheet_full(self, worksheet, remove_null=True):
        len_table = 1
        worksheet.append(["", self.Name, LANGUAGE_DICT['revenues'], LANGUAGE_DICT['expenses'], LANGUAGE_DICT['total'], LANGUAGE_DICT['forecast'], f"{LANGUAGE_DICT['diff']} ({LANGUAGE_DICT['currency']})", f"{LANGUAGE_DICT['diff']} (%)"])
        for sub in self.Subcategories.keys():
            sub_list = []
            sub_list.append("")
            sub_list.append(sub)
            sub_list.append(self.Subcategories[sub].get_revenue())
            sub_list.append(self.Subcategories[sub].get_expense())
            sub_list.append(self.Subcategories[sub].get_total())
            sub_list.append(self.Subcategories[sub].get_forecast())
            sub_list.append(self.Subcategories[sub].get_total() - self.Subcategories[sub].get_forecast())
            sub_list.append(self.Subcategories[sub].get_difference())
            if (sub_list[2] == 0.0 and sub_list[3] == 0.0 and sub_list[4] == 0.0 and remove_null):
                pass
            else:
                len_table += 1
                worksheet.append(sub_list)
        worksheet.append(["", LANGUAGE_DICT['bilan'], self.Category_Revenues, self.Category_Expenses, self.Category_Total, self.Forecast, self.Category_Total - self.Forecast, self.Difference])
        return len_table
    
    def get_name(self):
        return self.Name
    
    def get_nb_entries(self):
        return len(self.Subcategories.keys())

    def get_entry(self, key):
        if (key in self.Subcategories.keys()):
            return self.Subcategories[key]
        else:
            return None

    def get_revenue(self):
        return self.Category_Revenues

    def get_expense(self):
        return self.Category_Expenses

    def get_total(self):
        return self.Category_Total

    def get_forecast(self):
        return self.Forecast

    def get_difference(self):
        return self.Difference