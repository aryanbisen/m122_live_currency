# Cryptocurrency Price Checker

This Python script retrieves the current price of Bitcoin and the top 5 cryptocurrencies from the CoinMarketCap API and sends an email with the information.

## Installation
1. Clone the repository.
2. Install the required packages:
    - `python-dotenv`: For loading environment variables from a `.env` file.
    - `requests`: For making HTTP requests to the CoinMarketCap API.
    - `Flask-Mail`: For sending emails via SMTP in Flask applications.

3. Set up environment variables by creating a `.env` file in the root directory and adding the following variables:
    ```plaintext
    API_KEY=your_coinmarketcap_api_key
    EMAIL=your_email@gmail.com
    PASSWORD=your_email_password
    RECEIVER_EMAIL=recipient_email@example.com
    ```
   
## Notes
- The email functionality only supports Gmail. If you're using a different email provider, you might need to modify the SMTP server settings.
- Make sure to create an app password when you're using gmail.

## Additional Information
Within the repository, you'll discover two Python files.
- `send_email_script.py`: This script is for sending emails and cronjob usage
- `app.py`: This script is for sending emails and for displaying the prices on a webpage with flask.
