import os
from datetime import datetime, timezone

from sqlalchemy import create_engine, text


DB_PATH = os.getenv("BTC_DB_PATH", "/app/data/prices.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True)


def ensure_sqlite_dir() -> None:
    if DATABASE_URL.startswith("sqlite:///"):
        db_file = DATABASE_URL.replace("sqlite:///", "", 1)
        db_dir = os.path.dirname(db_file)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)


def init_db() -> None:
    ensure_sqlite_dir()
    if DATABASE_URL.startswith("sqlite:///"):
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                created_at_utc TEXT NOT NULL
            )
        """
    else:
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS price_history (
                id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                symbol VARCHAR(32) NOT NULL,
                price DOUBLE NOT NULL,
                created_at_utc VARCHAR(64) NOT NULL
            )
        """

    with ENGINE.begin() as conn:
        conn.execute(text(create_table_sql))


def save_price(symbol: str, price: float) -> None:
    with ENGINE.begin() as conn:
        conn.execute(
            text(
                """
            INSERT INTO price_history (symbol, price, created_at_utc)
            VALUES (:symbol, :price, :created_at_utc)
            """
            ),
            {
                "symbol": symbol,
                "price": float(price),
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
            },
        )


def get_recent_prices(symbol: str = "BTC", limit: int = 50) -> list:
    with ENGINE.begin() as conn:
        rows = conn.execute(
            text(
                """
            SELECT symbol, price, created_at_utc
            FROM price_history
            WHERE symbol = :symbol
            ORDER BY id DESC
            LIMIT :limit
            """
            ),
            {"symbol": symbol, "limit": int(limit)},
        ).mappings().all()
    return [dict(row) for row in rows]
