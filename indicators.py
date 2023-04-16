import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

import yfinance as yf
class indicators:

    @staticmethod
    def get_data(symbol,start,end):
        data=yf.download(symbol,start=start,end=end)
        df=pd.DataFrame(data)
        df.reset_index(inplace=True)
        df=data.set_index(pd.DatetimeIndex(data['Date'].values))
        return df
    @staticmethod
    def SMA(data,period=30,column='Close'):
        return data[column].rolling(window=period).mean()

    @staticmethod
    def EMA(data,period=30,column='Close'):
        return data[column].ewm(span=period,adjust=False).mean()

    @staticmethod
    def MACD(data,period_long=26,period_short=12,period_signal=9,column='Close'):
        shortEMA=indicators.EMA(data,period_short,column)
        longEMA=indicators.EMA(data,period_long,column)
        data['MACD']=shortEMA-longEMA 
        data['Signal_Line']=indicators.EMA(data,period_signal,'MACD')
        return data
    @staticmethod
    def RSI(data,period=14,column='Close'):
        delta=data[column].diff(1)
        delta=delta[1:]
        up=delta.copy()
        down=delta.copy()
        up[up<0]=0
        down[down>0]=0
        data['up']=up
        data['down']=down
        AVG_Gain=indicators.SMA(data,period,'up')
        AVG_Loss=abs(indicators.SMA(data,period,'down'))
        RSI_value=AVG_Gain/AVG_Loss
        RSI_value=100.0-(100.0/(1.0+RSI_value))
        data['RSI']=RSI_value
        return data
    @staticmethod
    def do(symbol,start,end,options):
        indicators.df=indicators.get_data(symbol,start,end)
        indicators.MACD(indicators.df)
        indicators.RSI(indicators.df)   
        if options=='SMA':
            indicators.df['SMA']=indicators.SMA(indicators.df)
            indicators.df['EMA']=indicators.EMA(indicators.df)
            column_list=['SMA','Close']
            indicators.df[column_list].plot(figsize=(12.2,6.4))
            plt.title('Simple Moving Average for '+symbol)
            plt.ylabel('Price (USD')
            plt.xlabel('Date')
            plt.savefig('SMA.png')
        elif options=='EMA':
            indicators.df['SMA']=indicators.SMA(indicators.df)
            indicators.df['EMA']=indicators.EMA(indicators.df)
            column_list=['EMA','Close']
            plt.title('Exponential Moving Average for '+symbol)
            plt.ylabel('Price (USD')
            plt.xlabel('Date')
            indicators.df[column_list].plot(figsize=(12.2,6.4))
            plt.savefig('EMA.png')
        elif options=='MACD':
            column_list=['MACD','Signal_Line']
            indicators.df[column_list].plot(figsize=(12.2,6.4))
            plt.title('Moving Average Convergence Divergence for '+symbol)
            plt.ylabel('Price (USD')
            plt.xlabel('Date')
            plt.savefig('MACD.png')
        elif options=='RSI':
            column_list=['RSI']
            indicators.df[column_list].plot(figsize=(12.2,6.4))
            plt.title('Relative Strength Index for '+symbol)
            plt.ylabel('Price (USD')
            plt.xlabel('Date')
            plt.savefig('RSI.png')
