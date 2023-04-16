ainBooking()
bot.get_webpage()
station=open("station.txt",'r')
stat1="Delhi"
stat1=stat1.upper()
l=[]
if(len(stat1)>4):
    while(1):
        a=station.readline()
        l=a.split()
        if(l[0]==stat1):
            stat1=l[-1]
            break
bot.find_train(stat1,"SBC")
# time.sleep(5)
x= "AC 2 Tier (2A)"
bot.select_class(x)
bot.train_select_quota('GENERAL')
bot.train_date('17','10','2023',True)
bot.click_button()
aa=bot.getData()
print(bot.output(aa))

print(aa)