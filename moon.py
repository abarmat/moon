#!/usr/bin/env python3

import requests
import argparse
import sys
from datetime import datetime, timedelta

def get_crypto_prices(crypto_ids, currency='usd'):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    ids_param = ','.join(crypto_ids)
    params = {
        'ids': ids_param,
        'vs_currencies': currency
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = {}
        for crypto_id in crypto_ids:
            try:
                prices[crypto_id] = data[crypto_id][currency]
            except KeyError:
                prices[crypto_id] = None
        return prices
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        sys.exit(1)

def get_historical_crypto_prices(crypto_id, currency='usd', days=7):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range'
    params = {
        'vs_currency': currency,
        'from': int(start_date.timestamp()),
        'to': int(end_date.timestamp())
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        prices = data['prices']
        historical_prices = {}
        for price in prices:
            date = datetime.fromtimestamp(price[0] / 1000).strftime('%Y-%m-%d')
            historical_prices[date] = price[1]
        return historical_prices
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
        sys.exit(1)
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Query the current cryptocurrency prices.')
    parser.add_argument('-i', '--crypto_ids', type=str, nargs='+', default=['bitcoin'],
                        help='Cryptocurrency IDs (default: bitcoin). Examples: bitcoin ethereum litecoin.')
    parser.add_argument('-c', '--currency', type=str, default='usd',
                        help='Currency code (default: usd). Examples: usd, eur, gbp, jpy.')
    parser.add_argument('-d', '--historical', type=int, default=0,
                        help='Number of days for historical data (default: 0).')

    args = parser.parse_args()
    crypto_ids = [crypto_id.lower() for crypto_id in args.crypto_ids]
    currency = args.currency.lower()
    historical_days = args.historical

    if historical_days > 0:
        for crypto_id in crypto_ids:
            historical_prices = get_historical_crypto_prices(crypto_id, currency, historical_days)
            print(f"Historical prices for {crypto_id.capitalize()} in {currency.upper()}:")
            for date, price in historical_prices.items():
                print(f"{date}: {price} {currency.upper()}")
    else:
        prices = get_crypto_prices(crypto_ids, currency)
        for crypto_id in crypto_ids:
            price = prices.get(crypto_id)
            if price is not None:
                print(f"The current {crypto_id.capitalize()} price is {price} {currency.upper()}.")
            else:
                print(f"Price for {crypto_id.capitalize()} in {currency.upper()} is not available.")

if __name__ == '__main__':
    main()
