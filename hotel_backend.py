import time
import travel_book.constants as const
from travel_book.hotel_book import HotelBooking as HB
import os  

def hotel_main(country,currency:str,hotel,check_in_date,check_out_date,adults,children,rooms,star_filter,agree):
    bot=HB()
    bot.get_webpage()
    time.sleep(3)
    # country=input("Please Select the country you are living in.. ")
    bot.country_select(country)
    currency=currency.upper()
    f=open('./travel_book/currency.txt','r')
    if(len(currency)>3):
        l=[]
        while(1):
            a=f.readline()
            l=a.split(',')
            if(l[0]==currency):
                currency=l[2]
                break
    bot.currency_select(currency)
    bot.culture_save()
    bot.place_or_hotel(hotel)
    l=check_in_date.split()
    date=l[0]
    month_inp=l[1]+" "+l[2]
    l=check_out_date.split()
    date_out=l[0]
    month_out=l[1]+" "+l[2]
    bot.date_select(date,month_inp,date_out,month_out)
    people=adults
    child=children
    room=rooms
    bot.no_of_people(people,child,room)
    bot.search_hotel()
    filter=star_filter
    bot.star_filter_apply(filter)
    lowTohigh=agree
    bot.price_filter(lowTohigh)
    l=bot.get_data()
    bot.__exit__()
    return l