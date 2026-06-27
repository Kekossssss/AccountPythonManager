import os
import math
from sshkeyboard import listen_keyboard, stop_listening
from termcolor import colored
from Classes.account_manager_class import Account_manager
from Classes.account_class import Account
from Utils.global_var import YEARS, MONTHS, CATEGORIES, SUBCATEGORIES

########################################################################
## TITLES                                                             ##
########################################################################
ONE_LINE_TITLE = [
    "  /$$$$$$$                  /$$                       /$$           /$$      /$$",
    " | $$__  $$                | $$                      | $$          | $$$    /$$$",
    " | $$  \\ $$ /$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$        | $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$",
    " | $$$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$|_  $$_/        | $$ $$/$$ $$ |____  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$",
    " | $$__  $$| $$  | $$| $$  | $$| $$  \\ $$| $$$$$$$$  | $$          | $$  $$$| $$  /$$$$$$$| $$  \\ $$  /$$$$$$$| $$  \\ $$| $$$$$$$$| $$  \\__/",
    " | $$  \\ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/  | $$ /$$      | $$\\  $ | $$ /$$__  $$| $$  | $$ /$$__  $$| $$  | $$| $$_____/| $$",
    " | $$$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$  |  $$$$/      | $$ \\/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$",
    " |_______/  \\______/  \\_______/ \\____  $$ \\_______/   \\___/        |__/     |__/ \\_______/|__/  |__/ \\_______/ \\____  $$ \\_______/|__/",
    "                                /$$  \\ $$                                                                      /$$  \\ $$",
    "                               |  $$$$$$/                                                                     |  $$$$$$/",
    "                                \\______/                                                                       \\______/",
    "                                                |---------------------------------|",
    "                                                | VERSION 1.0 - Made by Kekosssss |",
    "                                                |---------------------------------|"
]
ONE_LINE_TITLE_REQUIRED_WIDTH = max([len(ONE_LINE_TITLE[i]) for i in range(len(ONE_LINE_TITLE))])
ONE_LINE_TITLE_REQUIRED_HEIGHT = len(ONE_LINE_TITLE)

TWO_LINE_TITLE = [
    "  /$$$$$$$                  /$$                       /$$",
    " | $$__  $$                | $$                      | $$",
    " | $$  \\ $$ /$$   /$$  /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$",
    " | $$$$$$$ | $$  | $$ /$$__  $$ /$$__  $$ /$$__  $$|_  $$_/",
    " | $$__  $$| $$  | $$| $$  | $$| $$  \\ $$| $$$$$$$$  | $$",
    " | $$  \\ $$| $$  | $$| $$  | $$| $$  | $$| $$_____/  | $$ /$$",
    " | $$$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$  |  $$$$/",
    " |_______/  \\______/  \\_______/ \\____  $$ \\_______/   \\___/",
    "                                /$$  \\ $$",
    "                               |  $$$$$$/",
    "                                \\______/",
    "  /$$      /$$",
    " | $$$    /$$$",
    " | $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$",
    " | $$ $$/$$ $$ |____  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$",
    " | $$  $$$| $$  /$$$$$$$| $$  \\ $$  /$$$$$$$| $$  \\ $$| $$$$$$$$| $$  \\__/",
    " | $$\\  $ | $$ /$$__  $$| $$  | $$ /$$__  $$| $$  | $$| $$_____/| $$",
    " | $$ \\/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$",
    " |__/     |__/ \\_______/|__/  |__/ \\_______/ \\____  $$ \\_______/|__/",
    "                                             /$$  \\ $$",
    "                                            |  $$$$$$/",
    "                                             \\______/",
    "           |---------------------------------|",
    "           | VERSION 1.0 - Made by Kekosssss |",
    "           |---------------------------------|"
]
TWO_LINE_TITLE_REQUIRED_WIDTH = max([len(TWO_LINE_TITLE[i]) for i in range(len(TWO_LINE_TITLE))])
TWO_LINE_TITLE_REQUIRED_HEIGHT = len(TWO_LINE_TITLE)

