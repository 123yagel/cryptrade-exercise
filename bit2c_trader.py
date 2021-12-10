import json

import requests

from crypto_trader import CryptoTrader

GET_PRICE_URL = 'https://bit2c.co.il/Exchanges/GetPrice?IsBid=true&total=1&pair={}&amount=0'

TRADER_WEBSOCKET_URL = 'wss://bit2c.co.il/signalr/connect?transport=webSockets&clientProtocol=2.1'
# TODO: implement using this websocket


class Bit2cTrader(CryptoTrader):
    _ALLOWED_CURR_PAIRS = {'BtcNis', 'EthNis', 'BchabcNis', 'LtcNis', 'EtcNis', 'BtgNis', 'LtcBtc', 'BchsvNis',
                           'GrinNis'}

    def connect(self):
        pass

    def _get_price(self, curr_pair):
        resp = requests.get(GET_PRICE_URL.format(curr_pair))
        if resp.status_code != 200:
            raise RuntimeError(f'Can\'t get ticker information for {curr_pair}, got status code: {resp.status_code}')
        # Keys: (['amount', 'total', 'av_price', 'min_price', 'max_price']
        return json.loads(resp.content)['max_price']

    def btc2eth(self):
        btc2nis = self.get_price('BtcNis')
        eth2nis = self.get_price('EthNis')
        return btc2nis / eth2nis

