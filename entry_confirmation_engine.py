import requests
import pandas as pd
import sqlite3
import asyncio
import time

from telegram import Bot
from datetime import datetime
from zoneinfo import ZoneInfo

print("\n==============================")
print("ENTRY CONFIRMATION ENGINE")
print("==============================\n")

# =========================================
# TELEGRAM SETTINGS
# =========================================

import os

TOKEN = os.getenv(
    "TELEGRAM_TOKEN"
)
import os
CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)

# =========================================
# DATABASE
# =========================================

conn = sqlite3.connect(
    "blissfinity.db"
)

cursor = conn.cursor()

# =========================================
# TELEGRAM FUNCTION
# =========================================

async def send_telegram(message):

    try:

        bot = Bot(
            token=TOKEN
        )

        await bot.send_message(

            chat_id=CHAT_ID,
            text=message

        )

    except Exception as e:

        print(
            "Telegram Error:"
        )

        print(e)

# =========================================
# CHECK DUPLICATE SIGNAL
# =========================================

def signal_exists(signal_id):

    try:

        cursor.execute(

            """

            SELECT signal_id
            FROM sent_signals
            WHERE signal_id = ?

            """,

            (signal_id,)

        )

        result = cursor.fetchone()

        return result is not None

    except:

        return False

# =========================================
# SAVE SIGNAL
# =========================================

def save_signal(signal_id):

    try:

        cursor.execute(

            """

            INSERT INTO sent_signals (
                signal_id
            )

            VALUES (?)

            """,

            (signal_id,)

        )

        conn.commit()

    except:

        pass

# =========================================
# SAVE TRADE
# =========================================

def save_trade(

    pair,
    direction,
    entry,
    stoploss,
    tp1,
    tp2,
    score

):

    try:

        cursor.execute(

            """

            INSERT INTO active_trades (

                pair,
                direction,
                entry,
                stoploss,
                tp1,
                tp2,
                score,
                status

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?)

            """,

            (

                pair,
                direction,
                entry,
                stoploss,
                tp1,
                tp2,
                score,
                "ACTIVE"

            )

        )

        conn.commit()

    except Exception as e:

        print(
            "Trade Save Error:"
        )

        print(e)

# =========================================
# SCAN SINGLE PAIR
# =========================================