SHORT_TITLE = [
    "    ___           _            _",
    "   / __\\_   _  __| | __ _  ___| |_",
    "  /__\\// | | |/ _` |/ _` |/ _ \\ __|",
    " / \\/  \\ |_| | (_| | (_| |  __/ |_",
    " \\_____/\\__,_|\\__,_|\\__, |\\___|\\__|",
    "                    |___/",
    "   /\\/\\   __ _ _ __   __ _  __ _  ___ _ __",
    "  /    \\ / _` | '_ \\ / _` |/ _` |/ _ \\ '__|",
    " / /\\/\\ \\ (_| | | | | (_| | (_| |  __/ |",
    " \\/    \\/\\__,_|_| |_|\\__,_|\\__, |\\___|_|",
    "                           |___/",
    "  |---------------------------------|",
    "  | VERSION 1.0 - Made by Kekosssss |",
    "  |---------------------------------|"
]
SHORT_TITLE_REQUIRED_WIDTH = max([len(SHORT_TITLE[i]) for i in range(len(SHORT_TITLE))])
SHORT_TITLE_REQUIRED_HEIGHT = len(SHORT_TITLE)

GOODBYE_TITLESCREEN = [
    "   /$$$$$$                            /$$ /$$$$$$$",
    "  /$$__  $$                          | $$| $$__  $$",
    " | $$  \\__/  /$$$$$$   /$$$$$$   /$$$$$$$| $$  \\ $$ /$$   /$$  /$$$$$$",
    " | $$ /$$$$ /$$__  $$ /$$__  $$ /$$__  $$| $$$$$$$ | $$  | $$ /$$__  $$",
    " | $$|_  $$| $$  \\ $$| $$  \\ $$| $$  | $$| $$__  $$| $$  | $$| $$$$$$$$",
    " | $$  \\ $$| $$  | $$| $$  | $$| $$  | $$| $$  \\ $$| $$  | $$| $$_____/",
    " |  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$$| $$$$$$$/|  $$$$$$$|  $$$$$$$",
    " \\______/  \\______/  \\______/  \\_______/|_______/  \\____  $$ \\_______/",
    "                                                   /$$  | $$",
    "                                                  |  $$$$$$/",
    "                                                   \\______/"
]
GOODBYE_TITLESCREEN_REQUIRED_WIDTH = max([len(GOODBYE_TITLESCREEN[i]) for i in range(len(GOODBYE_TITLESCREEN))])
GOODBYE_TITLESCREEN_REQUIRED_HEIGHT = len(GOODBYE_TITLESCREEN)

########################################################################
## MENU                                                               ##
########################################################################
MENU = [
    "Available options :",
    "     A - Generate and update all reports",
    "     Z - Reports generation menu",
    "     E - Display data",
    "     R - Change Source Location",
    "     T - Exit"
]
MENU_HEIGHT = len(MENU)

REPORTS_MENU = [
    "Available options :",
    "     A - Rebuilding/Updating data",
    "     Z - Update all transaction sheets",
    "     E - Generate monthly reports",
    "     R - Generate yearly reports",
    "     Q - Generate account summaries",
    "     S - Restrain (WIP)",
    "     D - Return to main menu"
]
REPORTS_MENU_HEIGHT = len(REPORTS_MENU)

DISPLAYDATA_MENU = [
    "Available options :",
    "     A - Transactions",
    "     Z - Subcategories",
    "     E - Categories",
    "     R - Months",
    "     Q - Years",
    "     S - Accounts",
    "     D - DataBase Queries (WIP)",
    "     F - Return to main menu"
]
DISPLAYDATA_MENU_HEIGHT = len(DISPLAYDATA_MENU)

########################################################################
## MISC FUNCTIONS                                                     ##
########################################################################
def len_str_list(l:list[str], inter_str_char=""):
    length = 0
    for i in range(len(l)):
        length += len(str(l[i]))
        if i != len(l)-1: length += len(inter_str_char)
    return length

def round_sup(val:float):
    s:float = val - float(int(val))
    if s <= 0.0 : return int(val)
    else: return int(val) + 1

