import numpy
#21sma5min


def straight_buy(tick_price):
    if tick_price > 0:
        return True


def sma21_bull_buy(tick_price, rsi, sma21, highTFema):
    if rsi[-1] >= 48 and tick_price <= sma21[-1] and sma21[-2] >= highTFema[-2]:
        return True


def sma21_bull_sell(rsi):
    if rsi[-1] >= 78:
        return True


def sma21_bear_sell(tick_price, rsi, sma21, highTFema):
    if rsi[-1] <= 52 and tick_price >= sma21[-1] and sma21[-2] <= highTFema[-2]:
        return True


def sma21_bear_buy(rsi):
    if rsi[-1] <= 24:
        return True

