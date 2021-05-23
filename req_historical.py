
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
from config import *
from time import time

request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://fapi.binance.com")


def get_historical_data(symbol, start_time, end_time, interval):
    if interval == "15m":
        return get_historical_any_tf(symbol, start_time, end_time, CandlestickInterval.MIN15)
    elif interval == "5m":
        return get_historical_any_tf(symbol, start_time, end_time, CandlestickInterval.MIN5)


def get_historical_any_tf(symbol, startTime, endTime, interval, limit=1000):
    return request_client.get_candlestick_data(symbol, interval, startTime, endTime, limit)



# print("======= Kline/Candlestick Data =======")
# PrintMix.print_data(result)
# print("======================================"
