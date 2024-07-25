import os
import requests

coin_market_cap_api_key = os.getenv("COIN_MARKET_CAP_API_KEY")
gold_api_key = os.getenv("GOLD_API_KEY")


def request_crypto_prices():
    try:
        request_url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?CMC_PRO_API_KEY={coin_market_cap_api_key}' \
                      f'&symbol=ETH,XRP,VET,ADA'

        response = requests.get(request_url)
        response.raise_for_status()

        data = response.json()

        ada = round(data["data"]["ADA"]["quote"]["USD"]["price"], 3)
        eth = round(data["data"]["ETH"]["quote"]["USD"]["price"], 2)
        xrp = round(data["data"]["XRP"]["quote"]["USD"]["price"], 3)
        vet = round(data["data"]["VET"]["quote"]["USD"]["price"], 3)

        return ada, eth, xrp, vet

    except requests.exceptions.RequestException:
        print("Something went wrong! An request error occurred.")

        return 0, 0, 0, 0


def request_gold_price():
    symbol = "XAU"
    currency = "USD"

    try:
        request_url = f'https://www.goldapi.io/api/{symbol}/{currency}'
        headers = {
            "x-access-token": gold_api_key,
            "Content-Type": "application/json"
        }

        response = requests.get(request_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        price = data["price_gram_24k"]
        return price

    except requests.exceptions.RequestException:
        print("Something went wrong! An request error occurred.")
        return 0
