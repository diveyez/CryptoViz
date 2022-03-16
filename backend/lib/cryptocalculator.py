import json
import json
import requests
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.simple_moving_average import simple_moving_average as sma
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.bollinger_bands import upper_bollinger_band as ubb
from pyti.bollinger_bands import middle_bollinger_band as mbb
from pyti.bollinger_bands import lower_bollinger_band as lbb
import pandas as pd


class CryptoCalculator:

    def ema(self, df):
        period = 9
        if len(df) < period:
            period = len(df) // 2
        return ema(df, period)
    
    def sma(self, df):
        period = 15
        if len(df) < period:
            period = len(df) // 2
        return sma(df,15)
    
    def rsi(self, df):
        period = 14
        if len(df) < period:
            period = len(df) // 2
        return rsi(df, period)

    def ubb(self, df):
        period = 20
        if len(df) < period:
            period = len(df) // 2
        return ubb(df,period)
    
    def mbb(self, df):
        period = 20
        if len(df) < period:
            period = len(df) // 2
        return mbb(df,period)

    def lbb(self, df):
        period = 20
        if len(df) < period:
            period = len(df) // 2
        return lbb(df,period)
