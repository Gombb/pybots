import numpy


def straight_buy(tick_price):
    if tick_price > 0:
        return True


def sma21_bull_buy(tick_price, rsi, sma21, highTFema):    
    rsi_is_bull = rsi[-1] >= 51
    low_crossed_sma = tick_price <= sma21[-1]
    bulltrend = sma21[-2] > highTFema[-2]
    # print(f'rsi is bull: {rsi_is_bull}')
    # print(f'low crossed sma: {price_crossed_sma}')
    # print(f'bulltrend: {bulltrend}')
    result = {"rsi_is_bull": rsi_is_bull, "low_crossed_sma": low_crossed_sma, "bulltrend": bulltrend}    
    if rsi_is_bull and low_crossed_sma and bulltrend:
        return True
    else: 
        print(result)


def sma21_bull_sell(rsi):
    if rsi[-1] >= 80:
        return True
    else:
        return False


def sma21_bear_sell(tick_price, rsi, sma21, highTFema):
    rsi_is_bear = rsi[-1] <= 49
    high_crossed_sma = tick_price >= sma21[-1]
    beartrend = sma21[-2] < highTFema[-2]
    # print("________")
    # print(f'rsi is bear: {rsi_is_bear}')
    # print(f'high crossed sma: {price_crossed_sma}')
    # print(f'beartrend: {beartrend}')
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
