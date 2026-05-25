import requests
import pandas as pd
from datetime import datetime
import pytz

print("\n==============================")
print("WEEKLY WATCHLIST ENGINE")
print("==============================\n")

# =========================================
# NIGERIA TIME
# =========================================

nigeria = pytz.timezone("Africa/Lagos")

now = datetime.now(nigeria)

print(f"Nigeria Time: {now}\n")

# =========================================
# PAIRS
# =========================================

pairs = [

    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XRP_USDT",
    "BNB_USDT",
    "DOGE_USDT",
    "ADA_USDT",
    "LINK_USDT",
    "AVAX_USDT",
    "MATIC_USDT",
    "ATOM_USDT",
    "LTC_USDT",
    "TRX_USDT",
    "APT_USDT",
    "ARB_USDT",
    "OP_USDT",
    "INJ_USDT",
    "SEI_USDT",
    "TIA_USDT",
    "SUI_USDT"
]

# =========================================
# STORAGE
# =========================================

bullish_watchlist = []

bearish_watchlist = []

# =========================================
# SCAN PAIRS
# =========================================

for pair in pairs:

    try:

        print(f"Scanning {pair}...")

        # =================================
        # WEEKLY DATA
        # =================================

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Week1"
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

        if len(df) < 3:

            print("Not enough data")

            continue

        # =================================
        # WEEKLY STRUCTURE
        # =================================

        previous_week = df.iloc[-2]

        current_week = df.iloc[-1]

        # =================================
        # BULLISH V SHAPE
        # bearish → bullish
        # =================================

        bullish_bias = (

            previous_week["close"] < previous_week["open"]
            and
            current_week["close"] > current_week["open"]

        )

        # =================================
        # BEARISH A SHAPE
        # bullish → bearish
        # =================================

        bearish_bias = (

            previous_week["close"] > previous_week["open"]
            and
            current_week["close"] < current_week["open"]

        )

        # =================================
        # SAVE WATCHLIST
        # =================================

        if bullish_bias:

            bullish_watchlist.append(pair)

            print(f"{pair} → BULLISH")

        elif bearish_bias:

            bearish_watchlist.append(pair)

            print(f"{pair} → BEARISH")

        else:

            print(f"{pair} → NEUTRAL")

    except Exception as e:

        print(f"Error scanning {pair}")

        print(e)

# =========================================
# SAVE FILES
# =========================================

with open("bullish_watchlist.txt", "w") as file:

    for pair in bullish_watchlist:

        file.write(pair + "\n")

with open("bearish_watchlist.txt", "w") as file:

    for pair in bearish_watchlist:

        file.write(pair + "\n")

# =========================================
# FINAL RESULTS
# =========================================

print("\n==============================")
print("WATCHLIST RESULTS")
print("==============================\n")

print("BULLISH PAIRS:\n")

for pair in bullish_watchlist:

    print(pair)

print("\n")

print("BEARISH PAIRS:\n")

for pair in bearish_watchlist:

    print(pair)

print("\nWatchlists saved successfully.")