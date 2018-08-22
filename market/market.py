# from account_config import exs_config
import pendulum
import traceback
import ccxt
import time
from copy import deepcopy
from decimal import Decimal
import math


class Market(object):
    def __init__(self, ex_name):
        self.ex_name = ex_name
        # api key
        # self.key_name = key_name
        if self.ex_name == 'binance':
            self.exchange = ccxt.binance()
        elif self.ex_name == 'okex':
            self.exchange = ccxt.okex
        elif self.ex_name == 'huobipro':
            self.exchange = ccxt.huobipro
        # self.exchange.apiKey = exs_config[self.ex_name][self.key_name]['ACCESS_KEY']
        # self.exchange.secret = exs_config[self.ex_name][self.key_name]['SECRET_KEY']
