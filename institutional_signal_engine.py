import requests
import pandas as pd
from telegram import Bot
import asyncio
from datetime import datetime
import pytz

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN = "8893369285:AAHi1aRkGG8AJ5M66C_cNVGAmTOn_gvtM9M"

CHAT_ID = "6953501418"

# =========================================
# TELEGRAM FUNCTION
# =========================================

async def send_signal(message):

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

# =========================================
# NIGERIA TIME
# =========================================

nigeria = pytz.timezone("Africa/Lagos")

now = datetime.now(nigeria)

print("\n==============================")
print("INSTITUTIONAL SIGNAL ENGINE")
print("==============================\n")

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
    "LINK_USDT",
    "AVAX_USDT",
    "DOGE_USDT",
    "ADA_USDT"
]

# =========================================
# MAIN LOOP
# =========================================

for pair in pairs:

    try:

        print(f"\nScanning {pair}...\n")

        # =================================
        # WEEKLY DATA
        # =================================

        weekly_url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Week1"
        )

        weekly_response = requests.get(weekly_url)

        weekly_json = weekly_response.json()

        if "data" not in weekly_json:

            print("Weekly API Error")

            continue

        weekly_candles = weekly_json["data"]

        weekly_df = pd.DataFrame({

            "open": weekly_candles["open"],
            "close": weekly_candles["close"],
            "high": weekly_candles["high"],
            "low": weekly_candles["low"]

        })

        weekly_df["open"] = weekly_df["open"].astype(float)
        weekly_df["close"] = weekly_df["close"].astype(float)
        weekly_df["high"] = weekly_df["high"].astype(float)
        weekly_df["low"] = weekly_df["low"].astype(float)

        # =================================
        # DAILY DATA
        # =================================

        daily_url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Day1"
        )

        daily_response = requests.get(daily_url)

        daily_json = daily_response.json()

        if "data" not in daily_json:

            print("Daily API Error")

            continue

        daily_candles = daily_json["data"]

        daily_df = pd.DataFrame({

            "open": daily_candles["open"],
            "close": daily_candles["close"],
            "high": daily_candles["high"],
            "low": daily_candles["low"]

        })

        daily_df["open"] = daily_df["open"].astype(float)
        daily_df["close"] = daily_df["close"].astype(float)
        daily_df["high"] = daily_df["high"].astype(float)
        daily_df["low"] = daily_df["low"].astype(float)

        # =================================
        # WEEKLY BIAS
        # =================================

        previous_week = weekly_df.iloc[-2]

        current_week = weekly_df.iloc[-1]

        bullish_weekly_bias = (

            previous_week["close"] < previous_week["open"]
            and
            current_week["close"] > current_week["open"]

        )

        bearish_weekly_bias = (

            previous_week["close"] > previous_week["open"]
            and
            current_week["close"] < current_week["open"]

        )

        # =================================
        # DAILY BOS
        # =================================

        recent_high = (

            daily_df["high"]
            .iloc[-10:-1]
            .max()

        )

        recent_low = (

            daily_df["low"]
            .iloc[-10:-1]
            .min()

        )

        latest_daily = daily_df.iloc[-1]

        bullish_bos = (

            latest_daily["close"] > recent_high

        )

        bearish_bos = (

            latest_daily["close"] < recent_low

        )

        # =================================
        # FRESH LEVEL DETECTION
        # =================================

        fresh_v_level = None

        fresh_a_level = None

        for i in range(1, len(daily_df) - 10):

            previous = daily_df.iloc[i - 1]

            current = daily_df.iloc[i]

            future_data = daily_df.iloc[i + 1:i + 10]

            # =============================
            # V SHAPE
            # =============================

            if (

                previous["close"] < previous["open"]
                and
                current["close"] > current["open"]

            ):

                level = previous["low"]

                mitigated = False

                for j in range(len(future_data)):

                    if future_data.iloc[j]["low"] <= level:

                        mitigated = True

                        break

                if not mitigated:

                    fresh_v_level = level

            # =============================
            # A SHAPE
            # =============================

            elif (

                previous["close"] > previous["open"]
                and
                current["close"] < current["open"]

            ):

                level = previous["high"]

                mitigated = False

                for j in range(len(future_data)):

                    if future_data.iloc[j]["high"] >= level:

                        mitigated = True

                        break

                if not mitigated:

                    fresh_a_level = level

        # =================================
        # LONG SIGNAL
        # =================================

        if (

            bullish_weekly_bias
            and
            bullish_bos
            and
            fresh_v_level is not None

        ):

            entry = round(fresh_v_level, 2)

            stop_loss = round(
                entry * 0.995,
                2
            )

            risk = entry - stop_loss

            tp1 = round(
                entry + (risk * 2),
                2
            )

            tp2 = round(
                entry + (risk * 3),
                2
            )

            message = f"""
🚀 BLISSFINITY INSTITUTIONAL SIGNAL

Pair:
{pair}

Bias:
BULLISH

Weekly Confirmation:
Weekly V-Shape Rejection

Daily Confirmation:
Bullish BOS Confirmed

Entry Level:
{entry}

Stop Loss:
{stop_loss}

Take Profit:
TP1: {tp1}
TP2: {tp2}

Risk Reward:
1:3

Level Type:
Fresh V-Shape Support
"""

            print(message)

            asyncio.run(
                send_signal(message)
            )

        # =================================
        # SHORT SIGNAL
        # =================================

        elif (

            bearish_weekly_bias
            and
            bearish_bos
            and
            fresh_a_level is not None

        ):

            entry = round(fresh_a_level, 2)

            stop_loss = round(
                entry * 1.005,
                2
            )

            risk = stop_loss - entry

            tp1 = round(
                entry - (risk * 2),
                2
            )

            tp2 = round(
                entry - (risk * 3),
                2
            )

            message = f"""
🚀 BLISSFINITY INSTITUTIONAL SIGNAL

Pair:
{pair}

Bias:
BEARISH

Weekly Confirmation:
Weekly A-Shape Rejection

Daily Confirmation:
Bearish BOS Confirmed

Entry Level:
{entry}

Stop Loss:
{stop_loss}

Take Profit:
TP1: {tp1}
TP2: {tp2}

Risk Reward:
1:3

Level Type:
Fresh A-Shape Resistance
"""

            print(message)

            asyncio.run(
                send_signal(message)
            )

        else:

            print("No institutional setup found.")

    except Exception as e:

        print(f"Error scanning {pair}")

        print(e)

print("\nEngine completed successfully.")