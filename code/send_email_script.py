import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests import Session
from dotenv import load_dotenv
import datetime

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
        
def send_email(receiver_email, message):
    smtp_server = "smtp.gmail.com"
    port = 587
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_email
    msg['Subject'] = "Top Cryptocurrencies Prices"

    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver_email, msg.as_string())
        server.quit()
        log_message = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Email sent successfully"
        with open('/mnt/c/Github_repositories/TBZ/m122_live_currency/code/log.txt', 'a') as log_file:
            log_file.write(log_message + '\n')
            
    except Exception as e:
        print("Error sending email:", e)

def main():
    cmc = CMC(os.getenv('API_KEY'))
    btc_price = cmc.getPrice('BTC')['data']['BTC']['quote']['USD']['price']
    top_currencies = cmc.getTopCurrencies()
    email_message = f"Current Bitcoin Price\n${btc_price}\n\nTop 5 Cryptocurrencies\n"
    for currency in top_currencies:
        email_message += f"{currency['name']}: ${currency['price']}\n"
    receiver_email = os.getenv('RECEIVER_EMAIL')
    send_email(receiver_email, email_message)

if __name__ == "__main__":
    main()