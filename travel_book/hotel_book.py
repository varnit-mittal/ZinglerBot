from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.ui as uiClasses
from selenium.webdriver.support.select import Select
import travel_book.constants as const
from datetime import datetime
from prettytable import PrettyTable 
from typing import List,Tuple,Dict
import re
from bs4 import BeautifulSoup
import textwrap
import selenium.common.exceptions as exc
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

class HotelBooking(webdriver.Chrome):
    def __init__(self,driver_path=r"C:\Users\HP\OneDrive\Desktop\web_scrapper\web_scrapping_hacknite\chromedriver_win32"):
        self.driver_path=driver_path
        os.environ['PATH']+=self.driver_path
        super(HotelBooking,self).__init__()
        self.driver= webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
    
    def __exit__(self):
        # if(self.tearDown):
        self.driver.quit()

    def get_webpage(self):
        driver=self.driver
        driver.get(const.HOTEL_BASE_URL)

    def country_select(self,country):
        driver=self.driver
        driver.find_element(By.CLASS_NAME,'CultureSelectorButton_CultureSelectorButton__labels__MGU0N').click()
        try:
            Select(driver.find_element('id',"culture-selector-market")).select_by_visible_text(country)
        except Exception as e:
            print("No such Country Exist")
            driver.quit()
            exit()

    def currency_select(self,currency):
        driver=self.driver
        try:
            Select(driver.find_element('id',"culture-selector-currency")).select_by_value(currency)
        except Exception as e:
            print("No such currency available")
            driver.quit()
            exit()

    def culture_save(self):
        driver=self.driver
        driver.find_element('id','culture-selector-save').click()        

    def place_or_hotel(self,name):
        driver=self.driver
        time.sleep(2)
        stay_name=driver.find_element(By.ID,"destination-autosuggest")
        time.sleep(2)
        stay_name.click()
        ActionChains(driver).move_to_element(stay_name).send_keys(name).perform()
        search_stay_name_element=driver.find_element('css selector','[data-test-id="autosuggest-suggestion"]')
        ActionChains(driver).move_to_element(search_stay_name_element).click(search_stay_name_element).perform()

    def date_select(self,check_in_date:str,check_in_month:str,check_out_date:str,check_out_month:str)->None:
        driver=self.driver
        try:
            time.sleep(2)
            driver.find_element('id',"checkin").click()
            time.sleep(2)
            Select(driver.find_element('id','checkin-calendar__bpk_calendar_nav_select')).select_by_visible_text(check_in_month)
            time.sleep(2)
            dates=driver.find_elements(By.CLASS_NAME,'BpkCalendarDate_bpk-calendar-date__NGE5N')
            for date in dates:
                first_result=date.find_element(By.XPATH,(f"//*[text()='{check_in_date}']"));
                time.sleep(1)
                first_result.click()
                if(first_result):
                    break
            time.sleep(2)
            driver.find_element('id','checkout').click()
            time.sleep(2)
            Select(driver.find_element('id','checkout-calendar__bpk_calendar_nav_select')).select_by_visible_text(check_out_month)
            time.sleep(2)
            dates=driver.find_elements(By.CLASS_NAME,'BpkCalendarDate_bpk-calendar-date__NGE5N')
            for date in dates:
                first_result=date.find_element(By.XPATH,(f"//*[text()='{check_out_date}']"));
                time.sleep(1)
                first_result.click()
                if(first_result):
                    break
        except Exception as e:
            print("No Booking Available With Such Data")
            driver.quit()
            exit()

    def no_of_people(self,num_adult,num_children,num_room):
        driver=self.driver
        driver.find_element('id','guests-rooms').click()
        count=1
        time.sleep(2)
        adult_select=driver.find_elements('css selector','button[aria-controls="adults"]')
        for select in adult_select:
            if(num_adult<2):
                select.click()
                break
            if(num_adult>2 and count ==2):
                for i in range(num_adult-2):
                    select.click()
            count+=1

        
        time.sleep(2)
        children_select=driver.find_elements('css selector','button[aria-controls="children"]')
        count=1
        for select in children_select:
            if(num_children==0):
                break
            if(num_children>0 and count ==2):
                for i in range(num_children):
                    select.click()
            count+=1

        time.sleep(2)
        room_select=driver.find_elements('css selector','button[aria-controls="rooms"]')
        count=1
        for select in room_select:
            if(num_room<=1):
                break
            if(num_room>1 and count ==2):
                for i in range(num_room-1):
                    select.click()
            count+=1

        time.sleep(1)
        done=driver.find_element('id','guest-rooms-children-popover')
        time.sleep(1)
        done=done.find_element(By.CLASS_NAME,'BpkLink_bpk-link__MzVjN').click()

    def search_hotel(self):
        time.sleep(1)
        self.driver.find_element('css selector','button[data-test-id="search-button"]').click()

    def star_filter_apply(self,stars):
        driver=self.driver
        time.sleep(1)
        driver.find_element('css selector','button[data-test-id="filterExpandButton"]').click()
        time.sleep(1)
        stars_select=driver.find_elements('css selector','.BpkText_bpk-text__MmJjN.BpkText_bpk-text--base__ZGRlM.CheckboxFilter_CheckboxFilter__item--starsLabel__MTI0Z')
        for star_element in stars:
            for element in stars_select:
                time.sleep(3)
                if(element.get_attribute('innerHTML').strip()==f'{star_element}'):
                    element.click()
                    break
        time.sleep(1)
        driver.find_element('css selector','button[data-testid="show-result-button"]').click()

    def price_filter(self,lowTohigh=False):
        if(lowTohigh):
            time.sleep(1)
            self.driver.find_element('css selector','[data-test-id="search-sort-price"]').click()

    def get_data(self):
        driver=self.driver
        time.sleep(1)
        hotels=driver.find_elements('css selector','.BpkTicket_bpk-ticket__MGUwN.CardRowLayout_CardRowLayout__ticket__MWVhN')
        hotel_name=[]
        hotel_price=[]
        hotel_link=[]
        for hotel in hotels:
            time.sleep(0.5)
            name_class=hotel.find_element('css selector','[data-test-id="hotel-name"]')
            hotel_name.append(name_class.get_attribute('innerHTML').strip())
            price_class=hotel.find_element('css selector','.BpkText_bpk-text__MmJjN.BpkText_bpk-text--xxl__NmFiM')
            hotel_price.append(price_class.get_attribute('innerHTML').strip())
            link_class=hotel.find_elements(By.CLASS_NAME,'MainRate_MainRate__ctaAndAmenity__MjI0Y')
            for link in link_class:
                link.find_element(By.CLASS_NAME,'MainRate_MainRate__ctaButton__NGRlY')
                soup=BeautifulSoup(link.get_attribute('innerHTML'),'lxml')
                for i in soup.find_all('a',attrs={'href': re.compile("^//")}):
                    if(i.get('href')):
                        hotel_link.append(i.get('href'))
                    else:
                        hotel_link.append("No Data Available")

        l1=[]
        for i in range(len(hotel_name)):
            l=[]
            l.append(hotel_name[i])
            l.append(hotel_price[i])
            # l.append(hotel_link[i])
            l1.append(l)

        return l1
        # return (hotel_name,hotel_price,hotel_link)
    
    @staticmethod
    def table_formation(l):
        table=PrettyTable(["Hotel Name",'Hotel Price'])
        table.add_rows(l)
        return table


# bot=HotelBooking()
# bot.get_webpage()
# # bot.isBot()
# time.sleep(3)
# bot.country_select('United States')
# currency="India"
# currency=currency.upper()
# f=open('currency.txt','r')
# if(len(currency)>3):
#     l=[]
#     while(1):
#         a=f.readline()
#         l=a.split(',')
#         if(l[0]==currency):
#             currency=l[2]
#             break
# # print(currency)
# bot.currency_select(currency)
# bot.culture_save()
# bot.place_or_hotel('New York')
# date="12"
# month="September"
# year="2023"
# month_inp=month+" "+year
# bot.date_select(date,month_inp,"15","November 2023")
# bot.no_of_people(1,1,1)
# bot.search_hotel()
# bot.star_filter_apply("3 stars","4 stars")
# bot.price_filter(True)
# l=bot.get_data()

# print(bot.table_formation(l))