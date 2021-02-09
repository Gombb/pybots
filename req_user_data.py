from binance_f import RequestClient
from binance_f.constant import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://fapi.binance.com")


def request_user_balance():
    
    result = request_client.get_balance()
    return {"balance": result[0].balance, "asset": result[0].asset}



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