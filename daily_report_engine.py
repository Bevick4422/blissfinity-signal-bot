import sqlite3
import pandas as pd
import asyncio

from telegram import Bot
from datetime import datetime
from zoneinfo import ZoneInfo

print("\n==============================")
print("DAILY REPORT ENGINE")
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

# =========================================
# LOAD TRADES
# =========================================

try:

    df = pd.read_sql(

        """

        SELECT *
        FROM active_trades

        """,

        conn

    )

except Exception as e:

    print(
        "Could not load trades."
    )

    print(e)

    exit()

# =========================================
# EMPTY CHECK
# =========================================

if len(df) == 0:

    print(
        "No trades available."
    )

    exit()

# =========================================
# TOTALS
# =========================================

total_trades = len(df)

wins = len(

    df[
        df["status"] == "TP HIT"
    ]

)

losses = len(

    df[
        df["status"] == "SL HIT"
    ]

)

active = len(

    df[
        df["status"] == "ACTIVE"
    ]

)

completed = wins + losses

# =========================================
# WINRATE
# =========================================

if completed > 0:

    winrate = round(

        (wins / completed) * 100,

        2

    )

else:

    winrate = 0

# =========================================
# BEST SIGNAL
# =========================================

try:

    best_trade = df.sort_values(

        by="score",

        ascending=False

    ).iloc[0]

    best_pair = best_trade["pair"]

    best_score = best_trade["score"]

except:

    best_pair = "N/A"

    best_score = 0

# =========================================
# DATE
# =========================================

lagos_time = datetime.now(
    ZoneInfo("Africa/Lagos")
)

today = lagos_time.strftime(
    "%d %B %Y"
)

# =========================================
# REPORT MESSAGE
# =========================================

message = f'''
📊 BLISSFINITY DAILY REPORT

Date:
{today}

Total Signals:
{total_trades}

Wins:
{wins}

Losses:
{losses}

Active Trades:
{active}

Winrate:
{winrate}%

Highest Score Signal:
{best_pair}

Signal Score:
{best_score}/10

⚡ SYSTEM STATUS:
ACTIVE
'''

print(message)

# =========================================
# SEND REPORT
# =========================================

asyncio.run(
    send_telegram(message)
)

# =========================================
# CLOSE DATABASE
# =========================================

conn.close()

print(
    "\nDaily report sent.\n"
)