import requests
import pandas as pd
import sqlite3
import asyncio

from telegram import Bot
from datetime import datetime
from zoneinfo import ZoneInfo

print("\n==============================")
print("ENTRY CONFIRMATION ENGINE")
print("==============================\n")

# =========================================
# SESSION FILTER
# =========================================

current_hour = datetime.now(
    ZoneInfo("Africa/Lagos")
).hour

london_session = (
    8 <= current_hour <= 12
)

newyork_session = (
    14 <= current_hour <= 18
)

allowed_session = (
    london_session
    or
    newyork_session
)

if not allowed_session:

    print(
        "Outside institutional sessions."
    )

    print(
        "Engine stopped.\n"
    )

    exit()

print(
    "Institutional session active.\n"
)

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN = "8893369285:AAHvZEWi9F6g5QpiXfpSLFo8YgV0TiTevIU"

CHAT_ID = "6953501418"

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
# DATABASE
# =========================================

conn = sqlite3.connect(
    "blissfinity.db"
)

cursor = conn.cursor()

# =========================================
# DUPLICATE CHECK
# =========================================

def signal_already_sent(signal_id):

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

# =========================================
# LOAD MARKET WATCHLIST
# =========================================

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
    f"{len(market_pairs)} market pairs loaded.\n"
)

# =========================================
# SCAN FUNCTION
# =========================================

def scan_pair(pair, direction):

    try:

        print(
            f"Scanning {pair} ({direction})..."
        )

        # =====================================
        # 4H DATA
        # =====================================

        htf_url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Min240"
        )

        response = requests.get(
            htf_url
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
        # 1H DATA
        # =====================================

        ltf_url = (
            f"https://contract.mexc.com/api/v1/contract/kline/"
            f"{pair}?interval=Min60"
        )

        response = requests.get(
            ltf_url
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

        ltf_latest = ltf_df.iloc[-1]

        ltf_previous = ltf_df.iloc[-2]

        # =====================================
        # LONG SETUPS
        # =====================================

        if direction == "LONG":

            sweep = (
                latest["low"]
                <
                previous["low"]
            )

            bos = (
                latest["close"]
                >
                previous["high"]
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
                entry + (risk * 2),
                4
            )

            tp2 = round(
                entry + (risk * 3),
                4
            )

        # =====================================
        # SHORT SETUPS
        # =====================================

        else:

            sweep = (
                latest["high"]
                >
                previous["high"]
            )

            bos = (
                latest["close"]
                <
                previous["low"]
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
                entry - (risk * 2),
                4
            )

            tp2 = round(
                entry - (risk * 3),
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
        # FLEXIBLE CONFIRMATION
        # =====================================

        confirmation_count = 0

        if sweep:
            confirmation_count += 1

        if fvg:
            confirmation_count += 1

        if ob:
            confirmation_count += 1

        if ltf_confirmation:
            confirmation_count += 1

        if confirmation_count < 1:

            return

        # =====================================
        # SCORE SYSTEM
        # =====================================

        score = 0

        if sweep:
            score += 3

        if fvg:
            score += 3

        if ob:
            score += 3

        if bos:
            score += 2

        if ltf_confirmation:
            score += 4

        if score < 6:

            return

        # =====================================
        # DUPLICATE FILTER
        # =====================================

        signal_id = (
            f"{pair}_{direction}"
        )

        if signal_already_sent(signal_id):

            print(
                "Duplicate signal skipped."
            )

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
        # SESSION NAME
        # =====================================

        session_name = (

            "London"

            if london_session

            else

            "New York"

        )

        # =====================================
        # TELEGRAM MESSAGE
        # =====================================

        message = f'''
🚀 BLISSFINITY ELITE SIGNAL

Pair:
{pair}

Direction:
{direction}

Session:
{session_name}

Entry Zone:
{entry}

Stoploss:
{stoploss}

TP1:
{tp1}

TP2:
{tp2}

Risk To Reward:
1:{rr}

Score:
{score}

⚠️ Risk Management

Maximum Daily Exposure:
10% Of Portfolio

1 Trade = 10%
2 Trades = 5% Each
3 Trades = 3.3% Each
4 Trades = 2.5% Each

BLISSFINITY AI CONFIDENCE:
HIGH
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
# RUN FULL MARKET SCAN
# =========================================

print(
    "\nSCANNING FULL MARKET...\n"
)

for pair in market_pairs:

    # =====================================
    # LONG SCAN
    # =====================================

    scan_pair(
        pair,
        "LONG"
    )

    # =====================================
    # SHORT SCAN
    # =====================================

    scan_pair(
        pair,
        "SHORT"
    )

# =========================================
# CLOSE DATABASE
# =========================================

conn.close()

print(
    "\nEngine completed successfully.\n"
)