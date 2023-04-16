from fileio import symbolGiver
from trade import Recommendation
from AmericanStockBuySell import Alpaca
def trade_page(list_order:str,buy_sell:str,qty:int,typeOfOrder,lp:int,sp:int):
        return_value=[]
        symbol_list = []
        symbol_list.append(symbolGiver.input_stock(list_order))
        if(symbol_list[0]=='xxxx'):
            return 'ERROR'
        recommend = Recommendation.recommendation([list_order])
        return_value.append(recommend)
        
        buy_sell =buy_sell.lower()
        qty = int(qty)
        typeOfOrder =typeOfOrder.lower()
        if(typeOfOrder == 'market'):
            Alpaca.createMarketOrder(
                symbol_list[0], qty, buy_sell, "market", 'gtc')
            # print("Order Placed successfully")
        elif(typeOfOrder == 'limit'):
            Alpaca.createLimitOrder(
                symbol_list[0], qty, buy_sell, "limit", 'gtc', lp)
        elif(typeOfOrder == 'stop'):
            Alpaca.createStopOrder(
                symbol_list[0], qty, buy_sell, "stop", 'gtc', sp)
        elif(typeOfOrder == 'stop_limit'):
            Alpaca.createStopLimitOrder(
                symbol_list[0], qty, buy_sell, "stop_limit", 'gtc', lp, sp)
        return [return_value[0][0][0],return_value[0][0][1]]