def update_keys(manager:Account_manager, position:list):
    assert len(position) != 0, "Position is not a list"
    keys = []
    position_max = []
    ## Account
    if len(position) >= 1:
        acc_keys = list(manager.Accounts.keys())
        if len(acc_keys) != 0:
            if position[0] < len(acc_keys):
                keys.append(acc_keys[position[0]])
            else:
                keys.append(acc_keys[-1])
            position_max.append(len(acc_keys)-1)
            account = manager.Accounts[keys[0]]
        else:
            keys.append(None)
            position_max.append(None)
        ## Year
        if len(position) >= 2 and keys[0] != None:
            year_keys = list(account.Yearly_reports.keys())
            if len(year_keys) != 0:
                if position[1] < len(year_keys):
                    keys.append(year_keys[position[1]])
                else:
                    keys.append(year_keys[-1])
                position_max.append(len(year_keys)-1)
                year = account.Yearly_reports[keys[1]]
            else:
                keys.append(None)
                position_max.append(None)
            ## Month
            if len(position) >= 3 and keys[1] != None:
                month_keys = list(year.Months.keys())
                if len(month_keys) != 0:
                    if position[2] < len(month_keys):
                        keys.append(month_keys[position[2]])
                    else:
                        keys.append(month_keys[-1])
                    position_max.append(len(month_keys)-1)
                    month = year.Months[keys[2]]
                else:
                    keys.append(None)
                    position_max.append(None)
                ## Category
                if len(position) >= 4 and keys[2] != None:
                    category_keys = list(month.Categories.keys())
                    if len(category_keys) != 0:
                        if position[3] < len(category_keys):
                            keys.append(category_keys[position[3]])
                        else:
                            keys.append(category_keys[-1])
                        position_max.append(len(category_keys)-1)
                        category = month.Categories[keys[3]]
                    else:
                        keys.append(None)
                        position_max.append(None)
                    ## SubCategory
                    if len(position) == 5 and keys[3] != None:
                        subcategory_keys = list(category.Subcategories.keys())
                        if len(subcategory_keys) != 0:
                            if position[4] < len(subcategory_keys):
                                keys.append(subcategory_keys[position[4]])
                            else:
                                keys.append(subcategory_keys[-1])
                            position_max.append(len(subcategory_keys)-1)
                        else:
                            keys.append(None)
                            position_max.append(None)
    return keys, position_max

########################################################################
## INTERACTION FUNCTIONS                                              ##
########################################################################
input_key = ""

def compute_new_position(position:list, position_max:list, position_level:int):
    ## Compute new value
    if input_key == 'right' and position_max[position_level] != None and position[position_level] < position_max[position_level]:
        position[position_level] += 1
    elif input_key == 'left' and position[position_level] > 0:
        position[position_level] -= 1
    elif input_key == 'up' and position_level > 0:
        position_level -= 1
    elif input_key == 'down' and position_level < len(position)-1 and position_max[position_level] != None:
        position_level += 1
    ## Clamping
    for i in range(len(position_max)):
        if position[i] != None and position_max[i] != None and position[i] > position_max[i]:
            position[i] = position_max[i]
    return position, position_level

def update_terminal_position(position:list, position_max:list, position_level:int):
    print_info_message("Navigate the menu using the arrows, leave by pressing enter")
    def press(key):
        global input_key
        if key == 'right' or key == 'd':
            input_key = 'right'
            stop_listening()
        elif key == 'left' or key == 'q':
            input_key = 'left'
            stop_listening()
        elif key == 'up' or key == 'z':
            input_key = 'up'
            stop_listening()
        elif key == 'down' or key == 's':
            input_key = 'down'
            stop_listening()
        elif key == 'enter':
            input_key = 'enter'
            stop_listening()
    listen_keyboard(
        on_press=press,
        sequential=True,
    )
    return compute_new_position(position, position_max, position_level)

########################################################################
## PRINT FUNCTIONS                                                    ##
########################################################################
def print_line(line:str='', size=None, text_color="white"):
    if size == None:
        size = os.get_terminal_size()
    print(colored("# ", color='magenta', attrs=['bold']), end='')
    print(colored(line, color=text_color, attrs=['bold']), end='')
    for _ in range(size.columns-len(line)-3):
        print(" ", end='')
    print(colored("#", color='magenta', attrs=['bold']))

def print_full_line(size=None):
    if size == None:
        size = os.get_terminal_size()
    for _ in range(size.columns):
        print(colored("#", color='magenta', attrs=['bold']), end='')
    print('')

def print_highlighted_line(elements:list, size=None, position:int=None, activate_highlight=False):
    if size == None:
        size = os.get_terminal_size()
    ## Compute number of lines needed
    full_line_len = len_str_list(elements, inter_str_char=" - ") + len("#  #")
    nb_lines = round_sup(full_line_len/size.columns)
    ## Print lines
    current_line = 1
    ind_element = 0
    while current_line <= nb_lines:
        print(colored("# ", color='magenta', attrs=['bold']), end='')
        line_length = 2
        while ind_element < len(elements) and line_length + len(elements[ind_element]) + len(" - ") < size.columns - 2:
            if position == ind_element:
                if activate_highlight:
                    print(colored(elements[ind_element], color='white', on_color='on_light_magenta', attrs=['bold']), end='')
                else:
                    print(colored(elements[ind_element], color='white', on_color='on_dark_grey', attrs=['bold']), end='')
            else:
                print(colored(elements[ind_element], color='white', attrs=['bold']), end='')
            line_length += len(elements[ind_element])
            if ind_element != len(elements)-1:
                print(colored(" - ", color='white', attrs=['bold']), end='')
                line_length += len(" - ")
            ind_element += 1
        for _ in range(size.columns - line_length - 1):
            print(colored(" ", color='magenta', attrs=['bold']), end='')
        print(colored("#", color='magenta', attrs=['bold']))
        current_line += 1
    return nb_lines

