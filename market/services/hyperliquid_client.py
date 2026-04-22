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
    universe = meta.get("universe", []) if isinstance(meta, dict) else meta

    if not isinstance(universe, list) or not isinstance(asset_contexts, list):
        raise ValueError("Cau truc metaAndAssetCtxs khong hop le.")
    return universe, asset_contexts
