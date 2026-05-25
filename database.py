import sqlite3

print("\n==============================")
print("INITIALIZING DATABASE")
print("==============================\n")

# =========================================
# CONNECT DATABASE
# =========================================

conn = sqlite3.connect(
    "blissfinity.db"
)

cursor = conn.cursor()

# =========================================
# ACTIVE TRADES TABLE
# =========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS active_trades (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    pair TEXT,

    direction TEXT,

    entry REAL,

    stoploss REAL,

    tp1 REAL,

    tp2 REAL,

    score INTEGER,

    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

# =========================================
# TRADE HISTORY TABLE
# =========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS trade_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    pair TEXT,

    direction TEXT,

    entry REAL,

    stoploss REAL,

    tp1 REAL,

    tp2 REAL,

    score INTEGER,

    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

# =========================================
# SENT SIGNALS TABLE
# =========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS sent_signals (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    signal_id TEXT UNIQUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

# =========================================
# SAVE CHANGES
# =========================================

conn.commit()

# =========================================
# CLOSE DATABASE
# =========================================

conn.close()

print("Database initialized successfully.\n")