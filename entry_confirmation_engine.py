import os
import time
import asyncio
import requests
import pandas as pd

from telegram import Bot

# =========================================
# TELEGRAM VARIABLES
# =========================================

TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

if not TOKEN:

    raise ValueError(
        "TELEGRAM_TOKEN environment variable missing"
    )

bot = Bot(
    token=TOKEN.strip()
)

# =========================================
# SETTINGS
# =========================================

TIMEFRAME = "15m"

SIGNAL_SCORE_THRESHOLD = 2

MAX_SIGNALS_PER_CYCLE = 4

# =========================================
# MARKET TOKENS
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
# GET MARKET DATA
# =========================================

def get_candles(symbol):

    try:

        url = (

            "https://contract.mexc.com"

            f"/api/v1/contract/kline/{symbol}"

            f"?interval={TIMEFRAME}"

        )

        response = requests.get(
            url,
            timeout=10
        )

        data = response.json()

        candles = data.get(
            "data",
            {}
        )

        if not candles:

            return None

        df = pd.DataFrame({

            "open": candles["open"],
            "high": candles["high"],
            "low": candles["low"],
            "close": candles["close"]

        })

        df = df.astype(float)

        return df

    except Exception as e:

        print(
            f"{symbol} candle error:"
        )

        print(e)

        return None

# =========================================
# SIMPLE BOS DETECTION
# =========================================

def bullish_bos(df):

    try:

        latest_close = df["close"].iloc[-1]

        previous_high = (

            df["high"]
            .iloc[-6:-1]
            .max()

        )

        return latest_close > previous_high

    except:

        return False

# =========================================
# SIMPLE BEARISH BOS
# =========================================

def bearish_bos(df):

    try:

        latest_close = df["close"].iloc[-1]

        previous_low = (

            df["low"]
            .iloc[-6:-1]
            .min()

        )

        return latest_close < previous_low

    except:

        return False

# =========================================
# ATR VOLATILITY
# =========================================

def volatility_ok(df):

    try:

        current_range = (

            df["high"].iloc[-1]
            -
            df["low"].iloc[-1]

        )

        average_range = (

            (
                df["high"]
                -
                df["low"]
            )

            .rolling(10)
            .mean()

            .iloc[-1]

        )

        return current_range >= average_range * 0.5

    except:

        return False

# =========================================
# BUILD SIGNAL SCORE
# =========================================

def calculate_score(df, direction):

    score = 0

    try:

        if volatility_ok(df):

            score += 1

        latest_close = df["close"].iloc[-1]

        latest_open = df["open"].iloc[-1]

        if direction == "LONG":

            if latest_close > latest_open:

                score += 1

        if direction == "SHORT":

            if latest_close < latest_open:

                score += 1

        recent_trend = (

            df["close"].iloc[-1]
            -
            df["close"].iloc[-5]

        )

        if direction == "LONG":

            if recent_trend > 0:

                score += 1

        if direction == "SHORT":

            if recent_trend < 0:

                score += 1

    except:

        pass

    return score

# =========================================
# SEND TELEGRAM SIGNAL
# =========================================

async def send_signal(

    pair,
    direction,
    entry,
    stoploss,
    tp1,
    tp2,
    score

):

    try:

        message = f"""

🚨 BLISSFINITY SIGNAL

Pair: {pair}

Direction: {direction}

Entry: {entry}

Stoploss: {stoploss}

TP1: {tp1}

TP2: {tp2}

Confidence Score: {score}/3

Risk Reminder:
Do not risk more than 10% daily.

"""

        await bot.send_message(

            chat_id=CHAT_ID,
            text=message

        )

        print(
            f"{pair} signal sent."
        )

    except Exception as e:

        print(
            "Telegram send error:"
        )

        print(e)

# =========================================
# SCAN PAIR
# =========================================

async def scan_pair(pair):

    try:

        df = get_candles(pair)

        if df is None:

            print(
                f"{pair} rejected -> No data"
            )

            return False

        # =====================================
        # LONG SETUP
        # =====================================

        print(
            f"Scanning {pair} (LONG)..."
        )

        if bullish_bos(df):

            if volatility_ok(df):

                score = calculate_score(
                    df,
                    "LONG"
                )

                if score >= SIGNAL_SCORE_THRESHOLD:

                    entry = round(
                        df["close"].iloc[-1],
                        4
                    )

                    stoploss = round(
                        entry * 0.985,
                        4
                    )

                    tp1 = round(
                        entry * 1.02,
                        4
                    )

                    tp2 = round(
                        entry * 1.04,
                        4
                    )

                    await send_signal(

                        pair,
                        "LONG",
                        entry,
                        stoploss,
                        tp1,
                        tp2,
                        score

                    )

                    return True

                else:

                    print(
                        f"{pair} rejected -> Low score LONG"
                    )

            else:

                print(
                    f"{pair} rejected -> Low volatility LONG"
                )

        else:

            print(
                f"{pair} rejected -> No bullish BOS"
            )

        # =====================================
        # SHORT SETUP
        # =====================================

        print(
            f"Scanning {pair} (SHORT)..."
        )

        if bearish_bos(df):

            if volatility_ok(df):

                score = calculate_score(
                    df,
                    "SHORT"
                )

                if score >= SIGNAL_SCORE_THRESHOLD:

                    entry = round(
                        df["close"].iloc[-1],
                        4
                    )

                    stoploss = round(
                        entry * 1.015,
                        4
                    )

                    tp1 = round(
                        entry * 0.98,
                        4
                    )

                    tp2 = round(
                        entry * 0.96,
                        4
                    )

                    await send_signal(

                        pair,
                        "SHORT",
                        entry,
                        stoploss,
                        tp1,
                        tp2,
                        score

                    )

                    return True

                else:

                    print(
                        f"{pair} rejected -> Low score SHORT"
                    )

            else:

                print(
                    f"{pair} rejected -> Low volatility SHORT"
                )

        else:

            print(
                f"{pair} rejected -> No bearish BOS"
            )

    except Exception as e:

        print(
            f"{pair} scan error:"
        )

        print(e)

    return False

# =========================================
# MAIN ENGINE
# =========================================

async def main():

    print("\n==============================")
    print("ENTRY CONFIRMATION ENGINE")
    print("==============================\n")

    signals_sent = 0

    for pair in TOKENS:

        if signals_sent >= MAX_SIGNALS_PER_CYCLE:

            break

        result = await scan_pair(pair)

        if result:

            signals_sent += 1

        await asyncio.sleep(2)

    print("\nScan cycle completed.\n")

# =========================================
# START ENGINE
# =========================================

if __name__ == "__main__":

    asyncio.run(main())