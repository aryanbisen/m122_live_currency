from pprint import pp
import requests
from requests import Session
import APIKey

# python ./cmc.py
class CMC:
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getPrice(self, symbol):
        url = self.apiurl + '/v2/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']
        return data

cmc = CMC(APIKey.API_KEY)

btc_price = cmc.getPrice('BTC')['BTC'][0]['quote']['USD']['price']
print(f"Bitcoin price: ${btc_price:.2f} USD")