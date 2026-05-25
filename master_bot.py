import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================
# TIMEZONE
# =========================================

LAGOS_TZ = ZoneInfo(
    "Africa/Lagos"
)

# =========================================
# DISPLAY
# =========================================

print("\n==============================")
print("BLISSFINITY MASTER BOT")
print("==============================\n")

# =========================================
# ENGINE RUNNER
# =========================================

def run_engine(name, command):

    print("==============================")
    print(f"RUNNING {name}")
    print("==============================\n")

    result = os.system(command)

    if result != 0:

        print(f"{name} exited with errors.\n")

    else:

        print(f"{name} completed.\n")

# =========================================
# MAIN LOOP
# =========================================

while True:

    try:

        # =====================================
        # CURRENT TIME
        # =====================================

        now = datetime.now(
            LAGOS_TZ
        )

        print(
            f"\nCurrent Nigeria Time: {now}\n"
        )

        # =====================================
        # SUNDAY FILTER
        # =====================================

        if now.weekday() == 6:

            print(
                "Sunday detected."
            )

            print(
                "Bot paused for 1 hour...\n"
            )

            time.sleep(3600)

            continue

        # =====================================
        # DAILY BIAS ENGINE
        # =====================================

        run_engine(
            "DAILY BIAS ENGINE",
            "python daily_bias_engine.py"
        )

        # =====================================
        # NEWS FILTER
        # =====================================

        run_engine(
            "NEWS FILTER",
            "python news_filter.py"
        )

        # =====================================
        # ENTRY ENGINE
        # =====================================

        run_engine(
            "ENTRY CONFIRMATION ENGINE",
            "python entry_confirmation_engine.py"
        )

        # =====================================
        # TRADE TRACKER
        # =====================================

        run_engine(
            "TRADE TRACKER",
            "python trade_tracker.py"
        )

        # =====================================
        # PERFORMANCE ANALYTICS
        # =====================================

        run_engine(
            "PERFORMANCE ANALYTICS",
            "python performance_analytics.py"
        )

        # =====================================
        # LOOP TIMER
        # =====================================

        print("==============================")
        print("CYCLE COMPLETED")
        print("==============================\n")

        print(
            "Sleeping for 5 minutes...\n"
        )

        time.sleep(300)

    except KeyboardInterrupt:

        print(
            "\nBot stopped manually.\n"
        )

        break

    except Exception as e:

        print(
            "\nMASTER BOT ERROR\n"
        )

        print(e)

        print(
            "\nRestarting in 30 seconds...\n"
        )

        time.sleep(30)