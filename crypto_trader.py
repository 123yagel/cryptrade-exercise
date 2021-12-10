from abc import ABC, abstractmethod


class CryptoTrader(ABC):
    _ALLOWED_CURR_PAIRS = []
    def __init__(self):
        self.connect()

    @abstractmethod
    def connect(self):
        #  When using Websockets, connect here
        pass

    @abstractmethod
    def _get_price(self, curr_pair):
        pass

    def get_price(self, curr_pair):
        if curr_pair not in self._ALLOWED_CURR_PAIRS:
            raise RuntimeError(f'There is no such currency pair ({curr_pair}) in trader {self.__class__.__name__}')
        return float(self._get_price(curr_pair))
