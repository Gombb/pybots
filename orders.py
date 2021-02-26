import logging
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.model import *
from binance_f.exception.binanceapiexception import BinanceApiException
import config
 

logger = logging.getLogger("binance-futures")
logger.setLevel(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET,  url="https://fapi.binance.com")


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


def limit_buy(symbol_ticker, quantity, price):
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.BUY, ordertype=OrderType.LIMIT, price=price, quantity=quantity, timeInForce=TimeInForce.GTC)


def limit_sell(symbol_ticker, quantity, price):
    result = request_client.post_order(symbol=symbol_ticker, side=OrderSide.SELL, ordertype=OrderType.LIMIT, price=price, quantity=quantity, timeInForce=TimeInForce.GTC)


def cancell_all_order(symbol_ticker):
    result = request_client.cancel_all_orders(symbol=symbol_ticker)
    return result