def print_info_message(line):
    print(colored(line, color='white', attrs=['bold']))

def input_custom(line:str):
    user_input = input(colored(line+"\n -> ", color='white', attrs=['bold']))
    return user_input

def print_title_line(i, size):
    if ONE_LINE_TITLE_REQUIRED_WIDTH < size.columns-3 and ONE_LINE_TITLE_REQUIRED_HEIGHT < size.lines-3:
        if i >= int(size.lines/2) - math.floor(ONE_LINE_TITLE_REQUIRED_HEIGHT/2) and i < int(size.lines/2) + math.ceil(ONE_LINE_TITLE_REQUIRED_HEIGHT/2):
            print_line(line=ONE_LINE_TITLE[i-(int(size.lines/2) - math.floor(ONE_LINE_TITLE_REQUIRED_HEIGHT/2))], size=size)
        else:
            print_line(size=size)
    elif TWO_LINE_TITLE_REQUIRED_WIDTH < size.columns-3 and TWO_LINE_TITLE_REQUIRED_HEIGHT < size.lines-3:
        if i >= int(size.lines/2) - math.floor(TWO_LINE_TITLE_REQUIRED_HEIGHT/2) and i < int(size.lines/2) + math.ceil(TWO_LINE_TITLE_REQUIRED_HEIGHT/2):
            print_line(line=TWO_LINE_TITLE[i-(int(size.lines/2) - math.floor(TWO_LINE_TITLE_REQUIRED_HEIGHT/2))], size=size)
        else:
            print_line(size=size)
    else:
        if i >= int(size.lines/2) - math.floor(SHORT_TITLE_REQUIRED_HEIGHT/2) and i < int(size.lines/2) + math.ceil(SHORT_TITLE_REQUIRED_HEIGHT/2):
            print_line(line=SHORT_TITLE[i-(int(size.lines/2) - math.floor(SHORT_TITLE_REQUIRED_HEIGHT/2))], size=size)
        else:
            print_line(size=size)

def print_title():
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    for i in range(size.lines-2):
        if i == 0 or i == size.lines-3:
            print_full_line(size=size)
        else:
            print_title_line(i, size)

def print_menu_line(i, size):
    if i >= 7 and i - 7 < MENU_HEIGHT:
        print_line(line=MENU[i-7], size=size)
    else:
        print_line(size=size)

def print_menu(account:Account_manager, source="Exemple/", name="Default"):
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    for i in range(size.lines-2):
        if i == 0 or i == size.lines-3:
            print_full_line(size=size)
        elif i == 2:
            print_line(line=f"Welcome {name} !", size=size)
        elif i == 3:
            print_line(line=f"Current source folder : {source}", size=size)
        elif i == 4:
            print_line(line="", size=size)
        elif i == 5:
            print_line(line=f"Current Total Balance : {account.Total:.2f}€", size=size)
        else:
            print_menu_line(i, size)

def print_reports_menu_line(i, size):
    if i >= 5 and i - 5 < REPORTS_MENU_HEIGHT:
        print_line(line=REPORTS_MENU[i-5], size=size)
    else:
        print_line(size=size)

def print_reports_menu(account:Account_manager):
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    for i in range(size.lines-2):
        if i == 0 or i == size.lines-3:
            print_full_line(size=size)
        elif i == 2:
            print_line(f"Accounts : {[k for k in account.Accounts.keys()]}")
        elif i == 3:
            print_line(f"Years with data : {YEARS}")
        else:
            print_reports_menu_line(i, size)

def print_displayData_menu_line(i, size):
    if i >= 5 and i - 5 < DISPLAYDATA_MENU_HEIGHT:
        print_line(line=DISPLAYDATA_MENU[i-5], size=size)
    else:
        print_line(size=size)

