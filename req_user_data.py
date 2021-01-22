from binance_f import RequestClient
from binance_f.constant import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from config import *
request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET, url="https://fapi.binance.com")


def request_user_balance():
    
    result = request_client.get_balance()
    return {"balance": result[0].balance, "asset": result[0].asset}
