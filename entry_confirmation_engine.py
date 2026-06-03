import os
import asyncio
import requests
import pandas as pd
from telegram import Bot

print("ENTRY ENGINE FILE LOADED")

# =========================================
# TELEGRAM
# =========================================

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"TOKEN FOUND: {bool(TOKEN)}")
print(f"CHAT_ID FOUND: {bool(CHAT_ID)}")

if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN missing")

if not CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID missing")

bot = Bot(token=TOKEN.strip())

# =========================================
# SETTINGS
# =========================================

TIMEFRAME = "Min60"
MAX_SIGNALS = 4

# =========================================
# TOKENS
# =========================================

TOKENS = [
    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "DOGE_USDT",
    "XRP_USDT",
    "LINK_USDT",
    "AVAX_USDT",
    "WLD_USDT",
    "PENDLE_USDT",
    "NEAR_USDT",
    "MORPHO_USDT",
    "RON_USDT",
    "PIPPIN_USDT"
]

# =========================================
# GET DATA
# =========================================

def get_data(symbol):

    try:

        url = (
            f"https://contract.mexc.com/api/v1/contract/kline/{symbol}"
            f"?interval={TIMEFRAME}"
        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        candles = data.get("data")

        if not candles:
            return None

        df = pd.DataFrame({
            "open": candles["open"],
            "high": candles["high"],
            "low": candles["low"],
            "close": candles["close"]
        })

        return df.astype(float)

    except Exception as e:

        print(f"{symbol} data error:")
        print(e)

        return None

# =========================================
# LONG SETUP
# =========================================

def bullish_setup(df):

    try:

        latest_close = df["close"].iloc[-1]
        latest_open = df["open"].iloc[-1]

        previous_high = (
            df["high"]
            .iloc[-6:-1]
            .max()
        )

        return (
            latest_close > previous_high
            and latest_close > latest_open
        )

    except:
        return False

# =========================================
# SHORT SETUP
# =========================================

def bearish_setup(df):

    try:

        latest_close = df["close"].iloc[-1]
        latest_open = df["open"].iloc[-1]

        previous_low = (
            df["low"]
            .iloc[-6:-1]
            .min()
        )

        return (
            latest_close < previous_low
            and latest_close < latest_open
        )

    except:
        return False

# =========================================
# TELEGRAM SIGNAL
# =========================================

async def send_signal(
    pair,
    direction,
    entry,
    stoploss,
    tp1,
    tp2
):

    try:

        message = f"""
🚨 BLISSFINITY SIGNAL

Pair: {pair}

Direction: {direction}

Entry: {entry}

Stop Loss: {stoploss}

TP1: {tp1}

TP2: {tp2}

Risk Reminder:
Maximum daily risk = 10%
"""

        await bot.send_message(
            chat_id=CHAT_ID,
            text=message
        )

        print(f"{pair} {direction} signal sent.")

    except Exception as e:

        print(f"{pair} telegram error:")
        print(e)

# =========================================
# SCAN PAIR
# =========================================

async def scan_pair(pair):

    try:

        df = get_data(pair)

        if df is None:

            print(f"{pair} -> no data")

            return False

        print(f"Scanning {pair}...")

        latest_close = df["close"].iloc[-1]

        if bullish_setup(df):

            entry = round(latest_close, 4)
            stoploss = round(entry * 0.985, 4)
            tp1 = round(entry * 1.02, 4)
            tp2 = round(entry * 1.04, 4)

            await send_signal(
                pair,
                "LONG",
                entry,
                stoploss,
                tp1,
                tp2
            )

            return True

        elif bearish_setup(df):

            entry = round(latest_close, 4)
            stoploss = round(entry * 1.015, 4)
            tp1 = round(entry * 0.98, 4)
            tp2 = round(entry * 0.96, 4)

            await send_signal(
                pair,
                "SHORT",
                entry,
                stoploss,
                tp1,
                tp2
            )

            return True

        print(f"{pair} -> no setup")

        return False

    except Exception as e:

        print(f"{pair} scan error:")
        print(e)

        return False

# =========================================
# MAIN
# =========================================

async def main():

    print("\n==============================")
    print("LIGHTWEIGHT SIGNAL ENGINE")
    print("==============================\n")

    signals_sent = 0

    for pair in TOKENS:

        print(f"Processing {pair}")

        if signals_sent >= MAX_SIGNALS:
            break

        result = await scan_pair(pair)

        if result:
            signals_sent += 1

        await asyncio.sleep(1)

    print("\nScan cycle completed.\n")

# =========================================
# START
# =========================================

if __name__ == "__main__":
    asyncio.run(main())