from flask import Flask, render_template
from requests import Session
import APIKey

app = Flask(__name__)

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

cmc = CMC(APIKey.API_KEY)

@app.route("/")
def home():
    btc_price = cmc.getPrice('BTC')['data']['BTC']['quote']['USD']['price']
    return render_template("index.html", btc_price=btc_price)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
