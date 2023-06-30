import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class StockMarket:
    def __init__(self):
        self.accounts = []
        self.stock_data = pd.read_csv('stock_market_data.csv')

    def create_account(self, name, last_name, national_id, birth_date, balance):
        account = {'name': name, 'last_name': last_name, 'national_id': national_id, 'birth_date': birth_date,
                   'balance': balance, 'portfolio': {}}
        self.accounts.append(account)

    def charge_account(self, national_id, amount):
        account = self.find_account(national_id)
        if account:
            account['balance'] += amount

    def buy_stock(self, national_id, symbol, quantity):
        account = self.find_account(national_id)
        if account:
            stock_price = self.get_stock_price(symbol)
            if stock_price is not None and stock_price * quantity <= account['balance']:
                if symbol in account['portfolio']:
                    account['portfolio'][symbol] += quantity
                else:
                    account['portfolio'][symbol] = quantity
                account['balance'] -= stock_price * quantity

    def sell_stock(self, national_id, symbol, quantity):
        account = self.find_account(national_id)
        if account and symbol in account['portfolio'] and quantity <= account['portfolio'][symbol]:
            stock_price = self.get_stock_price(symbol)
            if stock_price is not None:
                account['portfolio'][symbol] -= quantity
                if account['portfolio'][symbol] == 0:
                    del account['portfolio'][symbol]
                account['balance'] += stock_price * quantity

    def get_stock_price(self, symbol):
        stock = self.stock_data[self.stock_data['Symbol'] == symbol]
        if not stock.empty:
            return stock.iloc[0]['Open']
        else:
            print(f"Error: Could not find price for symbol {symbol}.")
            return None

    def find_account(self, national_id):
        for account in self.accounts:
            if account['national_id'] ==national_id:
                return account
        return None

    def show_stock_list(self):
        sorted_stock_data = self.stock_data.sort_values(by='Open', ascending=False)
        print(sorted_stock_data[['Symbol', 'Open']])

    def show_portfolio(self, national_id):
        account = self.find_account(national_id)
        if account:
            print(f"Portfolio for {account['name']}:")
            for symbol, quantity in account['portfolio'].items():
                print(f"{symbol}: {quantity}")

    def plot_stock_chart(self, symbol):
        stock = self.stock_data[self.stock_data['Symbol'] == symbol]
        if not stock.empty:
            plt.plot(stock.index, stock['Open'])
            plt.xlabel('Day')
            plt.ylabel('Price')
            plt.title(f"Stock Price Chart for {symbol}")
            plt.show()

    def plot_regression(self):
        sns.regplot(x=self.stock_data.index, y=self.stock_data['Open'])
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.title("Stock Price Regression")
        plt.show()


class UserInterface:
    def __init__(self):
        self.stock_market = StockMarket()

    def display_menu(self):
        print("1. Show stock list")
        print("2. Buy stock")
        print("3. Sell stock")
        print("4. Show portfolio")
        print("5. Plot stock chart")
        print("6. Plot regression")
        print("7. Quit")

    def display_stock_list(self):
        self.stock_market.show_stock_list()

    def get_user_input(self):
        return input("Enter your choice: ")

    def buy_stock(self):
        national_id = input("Enter national ID: ")
        symbol = input("Enter stock symbol: ")
        quantity = int(input("Enter quantity: "))
        self.stock_market.buy_stock(national_id, symbol, quantity)

    def sell_stock(self):
        national_id = input("Enter national ID: ")
        symbol = input("Enter stock symbol: ")
        quantity = int(input("Enter quantity: "))
        self.stock_market.sell_stock(national_id, symbol, quantity)

    def show_portfolio(self):
        national_id = input("Enter national ID: ")
        self.stock_market.show_portfolio(national_id)

    def plot_stock_chart(self):
        symbol = input("Enter stock symbol: ")
        self.stock_market.plot_stock_chart(symbol)

    def plot_regression(self):
        self.stock_market.plot_regression()


def main():
    ui = UserInterface()
    while True:
        ui.display_menu()
        choice = ui.get_user_input()
        if choice == '1':
            ui.display_stock_list()
        elif choice == '2':
            national_id = input("Enter national ID: ")
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            ui.stock_market.buy_stock(national_id, symbol, quantity)
        elif choice == '3':
            national_id = input("Enter national ID: ")
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            ui.stock_market.sell_stock(national_id, symbol, quantity)
        elif choice == '4':
            national_id = input("Enter national ID: ")
            ui.stock_market.show_portfolio(national_id)
        elif choice == '5':
            symbol = input("Enter stock symbol: ")
            ui.stock_market.plot_stock_chart(symbol)
        elif choice == '6':
            ui.stock_market.plot_regression()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
