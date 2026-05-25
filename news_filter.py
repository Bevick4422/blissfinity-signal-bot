import requests
import pandas as pd

print("\n==============================")
print("NEWS VOLATILITY FILTER")
print("==============================\n")

# =========================================
# SETTINGS
# =========================================

VOLATILITY_MULTIPLIER = 2.5

# =========================================
# PAIRS TO CHECK
# =========================================

pairs = [

    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT"

]

# =========================================
# FUNCTION
# =========================================

def market_is_volatile(pair):

    try:

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Min60"
        )

        response = requests.get(url)

        json_data = response.json()

        if "data" not in json_data:

            return False

        candles = json_data["data"]

        df = pd.DataFrame({

            "high": candles["high"],
            "low": candles["low"]

        })

        df = df.astype(float)

        if len(df) < 30:

            return False

        # =====================================
        # CANDLE RANGES
        # =====================================

        df["range"] = (

            df["high"]
            -
            df["low"]

        )

        average_range = (

            df["range"]
            .iloc[-25:-1]
            .mean()

        )

        current_range = (

            df["range"]
            .iloc[-1]

        )

        # =====================================
        # VOLATILITY DETECTION
        # =====================================

        if current_range > (

            average_range
            *
            VOLATILITY_MULTIPLIER

        ):

            print(
                f"{pair} volatility spike detected."
            )

            return True

        return False

    except Exception as e:

        print(f"Error checking {pair}")

        print(e)

        return False

# =========================================
# GLOBAL CHECK
# =========================================

volatile_market = False

for pair in pairs:

    result = market_is_volatile(pair)

    if result:

        volatile_market = True

# =========================================
# OUTPUT
# =========================================

if volatile_market:

    print("\n⚠️ MARKET CONDITIONS UNSTABLE")

    print("Signal generation paused.\n")

else:

    print("\n✅ Market conditions stable")

    print("Signal generation allowed.\n")