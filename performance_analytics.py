import sqlite3
import pandas as pd

print("\n==============================")
print("PERFORMANCE ANALYTICS ENGINE")
print("==============================\n")

# =========================================
# CONNECT DATABASE
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
# TOTAL TRADES
# =========================================

total_trades = len(df)

# =========================================
# WINS
# =========================================

wins = len(

    df[
        df["status"] == "TP HIT"
    ]

)

# =========================================
# LOSSES
# =========================================

losses = len(

    df[
        df["status"] == "SL HIT"
    ]

)

# =========================================
# ACTIVE
# =========================================

active = len(

    df[
        df["status"] == "ACTIVE"
    ]

)

# =========================================
# WINRATE
# =========================================

completed = wins + losses

if completed > 0:

    winrate = round(

        (wins / completed) * 100,

        2

    )

else:

    winrate = 0

# =========================================
# RR CALCULATION
# =========================================

rr_results = []

for _, row in df.iterrows():

    try:

        entry = float(row["entry"])

        stoploss = float(row["stoploss"])

        tp2 = float(row["tp2"])

        risk = abs(
            entry - stoploss
        )

        reward = abs(
            tp2 - entry
        )

        if risk > 0:

            rr = reward / risk

            rr_results.append(rr)

    except:

        pass

if len(rr_results) > 0:

    average_rr = round(

        sum(rr_results)
        /
        len(rr_results),

        2

    )

else:

    average_rr = 0

# =========================================
# LONG VS SHORT
# =========================================

long_trades = len(

    df[
        df["direction"] == "LONG"
    ]

)

short_trades = len(

    df[
        df["direction"] == "SHORT"
    ]

)

# =========================================
# HIGH SCORE TRADES
# =========================================

high_score = len(

    df[
        df["score"] >= 10
    ]

)

# =========================================
# PRINT RESULTS
# =========================================

print("TOTAL TRADES:")
print(total_trades)

print("\nWINS:")
print(wins)

print("\nLOSSES:")
print(losses)

print("\nACTIVE:")
print(active)

print("\nWINRATE:")
print(f"{winrate}%")

print("\nAVERAGE RR:")
print(f"1:{average_rr}")

print("\nLONG TRADES:")
print(long_trades)

print("\nSHORT TRADES:")
print(short_trades)

print("\nHIGH SCORE TRADES:")
print(high_score)

# =========================================
# BEST SETUPS
# =========================================

print("\n==============================")
print("TOP SIGNALS")
print("==============================\n")

top_df = df.sort_values(

    by="score",

    ascending=False

).head(10)

print(

    top_df[[

        "pair",
        "direction",
        "score",
        "status"

    ]]

)

# =========================================
# CLOSE DATABASE
# =========================================

conn.close()

print(
    "\nAnalytics completed.\n"
)