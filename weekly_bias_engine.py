import requests
import pandas as pd
from datetime import datetime
import pytz

# =========================================
# NIGERIA TIME
# =========================================

nigeria = pytz.timezone("Africa/Lagos")

now = datetime.now(nigeria)

print("\n==============================")
print("WEEKLY BIAS ENGINE STARTED")
print("==============================\n")

print(f"Nigeria Time: {now}\n")

# =========================================
# PAIR
# =========================================

pair = "BTC_USDT"

print(f"Scanning {pair} weekly structure...\n")

# =========================================
# FETCH WEEKLY DATA
# =========================================

url = f"https://contract.mexc.com/api/v1/contract/kline/{pair}?interval=Week1"

response = requests.get(url)

json_data = response.json()

# =========================================
# DEBUG API RESPONSE
# =========================================

print("API RESPONSE RECEIVED\n")

if "data" not in json_data:

    print("ERROR: No data returned from API")

    print(json_data)

    exit()

candles = json_data["data"]

# =========================================
# CREATE DATAFRAME
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

if len(df) < 3:

    print("Not enough weekly candles")

    exit()

# =========================================
# PREVIOUS TWO WEEKS
# =========================================

previous_week = df.iloc[-2]

current_week = df.iloc[-1]

# =========================================
# PRINT WEEK DATA
# =========================================

print("PREVIOUS WEEK:")
print(previous_week)
print("\n")

print("CURRENT WEEK:")
print(current_week)
print("\n")

# =========================================
# V SHAPE SUPPORT
# bearish candle → bullish candle
# =========================================

bullish_v_shape = (

    previous_week["close"] < previous_week["open"]
    and
    current_week["close"] > current_week["open"]

)

# =========================================
# A SHAPE RESISTANCE
# bullish candle → bearish candle
# =========================================

bearish_a_shape = (

    previous_week["close"] > previous_week["open"]
    and
    current_week["close"] < current_week["open"]

)

# =========================================
# WEEKLY BIAS OUTPUT
# =========================================

print("================================")
print("WEEKLY BIAS RESULT")
print("================================\n")

if bullish_v_shape:

    print("BULLISH WEEKLY BIAS DETECTED")

elif bearish_a_shape:

    print("BEARISH WEEKLY BIAS DETECTED")

else:

    print("NO CLEAR WEEKLY BIAS")

print("\nEngine completed successfully.")