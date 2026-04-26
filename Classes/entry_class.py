import pandas as pd
import math
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *

#############################################################
## CLASSES                                                 ##
#############################################################
class Entry:    
    ## CLASS CONSTRUCTORS
    def __init__(self, name):
        self.Name = name
        self.Date = ""
        self.Revenue = 0.0
        self.Expense = 0.0
        self.Total = 0.0

    ## CLASS DISPLAYS
    def display(self, depth=9):
        if (depth >= 0):
            print(f"\t\t→ {self.Name} | {self.Date} | +{self.Revenue:.2f}{LANGUAGE_DICT['currency']} | -{self.Expense:.2f}{LANGUAGE_DICT['currency']} | {self.Total:.2f}{LANGUAGE_DICT['currency']}")

    ## CLASS FUNCTIONS
    def build(self, data:pd.DataFrame, row, col):
        date = str(data.iloc[row].iloc[col+1])
        self.Date = date.split(" ")[0]
        revenue = float(data.iloc[row].iloc[col+2])
        if (math.isnan(revenue) == False):
            self.Revenue = revenue
        expense = float(data.iloc[row].iloc[col+3])
        if (math.isnan(expense) == False):
            self.Expense = expense
        self.Total = self.Revenue - self.Expense
    
    def get_name(self):
        return self.Name

    def get_revenue(self):
        return self.Revenue

    def get_expense(self):
        return self.Expense

    def get_total(self):
        return self.Total