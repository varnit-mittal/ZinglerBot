from indicators import indicators
from fileio import symbolGiver
import time
def ind(stock,date_input,date_output,enter):
    while(True):
        a = indicators()
        # stock = input("Enter the stock you want to save indicators for  ")
        stock = symbolGiver.input_stock(stock)
        if(stock) == 'xxxx':
            print("Invalid Stock")
            return
        a.do(stock, date_input, date_output, enter)
        time.sleep(5)
        exit()