import logging
from binance_f import SubscriptionClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.base.printobject import *
import talib, numpy
import talib.abstract as ta
from time import time
import req_historical, req_user_data, data_manager
from strat import *
from config import *
from orders import *
import datetime



RSI_PERIOD = 14
SMA_5MIN_PERIOD = 21
EMA_15MIN_PERIOD = 50
SYMBOL = 'LINKUSDT'
CURRENT_TIME = int(time() * 1000)
UNIX_9DAYS = 691200000
POS_SIZE = 1
BUY_STOP_LVL = 0.92
SELL_STOP_LVL = 1.02

logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
sub_client = SubscriptionClient(api_key=API_KEY, secret_key=API_SECRET, uri="wss://fstream.binance.com/ws")

def sync_session_positon(symbol_ticker):
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


def check_position_limit(smybol_ticker):
    pass



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


def swap_unix_to_date(unix_value, mode="mili"):
    if mode == "mili":
        timestamp = datetime.datetime.fromtimestamp(unix_value/1000.0)    
    else:
        timestamp = datetime.datetime.fromtimestamp(unix_value)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def save_trades_data(side, strat, exec_prirce, quantity, rsi_last, sma__1, sma__2, ema_last):
    existing_data = data_manager.read_csv(data_manager.TRADE_HISTORY_PATH)
    current_time = swap_unix_to_date(CURRENT_TIME)
    current_data = {"time": current_time, "side": side, "strat": strat, "exec_price": exec_prirce, "quantity": quantity, "rsi": rsi_last, "-1 sma": sma__1, "-2 sma": sma__2, "ema": ema_last}
    existing_data.append(current_data)
    data_manager.write_csv(data_manager.TRADE_HISTORY_HEADERS, data_manager.TRADE_HISTORY_PATH, existing_data)


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
        print(f'last RSI value ||  {rsi_5min[-1]}')
        print(f'last SMA value || [-1] {sma_5min[-1]} || [-2] {sma_5min[-2]} || [-3] {sma_5min[-3]}')
        print(f'last EMA value ||  {ema_15min[-1]}')
        if user_session["in_position"] == False:
            # if straight_buy(tick_price):
            #     order = market_buy(SYMBOL, order_size)
            #     user_session["in_position"] = True
            #     user_session["active_position"] = "+ "+ str(order.origQty)
            #     buy_stop(SYMBOL, user_session["active_position"].split(" ")[1], str(round(tick_price * BUY_STOP_LVL, 3)))
            #     save_trades_data("bull", "straight_buy", tick_price, order.origQty)
            if sma21_bull_buy(tick_price, rsi_5min, sma_5min, ema_15min):
                order = market_buy(SYMBOL, order_size)
                save_trades_data("bull", "sma21_entry", tick_price, order.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                user_session["in_position"] = True
                user_session["active_position"] = "+ " + str(order.origQty)
                buy_stop(SYMBOL, str(order.origQty), str(round(tick_price * BUY_STOP_LVL, 3)))
            if sma21_bear_sell(tick_price, rsi_5min, sma_5min, ema_15min) == True:
                order = market_sell(SYMBOL, order_size)
                save_trades_data("bear", "sma21_entry", tick_price, order.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                user_session["in_position"] = True
                user_session["active_position"] = "- "+ str(order.origQty)
                sell_stop(SYMBOL, str(order.origQty), str(round(tick_price * SELL_STOP_LVL, 3)))
            

        if user_session["in_position"] == True:
            positional_direction = user_session["active_position"].split(" ")[0]
            if positional_direction == "+":
                if sma21_bull_sell(rsi_5min):
                    user_session["in_position"] = False
                    sell_order = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
                    save_trades_data("bull", "sma21_exit", tick_price, sell_order.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    user_session["active_position"] = 0 
                    cancel_order = cancell_all_order(SYMBOL)    
                    PrintBasic.print_obj(sell_order)
                    PrintBasic.print_obj(cancel_order)
            
            if positional_direction == "-":  
                if sma21_bear_buy(rsi_5min):
                    buy_order = market_buy(SYMBOL, user_session["active_position"].split(" ")[1])
                    save_trades_data("bear", "sma21_exit", tick_price, buy_order.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    user_session["in_position"] = False
                    user_session["active_position"] = 0
                    cancel_order = cancell_all_order(SYMBOL)
                    PrintBasic.print_obj(buy_order)
                    PrintBasic.print_obj(cancel_order)
            
                    
            
          
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
            
            sync_session_positon(SYMBOL)
            collect_closes(event.data.close, _5_min_close)
            positional_direction = user_session["active_position"].split(" ")[0]
            rsi_5min = calculate_rsi(_5_min_close)
            sma_5min = calculate_sma(_5_min_close, SMA_5MIN_PERIOD)
            ema_15min = calculate_ema(_15_min_close, EMA_15MIN_PERIOD)
            order_size = str(round(user_session["balance"] * POS_SIZE / _5_min_close[-1], 2))
            if positional_direction == "-":
                if sma_5min[-1] > ema_15min[-1] and sma_5min[-2] > ema_15min[-1] and sma_5min[-3] > ema_15min[-1]:
                    short_close = market_buy(SYMBOL, user_session["active_position"].split(" ")[1])
                    cancel_order = cancell_all_order(SYMBOL)
                    save_trades_data("bear", "sma21_backcross_exit", _5_min_close[-1], short_close.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    long_open = market_buy(SYMBOL, order_size)
                    buy_stop(SYMBOL, str(long_open.origQty), str(round(_5_min_close * BUY_STOP_LVL, 3)))
                    save_trades_data("bear", "sma21_backcross_entry", _5_min_close[-1], long_open.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    sync_session_positon(SYMBOL)
            if positional_direction == "+":
                if sma_5min[-1] < ema_15min[-1] and sma_5min[-2] < ema_15min[-1] and sma_5min[-3] < ema_15min[-1]:
                    long_close = market_sell(SYMBOL, user_session["active_position"].split(" ")[1])
                    cancel_order = cancell_all_order(SYMBOL)
                    save_trades_data("bull", "sma21_backcross_exit", _5_min_close[-1], long_close.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    short_open = market_sell(SYMBOL, order_size)
                    sell_stop(SYMBOL, str(short_open.origQty), str(round(_5_min_close[-1] * SELL_STOP_LVL, 3)))
                    save_trades_data("bull", "sma21_backceoss_entry", _5_min_close[-1], short_open.origQty, rsi_5min[-1], sma_5min[-1], sma_5min[-2], ema_15min[-1])
                    sync_session_positon(SYMBOL)



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
