from train_backend import train_main as tm
import streamlit as st
from streamlit_option_menu import option_menu
from email_read import email_main as em
import pandas as pd
import time
from Trade_main import trading_main as tr
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
        pass

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
            



        

# name=""
# while(1)
#     print("Hi User, Enter Your Name....")
#     str1=input()
#     if(str1!=""):
#         name=str1
#         break

# print(f'Hi {name}, How May I Help You....')
# print("These are my following functionalities...\n\n")
# print("1. Travel Book\n2. Trading\n3. Email Read\n\n")
# while(1):
#     print("Press 1 for Travel Booking: ")
#     print("Press 2 for Trading: ")
#     print("Press 3 for Email Management and Read: ")
#     print('Press -1 to exit Me')
#     i=int(input())
#     if(i==1):
#         print('Please Choose from the below options: ')
#         print('1. Train Management')
#         print('2. Hotel Management')
#         x=int(input())
        
#         if (x==1):
#             bot=TB()
#             bot.get_webpage()
#             station=open("./travel_book/station.txt",'r')
#             last_pos=station.tell()
#             print("Enter your source place: ")
#             stat1=input()
#             stat1=stat1.upper()
#             l=[]
#             if(len(stat1)>4):
#                 while(1):
#                     a=station.readline()
#                     l=a.split()
#                     if(l[0]==stat1):
#                         stat1=l[-1]
#                         break
#             station.seek(last_pos)
#             print("Enter Your Destination: ")
#             stat2=input()
#             stat2=stat2.upper()
#             l=[]
#             if(len(stat2)>4):
#                 while(2):
#                     a=station.readline()
#                     l=a.split()
#                     if(l[0]==stat2):
#                         stat2=l[-1]
#                         break
#             time.sleep(2)
#             l=input("Enter your travelling date in DD/MM/YYYY format ").split('/')
#             x=input("Do you opt for flexible dates (Y/N): ")
#             a=False
#             if(x=='Y'):
#                 a=True
#             bot.train_date(l[0],l[1],l[2],a)
#             bot.find_train(stat1,stat2)
#             time.sleep(2)
#             print("Select Your Quota from the given menu below: ")
#             print('1. GENERAL')
#             print('2. LADIES')
#             print('3. LOWER BERTH/SR.CITIZEN')
#             print('4. PERSON WITH DISABILITY')
#             print('5. TATKAL')
#             print('6. PREMIUM TATKAL')
#             x=int(input())
#             a=''
#             if(x==1):
#                 a='GENERAL'
#             elif(x==2):
#                 a='LADIES'
#             elif(x==3):
#                 a='LOWER BERTH/SR.CITIZEN'
#             elif(x==4):
#                 a='PERSON WITH DISABILITY'
#             elif(x==5):
#                 a='TATKAL'
#             elif(x==6):
#                 a='PREMIUM TATKAL'
#             bot.train_select_quota(a)
#             print("Select Your Class from the given menu below: ")
#             print("1. All Classes")
#             print("2. AC First Class (1A)")
#             print("3. Exec. Chair Car (EC)")
#             print("4. AC 2 Tier (2A)")
#             print("5. First Class (FC)")
#             print('6. AC 3 Tier (3A)')
#             print('7. AC 3 Economy (3E)')
#             print('8. Sleeper (SL)')
#             print('9. Second Sitting (2S)')
#             x=int(input())
#             a=""
#             if(x==1):
#                 a="All Classes"
#             elif(x==2):
#                 a="AC First Class (1A)"
#             elif(x==3):
#                 a="Exec. Chair Car (EC)"
#             elif(x==4):
#                 a="AC 2 Tier (2A)"
#             elif(x==5):
#                 a="First Class (FC)"
#             elif(x==6):
#                 a="AC 3 Tier (3A)"
#             elif(x==7):
#                 a='AC 3 Economy (3E)'
#             elif(x==8):
#                 a='Sleeper (SL)'
#             elif(x==9):
#                 a='Second Sitting (2S)'
#             bot.select_class(a)
            
#             bot.click_button()
#             aa=bot.getData()
#             print(bot.output(aa))
#             bot.__exit__()
            
#         elif(x==2):
#             bot=HB()
#             bot.get_webpage()
#             time.sleep(3)
#             country=input("Please Select the country you are living in.. ")
#             bot.country_select(country)
#             currency=input("Please Enter the Currency in which you want to continue(in symbol form or just enter the country)... ")
#             currency=currency.upper()
#             f=open('./travel_book/currency.txt','r')
#             if(len(currency)>3):
#                 l=[]
#                 while(1):
#                     a=f.readline()
#                     l=a.split(',')
#                     if(l[0]==currency):
#                         currency=l[2]
#                         break
#             bot.currency_select(currency)
#             bot.culture_save()
#             hotel=input("Enter the place name or hotel name where you want to stay(eg: New York)... ")
#             bot.place_or_hotel(hotel)
#             l=input("Enter your check-in date in 13 April 2023 type format.... ").split()
#             date=l[0]
#             month_inp=l[1]+" "+l[2]
#             l=input("Enter your check-out date in 13 April 2023 type format.... ").split()
#             date_out=l[0]
#             month_out=l[1]+" "+l[2]
#             bot.date_select(date,month_inp,date_out,month_out)
#             people=int(input("How many adults are travelling: "))
#             child=int(input("How many Children are travelling: "))
#             room=int(input("How many rooms do you need while staying: "))
#             bot.no_of_people(people,child,room)
#             bot.search_hotel()
#             filter=input("What stars do you want to apply as filter.. Enter(eg: 1 star,2 stars,4 stars)... ").split(',')
#             bot.star_filter_apply(filter)
#             lowTohigh=False
#             x=input("Do you want to sort the hotels in ascending order of price (Y/N): ")
#             if(x=='Y'):
#                 lowTohigh=True
#             bot.price_filter(lowTohigh)
#             l=bot.get_data()
#             print(bot.table_formation(l))
#             bot.__exit__()
        
#         else:
#             print("You have Entered a Wrong Input... ")
#             pass
        
#     elif(i==2):
#         bot=tm()
#         pass
#     elif(i==3):
#         bot=em()
#         bot.getEmails()
#         time.sleep(30)
#     elif(i==-1):
#         print("....SEE YOU SOON....")
#         print("BYE BYE....")
#         break
#     else:
#         print("YOU MIGHT HAVE ENTERED A WRONG VALUE...")
#         print("PLEASE RETRY...")
#         pass
#     time.sleep(8)
#     os.system('cls')