def print_displayData_menu(account:Account_manager):
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    for i in range(size.lines-2):
        if i == 0 or i == size.lines-3:
            print_full_line(size=size)
        elif i == 2:
            print_line(f"Accounts : {[k for k in account.Accounts.keys()]}")
        elif i == 3:
            print_line(f"Years with data : {YEARS}")
        else:
            print_displayData_menu_line(i, size)

def print_interactive_choice_lines(lines_printed, account:Account_manager, position:list, position_level:int, keys, size):
    if len(position) >= 1 and keys[0] != None:
        print_line(f"Account :", text_color='red', size=size)
        lines_printed += 1
        lines_printed += print_highlighted_line([k for k in account.Accounts.keys()], position=position[0], size=size, activate_highlight=(position_level==0))
        if len(position) >= 2 and keys[1] != None:
            print_line(f"Years :", text_color='red', size=size)
            lines_printed += 1
            lines_printed += print_highlighted_line([k for k in account.Accounts[keys[0]].Yearly_reports.keys()], position=position[1], size=size, activate_highlight=(position_level==1))
            if len(position) >= 3 and keys[2] != None:
                print_line(f"Month :", text_color='red', size=size)
                lines_printed += 1
                lines_printed += print_highlighted_line([k for k in account.Accounts[keys[0]].Yearly_reports[keys[1]].Months.keys()], position=position[2], size=size, activate_highlight=(position_level==2))
                if len(position) >= 4 and keys[3] != None:
                    print_line(f"Category :", text_color='red', size=size)
                    lines_printed += 1
                    lines_printed += print_highlighted_line([k for k in account.Accounts[keys[0]].Yearly_reports[keys[1]].Months[keys[2]].Categories.keys()], position=position[3], size=size, activate_highlight=(position_level==3))
                    if len(position) == 5 and keys[4] != None:
                        print_line(f"Sub-Category :", text_color='red', size=size)
                        lines_printed += 1
                        lines_printed += print_highlighted_line([k for k in account.Accounts[keys[0]].Yearly_reports[keys[1]].Months[keys[2]].Categories[keys[3]].Subcategories.keys()], position=position[4], size=size, activate_highlight=(position_level==4))
    return lines_printed

def print_year(lines_printed:int, manager:Account_manager, keys, size):
    print_line(f"", size=size)
    print_line(f"Years :", text_color='red', size=size)
    lines_printed += 2
    if (None in keys):
        print_line(f"    No Yearly Data available for this Account", size=size)
        lines_printed += 1
    else:
        account = manager.Accounts[keys[0]]
        for k in account.Yearly_reports.keys():
            year = account.Yearly_reports[k]
            print_line(f"    {year.Year} | {year.Yearly_Total:.2f}€ | {year.Forecast:.2f}€ | {year.Initial_Balance:.2f}€ | {year.Current_Balance:.2f}€ | {year.Expected_Balance:.2f}€")
            lines_printed += 1
        print_line(f"    TOTAL : {account.Bilan:.2f}€ | FORECAST : {account.Forecast:.2f}€")
        print_line(f"    INITIAL BALANCE : {account.Initial_Balance:.2f}€ | FINAL BALANCE : {account.Balance:.2f}€ | EXPECTED BALANCE : {account.Expected_Balance:.2f}€")
        lines_printed += 2
    while lines_printed < size.lines-3:
        print_line(f"", size=size)
        lines_printed += 1
    return lines_printed

def print_month(lines_printed:int, manager:Account_manager, keys, size):
    print_line(f"", size=size)
    print_line(f"Months :", text_color='red', size=size)
    lines_printed += 2
    if (None in keys):
        print_line(f"    No Monthly Data available for this selection", size=size)
        lines_printed += 1
    else:
        year = manager.Accounts[keys[0]].Yearly_reports[keys[1]]
        for k in year.Months.keys():
            month = year.Months[k]
            print_line(f"    {month.Month} | {month.Monthly_Total:.2f}€ | {month.Forecast:.2f}€ | {month.Initial_Balance:.2f}€ | {month.Current_Balance:.2f}€ | {month.Expected_Balance:.2f}€")
            lines_printed += 1
        print_line(f"    TOTAL : {year.Yearly_Total:.2f}€ | FORECAST : {year.Forecast:.2f}€")
        print_line(f"    INITIAL BALANCE : {year.Initial_Balance:.2f}€ | FINAL BALANCE : {year.Current_Balance:.2f}€ | EXPECTED BALANCE : {year.Expected_Balance:.2f}€")
        lines_printed += 2
    while lines_printed < size.lines-3:
        print_line(f"", size=size)
        lines_printed += 1
    return lines_printed

