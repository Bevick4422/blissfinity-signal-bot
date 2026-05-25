import requests

print("Connecting to MEXC...")

url = "https://contract.mexc.com/api/v1/contract/kline/BTC_USDT?interval=Min15"

response = requests.get(url)

print("Status Code:", response.status_code)

print("Response:")
print(response.text)