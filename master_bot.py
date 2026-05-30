import os
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# =========================================
# TIMEZONE
# =========================================

LAGOS_TZ = ZoneInfo("Africa/Lagos")

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

    print("\n========================================")
    print(f"STARTING: {name}")
    print(f"TIME: {datetime.now(LAGOS_TZ)}")
    print("========================================")

    try:

        result = os.system(command)

        print(
            f"{name} EXIT CODE: {result}"
        )

        if result != 0:

            print(
                f"{name} FAILED\n"
            )

        else:

            print(
                f"{name} COMPLETED\n"
            )

    except Exception as e:

        print(
            f"{name} CRASHED:"
        )

        print(e)

# =========================================
# MAIN LOOP
# =========================================

while True:

    try:

        now = datetime.now(
            LAGOS_TZ
        )

        print(
            f"\nCURRENT NIGERIA TIME: {now}\n"
        )

        # =====================================
        # SUNDAY FILTER
        # =====================================

        if now.weekday() == 6:

            print(
                "SUNDAY DETECTED"
            )

            print(
                "PAUSING FOR 1 HOUR\n"
            )

            time.sleep(3600)

            continue

        # =====================================
        # DAILY BIAS
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

        print(
            "\nABOUT TO RUN ENTRY ENGINE\n"
        )

        run_engine(
            "ENTRY CONFIRMATION ENGINE",
            "python entry_confirmation_engine.py"
        )

        print(
            "\nENTRY ENGINE FINISHED\n"
        )

        # =====================================
        # TRADE TRACKER
        # =====================================

        run_engine(
            "TRADE TRACKER",
            "python trade_tracker.py"
        )

        # =====================================
        # PERFORMANCE
        # =====================================

        run_engine(
            "PERFORMANCE ANALYTICS",
            "python performance_analytics.py"
        )

        # =====================================
        # LOOP COMPLETE
        # =====================================

        print(
            "\n========================================"
        )

        print(
            "FULL BOT CYCLE COMPLETE"
        )

        print(
            "========================================\n"
        )

        print(
            "Sleeping for 5 minutes...\n"
        )

        time.sleep(300)

    except KeyboardInterrupt:

        print(
            "\nBOT STOPPED MANUALLY\n"
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