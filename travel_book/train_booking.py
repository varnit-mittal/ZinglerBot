from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
import travel_book.constants as const
from datetime import datetime
from prettytable import PrettyTable 
from typing import List,Tuple,Dict
from bs4 import BeautifulSoup
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

class TrainBooking(webdriver.Chrome):
    def __init__(self,driver_path=r"C:\Users\HP\OneDrive\Desktop\web_scrapper\web_scrapping_hacknite\chromedriver_win32"):
        self.driver_path=driver_path
        os.environ['PATH']+=self.driver_path
        super(TrainBooking,self).__init__()
        self.driver= webdriver.Chrome(options=options)
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
    
    def __exit__(self):
            # if(self.tearDown):
            self.driver.quit()

    def get_webpage(self):
        driver=self.driver
        driver.get(const.TRAIN_BASE_URL)
        
    def find_train(self,place_source:str,place_destination:str)->None:
        driver=self.driver
        place=driver.find_element(By.ID,'origin')
        ActionChains(driver).move_to_element(place).click(place).perform()
        ActionChains(driver).move_to_element(place).send_keys(place_source).perform()
        ActionChains(driver).move_to_element(place).send_keys(Keys.TAB).perform()
        ac=driver.find_element(By.CLASS_NAME,'ng-star-inserted')
        ActionChains(driver).move_to_element(ac).click(ac).perform()

        place=driver.find_element(By.ID,'destination')
        ActionChains(driver).move_to_element(place).click(place).perform()
        ActionChains(driver).move_to_element(place).send_keys(place_destination).perform()
        ActionChains(driver).move_to_element(place).send_keys(Keys.TAB).perform()
        ac=driver.find_element(By.CLASS_NAME,'ng-star-inserted')
        ActionChains(driver).move_to_element(ac).click(ac).perform()
        
    def select_class(self,class_to_travel):
        driver=self.driver
        driver.find_element('id','journeyClass').click()
        change=driver.find_element(By.XPATH,(f"//*[text()='{class_to_travel}']"));
        change.click()

    def train_date(self,date_in:str,month_in,year_in,flexible_with_date:bool=False):
        month=datetime.now().month
        try:
            diff=int(month_in)-month
            if(diff<=4 and int(month_in)>=month):
                driver=self.driver
                driver.find_element('id','jDate').click()
                for i in range(diff):
                    driver.find_element(By.CLASS_NAME,'ui-datepicker-next').click()
                    # time.sleep(2)
                # ui-state-default ng-tns-c58-10 ng-star-inserted
                first_result=driver.find_element(By.XPATH,(f"//*[text()='{date_in}']"));
                first_result.click()
            else:
                raise Exception
        except Exception:
            print('Booking Not Available')
            self.driver.quit()
            exit()
        if(flexible_with_date):
            first_result=self.driver.find_element(By.XPATH,(f"//*[text()='Flexible With Date']"));
            first_result.click()

    def train_select_quota(self,quota:str="GENERAL"):
        driver=self.driver
        # aria-label="GENERAL"
        driver.find_element('id',"journeyQuota").click()
        qout=driver.find_element('css selector',f'[aria-label={quota}]')
        ActionChains(driver).move_to_element(qout).click(qout).perform()
    
    def click_button(self):
        self.driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
        try:
            first_result=self.driver.find_element(By.XPATH,(f"//*[text()='Yes']"));
            first_result.click()
        except:
            pass

    def getData(self):
        train_details=[]
        driver=self.driver
        train_names=self.driver.find_elements(By.CSS_SELECTOR,(".form-group.no-pad.col-xs-12.bull-back.border-all"))
        for train_name in train_names:
            train=train_name.find_element(By.CLASS_NAME,'train-heading')
            train_details.append(train.get_attribute('innerHTML'))
        name=[]
        for i in train_details:
            soup=BeautifulSoup(i,'lxml')
            name.append(soup.text)
        
        train_timings=driver.find_elements('css selector','.col-xs-5.hidden-xs')
        timings=[]
        for train_timing in train_timings:
            timings.append(train_timing.get_attribute('innerHTML'))

        timdate=[]
        for i in timings:   
            soup=BeautifulSoup(i,'lxml')
            l=soup.text.split(" | ")
            l1=[]
            l1.append(l[0])
            l1.append(l[-1])
            timdate.append(l1)  
        return [name,timdate]
    @staticmethod
    def output(aa):
        table=PrettyTable(["Train Name","Train Time","Train Date"])
        l=[]
        l1=[[]]
        for i in range(len(aa[0])):
            l.append(aa[0][i])
            for j in aa[1][i]:
                l.append(j)
        ass=0
        k=0
        for i in l:
            l1[k].append(i)
            ass+=1
            if(ass%3==0):
                l1.append([])
                k+=1
        l1.pop()
        return l1
# bot= TrainBooking()
# bot.get_webpage()
# station=open("station.txt",'r')
# stat1="Delhi"
# stat1=stat1.upper()
# l=[]
# if(len(stat1)>4):
#     while(1):
#         a=station.readline()
#         l=a.split()
#         if(l[0]==stat1):
#             stat1=l[-1]
#             break
# bot.find_train(stat1,"SBC")
# time.sleep(5)
# bot.train_date('17','6','2023',True)
# x= "AC 2 Tier (2A)"
# bot.select_class(x)
# bot.train_select_quota('GENERAL')
# bot.click_button()
# aa=bot.getData()
# print(bot.output(aa))

# print(aa)
# # white-back.col-xs-12.ng-star-inserted