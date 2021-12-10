#!/usr/bin/env python
import pprint

from bit2c_trader import Bit2cTrader
from bitstamp_trader import BitstampTrader


bitstamp_trader = BitstampTrader()
bit2c_trader = Bit2cTrader()


"""
~~~~~~~~~~
Exercise 1
~~~~~~~~~~

The implementation of querying the trader is implemented in the *_trader.py file and classes.

bit2c support only NIS fiat currency, while bitstamp support USD, EUR, and GBP.
As the is no common fiat, we can't compare ETH price directly.
One option is to use another change platform to change NIS<-->USD, but it didn't was part of the exercise.
So I decided to compare crypto-to-crypto price, with the common bitcoin crypto currency.

Bit2c doesn't support crypto-to-crypto.
The way for converting ETH<-->BTC is using ETH<-->NIS<-->BTC path, as I implemented it Bit2cTrader.btc2eth().
"""


def main_exe_1():
    # bitstamp gives only ethbtc but not btceth, so we calculate ourselves:
    bitstamp_eth2btc = bitstamp_trader.get_price('ethbtc')
    bitstamp_btc2eth = 1 / bitstamp_eth2btc
    bit2c_btc2eth = bit2c_trader.btc2eth()  # BTC->NIS->ETH

    print(f'bitstamp: {bitstamp_btc2eth} btc/eth')
    print(f'bit2c: {bit2c_btc2eth} btc/eth')

    buy_etherium_from = 'Bit2c' if bit2c_btc2eth > bitstamp_btc2eth else 'Bitstamp'

    print(f'If you have bitcoin and want to buy Ethereum, use {buy_etherium_from}.')


"""
~~~~~~~~~~
Exercise 2
~~~~~~~~~~

I implemented the logic in incremental method, as you can see from calc_price_1 to 3.
I think that calc_price_3 is the best one.

One can give calc_price different amount, and asks for different currency pairs.


I didn't put effort for writing it "the right way", but the next step is it:

class OrderbookTransaction:
    pass
class OrderbookTransactionSet:
    @property
    def total_price(self):
    
    @property
    def total_amount(self):
    
    def add_transaction(transaction):
    
    def remove_transaction(transaction):
    
    ....
    

"""


def calc_price_1(asks, buy_amount, **kwargs):
    total_taken_amount = 0
    total_taken_price = 0
    taken_asks = []

    for ask in asks:
        rate, amount = float(ask[0]), float(ask[1])
        if total_taken_amount + amount < buy_amount:
            taken_asks.append(ask)
            total_taken_amount += amount
            total_taken_price += rate * amount
    return total_taken_price, total_taken_amount, taken_asks


def calc_price_2(asks, buy_amount, percent_diff, **kwargs):
    total_taken_amount = 0
    total_taken_price = 0
    taken_asks = []

    for ask in asks:
        rate, amount = float(ask[0]), float(ask[1])
        if total_taken_amount + amount < buy_amount * (100 + percent_diff) / 100.0:
            taken_asks.append(ask)
            total_taken_amount += amount
            total_taken_price += rate * amount
        if abs(total_taken_amount - buy_amount) < buy_amount * percent_diff / 100.0:
            break
    return total_taken_price, total_taken_amount, taken_asks


def calc_price_3(asks, buy_amount, percent_diff, **kwargs):
    total_taken_amount = 0
    total_taken_price = 0
    taken_asks = []

    for ask in asks:
        rate, amount = float(ask[0]), float(ask[1])
        if total_taken_amount + amount < buy_amount * (100 + percent_diff) / 100.0:
            taken_asks.append(ask)
            total_taken_amount += amount
            total_taken_price += rate * amount
        if abs(total_taken_amount - buy_amount) < buy_amount * percent_diff / 100.0:
            diff = total_taken_amount - buy_amount
            if diff > 0:
                for ask in taken_asks:
                    if float(ask[1]) < diff:
                        taken_asks.remove(ask)
                        price = float(ask[0]) * float(ask[1])
                        total_taken_amount -= float(ask[1])
                        total_taken_price -= price
                        diff -= price
            break
    return total_taken_price, total_taken_amount, taken_asks


def main_exe_2():
    order_book = bitstamp_trader.get_orderbook('ethbtc')
    asks = order_book['asks']
    print(f'Asks:')

    # Print only first 20 asks (don't spam the user)
    pprint.pprint(asks[:20])

    calc_price_funcs = [
        calc_price_1,
        calc_price_2,
        calc_price_3,
    ]
    for calc_price in calc_price_funcs:
        name = calc_price.__name__
        price, amount, taken_asks = calc_price(asks=asks, buy_amount=1.0, percent_diff=3)
        print(f'{name}: Total price: {price}, Total amount: {amount}. Rate: {price / amount}')
        print('Asks:')
        pprint.pprint(taken_asks)


if __name__ == '__main__':
    main_exe_1()
    main_exe_2()

