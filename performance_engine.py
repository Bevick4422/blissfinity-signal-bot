import pandas as pd

print("\n==============================")
print("PERFORMANCE ANALYTICS ENGINE")
print("==============================\n")

# =========================================
# LOAD TRADE DATABASE
# =========================================

try:

    trades = pd.read_csv(
        "active_trades.csv"
    )

except Exception as e:

    print("Could not load trade database.")

    print(e)

    exit()

# =========================================
# CHECK EMPTY DATABASE
# =========================================

if trades.empty:

    print("No trades recorded yet.")

    exit()

# =========================================
# TOTAL TRADES
# =========================================

total_trades = len(trades)

# =========================================
# CLOSED TRADES
# =========================================

closed_trades = trades[

    trades["status"].isin(
        ["TP1", "TP2", "STOPLOSS"]
    )

]

# =========================================
# COUNTS
# =========================================

tp1_count = len(

    closed_trades[
        closed_trades["status"] == "TP1"
    ]

)

tp2_count = len(

    closed_trades[
        closed_trades["status"] == "TP2"
    ]

)

sl_count = len(

    closed_trades[
        closed_trades["status"] == "STOPLOSS"
    ]

)

# =========================================
# WINRATE
# =========================================

winning_trades = tp1_count + tp2_count

completed_trades = (

    tp1_count
    + tp2_count
    + sl_count

)

if completed_trades > 0:

    winrate = round(

        (
            winning_trades
            / completed_trades
        ) * 100,
        2

    )

else:

    winrate = 0

# =========================================
# LONG VS SHORT
# =========================================

long_trades = len(

    trades[
        trades["direction"] == "LONG"
    ]

)

short_trades = len(

    trades[
        trades["direction"] == "SHORT"
    ]

)

# =========================================
# BEST PAIRS
# =========================================

pair_performance = {}

for pair in trades["pair"].unique():

    pair_data = trades[
        trades["pair"] == pair
    ]

    wins = len(

        pair_data[
            pair_data["status"].isin(
                ["TP1", "TP2"]
            )
        ]

    )

    losses = len(

        pair_data[
            pair_data["status"] == "STOPLOSS"
        ]

    )

    total = wins + losses

    if total > 0:

        pair_winrate = round(
            (wins / total) * 100,
            2
        )

        pair_performance[pair] = pair_winrate

# =========================================
# BEST / WORST PAIRS
# =========================================

if len(pair_performance) > 0:

    best_pair = max(
        pair_performance,
        key=pair_performance.get
    )

    worst_pair = min(
        pair_performance,
        key=pair_performance.get
    )

else:

    best_pair = "N/A"

    worst_pair = "N/A"

# =========================================
# SUMMARY
# =========================================

print("========== BOT PERFORMANCE ==========\n")

print(f"Total Trades: {total_trades}")

print(f"Completed Trades: {completed_trades}")

print(f"TP1 Hits: {tp1_count}")

print(f"TP2 Hits: {tp2_count}")

print(f"Stoploss Hits: {sl_count}")

print(f"Winrate: {winrate}%")

print(f"LONG Trades: {long_trades}")

print(f"SHORT Trades: {short_trades}")

print(f"Best Pair: {best_pair}")

print(f"Worst Pair: {worst_pair}")

print("\n=====================================\n")

# =========================================
# SAVE ANALYTICS REPORT
# =========================================

report = pd.DataFrame([{

    "total_trades": total_trades,
    "completed_trades": completed_trades,
    "tp1_hits": tp1_count,
    "tp2_hits": tp2_count,
    "stoploss_hits": sl_count,
    "winrate": winrate,
    "long_trades": long_trades,
    "short_trades": short_trades,
    "best_pair": best_pair,
    "worst_pair": worst_pair

}])

report.to_csv(
    "performance_report.csv",
    index=False
)

print(
    "Performance report saved successfully."
)