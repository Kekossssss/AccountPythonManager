import os
import math
from termcolor import colored
from Classes.account_manager_class import Account_manager
from Utils.global_var import YEARS

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
    "     E - Display specific data",
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

########################################################################
## PRINT FUNCTIONS                                                    ##
########################################################################
def print_line(line:str='', size=None):
    if size == None:
        size = os.get_terminal_size()
    print(colored("# ", color='magenta', attrs=['bold']), end='')
    print(colored(line, color='white', attrs=['bold']), end='')
    for _ in range(size.columns-len(line)-3):
        print(" ", end='')
    print(colored("#", color='magenta', attrs=['bold']))

def print_full_line(size=None):
    if size == None:
        size = os.get_terminal_size()
    for _ in range(size.columns):
        print(colored("#", color='magenta', attrs=['bold']), end='')
    print('')

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

def use_option_menu(option:str, account:Account_manager, args):
    match option:
        case "ReportGeneration":
            generate_all_reports(account=account, args=args)
            return False
        case "ReportsMenu":
            reports_menu(account=account, args=args)
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