def print_categories(lines_printed:int, manager:Account_manager, keys, size):
    print_line(f"", size=size)
    print_line(f"Categories :", text_color='red', size=size)
    lines_printed += 2
    if (None in keys):
        print_line(f"    No Categories available for this selection", size=size)
        lines_printed += 1
    else:
        month = manager.Accounts[keys[0]].Yearly_reports[keys[1]].Months[keys[2]]
        for k in month.Categories.keys():
            category = month.Categories[k]
            print_line(f"    {category.Name} | {category.Category_Total:.2f}€ | {category.Forecast:.2f}€")
            lines_printed += 1
        print_line(f"    TOTAL : {month.Monthly_Total:.2f}€ | FORECAST : {month.Forecast:.2f}€")
        print_line(f"    INITIAL BALANCE : {month.Initial_Balance:.2f}€ | FINAL BALANCE : {month.Current_Balance:.2f}€ | EXPECTED BALANCE : {month.Expected_Balance:.2f}€")
        lines_printed += 2
    while lines_printed < size.lines-3:
        print_line(f"", size=size)
        lines_printed += 1
    return lines_printed

def print_subcategories(lines_printed:int, manager:Account_manager, keys, size):
    print_line(f"", size=size)
    print_line(f"Sub-Categories :", text_color='red', size=size)
    lines_printed += 2
    if (None in keys):
        print_line(f"    No Sub-Categories available for this selection", size=size)
        lines_printed += 1
    else:
        category = manager.Accounts[keys[0]].Yearly_reports[keys[1]].Months[keys[2]].Categories[keys[3]]
        for k in category.Subcategories.keys():
            subcategory = category.Subcategories[k]
            print_line(f"    {subcategory.Name} | {subcategory.Subtotal:.2f}€ | {subcategory.Forecast:.2f}€")
            lines_printed += 1
        print_line(f"    TOTAL : {category.Category_Total:.2f}€ | FORECAST : {category.Forecast:.2f}€")
        lines_printed += 1
    while lines_printed < size.lines-3:
        print_line(f"", size=size)
        lines_printed += 1
    return lines_printed

def print_transactions(lines_printed:int, manager:Account_manager, keys, size):
    print_line(f"", size=size)
    print_line(f"Transactions :", text_color='red', size=size)
    lines_printed += 2
    if (None in keys):
        print_line(f"    No transaction data available for this selection", size=size)
        lines_printed += 1
    else:
        subcategory = manager.Accounts[keys[0]].Yearly_reports[keys[1]].Months[keys[2]].Categories[keys[3]].Subcategories[keys[4]]
        for e in subcategory.Entries:
            print_line(f"    {e.Name} | {e.Date} | {e.Total:.2f}€")
            lines_printed += 1
        print_line(f"    TOTAL : {subcategory.Subtotal:.2f}€ | FORECAST : {subcategory.Forecast:.2f}€")
        lines_printed += 1
    while lines_printed < size.lines-3:
        print_line(f"", size=size)
        lines_printed += 1
    return lines_printed

def print_interactive_choice_data(lines_printed:int, manager:Account_manager, position:list, keys, size):
    if len(position) == 1:
        lines_printed = print_year(lines_printed, manager, keys, size)
    elif len(position) == 2:
        lines_printed = print_month(lines_printed, manager, keys, size)
    elif len(position) == 3:
        lines_printed = print_categories(lines_printed, manager, keys, size)
    elif len(position) == 4:
        lines_printed = print_subcategories(lines_printed, manager, keys, size)
    elif len(position) == 5:
        lines_printed = print_transactions(lines_printed, manager, keys, size)
    return lines_printed

def print_interactive_choice_menu(account:Account_manager, position:list, position_max:list, position_level:int, keys):
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    print_full_line(size=size)
    lines_printed = print_interactive_choice_lines(
        1, account, position, position_level, keys, size
    )
    lines_printed = print_interactive_choice_data(
        lines_printed, account, position, keys, size
    )
    print_full_line(size=size)
    return update_terminal_position(position, position_max, position_level)

def print_goodbye_line(i, size):
    if i >= int(size.lines/2) - math.floor(GOODBYE_TITLESCREEN_REQUIRED_HEIGHT/2) and i < int(size.lines/2) + math.ceil(GOODBYE_TITLESCREEN_REQUIRED_HEIGHT/2):
        print_line(line=GOODBYE_TITLESCREEN[i-(int(size.lines/2) - math.floor(GOODBYE_TITLESCREEN_REQUIRED_HEIGHT/2))], size=size)
    else:
        print_line(size=size)

