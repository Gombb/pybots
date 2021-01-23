import logging
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *
import talib, numpy
import talib.abstract as ta
from time import time
import req_historical, req_user_data
from strat import *
from config import *
from orders import *



RSI_PERIOD = 14
SYMBOL = 'ETHUSDT'
CURRENT_TIME = int(time() * 1000)
UNIX_9DAYS = 691200000
POS_SIZE = 0.25


logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
sub_client = SubscriptionClient(api_key=API_KEY, secret_key=API_SECRET, uri="wss://fstream.binance.com/ws")


def collect_closes(closing_price, close_list):
    close_list.append(float(closing_price))


    
def calculate_rsi(candle_closes, length=RSI_PERIOD):
    return ta.RSI(numpy.array(_5_min_close), length)

def calculate_sma(candle_closes, length):
    return ta.SMA(numpy.array(candle_closes), length)


def calculate_ema(candle_closes, length):

    return talib.EMA(numpy.array(candle_closes), length)


def pre_fill_close_list(start_time, end_time, interval, close_list):
    candle_data = req_historical.get_historical_data(start_time, end_time, interval)
    for obj in candle_data:
        close_list.append(float(obj.close))


def ticker_callback(data_type: 'SubscribeMessageType', event: 'any'):
    global user_session
    if data_type == SubscribeMessageType.RESPONSE:
        print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        # PrintBasic.print_obj(event)
        tick_price = float(event.lastPrice)
        order_size = round(user_session["balance"] * POS_SIZE / _5_min_close[-1], 3)
        buy_stop_lvl = round(tick_price * 0.97, 2)
        sell_stop_lvl = round(tick_price * 0.97, 2)
        # print(tick_price)
        # print(user_session)
        # print(user_session["in_position"])
        if user_session["in_position"] == False:
            # if straight_buy(tick_price):
            #     order = market_buy(SYMBOL, order_size)
            #     print(order)
            #     print(order.origQty)
            #     user_session["in_position"] = True
            #     user_session["active_position"] = "+ "+ str(order.origQty)
            if sma21_bull_buy(tick_price, rsi_5min, sma21_5min, ema200_15min):
                order = market_buy(SYMBOL, order_size)
                print(order)
                user_session["active_position"] = "+ "+order_size
                buy_stop(SYMBOL, order_size, buy_stop_lvl)
                user_session["in_position"] = True
            if sma21_bear_sell(tick_price, rsi_5min, sma21_5min, ema200_15min):
                order = market_sell(SYMBOL, order_size)
                print(order)
                user_session["active_position"] = "- "+order_size
                sell_stop(SYMBOL, order_size, sell_stop_lvl)
                user_session["in_position"] = True
        if user_session["in_position"] == True:
            if sma21_bull_sell(rsi_5min):
                order = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
                user_session["in_position"] = False 
                print(order)
            if sma21_bear_buy(rsi_5min):
                order = market_buy(SYMBOL, user_session["active_position"].split(" ")[1])
                user_session["in_position"] = False
                print(order)
    else:
        print("Unknown Data:")
    # print()


def candle_callback_5min(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
            print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        # print("5min alive!")
        
        if event.data.isClosed == "True":
            print(user_session)
            print("Event type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Symbol: ", event.symbol)
            print("Data:")
            
            PrintBasic.print_obj(event.data)
            collect_closes(event.data.close, _5_min_close)
    else:
        print("Unknown Data:")
    # print()



def candle_callback_15min(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
            print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        # print("15min alive!")
        if event.data.isClosed == "True":
            print("Event type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Symbol: ", event.symbol)
            print("Data:")    
            PrintBasic.print_obj(event.data)
            collect_closes(event.data.close, _15_min_close)
    else:
        print("Unknown Data:")
    # print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)



user_session = {"in_position": False}
user_session["balance"] = req_user_data.request_user_balance()["balance"]
_5_min_close = []
_15_min_close = []


pre_fill_close_list(CURRENT_TIME-UNIX_9DAYS/3, CURRENT_TIME, "5m", _5_min_close)
pre_fill_close_list(CURRENT_TIME-UNIX_9DAYS, CURRENT_TIME, "15m", _15_min_close)


rsi_5min = calculate_rsi(_5_min_close)
sma21_5min = calculate_sma(_5_min_close, 21)
ema200_15min = calculate_ema(_15_min_close, 200)


sub_client.subscribe_symbol_ticker_event("ethusdt", ticker_callback, error)
sub_client.subscribe_candlestick_event("ethusdt", CandlestickInterval.MIN5, candle_callback_5min, error)
sub_client.subscribe_candlestick_event("ethusdt", CandlestickInterval.MIN15, candle_callback_15min, error)