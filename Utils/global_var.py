import os

## MONTHS LANGUAGES OPTIONS
MONTHS_FR = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTHS = []

## LANGUAGE PACKS OPTIONS
FRENCH = {
    'currency': "€",
    ## File strings
    'init_account': "Comptes_initialisation.txt",
    'default_user': "Moi",
    'account_report': "Rapport_Global",
    'annual_report': "Rapport_Annuel",
    'monthly_report': "Rapport_Mensuel",
    ## Table outputs
    'revenue': "Revenu",
    'revenues': "Revenus",
    'expense': "Dépense",
    'expenses': "Dépenses",
    'percent': "Pourcentages",
    'total': "Total",
    'balance': "Balance",
    'amount': "Montant",
    'revenue_per_cat': "Revenus par catégorie",
    'expense_per_cat': "Dépenses par catégorie",
    'annual_revenue': "Revenus annuels",
    'annual_expense': "Dépenses annuelles",
    'global_revenue': "Revenus totaux",
    'global_expense': "Dépenses totales",
    'bilan': "Bilan",
    'initial_balance': "Balance initiale",
    'actual_balance': "Balance actuelle",
    'evol': "Evolution",
    'account': "Compte",
    'year': "Année",
    'month': "Mois",
    'cat': "Catégorie",
    'cats': "Catégories",
    'subcat': "Sous-Catégorie",
    'subcats': "Sous-Catégories",
    ## Display functions keys
    'display_account_manager': "Génération du rapport pour",
    'display_account': "Rapport pour",
    'no_entries': "n'a aucunes données"
}

ENGLISH = {
    'currency': "£",
    ## File strings
    'init_account': "Account_init.txt",
    'default_user': "Me",
    'account_report': "Global_Report",
    'annual_report': "Annual_Report",
    'monthly_report': "Monthly_Report",
    ## Table outputs
    'revenue': "Revenue",
    'revenues': "Revenues",
    'expense': "Expense",
    'expenses': "Expenses",
    'percent': "Percents",
    'total': "Total",
    'balance': "Balance",
    'amount': "Amount",
    'revenue_per_cat': "Revenues per category",
    'expense_per_cat': "Expenses per category",
    'annual_revenue': "Annual Revenues",
    'annual_expense': "Annual Expenses",
    'global_revenue': "Total Revenues",
    'global_expense': "Total Expenses",
    'bilan': "Bilan",
    'initial_balance': "Initial Balance",
    'actual_balance': "Current Balance",
    'evol': "Evolution",
    'account': "Account",
    'year': "Year",
    'month': "Month",
    'cat': "Category",
    'cats': "Categories",
    'subcat': "Subcategory",
    'subcats': "Subcategories",
    ## Display functions keys
    'display_account_manager': "Generating account summary for",
    'display_account': "Report for",
    'no_entries': "has no entries"
}

ENGLISH_USA = {
    'currency': "$",
    ## File strings
    'init_account': "Account_init.txt",
    'default_user': "Me",
    'account_report': "Global_Report",
    'annual_report': "Annual_Report",
    'monthly_report': "Monthly_Report",
    ## Table outputs
    'revenue': "Revenue",
    'revenues': "Revenues",
    'expense': "Expense",
    'expenses': "Expenses",
    'percent': "Percents",
    'total': "Total",
    'balance': "Balance",
    'amount': "Amount",
    'revenue_per_cat': "Revenues per category",
    'expense_per_cat': "Expenses per category",
    'annual_revenue': "Annual Revenues",
    'annual_expense': "Annual Expenses",
    'global_revenue': "Total Revenues",
    'global_expense': "Total Expenses",
    'bilan': "Bilan",
    'initial_balance': "Initial Balance",
    'actual_balance': "Current Balance",
    'evol': "Evolution",
    'account': "Account",
    'year': "Year",
    'month': "Month",
    'cat': "Category",
    'cats': "Categories",
    'subcat': "Subcategory",
    'subcats': "Subcategories",
    ## Display functions keys
    'display_account_manager': "Generating account summary for",
    'display_account': "Report for",
    'no_entries': "has no entries"
}

YEARS = []
CATEGORIES = {}
CURRENT_FOLDER = os.getcwd()

LANGUAGE_DICT = {}

## FUNCTIONS TO SET VALUES
def set_month_list(month_choosed):
    for i in month_choosed:
        MONTHS.append(i)

def set_lang_dict(lang_dict:dict):
    for k in lang_dict.keys():
        LANGUAGE_DICT[k] = lang_dict[k]

def set_language_pack(lang):
    match lang:
        case "English":
            set_month_list(MONTHS_EN)
            set_lang_dict(ENGLISH)
        case "Français":
            set_month_list(MONTHS_FR)
            set_lang_dict(FRENCH)
        case "English (USA)":
            set_month_list(MONTHS_EN)
            set_lang_dict(ENGLISH_USA)
        case _:
            print(f"{lang} is not currently supported")