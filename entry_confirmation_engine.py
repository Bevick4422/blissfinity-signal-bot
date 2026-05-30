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

    raise ValueError(
        "TELEGRAM_TOKEN missing"
    )

```
raise ValueError(
    "TELEGRAM_TOKEN missing"
)
```

bot = Bot(
token=TOKEN.strip()
)

# =========================================

# SETTINGS

# =========================================

TIMEFRAME = "15m"

MAX_SIGNALS = 4

# =========================================

# MARKET TOKENS

# =========================================

TOKENS = [

```
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
```

]

# =========================================

# GET MARKET DATA

# =========================================

def get_data(symbol):

```
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
        f"{symbol} data error:"
    )

    print(e)

    return None
```

# =========================================

# LONG SETUP

# =========================================

def bullish_setup(df):

```
try:

    latest_close = df["close"].iloc[-1]

    previous_high = (

        df["high"]
        .iloc[-5:-1]
        .max()

    )

    latest_open = df["open"].iloc[-1]

    breakout = latest_close > previous_high

    bullish_candle = latest_close > latest_open

    return breakout and bullish_candle

except:

    return False
```

# =========================================

# SHORT SETUP

# =========================================

def bearish_setup(df):

```
try:

    latest_close = df["close"].iloc[-1]

    previous_low = (

        df["low"]
        .iloc[-5:-1]
        .min()

    )

    latest_open = df["open"].iloc[-1]

    breakdown = latest_close < previous_low

    bearish_candle = latest_close < latest_open

    return breakdown and bearish_candle

except:

    return False
```

# =========================================

# SEND SIGNAL

# =========================================

async def send_signal(

```
pair,
direction,
entry,
stoploss,
tp1,
tp2
```

):

```
try:

    message = f"""
```

🚨 BLISSFINITY SIGNAL

Pair: {pair}

Direction: {direction}

Entry: {entry}

Stoploss: {stoploss}

TP1: {tp1}

TP2: {tp2}

Risk Reminder:
Maximum daily risk = 10%

"""

```
    await bot.send_message(

        chat_id=CHAT_ID,
        text=message

    )

    print(
        f"{pair} {direction} signal sent."
    )

except Exception as e:

    print(
        f"{pair} telegram error:"
    )

    print(e)
```

# =========================================

# SCAN PAIR

# =========================================

async def scan_pair(pair):

```
try:

    df = get_data(pair)

    if df is None:

        print(
            f"{pair} rejected -> no data"
        )

        return False

    print(
        f"Scanning {pair}..."
    )

    # =====================================
    # LONG
    # =====================================

    if bullish_setup(df):

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
            tp2

        )

        return True

    # =====================================
    # SHORT
    # =====================================

    if bearish_setup(df):

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
            tp2

        )

        return True

    print(
        f"{pair} rejected -> no setup"
    )

except Exception as e:

    print(
        f"{pair} scan error:"
    )

    print(e)

return False
```

# =========================================

# MAIN ENGINE

# =========================================

async def main(print("LIGHTWEIGHT SIGNAL ENGINE STARTED")):

```
print("\n==============================")
print("LIGHTWEIGHT SIGNAL ENGINE")
print("==============================\n")

signals_sent = 0

for pair in TOKENS:print(f"Processing {pair}")

    if signals_sent >= MAX_SIGNALS:

        break

    result = await scan_pair(pair)

    if result:

        signals_sent += 1

    await asyncio.sleep(1)

print("\nScan cycle completed.\n")
```

# =========================================

# START

# =========================================

if **name** == "**main**":

```
asyncio.run(main())
```
