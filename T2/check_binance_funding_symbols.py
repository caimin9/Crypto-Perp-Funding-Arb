import requests
import csv
import time

# List of coins from the dashboard images
coins = [
    'MORPHO', 'ORDI', 'TIA', 'INJ', 'HYPER', 'PEPE', 'DOGE', 'UNI', 'LDO', 'ARB',
    'OP', 'WIF', 'JUP', 'ETH', 'BTC', 'SOL', 'W'
]

# Binance perp symbols are usually COINUSDT
symbols = [f"{coin}USDT" for coin in coins]

# Binance API endpoint for funding rates
url = "https://fapi.binance.com/fapi/v1/fundingRate"

results = []

for coin, symbol in zip(coins, symbols):
    params = {
        'symbol': symbol,
        'limit': 1  # Only need the latest
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            available = True
            funding_rate = data[0]['fundingRate']
        else:
            available = False
            funding_rate = None
    except Exception as e:
        available = False
        funding_rate = None
    results.append({
        'coin': coin,
        'symbol': symbol,
        'available_on_binance': available,
        'latest_funding_rate': funding_rate
    })
    time.sleep(0.2)  # Be nice to the API

# Write results to CSV
with open('T2/binance_funding_symbol_check.csv', 'w', newline='') as csvfile:
    fieldnames = ['coin', 'symbol', 'available_on_binance', 'latest_funding_rate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print("Check complete. Results saved to T2/binance_funding_symbol_check.csv") 