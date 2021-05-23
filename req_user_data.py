from binance_f import RequestClient
from binance_f.constant import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://fapi.binance.com")


def request_user_balance():
    
    result = request_client.get_balance()
    for dict in result: 
        if dict.asset == "USDT":
           result = dict 
    return {"balance": result.balance, "asset": result.asset}


def request_all_orders_for_symbol(symbol):
    result = request_client.get_all_orders(symbol=symbol)
    return result

def request_user_position():
    result = request_client.get_position()
    return result

# res = request_user_position()
# for i in res:
#     if i.symbol == "LINKUSDT":
#         PrintBasic.print_obj(i)
#         print(type(i))


def request_trading_stats():    
    result = request_client.get_account_trades(symbol="LINKUSDT")
    PrintMix.print_data(result)
    


# PrintMix.print_data(request_user_position())