import os
import pandas as pd
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
        self.Reports_extension = report_format
        self.Accounts = {}
        self.Total = 0.0
    
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
        while line_raw != "":
            line = line_raw.split(" ")
            assert line[0] in folder_list, "One of the account does not have his folder"
            assert os.path.isdir(self.Folder_path+line[0]), "The account does not have a folder, but something else"
            acc = Account(line[0], self.Folder_path+line[0], line[1])
            self.Accounts[line[0]] = acc
            self.Total += acc.get_balance()
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
    
    def generate_accounts_summary(self, summary_file_type="xlsx"):
        """
        Function that generates complete account specific summary with all available data
        """
        summary_name = LANGUAGE_DICT['account_report']
        if len(self.Accounts.keys()) != 0:
            summary_file_path = self.Folder_path + "/" + summary_name + "_" + self.Name + "." + summary_file_type
            writer = pd.ExcelWriter(summary_file_path, mode='w', engine='openpyxl')
            for acc in self.Accounts.keys():
                account = self.Accounts[acc]
                data = pd.DataFrame(index=None, columns=None)
                data.to_excel(writer, sheet_name=f"{acc}", index=False, header=False, float_format="%.2f")
                worksheet = writer.sheets[f"{acc}"]
                len_table1, len_table2 = account.fulfill_worksheet(worksheet)
                apply_worksheet_background(worksheet)
                set_columns_size(worksheet, max(20, len_table1))
                apply_case_style(worksheet, row=2, col=2)
                apply_simple_vertical_table(worksheet, width=2, height=3, start_row=2, start_col=4, is_last_total=True)
                apply_simple_vertical_table(worksheet, width=2, height=3, start_row=2, start_col=8, is_last_percent=True)
                worksheet_table_horizontal_background(worksheet, width=len_table1, height=5, start_row=6, start_col=2, is_last_total=2)
                worksheet_table_vertical_background(worksheet, width=4, height=len_table2, start_row=53, start_col=2, is_last_total=False, is_last_col_total=True)
                generate_line_chart(
                    worksheet, title=f"{LANGUAGE_DICT['revenues']}/{LANGUAGE_DICT['expenses']}", len_table=len_table1, nb_lines=2,
                    label_row=6, data_row=7, data_col=2,
                    graph_row=11, graph_col=1, graph_height=20, graph_width=max(13, len_table1)
                )
                generate_line_chart(
                    worksheet, title=f"{LANGUAGE_DICT['total']}/{LANGUAGE_DICT['balance']}", len_table=len_table1, nb_lines=2,
                    label_row=6, data_row=9, data_col=2,
                    graph_row=31, graph_col=1, graph_height=20, graph_width=max(13, len_table1),
                    colors=["0000AA", "FF8000"]
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['revenue_per_cat'], len_table=len_table2,
                    data_row=53, data_col=3, label_col=2,
                    graph_width=4, graph_height=18, graph_row=51, graph_col=6
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['expense_per_cat'], len_table=len_table2,
                    data_row=53, data_col=4, label_col=2,
                    graph_width=4, graph_height=18, graph_row=51, graph_col=10
                )
            workbook = writer.book
            workbook.save(summary_file_path)
            workbook.close()