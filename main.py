import pandas as pd
import csv
from datetime import datetime
from data import get_amount , get_category ,get_date , get_desc
import matplotlib.pyplot as plt

class CSV:
    Csv_file = 'finace_tracker.csv'
    columns = ['date', 'amount' ,'category' , 'description']
    formatt = '%d-%m-%Y' 
    @classmethod
    def initalize_csv(cls):
        # reading the file
        try:
            pd.read_csv(cls.Csv_file)
        # create one if not found
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.columns)
            df.to_csv(cls.Csv_file , index=False)
    @classmethod
    def add(cls ,date, amount , category , description):
        new_entry = {
            'date':date,
            'amount': amount,
            'category': category,
            'description': description
        }
        with open(cls.Csv_file,'a' , newline="")as csvfile:
            writer = csv.DictWriter(csvfile , fieldnames = cls.columns)
            writer.writerow(new_entry)
        print('entry was added -_- ')
    @classmethod
    def get_trans(cls , start_date , end_date ):
        df = pd.read_csv(cls.Csv_file)
        df['date'] = pd.to_datetime(df['date'],format=CSV.formatt , errors='coerce' )
        start_date = datetime.strptime(start_date , CSV.formatt)
        end_date = datetime.strptime(end_date , CSV.formatt)
        mask = (df['date']>= start_date)& (df['date']<= end_date)
        filter_df = df.loc[mask]
        if filter_df.empty:
            print('no transaction is found in this date')
        else:
            print(f'transaction from {start_date.strftime(CSV.formatt)} to {end_date.strftime(CSV.formatt)}:')
            print(filter_df.to_string(index=False , formatters={'date': lambda x: x.strftime(CSV.formatt)}))
            total_income = filter_df[filter_df['category'] == 'income']['amount'].sum()
            total_expense = filter_df[filter_df['category'] == 'expense']['amount'].sum()
            print(f'Total Income: ${total_income:.2f}')
            print(f'Total Expense: ${total_expense:.2f}')
            print(f'Net Balance: ${total_income - total_expense:.2f}')
            print('thank you for using this app')
            print('-----------------------------------')
        return filter_df

def plot_df(df):
    df = df.copy()
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)  
    income = df[df['category'] == 'income']['amount'].resample('D').sum()
    expense = df[df['category'] == 'expense']['amount'].resample('D').sum()

    plt.figure(figsize=(5, 5))
    plt.plot(income.index, income.values, label='Income', color='green')
    plt.plot(expense.index, expense.values, label='Expense', color='red')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.title('Income vs Expense')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


    








def add_values():

    date = get_date('enter the date(dd-mm-yy) , or press enter for todays date: ',allow_def=True)
    amount = get_amount()
    category = get_category()
    description =  get_desc()
    CSV.add(date , amount , category , description)
def main():
    CSV.initalize_csv()
    while True:
        print('1. Add a transaction')
        print('2. Get transactions by date range')
        print('3. Exit')
        print('4. Plot transactions')
        choice = input('Enter your choice: ')
        
        if choice == '1':
            add_values()
        elif choice == '2':
            start_date = get_date('Enter start date (dd-mm-yyyy): ')
            end_date = get_date('Enter end date (dd-mm-yyyy): ')
            df_fil =CSV.get_trans(start_date, end_date)
            
        elif choice == '3':
            print('Exiting the application. Thank you!')
            break
        elif choice == '4':
            df = pd.read_csv(CSV.Csv_file)
            df['date'] = pd.to_datetime(df['date'], format=CSV.formatt, errors='coerce')
            df = df.dropna(subset=['date'])
            if df.empty:
                print('No transactions found to plot.')
            else:
                plot_df(df)

        
        else:
            print('Invalid choice. Please try again.')
main()

