import csv
from io import StringIO
from datetime import datetime, timezone
import random

from flask import Flask, jsonify, render_template, request, Response

from hyperliquid_btc_crawler import fetch_all_mids
from storage import get_recent_prices, init_db, save_price


app = Flask(__name__)
init_db()


def build_order_book(mid_price: float, levels: int = 12) -> dict:
    asks = []
    bids = []
    for level in range(1, levels + 1):
        offset = level * 3.5
        ask_price = round(mid_price + offset, 2)
        bid_price = round(mid_price - offset, 2)
        asks.append(
            {
                "price": ask_price,
                "size": round(random.uniform(0.05, 1.8), 4),
                "total": round(random.uniform(2000, 120000), 2),
            }
        )
        bids.append(
            {
                "price": bid_price,
                "size": round(random.uniform(0.05, 1.8), 4),
                "total": round(random.uniform(2000, 120000), 2),
            }
        )
    asks.sort(key=lambda item: item["price"], reverse=True)
    bids.sort(key=lambda item: item["price"], reverse=True)
    return {"asks": asks, "bids": bids}


def build_recent_trades(history: list, max_items: int = 10) -> list:
    trades = []
    for idx in range(min(len(history) - 1, max_items)):
        curr = history[idx]
        prev = history[idx + 1]
        side = "Buy" if curr["price"] >= prev["price"] else "Sell"
        size = round(random.uniform(0.01, 0.5), 4)
        trades.append(
            {
                "time": curr["created_at_utc"][11:19],
                "price": curr["price"],
                "size": size,
                "side": side,
            }
        )
    return trades


def get_price_payload() -> dict:
    mids = fetch_all_mids()
    if "BTC" not in mids:
        raise ValueError("Khong tim thay gia BTC trong du lieu allMids.")

    coins = []
    for symbol, value in mids.items():
        try:
            coins.append({"symbol": symbol, "price": float(value)})
        except (TypeError, ValueError):
            continue
    coins.sort(key=lambda item: item["price"], reverse=True)

    btc_price = float(mids["BTC"])
    save_price("BTC", btc_price)
    btc_history = get_recent_prices(symbol="BTC", limit=30)

    return {
        "btc_price": btc_price,
        "market_symbol": "BTC-USD",
        "top_10_coins": coins[:10],
        "btc_history": btc_history[:10],
        "order_book": build_order_book(btc_price, levels=12),
        "recent_trades": build_recent_trades(btc_history, max_items=10),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def index():
    error = None
    payload = None
    try:
        payload = get_price_payload()
    except Exception as exc:
        error = str(exc)
    return render_template("index.html", payload=payload, error=error)


@app.get("/api/price")
def api_price():
    try:
        payload = get_price_payload()
        return jsonify(payload), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/history")
def api_history():
    try:
        history = get_recent_prices(symbol="BTC", limit=100)
        return jsonify({"symbol": "BTC", "history": history}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.get("/api/history.csv")
def api_history_csv():
    try:
        limit = request.args.get("limit", default=500, type=int)
        if limit <= 0:
            return jsonify({"error": "limit phai > 0"}), 400

        history = get_recent_prices(symbol="BTC", limit=limit)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["symbol", "price", "created_at_utc"])
        for row in history:
            writer.writerow([row["symbol"], row["price"], row["created_at_utc"]])

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        filename = f"btc_history_{timestamp}.csv"
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
