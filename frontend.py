from train_backend import train_main as tm
import streamlit as st
from streamlit_option_menu import option_menu
from email_read import email_main as em
import pandas as pd
import time
from Trade_main import trading_main as tr
from AmericanStockBuySell import Alpaca
from datetime import datetime
from hotel_backend import hotel_main as hm
from place_order import trade_page
from PIL import Image
from Indicator import ind
with st.sidebar:
	select = option_menu(menu_title="Main Menu"
						 ,options=["Home","Travel Booking", "Trading", "Email Read"]
						 )

st.markdown("<h1 style='text-align: center; color: white;'>Hi, My name is Zingler...</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>I am your personalized dashboard bot...</h2>", unsafe_allow_html=True)

if select=='Home':
	st.markdown('<style>input[type="text"]{height: 35px; width: 700px; font-size: 16px; text-align: left; border : 2px solid white;}</style>', unsafe_allow_html=True)
	str1=st.text_input("Enter Your Name: ", "")
	if(str1!=""):
		st.markdown(f"""<h2 style="text-align: center; color:#ffffff;">Hi {str1}</h2>""", unsafe_allow_html=True)
		st.markdown("<h3 style='text-align: center; color: orange;'>How May I Help You...</h3>", unsafe_allow_html=True)
		st.markdown("<h3 style='text-align: center; color: orange;'>Click on the following side buttons to explore my functionalities </h3>", unsafe_allow_html=True)

