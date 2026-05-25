import requests
import pandas as pd

print("\n==============================")
print("BOS ENGINE STARTED")
print("==============================\n")

# =========================================
# PAIR
# =========================================

pair = "BTC_USDT"

print(f"Scanning {pair} for BOS...\n")

# =========================================
# FETCH DAILY DATA
# =========================================

url = f"https://contract.mexc.com/api/v1/contract/kline/{pair}?interval=Day1"

response = requests.get(url)

json_data = response.json()

# =========================================
# CHECK API
# =========================================

if "data" not in json_data:

    print("API ERROR")

    print(json_data)

    exit()

candles = json_data["data"]

# =========================================
# DATAFRAME
# =========================================

df = pd.DataFrame({

    "open": candles["open"],
    "close": candles["close"],
    "high": candles["high"],
    "low": candles["low"]

})

# =========================================
# CLEAN DATA
# =========================================

df["open"] = df["open"].astype(float)
df["close"] = df["close"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)

# =========================================
# ENSURE ENOUGH DATA
# =========================================

if len(df) < 20:

    print("Not enough data")

    exit()

# =========================================
# RECENT STRUCTURE
# =========================================

recent_high = (

    df["high"]
    .iloc[-10:-1]
    .max()

)

recent_low = (

    df["low"]
    .iloc[-10:-1]
    .min()

)

latest = df.iloc[-1]

latest_close = latest["close"]

# =========================================
# BOS DETECTION
# =========================================

bullish_bos = (

    latest_close > recent_high

)

bearish_bos = (

    latest_close < recent_low

)

# =========================================
# RESULTS
# =========================================

print("================================")
print("STRUCTURE ANALYSIS")
print("================================\n")

print(f"Recent High: {recent_high}")
print(f"Recent Low: {recent_low}")
print(f"Latest Close: {latest_close}\n")

# =========================================
# FINAL OUTPUT
# =========================================

if bullish_bos:

    print("BULLISH BOS DETECTED")

elif bearish_bos:

    print("BEARISH BOS DETECTED")

else:

    print("NO BOS DETECTED")

print("\nEngine completed successfully.")