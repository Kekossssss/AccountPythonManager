import pandas as pd
import datetime
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *
from Classes.category_class import Category_report

#############################################################
## CLASSES                                                 ##
#############################################################
class Monthly_report:    
    ## CLASS CONSTRUCTORS
    def __init__(self, month, init_bal=0.0, path=""):
        self.Month = month
        self.Month_file_path = path
        self.Categories = {}
        self.Monthly_Revenues = 0.0
        self.Monthly_Expenses = 0.0
        self.Monthly_Total = 0.0
        self.Initial_Balance = init_bal
        self.Current_Balance = init_bal

    ## CLASS DISPLAYS
    def display(self, depth=9, show_empty_months_message=1):
        if (depth >= 0):
            if (len(self.Categories.keys()) == 0):
                if (show_empty_months_message):
                    print(colored(f"{self.Month} {LANGUAGE_DICT['no_entries']}", color="yellow", attrs=['underline' ,'bold']))
                    print("\n")
            else:
                print(colored(f"{self.Month}: {self.Current_Balance:.2f}{LANGUAGE_DICT['currency']} || +{self.Monthly_Revenues:.2f}{LANGUAGE_DICT['currency']} | -{self.Monthly_Expenses:.2f}{LANGUAGE_DICT['currency']} || {self.Monthly_Total:.2f}{LANGUAGE_DICT['currency']}", color="yellow", attrs=['underline', 'bold']))
                for cat in self.Categories.keys():
                    self.Categories[cat].display(depth - 1)
                print("\n")
    
    ## CLASS FUNCTIONS
    def add_category(self, name):
        category = Category_report(name)
        self.Categories[name] = category
    
    def build(self):
        ##TODO: Add support for csv file format
        self.Monthly_Revenues = 0.0
        self.Monthly_Expenses = 0.0
        self.Monthly_Total = 0.0
        self.Current_Balance = self.Initial_Balance
        file = pd.ExcelFile(self.Month_file_path)
        Sheet_names = file.sheet_names
        for sheet in Sheet_names:
            data = pd.read_excel(file, sheet_name=sheet)
            self.add_category(sheet)
            self.Categories[sheet].build(data)
            self.Monthly_Revenues += self.Categories[sheet].get_revenue()
            self.Monthly_Expenses += self.Categories[sheet].get_expense()
            self.Monthly_Total += self.Categories[sheet].get_total()
        self.Current_Balance += self.Monthly_Total

    def update_categories_stat(self):
        """
        Function that updates file sheets with relevant statistics
        """
        if (self.Month_file_path == ""):
            pass
        else:
            file = pd.ExcelFile(self.Month_file_path)
            Sheet_names = file.sheet_names
            for sheet in Sheet_names:
                revenue = float(self.Categories[sheet].get_revenue())
                expense = float(self.Categories[sheet].get_expense())
                total = float(self.Categories[sheet].get_total())
                list = [
                    [""     , ""     , ""   ],
                    [revenue, expense, total]
                ]
                data = pd.DataFrame(list, index=None, columns=None)
                with pd.ExcelWriter(self.Month_file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    data.to_excel(writer, sheet_name=sheet, index=False, header=False, startcol=9)
                    if not (revenue == 0 and expense == 0):
                        list_charts = [[LANGUAGE_DICT['subcats'], LANGUAGE_DICT['revenues'], LANGUAGE_DICT['expenses']]]
                        len_table = self.Categories[sheet].fulfill_worksheet(list_charts)
                        data_charts = pd.DataFrame(list_charts, index=None, columns=None)
                        data_charts.to_excel(writer, sheet_name=sheet, index=False, header=False, startcol=14, startrow=3)
                        worksheet = writer.sheets[sheet]
                        for i in range(len(worksheet._charts)-1, -1, -1):
                            del worksheet._charts[i]
                        if revenue != 0:
                            generate_pie_chart(
                                worksheet, 
                                title=LANGUAGE_DICT['revenues'], 
                                len_table=len_table, 
                                data_row=4, data_col=16, label_col=15, 
                                graph_width=8, graph_height=18, graph_row=1, graph_col=13
                            )
                            if expense != 0:
                                generate_pie_chart(
                                    worksheet, 
                                    title=LANGUAGE_DICT['expenses'], 
                                    len_table=len_table, 
                                    data_row=4, data_col=17, label_col=15, 
                                    graph_width=8, graph_height=18, graph_row=19, graph_col=13
                                )
                        else:
                            if expense != 0:
                                generate_pie_chart(
                                    worksheet, 
                                    title=LANGUAGE_DICT['expenses'], 
                                    len_table=len_table, 
                                    data_row=4, data_col=17, label_col=15, 
                                    graph_width=8, graph_height=18, graph_row=1, graph_col=13
                                )
    
    def fulfill_worksheet(self, worksheet, remove_null=True):
        worksheet.append(["", "", "", "", ""])
        worksheet.append(["", f"{self.Month}", "", LANGUAGE_DICT['initial_balance'], self.Initial_Balance])
        if (int(datetime.datetime.now().month) != (MONTHS.index(self.Month)+1)):
            worksheet.append(["", "", "", f"{LANGUAGE_DICT['balance']} 31/{MONTHS.index(self.Month)+1}", self.Current_Balance])
        else:
            worksheet.append(["", "", "", LANGUAGE_DICT['actual_balance'], self.Current_Balance])
        worksheet.append(["", "", "", f"{LANGUAGE_DICT['evol']} (%)", ((self.Current_Balance-self.Initial_Balance)/self.Initial_Balance)])
        worksheet.append(["", "", "", "", ""])
        worksheet.append(["", LANGUAGE_DICT['cats'], LANGUAGE_DICT['revenues'], LANGUAGE_DICT['expenses'], LANGUAGE_DICT['total']])
        len_table = 1
        for cat in self.Categories.keys():
            cat_list = []
            cat_list.append("")
            cat_list.append(cat)
            cat_list.append(self.Categories[cat].get_revenue())
            cat_list.append(self.Categories[cat].get_expense())
            cat_list.append(self.Categories[cat].get_total())
            if (cat_list[2] == 0.0 and cat_list[3] == 0.0 and cat_list[4] == 0.0 and remove_null):
                pass
            else:
                len_table += 1
                worksheet.append(cat_list)
        worksheet.append(["", LANGUAGE_DICT['bilan'], self.Monthly_Revenues, self.Monthly_Expenses, self.Monthly_Total])
        return len_table
    
    ## CLASS GET FUNCTIONS
    def get_month(self):
        return self.Month
    
    def get_file_path(self):
        return self.Month_file_path
    
    def get_nb_entries(self):
        return len(self.Categories.keys())
    
    def get_entries(self):
        return self.Categories.keys()
    
    def get_entry(self, key):
        if (key in self.Categories.keys()):
            return self.Categories[key]
        else:
            return None

    def get_revenue(self):
        return self.Monthly_Revenues

    def get_expense(self):
        return self.Monthly_Expenses

    def get_total(self):
        return self.Monthly_Total
    
    def get_balance(self):
        return self.Current_Balance