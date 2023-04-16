from tradingview_ta import TA_Handler, Interval
import unicorn_binance_websocket_api as unicorn
import pandas as pd
from typing import List

class Recommendation:
    def __init__(self) -> None:
        pass

    @staticmethod
    def input_stock(stock):
        r = open("sym.txt", "r")
        data = r.readlines()
        dict = {}
        indian = False
        for i in data:
            l = i.split(' ', 1)
            if(l[0] == "ABB"):
                indian = True
            if(indian == True):
                dict[(l[1][:-1]).upper()] = l[0].upper()+".NS"
            else:
                dict[(l[1][:-1]).upper()] = l[0].upper()
        stock = stock.upper()
        try:
            symbol = dict[stock]
            return symbol
        except KeyError:
            option = {}
            for i in dict.keys():
                if stock in i:
                    option[i] = dict[i]

            if len(option) == 0:
                return "xxxx"
            elif len(option) == 1:
                return list(option.values())[0]
            else:
                for key, val in option.items():
                    print(key+' - '+val)
                stock = str(input("Enter Stock symbol from this list  "))
                return stock
    @staticmethod
    def recommendation(stock:List=[]):
        if(len(stock)==0):
            stock = input().split(
                ','
            )
        temp = Recommendation()
        a=[]
        for i in stock:
            a.append(temp.input_stock(i))
        symbols=[]
        for i in a:
            i=str(i)
            if(i!='xxxx'):
                symbols.append(i.upper())
        l1=[]
        for symbol in symbols:
            l=[]
            if ( symbol[-3]!='.'and symbol[-4]=='-' ):
                symbol=symbol.replace('-', '')
                symbol = symbol+'T'
                l.append(symbol)
                l.append("Crypto")
                l.append("Binance")

            elif(symbol[-3]=='.'):
                symbol=symbol[:-3]
                l.append(symbol)
                l.append("India")
                l.append("NSE")

            else:
                l.append(symbol)
                l.append("america")
                l.append("NASDAQ")

            l1.append(l)
        k=[]
        for l in l1:
            temp=[]
            output = TA_Handler(symbol=l[0], screener=l[1],
                                exchange=l[2], interval=Interval.INTERVAL_1_HOUR)

            temp.append(l[0])
            temp.append(output.get_analysis().summary['RECOMMENDATION'])
            k.append(temp)

        return k
'''Crypto Binance'''
'''India NSE'''
'''america NASDAQ'''
