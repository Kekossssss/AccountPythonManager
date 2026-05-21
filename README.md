# AccountManager

Python script used to parse through transactions data for a set of accounts accross the years in order to organise it and get relevant data and informations. Also support forecasts and gives relevant informations comparing it with the current state of the account.

## Installation

In order to use this project, you first need to make sure you have the following packages installed :

```bash
termcolor, pandas, openpyxl, argparse, datetime
```

Then, clone this repository using :

```bash
git clone 
```

## Running the tool

In order to run the tool, there are a few things that need to be done :

### Creating the data structure

- Start by choosing a location where to put all of your accounts data (e.g /home/my_accounts/).
- Use the template "**Account_Init.txt**" (Use the version that best matches your prefered language) in order to inform the programm of the start date of your account management, as well as the initial balance of your accounts. Put this template at the root of your choosed location.
- Create a new folder for each account that you want to follow, pay attention to use '_' to separate words and no space (' ').
- For each one of these account, create a folder for each year where you have transactions data to follow, use the year as the name of the folder, without any additionnal characters.
- For each year, use the provided template "**Month_Year.xlsx**" (Use the version that best matches your prefered language) to enter each transaction that happened for each of the months of this year. Not all months need to be covered by a file, but do not put duplicates.
- For each month, use the "**Forecast**" sheet to put what you forecast to spend for each category and sub-category for this month. Add as much sheets as you want with different names, one for each category of transactions. Keep the provided style of tables, data and cells (although you can change the colors, font and sizes), and add as many lines or tables as you need. This enables you to add as many category and sub-categories as you want. You do not need to repercutate the changes you make in a month for all of the others, as each category/subcategory does not need to appear in every other month. Please, keep the same grammar for these, as even a case change can cause a duplicate category. Use the "DD/MM/YYYY" format for the dates and feel free to change the currency type to match your country currency.

As you've finished with these prerequisites, your directory structure should match the following :

```bash
.
+-- Account_Init.txt
+-- Bank_Account
|   +-- 2025
|       +-- November_2025.xlsx
|       +-- December_2025.xlsx
|   +-- 2026
|       +-- January_2026.xlsx
|       +-- March_2026.xlsx
|       +-- April_2026.xlsx
+-- Savings_Account
|   +-- 2026
|       +-- February_2026.xlsx
+-- Shared_Account
+-- Work_Account
```

### Tool options

To run the tool, the baseline is to use the following command line :

```bash
python3 main.py -f path/to/accounts/folder/
```

But, there are a few options that are provided in order to improve the outputs provided, which you can view by using :

```bash
python3 main.py -h
```

Alternatively, here is a list of the different options and what they do :

| Short Arg | Long Arg   | Type | Description                                |
|-----------|------------|------|--------------------------------------------|
| -h        | --help     | None | Provide some usefull tips on the arguments |
| -f        | --folders  | List | Path to folders in which to find the user(s) accounts data |
| -d        | --depth    | Int  | Printing depth for account data |
| -n        | --name     | List | Overide for the account owner's names |
| -l        | --language | Str | Choose the language to use for parsing and summaries |

Here is an exemple command for running the tool for one user accounts, in English and with subcategories informations displayed in the terminal

```bash
python3 main.py -f "/home/my_accounts/" -n "Tony_Stark" -l "English (USA)"
```

Please note that this can take some time, as modifying and creating excel files is time consuming, do not kill the jobs too soon. (6 months takes approximately 15 seconds to generate everything)

### Reviewing outputs

Once the programm as run, you'll see that you have new, and modified files in your accounts directory, you should have the following king of folder structure :

```bash
.
+-- Account_Init.txt
+-- Bank_Account
|   +-- 2025
|       +-- November_2025.xlsx
|       +-- December_2025.xlsx
|       +-- Monthly_Report_2025.xlsx
|   +-- 2026
|       +-- January_2026.xlsx
|       +-- March_2026.xlsx
|       +-- April_2026.xlsx
|       +-- Monthly_Report_2026.xlsx
|   +-- Annual_Report_Bank_Account.xlsx
+-- Savings_Account
|   +-- 2026
|       +-- February_2026.xlsx
|       +-- Monthly_Report_2026.xlsx
|   +-- Annual_Report_Savings_Account.xlsx
+-- Shared_Account
|   +-- Annual_Report_Shared_Account.xlsx
+-- Work_Account
|   +-- Annual_Report_Work_Account.xlsx
+-- Global_Report_Tony_Stark.xlsx
```

By order, you'll get :

- **Updated Transaction Data :** For each month and categories, you'll get some updated totals and pie charts to quickly see the amount you spent/won in each category, and in which subcategories.
- **Monthly Reports :** Gives a sheet for each month, with various data regarding the initial versus current balance, comparison with the forecasted balance. You also get Pie Charts as well as some comparison between real and forecasted categories spendings/revenue.
- **Yearly Reports :** Gives a sheet for each year, with various data, including balance evolution and comparison against forecasted balance. Monthly evolution of the revenue, spendings, total, balance and comparison with the monthly forecast. Line Charts to graphically see the revenue/spendings as well as the bilan and balance comparison with the forecasted. As a bonus, you also get a table and PieCharts summarizing your spendings accross the whole year for each category.
- **Global Report :** Gives a sheet for each account, as well as a sheet summarizing all accounts. Same data as the yearly report, but for all years of each account instead of the months. With the summary sheet showing the current state of each account and a global balance. Again, with comparison against the forecast.

## Quick Notes

- Currently only supports .xlsx table files, but working on adding support for more file format (both inputs and outputs)
- Currently only offer French and English (£, $), but you can add a language by simply modifying the Utils/global_var.py file, and adding the choice in the parser in main.py. Please also remember to provide a template for both Account_Init.txt and Month_Year.xlsx for the new language.
- Forecast information is not mandatory, and the sheet can simply be removed if you don't want to add this information.
- More configuration options are in the works, including limiting the summaries generated and more terminal display capabilities.
