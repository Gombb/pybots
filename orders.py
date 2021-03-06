import logging
import config
import math
from binance_d import RequestClient
from binance_d.constant.test import *
from binance_d.model import *
from binance_d.exception.binanceapiexception import BinanceApiException


logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET,  url="https://dapi.binance.com")


def sell_stop(symbol_ticker, quantity, stop_price):
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.BUY, ordertype=OrderType.STOP_MARKET, quantity=quantity, stopPrice=stop_price, closePosition=True)
    return result


def buy_stop(symbol_ticker, quantity, stop_price):
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, quantity=quantity, stopPrice=stop_price, closePosition=True)
    return result


def market_buy(symbol_ticker, quantity): 
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=quantity)
    return result


def market_sell(symbol_ticker, quantity): 
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.SELL, ordertype=OrderType.MARKET, quantity=quantity)
    return result


def cancell_all_order(symbol_ticker):
    result = request_client.cancel_all_orders(symbol=symbol_ticker)
    return result


