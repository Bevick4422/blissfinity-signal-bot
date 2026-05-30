def detect_signal(df):

    latest = df.iloc[-1]

    price = latest["close"]

    recent_high = df["high"].iloc[-5]
    recent_low = df["low"].iloc[-5]

    # SIMPLE PLACEHOLDER LOGIC

    if price < recent_high:
        return "SHORT"

    elif price > recent_low:
        return "LONG"

    return None