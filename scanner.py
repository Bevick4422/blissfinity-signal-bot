import requests
import pandas as pd

def fetch_data(pair, timeframe):

    url = f"https://contract.mexc.com/api/v1/contract/kline/{pair}?interval={timeframe}"

    response = requests.get(url)

    data = response.json()["data"]

    df = pd.DataFrame({
        "close": data["close"],
        "high": data["high"],
        "low": data["low"]
    })

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    return df