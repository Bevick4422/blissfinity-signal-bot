import requests
import pandas as pd
import ta
from telegram import Bot
import asyncio
import time

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN ="8893369285:AAHvZEWi9F6g5QpiXfpSLFo8YgV0TiTevIU"
CHAT_ID = "6953501418"

# =========================================
# 50 FUTURES PAIRS
# =========================================

pairs = [

    "BTC_USDT",
    "ETH_USDT",
    "SOL_USDT",
    "XRP_USDT",
    "DOGE_USDT",
    "ADA_USDT",
    "BNB_USDT",
    "LINK_USDT",
    "AVAX_USDT",
    "SUI_USDT",

    "LTC_USDT",
    "TRX_USDT",
    "DOT_USDT",
    "ATOM_USDT",
    "APT_USDT",
    "ARB_USDT",
    "OP_USDT",
    "NEAR_USDT",
    "INJ_USDT",
    "FIL_USDT",

    "PEPE_USDT",
    "WIF_USDT",
    "BONK_USDT",
    "SHIB_USDT",
    "FLOKI_USDT",
    "SEI_USDT",
    "TIA_USDT",
    "JUP_USDT",
    "RUNE_USDT",
    "ETC_USDT",

    "MATIC_USDT",
    "AAVE_USDT",
    "UNI_USDT",
    "SAND_USDT",
    "GALA_USDT",
    "ICP_USDT",
    "DYDX_USDT",
    "CRV_USDT",
    "LDO_USDT",
    "EOS_USDT",

    "ALGO_USDT",
    "XTZ_USDT",
    "EGLD_USDT",
    "KAS_USDT",
    "STX_USDT",
    "THETA_USDT",
    "FLOW_USDT",
    "CHZ_USDT",
    "ZIL_USDT",
    "1INCH_USDT"
]

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
# DUPLICATE SIGNAL MEMORY
# =========================================

last_signals = {}

# =========================================
# MAIN LOOP
# =========================================

while True:

    print("\n==============================")
    print("STARTING NEW MARKET SCAN...")
    print("==============================\n")

    for pair in pairs:

        try:

            print(f"Scanning {pair}...")

            # =================================
            # FETCH MARKET DATA
            # =================================

            url = f"https://contract.mexc.com/api/v1/contract/kline/{pair}?interval=Hour4"

            response = requests.get(url)

            json_data = response.json()

            # CHECK API RESPONSE
            if "data" not in json_data:

                print(f"Skipping {pair} - API Error")

                continue

            candles = json_data["data"]

            # =================================
            # CREATE DATAFRAME
            # =================================

            df = pd.DataFrame({
                "close": candles["close"],
                "high": candles["high"],
                "low": candles["low"]
            })

            # =================================
            # CLEAN DATA
            # =================================

            df["close"] = df["close"].astype(float)
            df["high"] = df["high"].astype(float)
            df["low"] = df["low"].astype(float)

            # =================================
            # INDICATORS
            # =================================

            df["ema20"] = ta.trend.ema_indicator(
                df["close"],
                window=20
            )

            df["rsi"] = ta.momentum.rsi(
                df["close"],
                window=14
            )

            # =================================
            # LATEST MARKET DATA
            # =================================

            latest = df.iloc[-1]

            price = latest["close"]
            ema = latest["ema20"]
            rsi = latest["rsi"]

            # =================================
            # SUPPORT & RESISTANCE
            # =================================

            support = df["low"].tail(20).min()

            resistance = df["high"].tail(20).max()

            signal = None

            # =================================
            # LONG SETUP
            # =================================

            if price > ema and rsi > 60:

                signal = "LONG"

                entry_zone = f"{round(price - 20,2)} - {round(price + 20,2)}"

                stop_loss = round(
                    support - (price * 0.002),
                    2
                )

                risk = price - stop_loss

                tp1 = round(
                    price + (risk * 2),
                    2
                )

                tp2 = round(
                    price + (risk * 3),
                    2
                )

            # =================================
            # SHORT SETUP
            # =================================

            elif price < ema and rsi < 40:

                signal = "SHORT"

                entry_zone = f"{round(price - 20,2)} - {round(price + 20,2)}"

                stop_loss = round(
                    resistance + (price * 0.002),
                    2
                )

                risk = stop_loss - price

                tp1 = round(
                    price - (risk * 2),
                    2
                )

                tp2 = round(
                    price - (risk * 3),
                    2
                )

            # =================================
            # QUALITY FILTERS
            # =================================

            if signal and risk > 0:

                # REMOVE LOW-PRICE COINS
                if price < 1:

                    print(f"Skipping {pair} - price too low")

                    continue

                # AVOID HUGE STOPLOSSES
                if risk > (price * 0.03):

                    print(f"Skipping {pair} - stoploss too large")

                    continue

                # PREVENT DUPLICATE SIGNALS
                previous_signal = last_signals.get(pair)

                if previous_signal == signal:

                    print(f"Duplicate signal skipped for {pair}")

                    continue

                # SAVE SIGNAL MEMORY
                last_signals[pair] = signal

                # =================================
                # SIGNAL MESSAGE
                # =================================

                message = f"""
🚀 BLISSFINITY SIGNAL BOT

Trading Pair:
{pair}

Direction:
{signal}

Timeframe:
4H

Entry Zone:
{entry_zone}

Stop Loss:
{stop_loss}

Take Profit Targets:
TP1: {tp1}
TP2: {tp2}

Risk-to-Reward:
1:3

Market Data:
Price: {round(price,2)}
EMA20: {round(ema,2)}
RSI: {round(rsi,2)}

Support:
{round(support,2)}

Resistance:
{round(resistance,2)}
"""

                print(message)

                asyncio.run(
                    send_signal(message)
                )

            else:

                print(f"No signal for {pair}")

        except Exception as e:

            print(f"Error scanning {pair}")

            print(e)

    # =====================================
    # WAIT BEFORE NEXT SCAN
    # =====================================

    print("\nWaiting 30 minutes before next scan...\n")

    # 1800 seconds = 30 minutes
    time.sleep(1800)