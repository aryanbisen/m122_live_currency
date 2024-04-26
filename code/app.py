# Import required modules
from flask import Flask, render_template
from requests import Session
from dotenv import load_dotenv
import os

# Create Flask app instance
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Define the CMC class
class CMC:
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getPrice(self, symbol):
        url = self.apiurl + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()
        return data

    def getTopCurrencies(self, limit=5):
        url = f'{self.apiurl}/v1/cryptocurrency/listings/latest'
        parameters = {'limit': limit}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']
        
        top_currencies = []
        for currency in data[:limit]:
            name = currency['name']
            symbol = currency['symbol']
            price = round(currency['quote']['USD']['price'], 2) 
            top_currencies.append({'name': name, 'symbol': symbol, 'price': price})
        return top_currencies

cmc = CMC(os.getenv('API_KEY'))

@app.route("/")
def home():
        btc_price = cmc.getPrice('BTC')['data']['BTC']['quote']['USD']['price']
        top_currencies = cmc.getTopCurrencies()
        return render_template("index.html", btc_price=btc_price, top_currencies=top_currencies)

if __name__ == '__main__':
    app.run(debug=bool(os.getenv('DEBUG')), port=int(os.getenv('PORT')))
