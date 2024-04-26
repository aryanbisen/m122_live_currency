from flask import Flask, render_template
from requests import Session
import os
from dotenv import load_dotenv


env_path = ".env"

load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

class CMC:
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getAllCoins(self):
        url = self.apiurl + '/v1/cryptocurrency/map'
        r = self.session.get(url)
        data = r.json()['data']
        return data

    def getTopCurrencies(self, limit=5):
        url = f'{self.apiurl}/v1/cryptocurrency/listings/latest'
        parameters = {'limit': limit}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']
        # Sort data based on market capitalization
        sorted_data = sorted(data, key=lambda x: x['quote']['USD']['market_cap'], reverse=True)
        print("\nTop 5 cryptocurrencies by market capitalization:")
        for i, currency in enumerate(sorted_data[:limit], start=1):  # Use sorted_data here
            name = currency['name']
            symbol = currency['symbol']
            price = currency['quote']['USD']['price']
            print(f"{i}. {name} ({symbol}): ${price}")
        return sorted_data

    def getPrice(self, symbol):
        url = self.apiurl + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()
        return data

cmc = CMC(os.getenv("API_KEY"))

@app.route("/")
def home():
    btc_price = cmc.getPrice('BTC')['data']['BTC']['quote']['USD']['price']
    top_currencies = cmc.getTopCurrencies()
    return render_template("index.html", btc_price=btc_price, top_currencies=top_currencies)


if __name__ == '__main__':
    app.run(debug=True,port=5500)