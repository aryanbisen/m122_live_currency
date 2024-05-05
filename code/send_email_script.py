import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests import Session
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

class CoinMarketCap:
    def __init__(self, api_key):
        self.api_url = 'https://pro-api.coinmarketcap.com'     
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
        self.session = Session()
        self.session.headers.update(self.headers)

    def get_price(self, symbol):
        # Endpoint URL for getting cryptocurrency price
        url = self.api_url + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()
        return data

    def get_top_currencies(self, limit=5):
        # Endpoint URL for getting top cryptocurrencies
        url = f'{self.api_url}/v1/cryptocurrency/listings/latest'
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
    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    port = 587
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = receiver_email
    msg['Subject'] = "Top Cryptocurrencies Prices"

    # Attach message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Establish connection and send email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver_email, msg.as_string())
        server.quit()
        # Log successful email sending with timestamp
        log_message = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Email sent successfully"
        with open('log.txt', 'a') as log_file:
            log_file.write(log_message + '\n')
            
    except Exception as e:
        print("Error sending email:", e)

def main():
    cmc = CoinMarketCap(os.getenv('API_KEY'))
    btc_price = cmc.get_price('BTC')['data']['BTC']['quote']['USD']['price']
    top_currencies = cmc.get_top_currencies()
    
    # Compose email message
    email_message = f"Current Bitcoin Price\n${btc_price}\n\nTop 5 Cryptocurrencies\n"
    for currency in top_currencies:
        email_message += f"{currency['name']}: ${currency['price']}\n"
    receiver_email = os.getenv('RECEIVER_EMAIL')
    # Send email
    send_email(receiver_email, email_message)

if __name__ == "__main__":
    main()
