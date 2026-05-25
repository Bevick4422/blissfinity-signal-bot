import requests
import pandas as pd

print("\n==============================")
print("DAILY BOS WATCHLIST ENGINE")
print("==============================\n")

# =========================================
# LOAD WATCHLISTS
# =========================================

try:

    with open("bullish_watchlist.txt", "r") as file:

        bullish_pairs = [

            line.strip()
            for line in file.readlines()
            if line.strip()

        ]

except:

    bullish_pairs = []

try:

    with open("bearish_watchlist.txt", "r") as file:

        bearish_pairs = [

            line.strip()
            for line in file.readlines()
            if line.strip()

        ]

except:

    bearish_pairs = []

# =========================================
# STORAGE
# =========================================

confirmed_bullish = []

confirmed_bearish = []

# =========================================
# BULLISH BOS SCAN
# =========================================

print("SCANNING BULLISH WATCHLIST...\n")

for pair in bullish_pairs:

    try:

        print(f"Scanning {pair}...")

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Day1"
        )

        response = requests.get(url)

        json_data = response.json()

        if "data" not in json_data:

            print("API Error")

            continue

        candles = json_data["data"]

        df = pd.DataFrame({

            "open": candles["open"],
            "close": candles["close"],
            "high": candles["high"],
            "low": candles["low"]

        })

        # =================================
        # CLEAN DATA
        # =================================

        df["open"] = df["open"].astype(float)
        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        if len(df) < 15:

            print("Not enough data")

            continue

        # =================================
        # DAILY BOS
        # =================================

        recent_high = (

            df["high"]
            .iloc[-10:-1]
            .max()

        )

        latest_close = (

            df.iloc[-1]["close"]

        )

        bullish_bos = (

            latest_close > recent_high

        )

        if bullish_bos:

            confirmed_bullish.append(pair)

            print(f"{pair} → BULLISH BOS CONFIRMED")

        else:

            print(f"{pair} → No BOS")

    except Exception as e:

        print(f"Error scanning {pair}")

        print(e)

# =========================================
# BEARISH BOS SCAN
# =========================================

print("\nSCANNING BEARISH WATCHLIST...\n")

for pair in bearish_pairs:

    try:

        print(f"Scanning {pair}...")

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Day1"
        )

        response = requests.get(url)

        json_data = response.json()

        if "data" not in json_data:

            print("API Error")

            continue

        candles = json_data["data"]

        df = pd.DataFrame({

            "open": candles["open"],
            "close": candles["close"],
            "high": candles["high"],
            "low": candles["low"]

        })

        # =================================
        # CLEAN DATA
        # =================================

        df["open"] = df["open"].astype(float)
        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        if len(df) < 15:

            print("Not enough data")

            continue

        # =================================
        # DAILY BOS
        # =================================

        recent_low = (

            df["low"]
            .iloc[-10:-1]
            .min()

        )

        latest_close = (

            df.iloc[-1]["close"]

        )

        bearish_bos = (

            latest_close < recent_low

        )

        if bearish_bos:

            confirmed_bearish.append(pair)

            print(f"{pair} → BEARISH BOS CONFIRMED")

        else:

            print(f"{pair} → No BOS")

    except Exception as e:

        print(f"Error scanning {pair}")

        print(e)

# =========================================
# SAVE CONFIRMED FILES
# =========================================

with open("confirmed_bullish.txt", "w") as file:

    for pair in confirmed_bullish:

        file.write(pair + "\n")

with open("confirmed_bearish.txt", "w") as file:

    for pair in confirmed_bearish:

        file.write(pair + "\n")

# =========================================
# FINAL RESULTS
# =========================================

print("\n==============================")
print("CONFIRMED DAILY BOS")
print("==============================\n")

print("CONFIRMED BULLISH:\n")

for pair in confirmed_bullish:

    print(pair)

print("\n")

print("CONFIRMED BEARISH:\n")

for pair in confirmed_bearish:

    print(pair)

print("\nConfirmed watchlists saved successfully.")