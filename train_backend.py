from travel_book.train_booking import TrainBooking as TB
# from email_read.email_read import email_main as em
# from trading.Trade_main import trading_main as tm
import time
import travel_book.constants as const
# from travel_book.hotel_book import HotelBooking as HB
import os

def train_main(str1,str2,lis,agree,option,option2):
    bot=TB()
    bot.get_webpage()
    station=open("./travel_book/station.txt",'r')
    last_pos=station.tell()
    # print("Enter your source place: ")
    stat1=str1
    stat1=stat1.upper()
    l=[]
    if(len(stat1)>4):
        while(1):
            a=station.readline()
            l=a.split()
            if(l[0]==stat1):
                stat1=l[-1]
                break
    station.seek(last_pos)
    stat2=str2
    stat2=stat2.upper()
    l=[]
    if(len(stat2)>4):
        while(2):
            a=station.readline()
            l=a.split()
            if(l[0]==stat2):
                stat2=l[-1]
                break
    time.sleep(2)
    
    bot.train_date(lis[0],lis[1],lis[2],agree)
    bot.find_train(stat1,stat2)
    time.sleep(2)

    bot.train_select_quota(option)
    bot.select_class(option2)
    bot.click_button()
    aa=bot.getData()
    table=bot.output(aa)
    bot.__exit__()
    return table