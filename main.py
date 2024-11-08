from db.gov_spending.get_budget import BudgetCSV
import sys


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'get_gov_spending':
        BudgetCSV(2024, list(range(2017, 2025))).get_data()


    # if len(sys.argv) > 1 and sys.argv[1] == u

    else:
        print('add argument: update_budget')
