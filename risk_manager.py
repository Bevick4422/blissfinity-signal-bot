print("\n==============================")
print("RISK MANAGER")
print("==============================\n")

# =========================================
# SETTINGS
# =========================================

ACCOUNT_BALANCE = 1000

RISK_PERCENT = 1

LEVERAGE = 10

# =========================================
# CALCULATOR
# =========================================

def calculate_position_size(

    entry,
    stoploss

):

    try:

        # ---------------------------------
        # RISK CAPITAL
        # ---------------------------------

        risk_amount = (

            ACCOUNT_BALANCE
            *
            (RISK_PERCENT / 100)

        )

        # ---------------------------------
        # STOP DISTANCE
        # ---------------------------------

        stop_distance = abs(

            entry
            -
            stoploss

        )

        if stop_distance <= 0:

            return None

        # ---------------------------------
        # POSITION SIZE
        # ---------------------------------

        position_size = (

            risk_amount
            /
            stop_distance

        )

        # ---------------------------------
        # LEVERAGED SIZE
        # ---------------------------------

        leveraged_size = (

            position_size
            *
            LEVERAGE

        )

        # ---------------------------------
        # ROUNDING
        # ---------------------------------

        position_size = round(
            position_size,
            2
        )

        leveraged_size = round(
            leveraged_size,
            2
        )

        return {

            "risk_amount": round(
                risk_amount,
                2
            ),

            "position_size": position_size,

            "leveraged_size": leveraged_size

        }

    except Exception as e:

        print(e)

        return None

# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    result = calculate_position_size(

        entry=100,
        stoploss=95

    )

    print(result)