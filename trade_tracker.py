import requests
import sqlite3
import asyncio
import time
import pandas as pd

from telegram import Bot

print("\n==============================")
print("TRADE TRACKER ENGINE")
print("==============================\n")

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN ="8893369285:AAHvZEWi9F6g5QpiXfpSLFo8YgV0TiTevIU"

CHAT_ID = "6953501418"

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
# LOAD ACTIVE TRADES
# =========================================

def load_active_trades():

    try:

        df = pd.read_sql(

            """

            SELECT *
            FROM active_trades
            WHERE status = 'ACTIVE'

            """,

            conn

        )

        return df

    except Exception as e:

        print(
            "Could not load trades."
        )

        print(e)

        return pd.DataFrame()

# =========================================
# UPDATE TRADE STATUS
# =========================================

def update_trade_status(

    trade_id,
    status

):

    try:

        cursor.execute(

            """

            UPDATE active_trades

            SET status = ?

            WHERE id = ?

            """,

            (

                status,
                trade_id

            )

        )

        conn.commit()

    except Exception as e:

        print(
            "Database Update Error:"
        )

        print(e)

# =========================================
# GET CURRENT PRICE
# =========================================

def get_current_price(pair):

    try:

        url = (

            f"https://contract.mexc.com/api/v1/contract/ticker/{pair}"

        )

        response = requests.get(

            url,

            timeout=10

        )

        data = response.json()

        if "data" not in data:

            return None

        price = float(

            data["data"]["lastPrice"]

        )

        return price

    except:

        return None

# =========================================
# TRACK SINGLE TRADE
# =========================================

def track_trade(row):

    try:

        trade_id = row["id"]

        pair = row["pair"]

        direction = row["direction"]

        entry = float(row["entry"])

        stoploss = float(row["stoploss"])

        tp1 = float(row["tp1"])

        tp2 = float(row["tp2"])

        score = row["score"]

        current_price = get_current_price(pair)

        if current_price is None:

            return

        print(
            f"Tracking {pair} | Current Price: {current_price}"
        )

        # =====================================
        # LONG TRADES
        # =====================================

        if direction == "LONG":

            # STOPLOSS HIT

            if current_price <= stoploss:

                update_trade_status(

                    trade_id,
                    "SL HIT"

                )

                message = f'''
❌ STOPLOSS HIT

Pair:
{pair}

Direction:
LONG

Entry:
{entry}

Stoploss:
{stoploss}

Current Price:
{current_price}

Score:
{score}
'''

                print(message)

                asyncio.run(
                    send_telegram(message)
                )

                return

            # TP2 HIT

            if current_price >= tp2:

                update_trade_status(

                    trade_id,
                    "TP HIT"

                )

                message = f'''
✅ TAKE PROFIT HIT

Pair:
{pair}

Direction:
LONG

Entry:
{entry}

TP2:
{tp2}

Current Price:
{current_price}

Score:
{score}
'''

                print(message)

                asyncio.run(
                    send_telegram(message)
                )

                return

        # =====================================
        # SHORT TRADES
        # =====================================

        else:

            # STOPLOSS HIT

            if current_price >= stoploss:

                update_trade_status(

                    trade_id,
                    "SL HIT"

                )

                message = f'''
❌ STOPLOSS HIT

Pair:
{pair}

Direction:
SHORT

Entry:
{entry}

Stoploss:
{stoploss}

Current Price:
{current_price}

Score:
{score}
'''

                print(message)

                asyncio.run(
                    send_telegram(message)
                )

                return

            # TP2 HIT

            if current_price <= tp2:

                update_trade_status(

                    trade_id,
                    "TP HIT"

                )

                message = f'''
✅ TAKE PROFIT HIT

Pair:
{pair}

Direction:
SHORT

Entry:
{entry}

TP2:
{tp2}

Current Price:
{current_price}

Score:
{score}
'''

                print(message)

                asyncio.run(
                    send_telegram(message)
                )

                return

    except Exception as e:

        print(
            f"Trade Tracking Error: {row['pair']}"
        )

        print(e)

# =========================================
# CONTINUOUS TRACKER
# =========================================

while True:

    try:

        print("\n==============================")
        print("TRACKING ACTIVE TRADES")
        print("==============================\n")

        active_df = load_active_trades()

        if len(active_df) == 0:

            print(
                "No active trades found."
            )

        else:

            print(
                f"{len(active_df)} active trades loaded.\n"
            )

            for _, row in active_df.iterrows():

                track_trade(row)

        print(
            "\nTracker cycle completed."
        )

        print(
            "\nSleeping for 5 minutes...\n"
        )

        time.sleep(300)

    except Exception as e:

        print(
            "\nTracker Engine Error:"
        )

        print(e)

        print(
            "\nRestarting in 1 minute...\n"
        )

        time.sleep(60)