import csv
import os
import os.path as osp
import pandas as pd

from Expenses import Expense

FILENAME = 'Expenses.csv'
FILE_PATH = osp.dirname(osp.abspath(__file__)) + '\\' + FILENAME

def main():
    # Check if the expenses file already exists 
    if not os.path.isfile(FILENAME):
        create_expenses_file(FILENAME)

#    add_exp = str(input("Do you want to add a new expense? (Y/N): "))
#    if add_exp == 'Y':

    # Get the name of expense
    name = get_expense_name()

    # Get the amount of the expense
    amount = get_expense_amount()

    # Get the category of the expense
    category = get_expense_category()

    # Write it to a csv file
    write_expenses_to_file(name, amount, category)

    # Read the file and summarize all the expenses
    summarize_expenses()


def create_expenses_file(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Amount', 'Category'])

def get_expense_name():
    name = str(input("Insert expense name: "))
    return name

def get_expense_amount():
    amount = float(input("Insert expense amount: "))
    return amount

def get_expense_category():
    # TODO: check code. Add checks to avoid bugs
    categories = {1: "Food & Drink", 2: "Home", 3: "Transport", 4: "Health", 5: "Others"}
    print("List of categories")
    for num, cat in categories.items():
          print(f"{num}. {cat}\n")
    category = int(input("""Enter your expense category number from the list above: """)) 
                      
    return categories[category]

def write_expenses_to_file(name, amount, category):
    expense = Expense(name, amount, category)
    new_exp_df = pd.DataFrame(expense.data, index=[0])
    
    # First, check if expenses had been totalized
    cur_df = pd.read_csv(FILE_PATH)
    if len(cur_df) > 1 and cur_df.iloc[-1]['Name'] == 'Total':
        # Delete 'Total' row before adding a new expense
        cur_df.drop(cur_df.tail(1).index, inplace=True)
        cur_df.to_csv(FILENAME, mode='w', index=False, header=True)
    
    # Append new expense to the existing list
    new_exp_df.to_csv(FILENAME, mode='a', index=False, header=False)
    print(f"Expense written in {FILE_PATH}")


def summarize_expenses():
    df = pd.read_csv(FILE_PATH)
    total_expenses = pd.DataFrame({'Name': 'Total', 'Amount': df['Amount'].sum()}, index=[0])
    total_expenses.to_csv(FILENAME, mode='a', index=False, header=False)
#    print(f"""The expenses are: \n {df}\n
#          Total: {df['Amount'].sum()}""")

if __name__ == "__main__":
    # import argparse
    # parser = argparse.ArgumentParser("Run Expense App")
    main()