def print_goodbye():
    os.system('cls' if os.name == 'nt' else 'clear')
    size = os.get_terminal_size()
    for i in range(size.lines-2):
        if i == 0 or i == size.lines-3:
            print_full_line(size=size)
        else:
            print_goodbye_line(i, size)

########################################################################
## DATA SORTING FUNCTIONS                                             ##
########################################################################
def assign_inputs_menu(x:str):
    x = x.capitalize()
    match x:
        case 'A' | '1':
            return "ReportGeneration"
        case 'Z' | '2':
            return "ReportsMenu"
        case 'E' | '3':
            return "DataDisplay"
        case 'T' | '5':
            return "End"
        case _:
            return "Unknown"

def assign_inputs_reports(x:str):
    x = x.capitalize()
    match x:
        case 'A' | '1':
            return "Rebuild"
        case 'Z' | '2':
            return "UpdateTransaction"
        case 'E' | '3':
            return "MonthlyReports"
        case 'R' | '4':
            return "YearlyReports"
        case 'Q' | '5':
            return "AccountSummaries"
        case 'S' | '6':
            return "Restrain"
        case 'D' | '7':
            return "End"
        case _:
            return "Unknown"

def assign_inputs_displayData(x:str):
    x = x.capitalize()
    match x:
        case 'A' | '1':
            return "Transaction"
        case 'Z' | '2':
            return "SubCategory"
        case 'E' | '3':
            return "Category"
        case 'R' | '4':
            return "Month"
        case 'Q' | '5':
            return "Year"
        case 'S' | '6':
            return "Account"
        case 'D' | '7':
            return "DataQueries"
        case 'F' | '8':
            return "End"
        case _:
            return "Unknown"

########################################################################
## DATA MANAGEMENT FUNCTIONS                                          ##
########################################################################
def check_name_characters(name):
    ##TODO: Verify name and return False as well as the incorrect characters if there is an issue
    return True, ""

def generate_all_reports(account:Account_manager, args):
    print_menu(account, source=account.Folder_path, name=account.Name)
    print_info_message("Reloading source data and updating subcategories data, please wait...")
    account.update()
    print_menu(account, source=account.Folder_path, name=account.Name)
    print_info_message("Generating monthly reports, please wait...")
    account.generate_monthly(summary_file_type=args.extension_format)
    print_menu(account, source=account.Folder_path, name=account.Name)
    print_info_message("Generating yearly reports, please wait...")
    account.generate_yearly(summary_file_type=args.extension_format)
    print_menu(account, source=account.Folder_path, name=account.Name)
    print_info_message("Generating account summaries, please wait...")
    account.generate_accounts_summary(summary_file_type=args.extension_format)

########################################################################
## TERMINAL PAGE FUNCTIONS                                            ##
########################################################################
def init_terminal():
    print_title()
    input_custom("Continue ?")

def check_sources(args, previous_wrong=False):
    if len(args.folders) == 0:
        ## Add a source to use
        print_title()
        source = input_custom(f"Specify the path to your source folder{"" if previous_wrong==False else " (Previous result was not a valid path)"}")
        if os.path.isdir(source) == False:
            check_sources(args, previous_wrong=True)
        else:
            return source
    elif len(args.folders) == 1:
        return args.folders[0]
    else:
        ##TODO: Choose one of the sources (only one at a time is supported in interactive mode)
        return args.folders[0]

def check_name(args, previous_wrong=False, false_characters=""):
    if len(args.name) == 0:
        ## Add a name to use
        print_title()
        name = input_custom(f"Specify the name you want to use for this source{"" if previous_wrong==False else f" (Previous result contained forbiden characters : {false_characters})"}")
        verdict, false_character = check_name_characters(name)
        if verdict:
            return name
        else:
            check_name(args, previous_wrong=True, false_characters=false_character)
    elif len(args.name) == 1:
        return args.name[0]
    else:
        ##TODO: Choose one of the names (only one at a time is supported in interactive mode)
        return args.name[0]

