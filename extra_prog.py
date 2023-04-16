class StockSymbolFile:
    def __init__(self) -> None:
        pass
    @staticmethod
    def getData():
        a=[]
        with open("current_stock.txt","r") as f:
             for i in f.readlines():
                 a.append(i[:-1])
        return a