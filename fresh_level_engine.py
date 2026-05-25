import requests
import pandas as pd

print("\n==============================")
print("FRESH LEVEL ENGINE STARTED")
print("==============================\n")

# =========================================
# PAIR
# =========================================

pair = "BTC_USDT"

print(f"Scanning {pair} for fresh levels...\n")

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

fresh_v_levels = []

fresh_a_levels = []

# =========================================
# DETECT LEVELS
# =========================================

for i in range(1, len(df) - 10):

    previous = df.iloc[i - 1]

    current = df.iloc[i]

    future_data = df.iloc[i + 1:i + 10]

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

        mitigated = False

        # CHECK FUTURE TOUCHES

        for j in range(len(future_data)):

            future_low = future_data.iloc[j]["low"]

            if future_low <= level:

                mitigated = True

                break

        # SAVE ONLY FRESH LEVELS

        if not mitigated:

            fresh_v_levels.append(level)

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

        mitigated = False

        # CHECK FUTURE TOUCHES

        for j in range(len(future_data)):

            future_high = future_data.iloc[j]["high"]

            if future_high >= level:

                mitigated = True

                break

        # SAVE ONLY FRESH LEVELS

        if not mitigated:

            fresh_a_levels.append(level)

# =========================================
# RESULTS
# =========================================

print("================================")
print("FRESH V SHAPE SUPPORT LEVELS")
print("================================\n")

for level in fresh_v_levels[-10:]:

    print(level)

print("\n")

print("================================")
print("FRESH A SHAPE RESISTANCE LEVELS")
print("================================\n")

for level in fresh_a_levels[-10:]:

    print(level)

print("\nEngine completed successfully.")