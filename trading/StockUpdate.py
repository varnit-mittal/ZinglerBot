from fileio import symbolGiver
import pandas as pd
import datetime
import time
import requests
from typing import List
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import os
from extra_prog import StockSymbolFile
from prettytable import PrettyTable
a=StockSymbolFile()
symbolList=a.getData()
class StockUpdate:
    @staticmethod
    def find(symbol):
        # symbol="TCS.NS"
        r=requests.get(f"https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch")
        soup=BeautifulSoup(r.text,'lxml')
        previous_close_value=soup.find_all('tr',class_=['Bxz(bb)', 'Bdbw(1px)', 'Bdbs(s)' ,'Bdc($seperatorColor)', 'H(36px)'])
        name=[]
        price=[]
        for element in soup.find_all('td',class_=['C($primaryColor)','W(51%)']):
            name.append(element.text)

        for element in soup.find_all('td',class_=['Ta(end)','Fw(b)','Fz(36px)','Lh(14px)']):
            price.append(element.text)
            
        dict1=dict(zip(name,price))
        new_dict={}
        l=["Previous Close","Open","Volume","Bid","Ask"]
        for i,key in enumerate(dict1):
            if key in l:
                new_dict[key]=dict1[key]
        al=[]
        for i in l:
            try:
                al.append(new_dict[i])
            except:
                al.append("No Data")
        return (l,al)
    @staticmethod
    def subscribe_stock(stock:List,time_to=60,times=5):
        while times>0:
            first=1
            for i in stock:
                print(f"Loading ....")
                a=StockUpdate.find(i)[0]
                b=StockUpdate.find(i)[1]
                a.insert(0,"Symbol")
                if(first):
                    table=PrettyTable(a)
                    first=0
                b.insert(0,i)
                table.add_row(b)
            print(table)
            print(f"Waiting for {time_to} seconds....")
            time.sleep(time_to)
            table=""
            os.system('cls')
            times-=1
    @staticmethod
    def find_price(stock):
        lst_price=[]
        a=StockUpdate.find(stock)[0]
        b=StockUpdate.find(stock)[1]
        return stock,b[0]
    @staticmethod
    def add_symbols():
        print("The Current list is: ...")
        for i in symbolList:
            print(i)
        stock=list(input("Enter the stocks you want to track separated by commas    ").split(","))
        for i in stock:
            data=symbolGiver.input_stock(i.upper())
            if data not in symbolList:
                symbolList.append(data)
            if(symbolList[-1]=="xxxx"):
                symbolList.pop()
        ff=open('current_stock.txt','w')
        for i in symbolList:
            ff.write(i+"\n")
        ff.close()
# def removeSymbols():
#     stock_to_be_removed=list(input("Enter the stocks you want to remove from the list separated by commas    ").split(","))
#     for 
# subscribe_stock("AAPL","BTC-USD","SBIN.NS",time_to=10)
# (add_symbols())
# subscribe_stock(symbolList,time_to=10)
# print(StockUpdate.find_price("BTC"))