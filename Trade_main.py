from AmericanStockBuySell import Alpaca
from newbie import Newbie
from trade import Recommendation
from StockUpdate import StockUpdate, symbolList
from fileio import symbolGiver
from prettytable import PrettyTable
from indicators import indicators
from tradingview_ta import TA_Handler, Interval

class trading_main:
    def __init__(self) -> None:
        pass

    @staticmethod
    def base_page(isNewbie,isInvest,money,isClosePos,getOrderSummary):
        if(isNewbie):
            return trading_main.newbie_page(isInvest,money,isClosePos,getOrderSummary)
        print("1. Buy / Sell Stocks")
        print("2. Check Account Summary")
        print("3. Close all positions")
        print("4. Subscribe to a Stock and view it's data")
        print("5. Save Indicators")
        # print("6. Get Recommendations")
        print("6. Exit")
        choice = int(input("Enter your choice  "))
        if choice == 1:
            return trading_main.trade_page()
        elif choice == 2:
            return Alpaca.account()
        elif choice == 3:
            print("Closing all positions ...")
            return Alpaca.closeAllPositions()
        elif choice == 4:
            return trading_main.stock_subscribe()
        elif choice == 5:
            a = indicators()
            stock = input("Enter the stock you want to save indicators for  ")
            stock = symbolGiver.input_stock(stock)
            if(stock) == 'xxxx':
                print("Invalid Stock")
                return
            date_input = input("Enter the start date in YYYY-MM-DD format  ")
            date_output = input("Enter the end date in YYYY-MM-DD format  ")
            enter = input(
                "Enter the number of days you want to enter the stock (SMA or EMA or RSI or MACD) ").upper()
            a.do(stock, date_input, date_output, enter)

        # elif choice == 6:

        elif choice == 6:
            return

    @staticmethod
    def stock_subscribe():
        isAdd = input(
            "Do you want to add a stock to your list? (y/n)  ").lower()
        if(isAdd == 'y' or isAdd == 'yes' or isAdd == 'true'):
            StockUpdate.add_symbols()
        StockUpdate.subscribe_stock(symbolList, times=5)

    @staticmethod
    def trade_page():
        list_order = list(input(
            "Enter the stocks you want to buy or sell separated by commas  ").split(','))
        symbol_list = []
        for i in list_order:
            print(i)
            symbol_list.append(symbolGiver.input_stock(i))
        recommend = Recommendation.recommendation(list_order)
        table = PrettyTable(["Stock", "Recommendation"])
        for i in recommend:
            table.add_row([i[0], i[1]])
        print("Our Recommendation for you is:")
        print(table)
        for i in range(len(list_order)):
            buy_sell = input("Do you want to buy or sell " +
                             list_order[i]+"? (buy/sell)  ").lower()
            qty = input("Enter the quantity of " +
                        list_order[i]+" you want to "+buy_sell+"  ")
            typeOfOrder = input(
                "Enter the type of order you want to place (market/limit/stop/stop_limit)  ").lower()
            if(typeOfOrder == 'market'):
                Alpaca.createMarketOrder(
                    symbol_list[i], qty, buy_sell, "market", 'gtc')
                print("Order Placed successfully")
            elif(typeOfOrder == 'limit'):
                lp = input("Enter the limit price  ")
                Alpaca.createLimitOrder(
                    symbol_list[i], qty, buy_sell, "limit", 'gtc', lp)
                print("Order Placed successfully")
            elif(typeOfOrder == 'stop'):
                sp = input("Enter the stop price  ")
                Alpaca.createStopOrder(
                    symbol_list[i], qty, buy_sell, "stop", 'gtc', sp)
                print("Order Placed successfully")
            elif(typeOfOrder == 'stop_limit'):
                lp = input("Enter the limit price  ")
                sp = input("Enter the stop price  ")
                Alpaca.createStopLimitOrder(
                    symbol_list[i], qty, buy_sell, "stop_limit", 'gtc', lp, sp)
                print("Order Placed successfully")

    @staticmethod
    def newbie_page(isInvest,money,isClosePos,getOrderSummary):
        return_list=[]
        if(isInvest):
            temp = Newbie()
            stockList = temp.findings()
            return_list.append(stockList)
            stocksymbol = []
            dict = {"Apple": "AAPL",
                    "Microsoft": "MSFT",
                    "Alphabet":"GOOG",
                    "Amazon.com":"AMZN",
                    "Facebook":"FB",
                    "Tesla":"TSLA",
                    "Nvidia" :"NVDA",
                    "PayPal Holdings":"PYPL",
                    "Meta Platforms":"META",
                    "PepsiCo":"PEP",
                    "Broadcom":"AVGO",
                    "ASML Holding N.V":"ASML",
                   "AstraZeneca" :"AZN",
                    "Costco" :"CMCSA",
                    "Cisco":"CSCO",
                    "T-MobileUS":"TMUS",
                    # "Verizon":"VZ",
                    "Adobe":"ADBE",
                    "Comcast" :"CMCSA",
                    "TexasInstruments" :"TXN",
                    "Amgen":"AMGN",
                    "Netflix":"NFLX"
                    }
            for i in stockList:
                    for j in dict.keys():
                        if((i in j) or( j in i)):
                            stocksymbol.append(dict[j])
            k=[]
            for l in stocksymbol:
                output = TA_Handler(symbol=l, screener="america",
                                exchange="NASDAQ", interval=Interval.INTERVAL_1_HOUR)
                temp=[]
                temp.append(l)
                temp.append(output.get_analysis().summary['RECOMMENDATION'])
                k.append(temp)
            # print(k)
            # print(stocksymbol)
            priceList=[]
            for i in stocksymbol:
                priceList.append(StockUpdate.find_price(i))
            # for i in priceList:
            #     print(i)
            # print(priceList)
            
            sm=0
            for i in priceList:
                a=float(''.join(i[1].split(',')))
                sm+=a
            if money==0:
                raise ValueError("Money cannot be zero")
            qty=sm//money
            if qty==0:
                qty=1  
            for i in k:
                if(i[1][-1]=='Y'):
                    Alpaca.createMarketOrder(i[0],qty,'buy','market','gtc')
                elif(i[1][0]=='N'):
                    pass
                else:
                    Alpaca.createMarketOrder(i[0],qty,'sell','market','gtc')
        
        # return_list.append(Alpaca.profit())
        
        if(isClosePos):
            Alpaca.closeAllPositions()
        if(getOrderSummary):
            return_list.append(Alpaca.account())
        return return_list

a = trading_main()
