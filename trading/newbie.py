import requests
from bs4 import BeautifulSoup
import constants as const
import random
from typing import List
class Newbie:
    @staticmethod
    def find_stocks()->List:
        html_text=requests.get(const.TOP_5_BASE_URL).text
        soup=BeautifulSoup(html_text,'lxml')
        randomList=[]
        for i in range(5):
            randNum=random.randint(2,20)
            randomList.append(randNum)
        j=1
        l=[]
        stocks=soup.find_all('h2',class_='card-title')
        for stock in stocks:
            if(j in randomList):
                a=stock.text.strip().replace(' ','')
                t=0
                while(a[t]!='\n'):
                    t+=1
                a=a[t+2:]
                l.append(a)
            j+=1
        return l
    @staticmethod
    def findings():
        stock=Newbie.find_stocks()
        a=stock[:]
        return a
# a=Newbie()
# print(a.findings())