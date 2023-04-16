class symbolGiver:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def input_stock(stock):
        r=open("sym.txt","r")
        data=r.readlines()
        dict={}
        indian = False
        for i in data:
            l=i.split(' ',1)
            if(l[0]=="ABB"):
                indian=True
            if(indian==True):
                dict[(l[1][:-1]).upper()]=l[0].upper()+".NS"
            else:
                dict[(l[1][:-1]).upper()]=l[0].upper()
        stock=stock.upper()
        try:
            symbol=dict[stock]
            return symbol
        except KeyError:
            option={}
            for i in dict.keys():
                if stock in i:
                    option[i]=dict[i]
                    
            if len(option)==0:
                return "xxxx" 
            elif len(option)==1:
                return list(option.values())[0]
            else:
                for key,val in option.items():
                    print(key+' - '+val)
                stock=str(input("Enter Stock symbol from this list  ")) 
                return stock


