import random
from datetime import datetime, timezone

from market.models import PriceHistory
from market.services.hyperliquid_client import fetch_all_mids, fetch_meta_and_asset_contexts

ALLOWED_MARKETS = [
    {"symbol": "ETH", "label": "ETHUSD"},
    {"symbol": "SOL", "label": "SOLUSDT"},
    {"symbol": "XRP", "label": "XRPUSD"},
    {"symbol": "HYPE", "label": "HYPEUSDT"},
    {"symbol": "SUI", "label": "SUIUSD"},
    {"symbol": "TAO", "label": "TAOUSD"},
    {"symbol": "ZRO", "label": "ZROUSDT"},
    {"symbol": "MON", "label": "MONUSDT"},
]


def normalize_symbol(symbol: str | None) -> str:
    if not symbol:
        return "ETH"
    return symbol.strip().upper()


def parse_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def build_asset_context_map() -> dict:
    universe, asset_contexts = fetch_meta_and_asset_contexts()
    ctx_map = {}
    for meta, ctx in zip(universe, asset_contexts):
        symbol = meta.get("name") if isinstance(meta, dict) else None
        if symbol and isinstance(ctx, dict):
            ctx_map[str(symbol).upper()] = ctx
    return ctx_map


def build_order_book(mid_price: float, levels: int = 12) -> dict:
    asks = []
    bids = []
    for level in range(1, levels + 1):
        offset = level * 3.5
        ask_price = round(mid_price + offset, 2)
        bid_price = round(mid_price - offset, 2)
        asks.append(
            {"price": ask_price, "size": round(random.uniform(0.05, 1.8), 4), "total": round(random.uniform(2000, 120000), 2)}
        )
        bids.append(
            {"price": bid_price, "size": round(random.uniform(0.05, 1.8), 4), "total": round(random.uniform(2000, 120000), 2)}
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
        trades.append(
            {
                "time": curr["created_at_utc"][11:19],
                "price": curr["price"],
                "size": round(random.uniform(0.01, 0.5), 4),
                "side": side,
            }
        )
    return trades


def save_price(symbol: str, price: float) -> None:
    PriceHistory.objects.create(symbol=symbol, price=float(price))


def get_recent_prices(symbol: str, limit: int) -> list:
    qs = PriceHistory.objects.filter(symbol=symbol).order_by("-id")[:limit]
    return [
        {"symbol": row.symbol, "price": row.price, "created_at_utc": row.created_at_utc.isoformat()}
        for row in qs
    ]


def build_price_payload(selected_symbol: str) -> dict:
    mids = fetch_all_mids()
    context_map = build_asset_context_map()
    selected_symbol = normalize_symbol(selected_symbol)

    allowed_pairs = []
    for market in ALLOWED_MARKETS:
        symbol = market["symbol"]
        if symbol in mids:
            allowed_pairs.append({"symbol": symbol, "label": market["label"], "price": parse_float(mids[symbol])})

    if not allowed_pairs:
        raise ValueError("Khong tim thay cac cap coin duoc cau hinh trong du lieu allMids.")

    allowed_symbols = {pair["symbol"] for pair in allowed_pairs}
    if selected_symbol not in allowed_symbols:
        selected_symbol = allowed_pairs[0]["symbol"]

    selected_pair = next(pair for pair in allowed_pairs if pair["symbol"] == selected_symbol)
    selected_ctx = context_map.get(selected_symbol, {})
    selected_price = parse_float(mids[selected_symbol])

    save_price(selected_symbol, selected_price)
    price_history = get_recent_prices(selected_symbol, 240)

    return {
        "selected_symbol": selected_symbol,
        "selected_label": selected_pair["label"],
        "selected_price": selected_price,
        "market_symbol": selected_pair["label"],
        "mark_price": parse_float(selected_ctx.get("markPx"), selected_price),
        "funding_rate": parse_float(selected_ctx.get("funding"), 0.0),
        "open_interest": parse_float(selected_ctx.get("openInterest"), 0.0),
        "day_volume": parse_float(selected_ctx.get("dayNtlVlm"), 0.0),
        "top_10_coins": allowed_pairs,
        "coin_pairs": allowed_pairs,
        "price_history": price_history[:180],
        "order_book": build_order_book(selected_price, levels=12),
        "recent_trades": build_recent_trades(price_history, max_items=10),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }
