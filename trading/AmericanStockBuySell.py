import alpaca_trade_api as a
import requests ,json
import config
alpaca_key="r8BcO9jQhIT0SgJWmx4fZVl7n2IhxlTQiumd8LB0"
alpaca_api="PKN6GDAUTTEG136IG0KK"
BASEURL="https://paper-api.alpaca.markets"
orderurl='{}/v2/orders'.format(BASEURL)
accounturl='{}/v2/account'.format(BASEURL)
headers={'APCA-API-KEY-ID':alpaca_api,'APCA-API-SECRET-KEY':alpaca_key}
class Alpaca:
    @classmethod
    def getAccount(cls):
        r=requests.get(accounturl,headers=headers)
        return json.loads(r.content)
    @classmethod
    def createMarketOrder(cls,symbol,qty,side,type,time_in_force):
        data={
            'symbol':symbol,
            'qty':qty,
            "side":side,
            "type":"market",
            "time_in_force":time_in_force
        }
        r=requests.post(orderurl,json=data,headers=headers)
        return json.loads(r.content)
    @classmethod
    def createLimitOrder(cls,symbol,qty,side,type,time_in_force,limit_price):
        data={
            'symbol':symbol,
            'qty':qty,
            "side":side,
            "type":"limit",
            "time_in_force":time_in_force,
            "limit_price":limit_price
        }
        r=requests.post(orderurl,json=data,headers=headers)
        return json.loads(r.content)
    @classmethod
    def createStopOrder(cls,symbol,qty,side,type,time_in_force,stop_price):
        data={
            'symbol':symbol,
            'qty':qty,
            "side":side,
            "type":"stop",
            "time_in_force":time_in_force,
            "stop_price":stop_price
        }
        r=requests.post(orderurl,json=data,headers=headers)
        return json.loads(r.content)
    @classmethod
    def createStopLimitOrder(cls,symbol,qty,side,type,time_in_force,stop_price,limit_price):
        data={
            'symbol':symbol,
            'qty':qty,
            "side":side,
            "type":"stop_limit",
            "time_in_force":time_in_force,
            "stop_price":stop_price,
            "limit_price":limit_price
        }
        r=requests.post(orderurl,json=data,headers=headers)
        return json.loads(r.content)
    @classmethod
    def getOrders(cls):
        r=requests.get(orderurl,headers=headers)
        return json.loads(r.content)
    @classmethod
    def closeAllPositions(cls):
        r=requests.delete(orderurl,headers=headers)
        return json.loads(r.content)
    @classmethod
    def getPositions(cls):
        l=cls.getOrders()
        for i in l:
            print(i['symbol'],i['qty'],i['side'])
    @classmethod
    def account(cls):
        print("ID: ",Alpaca.getAccount()['id'])
        print("ACCOUNT NUMBER:",Alpaca.getAccount()['account_number'])
        print("LEVERAGED (MARGIN) BALANCE: $",Alpaca.getAccount()['buying_power'])
        print("NON MARGINABLE BALANCE: $",Alpaca.getAccount()['non_marginable_buying_power'])
        "POSITIONS:",Alpaca.getPositions()
        print("Current Profit is ",cls.profit())
    @classmethod
    def profit(cls):
        return (int(Alpaca.getAccount()['portfolio_value'])-int(Alpaca.getAccount()['cash']))