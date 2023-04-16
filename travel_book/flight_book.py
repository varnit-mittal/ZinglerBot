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
import constants as const
from datetime import datetime
from prettytable import PrettyTable 
from typing import List,Tuple,Dict
import re
from bs4 import BeautifulSoup
import textwrap
import selenium.common.exceptions as exc
import undetected_chromedriver as uc
options = webdriver.ChromeOptions()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

class FlightBooking(webdriver.Chrome):
    def __init__(self,driver_path=r"C:\Users\HP\OneDrive\Desktop\web_scrapper\web_scrapping_hacknite\chromedriver_win32"):
        self.driver_path=driver_path
        os.environ['PATH']+=self.driver_path
        super(FlightBooking,self).__init__()
        self.driver= webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
    
    def __exit__(self):
        # if(self.tearDown):
        self.driver.quit()

    def get_webpage(self):
        driver=self.driver
        driver.get(const.FLIGHT_BASE_URL)
        time.sleep(2)

    def isBot(self):
        action=ActionChains(self.driver)
        try:
            element=self.driver.find_element(By.XPATH,(f"//*[text()='Click and hold']"));
            print(element)
            if(element):
                action.click_and_hold(on_element=element).perform()
        except Exception as e:
            pass
        time.sleep(1)

    def country_select(self,country):
        driver=self.driver
        driver.find_element('css selector','button[aria-label="Regional settings"]').click()
        try:
            Select(driver.find_element('id','select-market')).select_by_visible_text(country)
        except Exception as e:
            print("No such Country exist")
            driver.quit()
            exit()
        time.sleep(1)

    def currency_select(self,currency):
        driver=self.driver
        try:
            Select(driver.find_element('id','select-currency')).select_by_value(currency)
        except:
            print("No such currency available")
            driver.quit()
            exit()
        time.sleep(0.5)

    def culture_save(self):
        self.driver.find_element('css selector','.BpkButtonBase_bpk-button__NmRiZ.CulturePicker_saveButton__ZDJmZ').click()
        time.sleep(1)
    
bot=FlightBooking()
bot.get_webpage()
bot.isBot()
bot.country_select('Germany')
currency="India"
currency=currency.upper()
f=open('currency.txt','r')
if(len(currency)>3):
    l=[]
    while(1):
        a=f.readline()
        l=a.split(',')
        if(l[0]==currency):
            currency=l[2]
            break
# print(currency)
bot.currency_select(currency)
bot.culture_save()
# bot.flight_select()