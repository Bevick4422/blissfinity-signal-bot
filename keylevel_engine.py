import requests
import pandas as pd

print("\n==============================")
print("KEY LEVEL ENGINE STARTED")
print("==============================\n")

# =========================================
# PAIR
# =========================================

pair = "BTC_USDT"

print(f"Scanning {pair} for key levels...\n")

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
# STORAGE
# =========================================

v_shape_levels = []

a_shape_levels = []

# =========================================
# DETECT LEVELS
# =========================================

for i in range(1, len(df)):

    previous = df.iloc[i - 1]

    current = df.iloc[i]

    # =====================================
    # V SHAPE SUPPORT
    # bearish → bullish
    # =====================================

    if (

        previous["close"] < previous["open"]
        and
        current["close"] > current["open"]

    ):

        level = previous["low"]

        v_shape_levels.append(level)

    # =====================================
    # A SHAPE RESISTANCE
    # bullish → bearish
    # =====================================

    elif (

        previous["close"] > previous["open"]
        and
        current["close"] < current["open"]

    ):

        level = previous["high"]

        a_shape_levels.append(level)

# =========================================
# RESULTS
# =========================================

print("================================")
print("V SHAPE SUPPORT LEVELS")
print("================================\n")

for level in v_shape_levels[-10:]:

    print(level)

print("\n")

print("================================")
print("A SHAPE RESISTANCE LEVELS")
print("================================\n")

for level in a_shape_levels[-10:]:

    print(level)

print("\nEngine completed successfully.")