def use_option_reports(option:str, account:Account_manager, args):
    match option:
        case "Rebuild":
            print_reports_menu(account=account)
            print_info_message("Reloading source data, please wait...")
            account.build()
            return False
        case "UpdateTransaction":
            print_reports_menu(account=account)
            print_info_message("Updating subcategories data, please wait...")
            account.update_categories_stat()
            return False
        case "MonthlyReports":
            print_reports_menu(account=account)
            print_info_message("Generating monthly reports, please wait...")
            account.generate_monthly(summary_file_type=args.extension_format)
            return False
        case "YearlyReports":
            print_reports_menu(account=account)
            print_info_message("Generating yearly reports, please wait...")
            account.generate_yearly(summary_file_type=args.extension_format)
            return False
        case "AccountSummaries":
            print_reports_menu(account=account)
            print_info_message("Generating account summaries, please wait...")
            account.generate_accounts_summary(summary_file_type=args.extension_format)
            return False
        case "Restrain":
            print_reports_menu(account=account)
            print_info_message("Feature not yet supported")
            return False
        case "End":
            return False
        case "Unknown":
            return True
        case _:
            assert False, f"UNKNOWN INPUT {option}"

def reports_menu(account:Account_manager, args):
    user_input = ""
    option = "Start"
    wrong_input = False
    while option != "End":
        print_reports_menu(account=account)
        user_input = input_custom(f"What do you want to do ? (A, Z, E, ...){"" if not wrong_input else f" (Previous input unrecognized : {user_input})"}")
        option = assign_inputs_reports(user_input)
        wrong_input = use_option_reports(option=option, account=account, args=args)

def use_option_displayData(option:str, account:Account_manager, args):
    ##TODO: Add 'ALL_YEARS' or 'ALL_MONTHS' options when it makes sense to show, for exemple, expenses in a subcategory across the whole year
    match option:
        case "Transaction":
            position_level = 0
            position = [0, 0, 0, 0, 0]
            while input_key != 'enter':
                keys, position_max = update_keys(account, position)
                position, position_level = print_interactive_choice_menu(account, position, position_max, position_level, keys)
            return False
        case "SubCategory":
            position_level = 0
            position = [0, 0, 0, 0]
            while input_key != 'enter':
                keys, position_max = update_keys(account, position)
                position, position_level = print_interactive_choice_menu(account, position, position_max, position_level, keys)
            return False
        case "Category":
            position_level = 0
            position = [0, 0, 0]
            while input_key != 'enter':
                keys, position_max = update_keys(account, position)
                position, position_level = print_interactive_choice_menu(account, position, position_max, position_level, keys)
            return False
        case "Month":
            position_level = 0
            position = [0, 0]
            while input_key != 'enter':
                keys, position_max = update_keys(account, position)
                position, position_level = print_interactive_choice_menu(account, position, position_max, position_level, keys)
            return False
        case "Year":
            position_level = 0
            position = [0]
            while input_key != 'enter':
                keys, position_max = update_keys(account, position)
                position, position_level = print_interactive_choice_menu(account, position, position_max, position_level, keys)
            return False
        case "DataQueries":
            return False
        case "End":
            return False
        case "Unknown":
            return True
        case _:
            assert False, f"UNKNOWN INPUT {option}"

def displayData_menu(account:Account_manager, args):
    user_input = ""
    option = "Start"
    wrong_input = False
    while option != "End":
        print_displayData_menu(account=account)
        user_input = input_custom(f"What do you want to do ? (A, Z, E, ...){"" if not wrong_input else f" (Previous input unrecognized : {user_input})"}")
        option = assign_inputs_displayData(user_input)
        wrong_input = use_option_displayData(option=option, account=account, args=args)

def use_option_menu(option:str, account:Account_manager, args):
    match option:
        case "ReportGeneration":
            generate_all_reports(account=account, args=args)
            return False
        case "ReportsMenu":
            reports_menu(account=account, args=args)
            return False
        case "DataDisplay":
            displayData_menu(account=account, args=args)
            return False
        case "End":
            return False
        case "Unknown":
            return True
        case _:
            assert False, f"UNKNOWN INPUT {option}"

########################################################################
## EXTERNAL USE FUNCTIONS                                             ##
########################################################################
def interactive_mode(args):
    ## Initialisation of the program necessary values
    init_terminal()
    source = check_sources(args)
    name = check_name(args)
    account = Account_manager(source, name=name)
    print_title()
    print_info_message("Loading source folder and building up data, please wait...")
    account.build()
    ## Menu terminal
    user_input = ""
    option = "Start"
    wrong_input = False
    while option != "End":
        print_menu(account, source=source, name=name)
        user_input = input_custom(f"What do you want to do ? (A, Z, E, ...){"" if not wrong_input else f" (Previous input unrecognized : {user_input})"}")
        option = assign_inputs_menu(user_input)
        wrong_input = use_option_menu(option=option, account=account, args=args)
    print_goodbye()