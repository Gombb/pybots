
from binance_d import RequestClient
from binance_d.model import *
from binance_d.constant.test import *
from binance_d.base.printobject import *
from config import *
from time import time

SYMBOL = "ethusd_perp"
CURRENT_TIME = int(time() * 1000)
request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://dapi.binance.com")


def get_historical_data(start_time, end_time, interval):
    if interval == "15m":
        return get_historical_any_tf(start_time, end_time, CandlestickInterval.MIN15)
    elif interval == "5m":
        return get_historical_any_tf(start_time, end_time, CandlestickInterval.MIN5)


def get_historical_any_tf(startTime, endTime, interval, symbol=SYMBOL, limit=1000):
    return request_client.get_candlestick_data(symbol, interval, startTime, endTime, limit)



# print("======= Kline/Candlestick Data =======")
# PrintMix.print_data(result)
# print("======================================"
