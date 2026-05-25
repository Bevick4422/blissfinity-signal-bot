import requests
import pandas as pd
from telegram import Bot
import asyncio
from datetime import datetime

print("\n==============================")
print("DAILY BIAS ENGINE")
print("==============================\n")

# =========================================
# SUNDAY FILTER
# =========================================

today = datetime.now().weekday()

# Monday = 0
# Sunday = 6

if today == 6:

    print("Sunday detected.")

    print(
        "Skipping new bias generation today."
    )

    exit()

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN = "PASTE_YOUR_BOT_TOKEN_HERE"

CHAT_ID = "6953501418"

# =========================================
# TELEGRAM FUNCTION
# =========================================

async def send_telegram(message):

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

# =========================================
# PAIR LIST
# =========================================

pairs = [

    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XRP_USDT",
    "DOGE_USDT",
    "ADA_USDT",
    "AVAX_USDT",
    "LINK_USDT",
    "DOT_USDT",
    "MATIC_USDT",
    "UNI_USDT",
    "AAVE_USDT",
    "ATOM_USDT",
    "FIL_USDT",
    "ARB_USDT",
    "OP_USDT",
    "SUI_USDT",
    "APT_USDT",
    "INJ_USDT",
    "NEAR_USDT",
    "FTM_USDT",
    "SEI_USDT",
    "TIA_USDT",
    "RUNE_USDT",
    "PEPE_USDT",
    "SHIB_USDT",
    "TRX_USDT",
    "ETC_USDT",
    "LTC_USDT",
    "BCH_USDT",
    "ICP_USDT",
    "HBAR_USDT",
    "RNDR_USDT",
    "FET_USDT",
    "GRT_USDT",
    "THETA_USDT",
    "FLOW_USDT",
    "SAND_USDT",
    "MANA_USDT",
    "CHZ_USDT",
    "ZIL_USDT",
    "1INCH_USDT",
    "CRV_USDT",
    "DYDX_USDT",
    "GMX_USDT",
    "ENS_USDT",
    "BLUR_USDT",
    "PENDLE_USDT",
    "WLD_USDT",
    "JUP_USDT"
]

# =========================================
# STORAGE
# =========================================

bullish_pairs = []

bearish_pairs = []

# =========================================
# SCAN PAIRS
# =========================================

for pair in pairs:

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

        df = df.astype(float)

        if len(df) < 10:

            continue

        # =====================================
        # DAILY CANDLES
        # =====================================

        previous = df.iloc[-3]

        latest = df.iloc[-2]

        # =====================================
        # BULLISH DAILY REJECTION
        # =====================================

        bullish_rejection = (

            latest["low"]
            <
            previous["low"]

            and

            latest["close"]
            >
            latest["open"]

        )

        # =====================================
        # BEARISH DAILY REJECTION
        # =====================================

        bearish_rejection = (

            latest["high"]
            >
            previous["high"]

            and

            latest["close"]
            <
            latest["open"]

        )

        # =====================================
        # SAVE WATCHLISTS
        # =====================================

        if bullish_rejection:

            bullish_pairs.append(pair)

            print(
                "Bullish rejection detected."
            )

        elif bearish_rejection:

            bearish_pairs.append(pair)

            print(
                "Bearish rejection detected."
            )

        else:

            print("No rejection found.")

    except Exception as e:

        print(f"Error scanning {pair}")

        print(e)

# =========================================
# SAVE WATCHLIST FILES
# =========================================

with open(
    "confirmed_bullish.txt",
    "w"
) as file:

    for pair in bullish_pairs:

        file.write(pair + "\n")

with open(
    "confirmed_bearish.txt",
    "w"
) as file:

    for pair in bearish_pairs:

        file.write(pair + "\n")

# =========================================
# SUMMARY
# =========================================

message = f"""
📊 DAILY BIAS COMPLETE

Bullish Watchlist:
{len(bullish_pairs)}

Bearish Watchlist:
{len(bearish_pairs)}

Pairs Scanned:
{len(pairs)}

Strategy:
Daily Reject Daily
+
4H BOS
+
Institutional Entry Logic
"""

print(message)

# =========================================
# SEND TELEGRAM
# =========================================

try:

    asyncio.run(
        send_telegram(message)
    )

except Exception as e:

    print("Telegram Error")

    print(e)

print("\nEngine completed successfully.")