import numpy
#21sma5min


def straight_buy(tick_price):
    if tick_price > 0:
        return True


def sma21_bear_backcross(sma_5min, ema_15min):
    if sma_5min[-1] < ema_15min[-1] and sma_5min[-2] < ema_15min[-1]:
        return True


def sma21_bull_backcross(sma_5min, ema_15min):
    if sma_5min[-1] > ema_15min[-1] and sma_5min[-2] > ema_15min[-1]:
        return True



def bull_trend(low_moving_average, high_moving_average):
    return low_moving_average[-2] > high_moving_average[-2]



def bear_trend(low_moving_average, high_moving_average):
    return high_moving_average[-2] > low_moving_average[-2]



def sma21_bull_buy(tick_price, rsi, low_TF_MA, high_TF_MA):    
    rsi_is_bull = rsi[-1] >= 51
    low_crossed_sma = tick_price <= low_TF_MA[-1]
    bulltrend = low_TF_MA[-1] > high_TF_MA[-1]
    print(f'rsi is bull: {rsi_is_bull}')
    print(f'low crossed sma: {low_crossed_sma}')
    print(f'bulltrend: {bulltrend}')
    result = {"rsi_is_bull": rsi_is_bull, "low_crossed_sma": low_crossed_sma, "bulltrend": bulltrend}    
    if rsi_is_bull and low_crossed_sma and bulltrend:
        return True
    else: 
        print(result)


def sma21_bull_sell(rsi):
    if rsi[-1] >= 79:
        return True
    else:
        return False


def sma21_bear_sell(tick_price, rsi, low_TF_MA, high_TF_MA):
    rsi_is_bear = rsi[-1] <= 49
    high_crossed_sma = tick_price >= low_TF_MA[-1]
    beartrend = high_TF_MA[-1] > low_TF_MA[-1]
    print("________")
    print(f'rsi is bear: {rsi_is_bear}')
    print(f'high crossed sma: {high_crossed_sma}')
    print(f'beartrend: {beartrend}')
    result = {"rsi_is_bear": rsi_is_bear, "high_crossed_sma": high_crossed_sma, "beartrend": beartrend}
    if rsi_is_bear and high_crossed_sma and beartrend:
        return True
    else:
        print(result)


def sma21_bear_buy(rsi):
    if rsi[-1] <= 24:
        return True


def test_TP(rsi):
    if rsi[-1] > 25:
        return True 

