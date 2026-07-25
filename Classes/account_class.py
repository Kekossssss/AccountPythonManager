import pandas as pd
from termcolor import colored
from Utils.misc_excel_functions import *
from Utils.global_var import *
from Classes.year_class import Yearly_report

#############################################################
## CLASSES                                                 ##
#############################################################
class Account:
    ## CLASS CONSTRUCTORS
    def __init__(self, account_name, path, init_balance):
        self.Name = account_name
        self.Account_folder_path = path
        self.Yearly_reports = {}
        self.Revenues = 0.0
        self.Expenses = 0.0
        self.Bilan = 0.0
        self.Forecast = 0.0
        self.Difference = 0.0
        self.Initial_Balance = float(init_balance)
        self.Balance = float(init_balance)
        self.Expected_Balance = float(init_balance)
        self.Balance_Difference = 0.0

    ## CLASS DISPLAY FUNCTIONS
    def display(self, depth=9, show_empty_months_message=1):
        if (depth >= 0):
            print(colored("###############################################", attrs=['bold']))
            print(colored(f"{LANGUAGE_DICT['display_account']} {self.Name}: {self.Balance:.2f}{LANGUAGE_DICT['currency']}", color='blue', attrs=['bold']))
            print(colored("###############################################", attrs=['bold']))
            for year in self.Yearly_reports.keys():
                self.Yearly_reports[year].display(depth - 1, show_empty_months_message=show_empty_months_message)

    ## CLASS FUNCTIONS
    def build(self):
        self.Revenues = 0.0
        self.Expenses = 0.0
        self.Bilan = 0.0
        self.Forecast = 0.0
        self.Expected_Balance = self.Initial_Balance
        self.Balance_Difference = 0.0
        os.chdir(self.Account_folder_path)
        files_list = os.listdir()
        for i in files_list:
            path_to_folder = self.Account_folder_path + '/' + i
            if (os.path.isdir(path_to_folder)):
                if (int(i) not in YEARS):
                    YEARS.append(int(i))
                    YEARS.sort()
        for y in YEARS:
            if (str(y) in files_list):
                path_to_folder = self.Account_folder_path + '/' + str(y)
                report = Yearly_report(str(y), path_to_folder, init_bal=self.Balance)
                report.build()
                self.Yearly_reports[str(y)] = report
                self.Revenues += self.Yearly_reports[str(y)].get_revenue()
                self.Expenses += self.Yearly_reports[str(y)].get_expense()
                self.Bilan += self.Yearly_reports[str(y)].get_total()
                self.Forecast += self.Yearly_reports[str(y)].get_forecast()
                self.Balance = self.Yearly_reports[str(y)].get_balance()
                self.Expected_Balance += self.Yearly_reports[str(y)].get_forecast()
        if self.Forecast != 0.0 and self.Bilan != 0.0:
            self.Difference = ((self.Bilan - self.Forecast) / abs(self.Forecast))
        if self.Expected_Balance != 0.0 and self.Balance != 0.0:
            self.Balance_Difference = ((self.Balance - self.Expected_Balance) / abs(self.Expected_Balance))
    
    def update_categories_stat(self):
        """
        Function that updates file sheets with relevant statistics
        """
        for year in self.Yearly_reports.keys():
            self.Yearly_reports[year].update_categories_stat()
    
    def generate_monthly(self, summary_file_type="xlsx"):
        """
        Function that generates complete monthly summary with all available data
        """
        for year in self.Yearly_reports.keys():
            self.Yearly_reports[year].generate_monthly(summary_file_type=summary_file_type)
    
    def generate_yearly(self, summary_file_type="xlsx"):
        """
        Function that generates complete yearly summary with all available data
        """
        summary_name = LANGUAGE_DICT['annual_report']
        if len(self.Yearly_reports.keys()) != 0:
            summary_file_path = self.Account_folder_path + "/" + summary_name + "_" + self.Name + "." + summary_file_type
            writer = pd.ExcelWriter(summary_file_path, mode='w', engine='openpyxl')
            for y in self.Yearly_reports.keys():
                year = self.Yearly_reports[y]
                data = pd.DataFrame(index=None, columns=None)
                data.to_excel(writer, sheet_name=f"{y}", index=False, header=False, float_format="%.2f")
                worksheet = writer.sheets[f"{y}"]
                len_table1, len_table2, len_subcat_tables = year.fulfill_worksheet(worksheet)
                apply_worksheet_background(worksheet, max_row=300)
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
                                    start_row=6, start_col=2, width=13, height=9, col_width=25,
                                    row_title_list=[0],
                                    col_bold_list=[0], row_bold_list=[5, 8],
                                    row_currency_list=[1, 2, 3, 4, 6, 7],
                                    row_percent_list=[5, 8],
                                    row_color_list=[3, 4, 5, 6, 7, 8],
                                    row_accentuated_list=[3, 6]
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
                apply_complex_table(worksheet,
                                    width=6, height=len_table2,
                                    start_row=77, start_col=2,
                                    row_title_list=[0],
                                    col_bold_list=[0, 3],
                                    col_currency_list=[1, 2, 3, 4],
                                    col_percent_list=[5],
                                    col_color_list=[3, 4, 5],
                                    row_accentuated_list=[len_table2-1]
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['revenue_per_cat'], len_table=len_table2-1,
                    data_row=77, data_col=3, label_col=2,
                    graph_width=3, graph_height=18, graph_row=75, graph_col=8
                )
                generate_pie_chart(
                    worksheet, title=LANGUAGE_DICT['expense_per_cat'], len_table=len_table2-1,
                    data_row=77, data_col=4, label_col=2,
                    graph_width=3, graph_height=18, graph_row=75, graph_col=11
                )
                apply_worksheet_background(worksheet, max_row=1, max_col=100, start_row=max(95, len_table2+78), start_col=0, color="A0A0A0")
                current_row = max(95, len_table2+78) + 2
                for i in range(len(len_subcat_tables)):
                    apply_complex_table(worksheet,
                                        start_col=2, start_row=current_row, width=6, height=len_subcat_tables[i], col_width=25,
                                        row_title_list=[0],
                                        col_bold_list=[0, 3],
                                        col_currency_list=[1, 2, 3, 4],
                                        col_percent_list=[5],
                                        col_color_list=[3, 4, 5],
                                        row_accentuated_list=[len_subcat_tables[i]-1]
                    )
                    current_row += len_subcat_tables[i] + 1
            workbook = writer.book
            workbook.save(summary_file_path)
            workbook.close()
    
    def fulfill_worksheet(self, worksheet):
        nb_col = max(len(self.Yearly_reports), 12)
        len_table_horizontal = 1
        worksheet.append(["" for i in range(nb_col)])
        data_list = ["" for i in range(nb_col-7)]
        name = self.Name.split('_')
        name_proper = ""
        for a in name:
            name_proper += a + " "
        data_list.insert(1, name_proper)
        data_list.insert(3, LANGUAGE_DICT['global_revenue'])
        data_list.insert(4, self.Revenues)
        data_list.insert(6, LANGUAGE_DICT['global_forecast'])
        data_list.insert(7, self.Forecast)
        data_list.insert(9, LANGUAGE_DICT['initial_balance'])
        data_list.insert(10, self.Initial_Balance)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-7)]
        data_list.insert(3, LANGUAGE_DICT['global_expense'])
        data_list.insert(4, self.Expenses)
        data_list.insert(6, LANGUAGE_DICT['diff'])
        data_list.insert(7, self.Difference)
        data_list.insert(9, LANGUAGE_DICT['actual_balance'])
        data_list.insert(10, self.Balance)
        data_list.insert(11, LANGUAGE_DICT['actual_balance_forecast'])
        data_list.insert(12, self.Expected_Balance)
        worksheet.append(data_list)
        data_list = ["" for i in range(nb_col-5)]
        data_list.insert(3, LANGUAGE_DICT['bilan'])
        data_list.insert(4, self.Bilan)
        data_list.insert(9, f"{LANGUAGE_DICT['evol']} (%)")
        data_list.insert(10, (self.Balance-self.Initial_Balance)/self.Initial_Balance)
        data_list.insert(11, f"{LANGUAGE_DICT['evol_forecast']} (%)")
        data_list.insert(12, (self.Expected_Balance-self.Initial_Balance)/self.Initial_Balance)
        worksheet.append(data_list)
        worksheet.append(["" for i in range(nb_col)])
        list_year = ["", LANGUAGE_DICT['year']]
        list_revenus = ["", LANGUAGE_DICT['revenues']]
        list_expense = ["", LANGUAGE_DICT['expenses']]
        list_total = ["", LANGUAGE_DICT['total']]
        list_forecast = ["", LANGUAGE_DICT['forecast']]
        list_diff_forecast = ["", LANGUAGE_DICT['diff']]
        list_balance = ["", LANGUAGE_DICT['balance']]
        list_balance_forecast = ["", LANGUAGE_DICT['balance_forecast']]
        list_balance_diff_forecast = ["", LANGUAGE_DICT['diff']]
        for y in YEARS:
            if str(y) in self.Yearly_reports.keys():
                list_year.append(y)
                list_revenus.append(self.Yearly_reports[str(y)].get_revenue())
                list_expense.append(self.Yearly_reports[str(y)].get_expense())
                list_total.append(self.Yearly_reports[str(y)].get_total())
                list_forecast.append(self.Yearly_reports[str(y)].get_forecast())
                list_diff_forecast.append(self.Yearly_reports[str(y)].get_difference())
                list_balance.append(self.Yearly_reports[str(y)].get_balance())
                list_balance_forecast.append(self.Yearly_reports[str(y)].get_expected_balance())
                list_balance_diff_forecast.append(self.Yearly_reports[str(y)].get_balance_difference())
                len_table_horizontal += 1
        worksheet.append(list_year)
        worksheet.append(list_revenus)
        worksheet.append(list_expense)
        worksheet.append(list_total)
        worksheet.append(list_forecast)
        worksheet.append(list_diff_forecast)
        worksheet.append(list_balance)
        worksheet.append(list_balance_forecast)
        worksheet.append(list_balance_diff_forecast)
        for i in range(62):
            worksheet.append(["" for i in range(nb_col)])
        len_table_vertical = 1
        list_first_line = ["", LANGUAGE_DICT['cats'], LANGUAGE_DICT['revenues'], LANGUAGE_DICT['expenses'], LANGUAGE_DICT['total'], LANGUAGE_DICT['forecast'], LANGUAGE_DICT['diff']]
        worksheet.append(list_first_line)
        for c in CATEGORIES.keys():
            list_category = ["", c]
            tot_revenue = 0.0
            tot_expense = 0.0
            tot_tot = 0.0
            tot_forecast = 0.0
            tot_diff = 0.0
            for y in YEARS:
                if str(y) in self.Yearly_reports.keys():
                    for m in MONTHS:
                        if (self.Yearly_reports[str(y)].Months[m].get_entry(c) != None):
                            tot_revenue += self.Yearly_reports[str(y)].Months[m].get_entry(c).get_revenue()
                            tot_expense += self.Yearly_reports[str(y)].Months[m].get_entry(c).get_expense()
                            tot_tot += self.Yearly_reports[str(y)].Months[m].get_entry(c).get_total()
                            tot_forecast += self.Yearly_reports[str(y)].Months[m].get_entry(c).get_forecast()
                            tot_diff += self.Yearly_reports[str(y)].Months[m].get_entry(c).get_difference()
            if tot_tot != 0.0 and tot_forecast != 0.0:
                tot_diff = ((tot_tot - tot_forecast) / abs(tot_forecast))
            if not(tot_revenue == 0.0 and tot_expense == 0.0):
                list_category.append(tot_revenue)
                list_category.append(tot_expense)
                list_category.append(tot_tot)
                list_category.append(tot_forecast)
                list_category.append(tot_diff)
                worksheet.append(list_category)
                len_table_vertical += 1
        return len_table_horizontal, len_table_vertical
    
    def get_name(self):
        return self.Name
    
    def get_nb_entries(self):
        return len(self.Yearly_reports.keys())

    def get_revenue(self):
        return self.Revenues

    def get_expense(self):
        return self.Expenses

    def get_bilan(self):
        return self.Bilan

    def get_forecast(self):
        return self.Forecast

    def get_difference(self):
        return self.Difference

    def get_balance(self):
        return self.Balance

    def get_expected_balance(self):
        return self.Expected_Balance

    def get_balance_difference(self):
        return self.Balance_Difference