if select=='Travel Booking':
	st.markdown("<h3 style='text-align: center; color: yellow;'>Welcome to Travel Booking</h3>", unsafe_allow_html=True)
	st.markdown("<h3 style='text-align: center; color: yellow;'>Please Choose from the below options: </h3>", unsafe_allow_html=True)
	st.markdown("<h3 style='text-align: center; color: yellow;'>1. Train Management</h3>", unsafe_allow_html=True)
	st.markdown("<h3 style='text-align: center; color: yellow;'>2. Hotel Management</h3>", unsafe_allow_html=True)

	select = option_menu(menu_title="Travel Booking"
						 ,options=["Train Management", "Hotel Management"]
						 )
	if select=='Train Management':
		st.markdown("<h3 style='text-align: center; color: yellow;'>Welcome to Train Management</h3>", unsafe_allow_html=True)
		st.markdown("<h4 style='text-align: center; color: yellow;'>Please Enter your Source and Destination</h4>", unsafe_allow_html=True)
		submit=False
		with st.form("my_form"):
			str1=st.text_input("Enter Your Source: ", "")
			str2=st.text_input("Enter Your Destination: ", "")

			selected_date=st.date_input("Enter Your Date: ", )

			agree=st.checkbox("Do you opt for flexible dates: ")
			option=st.selectbox(
				"Select Your Quota from the given menu below:",
				("GENERAL", "LADIES", "LOWER BERTH/SR.CITIZEN", "PERSON WITH DISABILITY", "TATKAL", "PREMIUM TATKAL")
			)
			option2=st.selectbox(
				"Select Your Class from the given menu below:",
				("All Classes",'AC First Class (1A)','Exec. Chair Car (EC)','AC 2 Tier (2A)','First Class (FC)','AC 3 Tier (3A)','AC 3 Economy (3E)','Sleeper (SL)','Second Sitting (2S)')
			)
			# print(option2)
			lis=[]
			lis.append(str(selected_date.day)) #type:ignore
			lis.append(str(selected_date.month))  #type:ignore
			lis.append(str(selected_date.year) )   #type:ignore
			submit=st.form_submit_button("Submit")
			if submit:
				info=tm(str1, str2, lis, agree, option, option2)
				l=[[],[],[]]
				for i in info:
					l[0].append(i[0])
					l[1].append(i[1])
					l[2].append(i[2])
				
				nl=[]
				for i in range(len(l[0])):
					nl.append([l[0][i],l[1][i],l[2][i]])
				df = pd.DataFrame(nl,columns=['Train Name', 'Train Time', 'Train Date'])
				st.table(df)

		# table=tm(str1, str2, lis, agree, option, option2)
		# st.write(table)
	if select=='Hotel Management':
		with st.form("my_form"):
			country=st.text_input("Please Select the country you are living in..", "")
			currency=st.text_input("Please Enter the Currency in which you want to continue(in symbol form or just enter the country)...", "")
			hotel=st.text_input("Enter the place name or hotel name where you want to stay(eg: New York)... ", "")
			check_in_date=st.date_input("Enter Your Check-in date: ", )
			dict={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
			check_in_date=str(check_in_date.day)+" "+dict[check_in_date.month]+" "+str(check_in_date.year) #type:ignore
			check_out_date=st.date_input("Enter Your Check-out date: ", )
			check_out_date=str(check_out_date.day)+" "+dict[check_out_date.month]+" "+str(check_out_date.year) #type:ignore
			adults=st.number_input("Enter no. of adults",min_value=1,max_value=15,value=1,step=1)
			children=st.number_input("Enter no. of children",min_value=0,max_value=15,value=0,step=1)
			rooms=st.number_input("Enter no. of rooms",min_value=1,max_value=15,value=1,step=1)
			star_filter=st.multiselect('Which filters do you want to apply?', ['1 star', '2 stars', '3 stars', '4 stars', '5 stars'])
			agree=st.checkbox("Do you want to apply low to high price filter: ")
			submit=st.form_submit_button("Submit")
			if submit:
				l=hm(country, currency, hotel, check_in_date, check_out_date, adults, children, rooms, star_filter, agree)
				# nl=[]
				# for i in range(len(l[0])):
				#     nl.append([l[0][i],l[1][i]])
				df = pd.DataFrame(l,columns=['Hotel Name','Hotel Price'])
				st.table(df)
if select=='Trading':
	st.markdown("<h3 style='text-align: center; color: green;'>Welcome to Trading Bot</h3>", unsafe_allow_html=True)
	st.markdown("<h3 style='text-align: center; color: white;'>Please Choose from the below options: </h3>", unsafe_allow_html=True)
	select = option_menu(menu_title="Trade Options"
						 ,options=["Newbie", "Expert"]
						 )

	if select=='Newbie':
		submit=False
		with st.form("my_form"):
			st.markdown("<h5 style='text-align: center; color: orange;'>No worries, we will help you</h5>", unsafe_allow_html=True)
			invest=st.checkbox("Do you want to invest")
			money=0
			if(invest):
				temp=st.number_input("Enter money your want to spend",min_value=1,max_value=2000,value=500,step=20)
				money=temp
				st.markdown("<h5 style='text-align: center; color: orange;'>Please wait while we fetch the best stocks for you</h5>", unsafe_allow_html=True)
				st.markdown("<h5 style='text-align: center; color: green;'>Order Placed Successfully</h5>", unsafe_allow_html=True)
				# st.markdown("<h5 style='text-align: center; color: green;'>Please check your email for the stocks</h5>", unsafe_allow_html=True)
			isClosePos=st.checkbox("Do you want to close all your positions and take out net profit / loss ?")
			if(isClosePos):
				st.markdown("<h5 style='text-align: center; color: green;'>All your positions are closed successfully</h5>", unsafe_allow_html=True)
			submit=st.form_submit_button("Submit")
			if submit:
				p=tr()
			   
				stock_list=p.base_page(isNewbie=True, isInvest=invest, money=money, isClosePos=isClosePos,getOrderSummary=True)
				stock_name=stock_list[0] #type:ignore
				summary=stock_list[1] #type:ignore
				for i in range(len(stock_name)):
					st.markdown(f"""<h5 style='text-align: center; color: green;'>{stock_name[i]}</h5>""", unsafe_allow_html=True)
				df=pd.Series(summary,index=["ID","Account_Number","Buying_power","non_marginable_buying_power","Profit"])
				st.table(df)
	if select == 'Expert':
		select2 = option_menu(menu_title="Your Trading Tasks"
						 ,options=["Buy / Sell Stock", "Check Account Summary",'Close all positions','Save Indicators']
						 )
		if select2=="Buy / Sell Stock":
			with st.form("my_form"):
				list_order=st.text_input("Enter the stock name you want to buy or sell", "")
				buy_sell=str(st.selectbox("Buy or Sell",("buy","sell")))
				qty=int(st.number_input("Enter quantity",min_value=1,max_value=10,value=1,step=1))
				typeOfOrder=str(st.selectbox("Type of Order",("market","limit","stop","stop_limit")))
				lp,sp=0,0
				if typeOfOrder=="limit" or typeOfOrder=="stop_limit":
					lp=int(st.number_input("Enter Limit Price"))
				if typeOfOrder=="stop" or typeOfOrder=="stop_limit":
					sp=int(st.number_input("Enter StopLoss Price"))
				submit=st.form_submit_button("Submit")
				if submit:
					return_value=trade_page(list_order=list_order,buy_sell=buy_sell,qty=qty,typeOfOrder=typeOfOrder,lp=lp,sp=sp) 
					st.write(f"As per our calculation you should {return_value[1]} the stock")
		if select2=="Check Account Summary":
			df=pd.Series(Alpaca.account(),index=["ID","Account_Number","Buying_power","non_marginable_buying_power","Profit"])
			st.table(df)
		if select2=="Close all positions":
			Alpaca.closeAllPositions()
			st.markdown("<h5 style='text-align: center; color: green;'>All your positions are closed successfully</h5>", unsafe_allow_html=True)
		if select2=="Save Indicators":
			with st.form("my_form"):
				list_order=st.text_input("Enter the stock name you want to analyze indicators", "")
				date=st.date_input("Enter the date start you want to analyze indicators",)
				t1=str(date.day)  #type:ignore
				t2=str(date.month)  #type:ignore
				t3=str(date.year)  	#type:ignore
				date= t3+"-"+t2+"-"+t1
				date1=st.date_input("Enter the date end you want to analyze indicators",)
				t1=str(date1.day)   		#type:ignore
				t2=str(date1.month)   		#type:ignore
				t3=str(date1.year)   		#type:ignore
				date1= t3+"-"+t2+"-"+t1
				enter=str(st.selectbox("Type of Indicator",("RSI","MACD","EMA","SMA")))
				submit=st.form_submit_button("Submit")
				image=""
				if submit:
					ind(list_order,date,date1,enter)
					print(image)
					time.sleep(7)
				image=Image.open(f'{enter}.png')
				if(image):
					# st.image(image, caption='Sunrise by the mountains')
					st.image(image, caption=f'{enter} Graph', use_column_width=True)

if select=='Email Read':
	temp=em()
	messages=temp.getEmails()
	for i in range(len(messages)):
		# print(i[0])
		st.text("")
		st.text("")
		st.text("")
		st.write(f"""Subject: {messages[i][0]}""")
		st.write(f"""Sender: {messages[i][1]}""")
		st.write(f"""Body: {messages[i][2]}""")
		st.markdown(f"""---""")
			
