import requests
from requests import Session
import APIKey
from pprint import pprint as pp

class CMC:
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token,}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getAllCoins(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data



    def getPrice(self, symbol):
        url = self.apiurl + '/v2/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']['BTC'][0]['quote']['USD']['price']
        return data

cmc = CMC(APIKey.API_KEY)

# Get Bitcoin price
bitcoin_price = cmc.getPrice('BTC')
print(f"The current price of Bitcoin is: ${bitcoin_price}")


