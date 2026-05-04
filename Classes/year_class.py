import pandas as pd
import datetime
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *
from Classes.month_class import Monthly_report

#############################################################
## CLASSES                                                 ##
#############################################################
class Yearly_report:    
    ## CLASS CONSTRUCTORS
    def __init__(self, year, path, init_bal=0.0):
        self.Year = year
        self.Year_folder_path = path
        self.Months = {}
        self.Yearly_Revenues = 0.0
        self.Yearly_Expenses = 0.0
        self.Yearly_Total = 0.0
        self.Initial_Balance = init_bal
        self.Current_Balance = init_bal
    
    ## CLASS DISPLAY FUNCTIONS
    def display(self, depth=9, show_empty_months_message=1):
        if (depth >= 0):
            print(colored("-----------------------------------------------", attrs=['bold']))
            print(colored(f"{LANGUAGE_DICT['display_account']} {self.Year}: +{self.Yearly_Revenues:.2f}{LANGUAGE_DICT['currency']} | -{self.Yearly_Expenses:.2f}{LANGUAGE_DICT['currency']} | {self.Yearly_Total:.2f}{LANGUAGE_DICT['currency']}", color='red', attrs=['bold']))
            print(colored("-----------------------------------------------", attrs=['bold']))
            for m in MONTHS:
                self.Months[m].display(depth - 1, show_empty_months_message=show_empty_months_message)
            print(colored("-----------------------------------------------", attrs=['bold']))
            print(colored(f"{LANGUAGE_DICT['initial_balance']}: {self.Initial_Balance:.2f}{LANGUAGE_DICT['currency']} | {LANGUAGE_DICT['actual_balance']}: {self.Current_Balance:.2f}{LANGUAGE_DICT['currency']}", color='red', attrs=['bold']))
            print(colored("-----------------------------------------------", attrs=['bold']))
    
    ## CLASS FUNCTIONS    
    def build(self):
        self.Yearly_Revenues = 0.0
        self.Yearly_Expenses = 0.0
        self.Yearly_Total = 0.0
        self.Current_Balance = self.Initial_Balance
        os.chdir(self.Year_folder_path)
        temp_file_list = os.listdir()
        temp_month_list = [i.split("_")[0] for i in temp_file_list]
        temp_extension_list = [i.split(".")[1] for i in temp_file_list]
        for m in MONTHS:
            if m in temp_month_list:
                i = 0
                while temp_month_list[i] != m:
                    i += 1
                month_path = self.Year_folder_path + "/" + m + "_" + self.Year + "." + temp_extension_list[i]
                month = Monthly_report(m, self.Current_Balance, month_path)
                month.build()
            else:
                month = Monthly_report(m, self.Current_Balance)
            self.Months[m] = month
            self.Yearly_Revenues += self.Months[m].get_revenue()
            self.Yearly_Expenses += self.Months[m].get_expense()
            self.Yearly_Total += self.Months[m].get_total()
            self.Current_Balance += self.Months[m].get_total()

    def update_categories_stat(self):
        """
        Function that updates file sheets with relevant statistics
        """
        for m in self.Months.keys():
            self.Months[m].update_categories_stat()
    
    def generate_monthly(self, summary_file_type="xlsx"):
        """
        Function that generates complete monthly summary with all available data
        """
        summary_name = LANGUAGE_DICT['monthly_report']
        summary_file_path = self.Year_folder_path + "/" + summary_name + "_" + self.Year + "." + summary_file_type
        writer = pd.ExcelWriter(summary_file_path, mode='w', engine='openpyxl')
        for m in self.Months.keys():
            month = self.Months[m]
            if (month.get_file_path() == ""):
                pass
            else:
                data = pd.DataFrame(index=None, columns=None)
                data.to_excel(writer, sheet_name=f"{m}", index=False, header=False, float_format="%.2f")
                worksheet = writer.sheets[f"{m}"]
                len_table = month.fulfill_worksheet(worksheet)
                apply_worksheet_background(worksheet)
                apply_case_style(worksheet, row=2, col=2)
                apply_simple_vertical_table(worksheet, width=2, height=3, start_row=2, start_col=4, is_last_percent=True)
                worksheet_table_vertical_background(worksheet, start_col=2, start_row=6, width=4, height=len_table+1, is_last_total=True, is_last_col_total=True)
                generate_pie_chart(
                    worksheet, 
                    title=LANGUAGE_DICT['revenues'], 
                    len_table=len_table, 
                    data_row=6, data_col=3, label_col=2, 
                    graph_width=8, graph_height=18, graph_row=1, graph_col=6
                )
                generate_pie_chart(
                    worksheet, 
                    title=LANGUAGE_DICT['expenses'], 
                    len_table=len_table, 
                    data_row=6, data_col=4, label_col=2, 
                    graph_width=8, graph_height=18, graph_row=19, graph_col=6
                )  
        workbook = writer.book
        workbook.save(summary_file_path)
        workbook.close()  
    
    def fulfill_worksheet(self, worksheet, nb_col=14):
        len_table_horizontal = 0
        worksheet.append(["" for i in range(nb_col)])
        data_list = ["" for i in range(nb_col-5)]
        data_list.insert(1, self.Year)
        data_list.insert(3, LANGUAGE_DICT['annual_revenue'])
        data_list.insert(4, self.Yearly_Revenues)
        data_list.insert(7, LANGUAGE_DICT['initial_balance'])
        data_list.insert(8, self.Initial_Balance)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-4)]
        data_list.insert(3, LANGUAGE_DICT['annual_expense'])
        data_list.insert(4, self.Yearly_Expenses)
        if (int(datetime.datetime.now().year) != int(self.Year)):
            data_list.insert(7, f"{LANGUAGE_DICT['balance']} 31/12/{self.Year}")
        else:
            data_list.insert(7, LANGUAGE_DICT['actual_balance'])
        data_list.insert(8, self.Current_Balance)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-4)]
        data_list.insert(3, LANGUAGE_DICT['bilan'])
        data_list.insert(4, self.Yearly_Total)
        data_list.insert(7, f"{LANGUAGE_DICT['evol']} (%)")
        data_list.insert(8, (self.Current_Balance-self.Initial_Balance)/self.Initial_Balance)
        worksheet.append(data_list)
        worksheet.append(["" for i in range(nb_col)])
        list_mois = ["", LANGUAGE_DICT['month']]
        list_revenus = ["", LANGUAGE_DICT['revenues']]
        list_expense = ["", LANGUAGE_DICT['expenses']]
        list_total = ["", LANGUAGE_DICT['total']]
        list_balance = ["", LANGUAGE_DICT['balance']]
        for m in MONTHS:
            list_mois.append(m)
            list_revenus.append(self.Months[m].get_revenue())
            list_expense.append(self.Months[m].get_expense())
            list_total.append(self.Months[m].get_total())
            list_balance.append(self.Months[m].get_balance())
            len_table_horizontal += 1
        worksheet.append(list_mois)
        worksheet.append(list_revenus)
        worksheet.append(list_expense)
        worksheet.append(list_total)
        worksheet.append(list_balance)
        for i in range(42):
            worksheet.append(["" for i in range(nb_col)])
        len_table_vertical = 1
        list_first_line = ["", LANGUAGE_DICT['cats'], LANGUAGE_DICT['revenues'], LANGUAGE_DICT['expenses'], LANGUAGE_DICT['total']]
        worksheet.append(list_first_line)
        for c in CATEGORIES.keys():
            list_category = ["", c]
            tot_revenue = 0.0
            tot_expense = 0.0
            tot_tot = 0.0
            for m in MONTHS:
                if (self.Months[m].get_entry(c) != None):
                    tot_revenue += self.Months[m].get_entry(c).get_revenue()
                    tot_expense += self.Months[m].get_entry(c).get_expense()
                    tot_tot += self.Months[m].get_entry(c).get_total()
            if not(tot_revenue == 0.0 and tot_expense == 0.0):
                list_category.append(tot_revenue)
                list_category.append(tot_expense)
                list_category.append(tot_tot)
                worksheet.append(list_category)
                len_table_vertical += 1
        return len_table_horizontal, len_table_vertical
    
    def get_year(self):
        return self.Year
    
    def get_nb_entries(self):
        nb_months_with_data = 0
        for m in MONTHS:
            if self.Months[m].get_nb_entries() != 0:
                nb_months_with_data += 1
        return nb_months_with_data

    def get_revenue(self):
        return self.Yearly_Revenues

    def get_expense(self):
        return self.Yearly_Expenses

    def get_total(self):
        return self.Yearly_Total
    
    def get_balance(self):
        return self.Current_Balance
