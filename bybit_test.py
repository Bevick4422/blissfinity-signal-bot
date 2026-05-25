from pybit.unified_trading import HTTP

session = HTTP(
    testnet=False,
    api_key="VApIeV6wRpKS5G8cYx",
    api_secret="IeXG0kiJRddUjRAj9q6M9JiHSkSUHy9UPYkg"
)

response = session.get_kline(
    category="linear",
    symbol="BTCUSDT",
    interval="15",
    limit=5
)

print(response)