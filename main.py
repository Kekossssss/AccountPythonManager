import argparse
from Classes.account_manager_class import Account_manager
from Utils.global_var import *
from Utils.logger import *

def main(args):
    base_folder = os.getcwd()
    set_language_pack(args.language)
    set_verbose_level(args.verbose)
    ## Create Account managers
    for i in range(len(args.folders)):
        folder = args.folders[i]
        assert os.path.isdir(folder), f"{folder} is not a valid directory path"
        os.chdir(base_folder)
        if (len(args.name) > i):
            my_accounts = Account_manager(folder, name=args.name[i])
        else:
            if folder[-1] == '/':
                name = folder.split('/')[-2]
            else:
                name = folder.split('/')[-1]
            my_accounts = Account_manager(folder, name=name)
        print_info(f"Account initialisation finished")
        my_accounts.update(args.extension_format)
        print_info(f"Account reports update finished")
        my_accounts.generate_yearly(args.extension_format)
        print_info(f"Account yearly reports finished")
        my_accounts.generate_accounts_summary(args.extension_format)
        print_info(f"Account general report finished")
        my_accounts.display(depth=args.depth, show_empty_months_message=0)
        print_info(f"Account display finished")

if __name__=="__main__":
    parser = argparse.ArgumentParser(prog="AccountManager", description="Programm used to parse excel file containing transaction informations accross different accounts, years, months and categories. Also allows one to see summaries and generate them using a file format of their choice.")
    parser.add_argument('-f', "--folders", help="Path to folders in which to find the user(s) accounts data", action='extend', nargs='+', type=str, default=[])
    parser.add_argument('-d', "--depth", help="Printing depth for account data", type=int, default=0)
    parser.add_argument('-v', "--verbose", help="Level of debug messages", action='count', default=0)
    parser.add_argument('-n', "--name", help="Overide for the account owner's names", action='extend', nargs='+', type=str, default=[])
    parser.add_argument('-l', "--language", help="Choose the language to use for parsing and summaries", type=str, default='Français', choices=['Français', 'English', 'English (USA)'])
    parser.add_argument('-e', "--extension_format", help="Choose the extension to use for output summaries", type=str, default='xlsx', choices=['xlsx'])
    args = parser.parse_args()
    main(args)