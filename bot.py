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
SMA_5MIN_PERIOD = 21
EMA_15MIN_PERIOD = 50
SYMBOL = 'LINKUSDT'
CURRENT_TIME = int(time() * 1000)
UNIX_9DAYS = 691200000
POS_SIZE = 0.5
BUY_STOP_LVL = 0.96
SELL_STOP_LVL = 1.04


logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
sub_client = SubscriptionClient(api_key=API_KEY, secret_key=API_SECRET, uri="wss://fstream.binance.com/ws")

def check_positon(symbol_ticker):
    global user_session
    result = req_user_data.request_user_position()
    for ele in result:
        if ele.symbol == symbol_ticker and ele.positionAmt == 0.0:
            user_session["active_position"] = "0"
            user_session["in_position"] = False
        if ele.symbol == symbol_ticker and ele.positionAmt > 0.0:
            user_session["active_position"] = "+ " + str(ele.positionAmt)
            user_session["in_position"] = True
        if ele.symbol == symbol_ticker and ele.positionAmt < 0.0:
            user_session["in_position"] = True
            user_session["active_position"] = "- " + str(ele.positionAmt).split("-")[1] 


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
        order_size = str(round(user_session["balance"] * POS_SIZE / tick_price, 2))
        # buy_stop_price= str(round(tick_price * BUY_STOP_LVL, 2))
        # sell_stop_price = str(round(tick_price * SELL_STOP_LVL, 2))
        print(tick_price)
        print(user_session)
        rsi_5min = calculate_rsi(_5_min_close)
        sma_5min = calculate_sma(_5_min_close, SMA_5MIN_PERIOD)
        ema_15min = calculate_ema(_15_min_close, EMA_15MIN_PERIOD)
        print(f'5min RSI {rsi_5min[-1]} || len  {len(rsi_5min)}')
        print(f'sma21 {sma_5min[-1]} ||  len  {len(sma_5min)}')
        print(f'ema {ema_15min[-1]} ||  len  {len(ema_15min)}')
        # print(f'15min close {len(_15_min_close)} long')
        if user_session["in_position"] == False:
            # if straight_buy(tick_price):
            #     order = market_buy(SYMBOL, order_size)
            #     user_session["in_position"] = True
            #     user_session["active_position"] = "+ "+ str(order.origQty)
            #     buy_stop(SYMBOL, user_session["active_position"].split(" ")[1], str(round(tick_price * BUY_STOP_LVL, 3)))
            if sma21_bull_buy(tick_price, rsi_5min, sma_5min, ema_15min):
                order = market_buy(SYMBOL, order_size)
                user_session["in_position"] = True
                user_session["active_position"] = "+ " + str(order.origQty)
                buy_stop(SYMBOL, str(order.origQty), str(round(tick_price * BUY_STOP_LVL, 3)))
            if sma21_bear_sell(tick_price, rsi_5min, sma_5min, ema_15min) == True:
                order = market_sell(SYMBOL, order_size)
                user_session["in_position"] = True
                user_session["active_position"] = "- "+ str(order.origQty)
                sell_stop(SYMBOL, str(order.origQty), str(round(tick_price * SELL_STOP_LVL, 3)))
            

        if user_session["in_position"] == True:
            if user_session["active_position"].split(" ")[0] == "+" and tick_price < sma_5min[-1]:
                if sma_5min[-1] < ema_15min[-1] and sma_5min[-2] < ema_15min[-1] and sma_5min[-3] < ema_15min[-1]:
                    sell_order = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
                    user_session["in_position"] = False
                    user_session["active_position"] = 0 
                    cancel_order = cancell_all_order(SYMBOL)    
                    PrintBasic.print_obj(sell_order)
                    PrintBasic.print_obj(cancel_order)
            if user_session["active_position"].split(" ")[0] == "-" and tick_price > sma_5min[-1]:  
                if sma_5min[-1] > ema_15min[-1] and sma_5min[-2] > ema_15min[-1] and sma_5min[-3] > ema_15min[-1]:
                    buy_order = market_buy(SYMBOL, user_session["active_position"].split(" ")[1])
                    user_session["in_position"] = False
                    user_session["active_position"] = 0
                    cancel_order = cancell_all_order(SYMBOL)
                    PrintBasic.print_obj(buy_order)
                    PrintBasic.print_obj(cancel_order)
            if sma21_bull_sell(rsi_5min):
                sell_order = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
                user_session["in_position"] = False
                user_session["active_position"] = 0 
                cancel_order = cancell_all_order(SYMBOL)    
                PrintBasic.print_obj(sell_order)
                PrintBasic.print_obj(cancel_order)
            if sma21_bear_buy(rsi_5min):
                buy_order = market_buy(SYMBOL, user_session["active_position"].split(" ")[1])
                user_session["in_position"] = False
                user_session["active_position"] = 0
                cancel_order = cancell_all_order(SYMBOL)
                PrintBasic.print_obj(buy_order)
                PrintBasic.print_obj(cancel_order)
            # if test_TP(rsi_5min):
            #     print("true")
            #     sell_order = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
            #     user_session["in_position"] = False
            #     user_session["active_position"] = 0 
            #     cancel_order = cancell_all_order(SYMBOL)    
            #     PrintBasic.print_obj(sell_order)
            #     PrintBasic.print_obj(cancel_order)
                
    else:
        print("Unknown Data:")
    print()


def candle_callback_5min(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
            print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        # PrintBasic.print_obj(event.data)
        if event.data.isClosed == True:
            print(_5_min_close)
            print(_15_min_close)
            print(calculate_rsi(_5_min_close))
            print(calculate_sma(_5_min_close, SMA_5MIN_PERIOD))
            print(calculate_ema(_15_min_close, EMA_15MIN_PERIOD))
            print("Event type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Symbol: ", event.symbol)
            print("Data:")
            
            check_positon(SYMBOL)
            collect_closes(event.data.close, _5_min_close)
    else:
        print("Unknown Data:")
    print()



def candle_callback_15min(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
            print("Event ID: ", event)
    elif  data_type == SubscribeMessageType.PAYLOAD:
        # print("15min alive!")
        if event.data.isClosed == True:
            print("Event type: ", event.eventType)
            print("Event time: ", event.eventTime)
            print("Symbol: ", event.symbol)
            print("Data:")    
            PrintBasic.print_obj(event.data)
            collect_closes(event.data.close, _15_min_close)
    else:
        print("Unknown Data:")
    print()


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)



user_session = {"in_position": False}
user_session["balance"] = req_user_data.request_user_balance()["balance"]
check_positon(SYMBOL)
_5_min_close = []
_15_min_close = []


pre_fill_close_list(CURRENT_TIME-UNIX_9DAYS/9, CURRENT_TIME, "5m", _5_min_close)
pre_fill_close_list(CURRENT_TIME-UNIX_9DAYS/3, CURRENT_TIME, "15m", _15_min_close)


sub_client.subscribe_symbol_ticker_event("linkusdt", ticker_callback, error)
sub_client.subscribe_candlestick_event("linkusdt", CandlestickInterval.MIN5, candle_callback_5min, error)
sub_client.subscribe_candlestick_event("linkusdt", CandlestickInterval.MIN15, candle_callback_15min, error)
