import csv
from datetime import datetime, timezone

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from market.services.trading_service import build_price_payload, get_recent_prices, normalize_symbol


def index(request):
    error = None
    payload = None
    symbol = normalize_symbol(request.GET.get("symbol", "ETH"))
    try:
        payload = build_price_payload(symbol)
    except Exception as exc:
        error = str(exc)
    return render(request, "market/index.html", {"payload": payload, "error": error})


def api_price(request):
    try:
        symbol = normalize_symbol(request.GET.get("symbol", "ETH"))
        payload = build_price_payload(symbol)
        return JsonResponse(payload, status=200)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)


def api_history(request):
    try:
        symbol = normalize_symbol(request.GET.get("symbol", "ETH"))
        history = get_recent_prices(symbol, 100)
        return JsonResponse({"symbol": symbol, "history": history}, status=200)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)


def api_history_csv(request):
    try:
        limit = int(request.GET.get("limit", "500"))
        symbol = normalize_symbol(request.GET.get("symbol", "ETH"))
        if limit <= 0:
            return JsonResponse({"error": "limit phai > 0"}, status=400)

        history = get_recent_prices(symbol, limit)
        response = HttpResponse(content_type="text/csv")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        response["Content-Disposition"] = f'attachment; filename="{symbol.lower()}_history_{timestamp}.csv"'

        writer = csv.writer(response)
        writer.writerow(["symbol", "price", "created_at_utc"])
        for row in history:
            writer.writerow([row["symbol"], row["price"], row["created_at_utc"]])
        return response
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)