def scan_pair(pair, direction):

    try:

        print(
            f"Scanning {pair} ({direction})..."
        )

        # =====================================
        # ACTIVE TRADE LIMIT
        # =====================================

        active_df = pd.read_sql(

            """

            SELECT *
            FROM active_trades
            WHERE status = 'ACTIVE'

            """,

            conn

        )

        active_count = len(active_df)

        if active_count >= 4:

            print(
                "Maximum active trades reached."
            )

            return

        # =====================================
        # FETCH 4H DATA
        # =====================================

        htf_url = (

            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Min240"

        )

        response = requests.get(

            htf_url,
            timeout=10

        )

        data = response.json()

        if "data" not in data:

            return

        candles = data["data"]

        htf_df = pd.DataFrame({

            "open": candles["open"],
            "close": candles["close"],
            "high": candles["high"],
            "low": candles["low"]

        }).astype(float)

        if len(htf_df) < 50:

            return

        latest = htf_df.iloc[-1]
        previous = htf_df.iloc[-2]
        third = htf_df.iloc[-3]

        # =====================================
        # FETCH 1H DATA
        # =====================================

        ltf_url = (

            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Min60"

        )

        response = requests.get(

            ltf_url,
            timeout=10

        )

        data = response.json()

        if "data" not in data:

            return

        candles = data["data"]

        ltf_df = pd.DataFrame({

            "open": candles["open"],
            "close": candles["close"],
            "high": candles["high"],
            "low": candles["low"]

        }).astype(float)

        if len(ltf_df) < 20:

            return

        # =====================================
        # ATR CALCULATION
        # =====================================

        ltf_df["previous_close"] = (
            ltf_df["close"].shift(1)
        )

        ltf_df["tr1"] = (
            ltf_df["high"]
            -
            ltf_df["low"]
        )

        ltf_df["tr2"] = abs(
            ltf_df["high"]
            -
            ltf_df["previous_close"]
        )

        ltf_df["tr3"] = abs(
            ltf_df["low"]
            -
            ltf_df["previous_close"]
        )

        ltf_df["true_range"] = ltf_df[[

            "tr1",
            "tr2",
            "tr3"

        ]].max(axis=1)

        ltf_df["atr"] = (

            ltf_df["true_range"]

            .rolling(14)

            .mean()

        )

        ltf_latest = ltf_df.iloc[-1]
        ltf_previous = ltf_df.iloc[-2]

        latest_atr = ltf_latest["atr"]

        if pd.isna(latest_atr):

            return

        # =====================================
        # LONG LOGIC
        # =====================================

        if direction == "LONG":

            bos = (
                latest["close"]
                >
                previous["high"]
            )

            sweep = (
                latest["low"]
                <
                previous["low"]
            )

            fvg = (
                third["high"]
                <
                latest["low"]
            )

            ob = (
                previous["close"]
                <
                previous["open"]
            )

            ltf_confirmation = (
                ltf_latest["close"]
                >
                ltf_previous["high"]
            )

            entry = round(
                ltf_latest["close"],
                4
            )

            stoploss = round(
                latest["low"],
                4
            )

            risk = (
                entry - stoploss
            )

            tp1 = round(
                entry + (risk * 1.5),
                4
            )

            tp2 = round(
                entry + (risk * 2.5),
                4
            )

        # =====================================
        # SHORT LOGIC
        # =====================================

        else:

            bos = (
                latest["close"]
                <
                previous["low"]
            )

            sweep = (
                latest["high"]
                >
                previous["high"]
            )

            fvg = (
                third["low"]
                >
                latest["high"]
            )

            ob = (
                previous["close"]
                >
                previous["open"]
            )

            ltf_confirmation = (
                ltf_latest["close"]
                <
                ltf_previous["low"]
            )

            entry = round(
                ltf_latest["close"],
                4
            )

            stoploss = round(
                latest["high"],
                4
            )

            risk = (
                stoploss - entry
            )

            tp1 = round(
                entry - (risk * 1.5),
                4
            )

            tp2 = round(
                entry - (risk * 2.5),
                4
            )

        # =====================================
        # VALIDATION
        # =====================================

        if risk <= 0:

            return

        if not bos:

            return

        # =====================================
        # VOLATILITY FILTER
        # =====================================

        current_range = abs(

            ltf_latest["high"]
            -
            ltf_latest["low"]

        )

        if current_range < latest_atr * 0.7:

            return

        # =====================================
        # SCORE SYSTEM
        # =====================================

        score = 0

        if bos:
            score += 3

        if sweep:
            score += 2

        if fvg:
            score += 2

        if ob:
            score += 1

        if ltf_confirmation:
            score += 2

        if score < 4:

            return

        # =====================================
        # DUPLICATE FILTER
        # =====================================

        signal_id = (
            f"{pair}_{direction}"
        )

        if signal_exists(signal_id):

            return

        # =====================================
        # SAVE SIGNAL
        # =====================================

        save_signal(signal_id)

        # =====================================
        # SAVE TRADE
        # =====================================

        save_trade(

            pair,
            direction,
            entry,
            stoploss,
            tp1,
            tp2,
            score

        )

        # =====================================
        # RR
        # =====================================

        rr = round(

            abs(tp2 - entry)
            /
            abs(entry - stoploss),

            2

        )

        # =====================================
        # SIGNAL MESSAGE
        # =====================================

        message = f'''
🚀 BLISSFINITY ELITE SIGNAL

Pair:
{pair}

Direction:
{direction}

Entry:
{entry}

Stoploss:
{stoploss}

TP1:
{tp1}

TP2:
{tp2}

Risk Reward:
1:{rr}

Signal Score:
{score}/10

⚠️ Risk Management

Maximum Daily Exposure:
10% Of Portfolio

1 Trade = 10%
2 Trades = 5% Each
3 Trades = 3.3% Each
4 Trades = 2.5% Each
'''

        print(message)

        asyncio.run(
            send_telegram(message)
        )

    except Exception as e:

        print(
            f"Error scanning {pair}"
        )

        print(e)

# =========================================
# CONTINUOUS SCANNER
# =========================================

while True:

    try:

        lagos_time = datetime.now(
            ZoneInfo("Africa/Lagos")
        )

        current_hour = lagos_time.hour

        london_session = (
            8 <= current_hour <= 12
        )

        newyork_session = (
            14 <= current_hour <= 18
        )

        if not london_session and not newyork_session:

            print(
                "\nOutside institutional sessions."
            )

            print(
                "Sleeping 30 minutes...\n"
            )

            time.sleep(1800)

            continue

        print("\n==============================")
        print("SCANNING FULL MARKET")
        print("==============================\n")

        # =====================================
        # LOAD WATCHLIST
        # =====================================

        try:

            with open(
                "market_watchlist.txt",
                "r"
            ) as file:

                market_pairs = [

                    line.strip()

                    for line in file.readlines()

                    if line.strip()

                ]

        except:

            market_pairs = []

        print(
            f"{len(market_pairs)} pairs loaded.\n"
        )

        # =====================================
        # SCAN MARKET
        # =====================================

        for pair in market_pairs:

            scan_pair(
                pair,
                "LONG"
            )

            scan_pair(
                pair,
                "SHORT"
            )

        print(
            "\nScan cycle completed."
        )

        print(
            "\nSleeping for 5 minutes...\n"
        )

        time.sleep(300)

    except Exception as e:

        print(
            "\nContinuous Scanner Error:"
        )

        print(e)

        print(
            "\nRestarting in 1 minute...\n"
        )

        time.sleep(60)