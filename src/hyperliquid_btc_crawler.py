import argparse
import json
import time
from datetime import datetime, timezone

import requests


HYPERLIQUID_INFO_URL = "https://api.hyperliquid.xyz/info"


def fetch_all_mids(timeout: int = 10) -> dict:
    payload = {"type": "allMids"}
    response = requests.post(HYPERLIQUID_INFO_URL, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()


def fetch_meta_and_asset_contexts(timeout: int = 10) -> tuple[list, list]:
    payload = {"type": "metaAndAssetCtxs"}
    response = requests.post(HYPERLIQUID_INFO_URL, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or len(data) != 2:
        raise ValueError("Du lieu metaAndAssetCtxs khong hop le.")

    meta, asset_contexts = data
    if isinstance(meta, dict):
        universe = meta.get("universe", [])
    else:
        universe = meta

    if not isinstance(universe, list) or not isinstance(asset_contexts, list):
        raise ValueError("Cau truc metaAndAssetCtxs khong hop le.")
    return universe, asset_contexts


def fetch_btc_price(timeout: int = 10) -> float:
    mids = fetch_all_mids(timeout=timeout)

    if "BTC" not in mids:
        raise ValueError("Khong tim thay gia BTC trong du lieu allMids.")

    return float(mids["BTC"])


def fetch_top_coins(limit: int = 10, timeout: int = 10) -> list:
    mids = fetch_all_mids(timeout=timeout)
    coins = []
    for symbol, value in mids.items():
        try:
            coins.append({"symbol": symbol, "price": float(value)})
        except (TypeError, ValueError):
            continue

    coins.sort(key=lambda item: item["price"], reverse=True)
    return coins[:limit]


def log_btc_price(price: float, output_json: bool = False) -> None:
    now = datetime.now(timezone.utc).isoformat()
    data = {"timestamp_utc": now, "symbol": "BTC", "price": price}

    if output_json:
        print(json.dumps(data, ensure_ascii=True))
    else:
        print(f"[{now}] BTC = {price}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Crawl gia BTC tu Hyperliquid.")
    parser.add_argument(
        "--interval",
        type=float,
        default=0,
        help="So giay poll lien tuc. 0 = chi lay 1 lan.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="In output dang JSON 1 dong/log.",
    )
    args = parser.parse_args()

    if args.interval < 0:
        raise ValueError("--interval phai >= 0.")

    if args.interval == 0:
        price = fetch_btc_price()
        log_btc_price(price, output_json=args.json)
        return

    while True:
        try:
            price = fetch_btc_price()
            log_btc_price(price, output_json=args.json)
        except Exception as exc:
            error_data = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "symbol": "BTC",
                "error": str(exc),
            }
            if args.json:
                print(json.dumps(error_data, ensure_ascii=True))
            else:
                print(f"[{error_data['timestamp_utc']}] ERROR: {exc}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
