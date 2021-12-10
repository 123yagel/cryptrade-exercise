import json
import requests

from crypto_trader import CryptoTrader


class BitstampTrader(CryptoTrader):
    _ALLOWED_CURR_PAIRS = {'btcusd', 'btceur', 'btcgbp', 'btcpax', 'btcusdt', 'btcusdc', 'gbpusd', 'gbpeur', 'eurusd',
                           'ethusd', 'etheur', 'ethbtc', 'ethgbp', 'ethpax', 'ethusdt', 'ethusdc', 'adausd', 'adaeur',
                           'adabtc', 'xrpusd', 'xrpeur', 'xrpbtc', 'xrpgbp', 'xrppax', 'xrpusdt', 'uniusd', 'unieur',
                           'unibtc', 'ltcusd', 'ltceur', 'ltcbtc', 'ltcgbp', 'linkusd', 'linkeur', 'linkbtc', 'linkgbp',
                           'linketh', 'maticusd', 'maticeur', 'xlmusd', 'xlmeur', 'xlmbtc', 'xlmgbp', 'fttusd',
                           'ftteur', 'bchusd', 'bcheur', 'bchbtc', 'bchgbp', 'aaveusd', 'aaveeur', 'aavebtc', 'axsusd',
                           'axseur', 'algousd', 'algoeur', 'algobtc', 'compusd', 'compeur', 'compbtc', 'snxusd',
                           'snxeur', 'snxbtc', 'hbarusd', 'hbareur', 'chzusd', 'chzeur', 'celusd', 'celeur', 'enjusd',
                           'enjeur', 'batusd', 'bateur', 'batbtc', 'mkrusd', 'mkreur', 'mkrbtc', 'zrxusd', 'zrxeur',
                           'zrxbtc', 'audiousd', 'audioeur', 'audiobtc', 'sklusd', 'skleur', 'yfiusd', 'yfieur',
                           'yfibtc', 'sushiusd', 'sushieur', 'alphausd', 'alphaeur', 'storjusd', 'storjeur', 'sxpusd',
                           'sxpeur', 'grtusd', 'grteur', 'umausd', 'umaeur', 'umabtc', 'omgusd', 'omgeur', 'omgbtc',
                           'omggbp', 'kncusd', 'knceur', 'kncbtc', 'crvusd', 'crveur', 'crvbtc', 'sandusd', 'sandeur',
                           'fetusd', 'feteur', 'rgtusd', 'rgteur', 'slpusd', 'slpeur', 'eurtusd', 'eurteur', 'usdtusd',
                           'usdteur', 'usdcusd', 'usdceur', 'usdcusdt', 'daiusd', 'paxusd', 'paxeur', 'paxgbp',
                           'eth2eth', 'gusdusd'}

    def connect(self):
        pass

    def get_ticker(self, currency_pair):
        resp = requests.get(f'https://www.bitstamp.net/api/v2/ticker/{currency_pair}')
        if resp.status_code != 200:
            raise RuntimeError(f'Can\'t get ticker information for {currency_pair}, got status code: {resp.status_code}')
        return json.loads(resp.content)

    def _get_price(self, curr_pair):
        return self.get_ticker(curr_pair)['last']

    def get_orderbook(self, currency_pair):
        resp = requests.get(f'https://www.bitstamp.net/api/v2/order_book/{currency_pair}/')
        if resp.status_code != 200:
            raise RuntimeError(f'Can\'t get orderbook information for {currency_pair}, got status code: {resp.status_code}')
        return json.loads(resp.content)



