import os
import pandas as pd
import datetime
from termcolor import colored
from Utils.misc_excel_functions import *
from Classes.account_class import Account
from Utils.global_var import *

#############################################################
## CLASSES                                                 ##
#############################################################
class Account_manager:
    ## CLASS CONSTRUCTORS
    def __init__(self, path_to_folder, name, report_format="xlsx"):
        """
        Class enabling a user to manage different accounts and the yearly (or monthly, per category...) 
        expenses made with each one of them.

        Args:
            path_to_folder (str): Relative/Direct path to users budget folder
            name (str, optional): User name (defaults to "Me").
            report_format (str, optional): Format used to output the report files (defaults to xlsx format) (Only supports xlsx for now)
        """
        self.Name = name
        os.chdir(path_to_folder)
        self.Folder_path = os.getcwd() + '/'
        self.InitDate = None
        self.UpdateDate = f"{datetime.datetime.now().day}/{datetime.datetime.now().month}/{datetime.datetime.now().year}"
        self.Reports_extension = report_format
        self.Accounts = {}
        self.Forecast = 0.0
        self.Initial_total = 0.0
        self.Total = 0.0
        self.Expected_Balance = 0.0
    
    ## CLASS DISPLAY FUNCTIONS
    def display(self, accounts=[], depth=9, accounts_depth=None, show_empty_months_message=1):
        """
        Display function for looking into accounts data.

        Args:
            accounts (list[str], optional): Used to specify accounts name to give a description of (defaults to all accounts).
            depth (int, optional): Number of levels to show (defaults to all levels) (0 = Account balance, 1 = Yearly, 2 = Monthly,...).
            accounts_depth (list[tuples(str, int)], optional): Used to specify which accounts to show, and to what depth for each one of them through a list of lists (Use a value superior to 6 if you want maximum depth).
            show_empty_months_message (bool, optional): Used to specify if you want a message to warn you that there is no data for a specific month (defaults to 1).
        """
        print(colored("#############################################################################", color='magenta', attrs=['bold']))
        print(colored(f"\t\t{LANGUAGE_DICT['display_account_manager']} {self.Name} : {self.Total:.2f}{LANGUAGE_DICT['currency']}", color='magenta', attrs=['bold']))
        print(colored("#############################################################################", color='magenta', attrs=['bold']))
        if (accounts_depth != None):
            for i in range(len(accounts_depth)):
                acc = accounts_depth[i][0]
                dep = accounts_depth[i][1]
                if acc in self.Accounts.keys():
                    if (dep >= 0):
                        self.Accounts[acc].display(dep, show_empty_months_message=show_empty_months_message)
        else:
            if len(accounts) == 0:
                for acc in self.Accounts.keys():
                    if (depth >= 0):
                        self.Accounts[acc].display(depth, show_empty_months_message=show_empty_months_message)
            else:
                for acc in accounts:
                    if acc in self.Accounts.keys():
                        if (depth >= 0):
                            self.Accounts[acc].display(depth, show_empty_months_message=show_empty_months_message)
                    else:
                        print(f"This account does not exist : {acc}")
    
    ## CLASS FUNCTIONS
    def build(self):
        """
        Function used to build the initial dictionnary of accounts present in the user's budget folder.
        """
        os.chdir(self.Folder_path)
        folder_list = os.listdir()
        assert LANGUAGE_DICT['init_account'] in folder_list, "Initialisation File is not in main folder"
        file = open(LANGUAGE_DICT['init_account'])
        line_raw = file.readline()
        ## Grab initdate
        line = line_raw.split(' ')
        assert line[0] == "InitDate", "Initialisation date is not in init file"
        self.InitDate = line[1]
        line_raw = file.readline()
        self.Forecast = 0.0
        self.Initial_total = 0.0
        self.Total = 0.0
        self.Expected_Balance = 0.0
        while line_raw != "":
            line = line_raw.split(" ")
            assert line[0] in folder_list, "One of the account does not have his folder"
            assert os.path.isdir(self.Folder_path+line[0]), "The account does not have a folder, but something else"
            acc = Account(line[0], self.Folder_path+line[0], line[1])
            acc.build()
            self.Accounts[line[0]] = acc
            self.Forecast += acc.get_forecast()
            self.Initial_total += float(line[1])
            self.Total += acc.get_balance()
            self.Expected_Balance += acc.get_expected_balance()
            line_raw = file.readline()

    def update_categories_stat(self):
        """
        Function that updates file sheets with relevant statistics
        """
        for acc in self.Accounts.keys():
            self.Accounts[acc].update_categories_stat()

    def generate_monthly(self, summary_file_type="xlsx"):
        """
        Function that generates complete monthly summary with all available data
        """
        for acc in self.Accounts.keys():
            self.Accounts[acc].generate_monthly(summary_file_type=summary_file_type)

    def update(self, summary_file_type="xlsx"):
        """
        Function used to update the dictionnary of accounts present in the user's budget folder as well as all of the files with metrics.
        """
        self.build()
        self.update_categories_stat()
        self.generate_monthly(summary_file_type=summary_file_type)

    def generate_yearly(self, summary_file_type="xlsx"):
        """
        Function that generates complete yearly summary with all available data
        """
        for acc in self.Accounts.keys():
            self.Accounts[acc].generate_yearly(summary_file_type=summary_file_type)
    
    def fulfill_worksheet(self, worksheet):
        nb_col = max(len(self.Accounts.keys()), 9)
        len_table_horizontal = 1
        worksheet.append(["" for i in range(nb_col)])
        data_list = ["" for i in range(nb_col-3)]
        name = LANGUAGE_DICT['account_report'].split('_')
        name_proper = ""
        for a in name:
            name_proper += a + " "
        data_list.insert(1, name_proper)
        data_list.insert(3, f"{LANGUAGE_DICT['initial_balance_with_date']} {self.InitDate}")
        data_list.insert(4, self.Initial_total)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-4)]
        data_list.insert(3, f"{LANGUAGE_DICT['actual_balance_with_date']} {self.UpdateDate}")
        data_list.insert(4, self.Total)
        data_list.insert(5, LANGUAGE_DICT['balance_forecast'])
        data_list.insert(6, self.Expected_Balance)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-4)]
        data_list.insert(3, f"{LANGUAGE_DICT['evol']} (%)")
        data_list.insert(4, (self.Total-self.Initial_total)/self.Initial_total)
        data_list.insert(5, f"{LANGUAGE_DICT['evol_forecast']} (%)")
        data_list.insert(6, (self.Expected_Balance-self.Initial_total)/self.Initial_total)
        worksheet.append(data_list)
        worksheet.append(["" for i in range(nb_col)])
        list_acc = ["", LANGUAGE_DICT['account']]
        list_revenus = ["", LANGUAGE_DICT['global_revenue']]
        list_expense = ["", LANGUAGE_DICT['global_expense']]
        list_total = ["", LANGUAGE_DICT['total']]
        list_forecast = ["", LANGUAGE_DICT['forecast']]
        list_diff_forecast = ["", LANGUAGE_DICT['diff']]
        list_balance = ["", LANGUAGE_DICT['balance']]
        list_balance_forecast = ["", LANGUAGE_DICT['balance_forecast']]
        list_balance_diff_forecast = ["", LANGUAGE_DICT['diff']]
        for a in self.Accounts.keys():
            acc = self.Accounts[a]
            name = a.split('_')
            name_proper = ""
            for a in name:
                name_proper += a + " "
            list_acc.append(name_proper)
            list_revenus.append(acc.get_revenue())
            list_expense.append(acc.get_expense())
            list_total.append(acc.get_bilan())
            list_forecast.append(acc.get_forecast())
            list_diff_forecast.append(acc.get_difference())
            list_balance.append(acc.get_balance())
            list_balance_forecast.append(acc.get_expected_balance())
            list_balance_diff_forecast.append(acc.get_balance_difference())
            len_table_horizontal += 1
        worksheet.append(list_acc)
        worksheet.append(list_revenus)
        worksheet.append(list_expense)
        worksheet.append(list_total)
        worksheet.append(list_forecast)
        worksheet.append(list_diff_forecast)
        worksheet.append(list_balance)
        worksheet.append(list_balance_forecast)
        worksheet.append(list_balance_diff_forecast)
        return len_table_horizontal
    
    def generate_accounts_summary(self, summary_file_type="xlsx"):
        """
        Function that generates complete account specific summary with all available data
        """
        summary_name = LANGUAGE_DICT['account_report']
        if len(self.Accounts.keys()) != 0:
            summary_file_path = self.Folder_path + "/" + summary_name + "_" + self.Name + "." + summary_file_type
            writer = pd.ExcelWriter(summary_file_path, mode='w', engine='openpyxl')
            ## Global Account Summary
            data = pd.DataFrame(index=None, columns=None)
            data.to_excel(writer, sheet_name=f"{LANGUAGE_DICT['account_report']}", index=False, header=False, float_format="%.2f")
            worksheet = writer.sheets[f"{LANGUAGE_DICT['account_report']}"]
            len_table = self.fulfill_worksheet(worksheet)
            apply_worksheet_background(worksheet)
            set_columns_size(worksheet, max(20, len_table))
            apply_case_style(worksheet, row=2, col=2)
            apply_simple_vertical_table(worksheet,
                                        width=2, height=3, start_row=2, start_col=4,
                                        is_last_percent=True, is_last_total=True
            )
            apply_simple_vertical_table(worksheet,
                                        width=2, height=2, start_row=3, start_col=6,
                                        is_last_percent=True, is_last_total=True
            )
            apply_complex_table(worksheet,
                                start_row=6, start_col=2, width=len_table, height=9, col_width=50, start_col_width=30,
                                row_title_list=[0],
                                col_bold_list=[0], row_bold_list=[5, 8],
                                row_currency_list=[1, 2, 3, 4, 6, 7],
                                row_percent_list=[5, 8],
                                row_color_list=[3, 4, 5, 6, 7, 8],
                                row_accentuated_list=[3, 6]
            )
            ## Write per account yearly summary
            for acc in self.Accounts.keys():
                account = self.Accounts[acc]
                data = pd.DataFrame(index=None, columns=None)
                data.to_excel(writer, sheet_name=f"{acc}", index=False, header=False, float_format="%.2f")
                worksheet = writer.sheets[f"{acc}"]
                len_table1, len_table2 = account.fulfill_worksheet(worksheet)
                apply_worksheet_background(worksheet)
                set_columns_size(worksheet, max(20, len_table1))
                apply_case_style(worksheet, row=2, col=2)
                apply_simple_vertical_table(worksheet,
                                            width=2, height=3, start_row=2, start_col=4, 
                                            is_last_total=True
                )
                apply_simple_vertical_table(worksheet, 
                                            width=2, height=2, start_row=2, start_col=7, 
                                            is_last_percent=True, is_last_total=True
                )
                apply_simple_vertical_table(worksheet, 
                                            width=2, height=3, start_row=2, start_col=10, 
                                            is_last_percent=True, is_last_total=True
                )
                apply_simple_vertical_table(worksheet, 
                                            width=2, height=2, start_row=3, start_col=12, 
                                            is_last_percent=True, is_last_total=True
                )
                apply_complex_table(worksheet,
                                    start_row=6, start_col=2, width=len_table1, height=9, col_width=25,
                                    row_title_list=[0],
                                    col_bold_list=[0], row_bold_list=[5, 8],
                                    row_currency_list=[1, 2, 3, 4, 6, 7],
                                    row_percent_list=[5, 8],
                                    row_color_list=[3, 4, 5, 6, 7, 8],
                                    row_accentuated_list=[3, 6]
                )
                apply_complex_table(worksheet,
                                    width=6, height=len_table2,
                                    start_row=77, start_col=2,
                                    row_title_list=[0],
                                    col_bold_list=[0, 3],
                                    col_currency_list=[1, 2, 3, 4],
                                    col_percent_list=[5],
                                    col_color_list=[3, 4, 5]
                )
                generate_line_chart(
                    worksheet, title=f"{LANGUAGE_DICT['revenues']}/{LANGUAGE_DICT['expenses']}", len_table=len_table1, nb_lines=2,
                    label_row=6, data_row=7, data_col=2,
                    graph_row=15, graph_col=1, graph_height=20, graph_width=13
                )
                generate_line_chart(
                    worksheet, title=f"{LANGUAGE_DICT['total']} : {LANGUAGE_DICT['real']}/{LANGUAGE_DICT['forecast']}", len_table=len_table1, nb_lines=2,
                    label_row=6, data_row=9, data_col=2,
                    graph_row=35, graph_col=1, graph_height=20, graph_width=13,
                    colors=["0000AA", "0000AA"]
                )
                generate_line_chart(
                    worksheet, title=f"{LANGUAGE_DICT['balance']} : {LANGUAGE_DICT['real']}/{LANGUAGE_DICT['forecast']}", len_table=len_table1, nb_lines=2,
                    label_row=6, data_row=12, data_col=2,
                    graph_row=55, graph_col=1, graph_height=20, graph_width=13,
                    colors=["FF8000", "FF8000"]
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['revenue_per_cat'], len_table=len_table2,
                    data_row=77, data_col=3, label_col=2,
                    graph_width=3, graph_height=18, graph_row=75, graph_col=8
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['expense_per_cat'], len_table=len_table2,
                    data_row=77, data_col=4, label_col=2,
                    graph_width=3, graph_height=18, graph_row=75, graph_col=11
                )
            ## Saves file
            workbook = writer.book
            workbook.save(summary_file_path)
            workbook.close()