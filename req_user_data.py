from binance_d import RequestClient
from binance_d.constant import *
from binance_d.base.printobject import *
from binance_d.model.constant import *
from config import *


request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://dapi.binance.com")


def request_user_balance(asset):
    
    result = request_client.get_balance()
    for i in result:
        if i.asset == asset:
            return {"balance": i.balance, "asset": i.asset}


def request_user_position():
    result = request_client.get_position()
    return result


def request_trading_stats():    
    result = request_client.get_account_trades(symbol="LINKUSDT")
    PrintMix.print_data(result)