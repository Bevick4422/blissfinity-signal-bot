import requests
import pandas as pd
import ta
from telegram import Bot
import asyncio

# =========================================
# TELEGRAM SETTINGS
# =========================================

TOKEN = "8893369285:AAHi1aRkGG8AJ5M66C_cNVGAmTOn_gvtM9M"
CHAT_ID = "-5191516408"

# =========================================
# FETCH MARKET DATA
# =========================================

print("Fetching market data...")

url = "https://contract.mexc.com/api/v1/contract/kline/BTC_USDT?interval=Hour4"

response = requests.get(url)

json_data = response.json()

print("API Connected Successfully")

# =========================================
# EXTRACT DATA
# =========================================

candles = json_data["data"]

df = pd.DataFrame({
    "close": candles["close"],
    "high": candles["high"],
    "low": candles["low"]
})

# =========================================
# CLEAN DATA
# =========================================

df["close"] = df["close"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)

# =========================================
# INDICATORS
# =========================================

df["ema20"] = ta.trend.ema_indicator(
    df["close"],
    window=20
)

df["rsi"] = ta.momentum.rsi(
    df["close"],
    window=14
)

# =========================================
# LATEST MARKET DATA
# =========================================

latest = df.iloc[-1]

price = latest["close"]
ema = latest["ema20"]
rsi = latest["rsi"]

pair = "BTCUSDT"
timeframe = "4H"

# =========================================
# RECENT STRUCTURE LEVELS
# =========================================

recent_high = df["high"].iloc[-5]
recent_low = df["low"].iloc[-5]

# =========================================
# DEFAULT VALUES
# =========================================

signal = "NO SIGNAL"

entry_zone = "-"
stop_loss = "-"
tp1 = "-"
tp2 = "-"
rr = "-"

# =========================================
# LONG SETUP
# =========================================

if price > ema and rsi > 50:

    signal = "LONG"

    # ENTRY ZONE
    entry_zone = f"{round(price - 20, 2)} - {round(price + 20, 2)}"

    # STRUCTURE STOP LOSS
    stop_loss = round(recent_low - 15, 2)

    # RISK
    risk = price - stop_loss

    # TAKE PROFITS
    tp1 = round(price + (risk * 2), 2)
    tp2 = round(price + (risk * 3), 2)

    # RR
    rr = "1:3"

# =========================================
# SHORT SETUP
# =========================================

elif price < ema and rsi < 50:

    signal = "SHORT"

    # ENTRY ZONE
    entry_zone = f"{round(price - 20, 2)} - {round(price + 20, 2)}"

    # STRUCTURE STOP LOSS
    stop_loss = round(recent_high + 15, 2)

    # RISK
    risk = stop_loss - price

    # TAKE PROFITS
    tp1 = round(price - (risk * 2), 2)
    tp2 = round(price - (risk * 3), 2)

    # RR
    rr = "1:3"

# =========================================
# SIGNAL MESSAGE
# =========================================

message = f"""
🚀 BLISSFINITY SIGNAL BOT

Trading Pair:
{pair}

Direction:
{signal}

Timeframe:
{timeframe}

Entry Zone:
{entry_zone}

Stop Loss:
{stop_loss}

Take Profit Targets:
TP1: {tp1}
TP2: {tp2}

Risk-to-Reward:
{rr}

Market Data:
Price: {round(price, 2)}
EMA20: {round(ema, 2)}
RSI: {round(rsi, 2)}
"""

print(message)

# =========================================
# SEND TELEGRAM MESSAGE
# =========================================

async def send_signal():

    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text=message
    )

asyncio.run(send_signal())