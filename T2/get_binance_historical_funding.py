import requests
import csv
import time
from datetime import datetime, timedelta

# Read available symbols from the previous CSV
input_csv = 'T2/binance_funding_symbol_check.csv'
output_csv = 'T2/historical_funding_rates.csv'

symbols = []
with open(input_csv, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['available_on_binance'] == 'True':
            symbols.append((row['coin'], row['symbol']))

# Binance API endpoint
url = "https://fapi.binance.com/fapi/v1/fundingRate"

# Get timestamps for the last 30 days
end_time = int(time.time() * 1000)
start_time = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

all_rows = []

for coin, symbol in symbols:
    print(f"Fetching {symbol}...")
    params = {
        'symbol': symbol,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000
    }
    done = False
    while not done:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            for entry in data:
                all_rows.append({
                    'timestamp': entry['fundingTime'],
                    'coin': coin,
                    'symbol': symbol,
                    'fundingRate': entry['fundingRate']
                })
            # If we got less than 1000, we're done
            if len(data) < 1000:
                done = True
            else:
                # Move start_time forward
                params['startTime'] = int(data[-1]['fundingTime']) + 1
        else:
            done = True
        time.sleep(0.2)

# Write all funding rates to a single CSV
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'coin', 'symbol', 'fundingRate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_rows:
        writer.writerow(row)

print(f"Done. Historical funding rates saved to {output_csv}") 