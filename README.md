# hyperliquid

Dashboard giao dich phong cach Hyperliquid duoc xay dung lai bang Django, voi cau truc de bao tri.

## Tinh nang chinh

- Giao dien trading style: watchlist, chart nen, order book, recent trades
- Ho tro cap coin whitelist: `ETH`, `SOL`, `XRP`, `HYPE`, `SUI`, `TAO`, `ZRO`, `MON`
- Chi so theo tung coin: mark, funding, open interest, 24h volume
- Luu lich su gia vao DB (MySQL/SQLite)
- Export CSV theo coin
- DB Web UI: Adminer + phpMyAdmin

## Cau truc thu muc (Django)

- `manage.py`: entrypoint Django
- `hyperdash/`: project settings + urls
- `market/`: app chinh (models, views, urls, services)
- `market/services/`: tach logic API Hyperliquid va xu ly market
- `templates/market/index.html`: giao dien dashboard
- `docker/docker-compose.yml`: web + mysql + adminer + phpmyadmin

## Chay bang Docker Compose

Trong thu muc `docker`:

```bash
docker compose up -d --build
```

Mo:

- Web app: http://localhost:8000
- Adminer: http://localhost:8080
- phpMyAdmin: http://localhost:8081

Xem log:

```bash
docker compose logs -f btc-crawler
```

Dung:

```bash
docker compose down
```

## Chay local khong Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Mo: http://localhost:8000

Neu muon dung SQLite local:

```bash
set DATABASE_URL=sqlite:///D:/Project/hyperliquid/data/prices.db
python manage.py migrate
python manage.py runserver
```

## DATABASE_URL

- MySQL (compose): `mysql+pymysql://hyperliquid:hyperliquid@mysql:3306/hyperliquid`
- SQLite: `sqlite:///D:/Project/hyperliquid/data/prices.db`

## API

- `GET /api/price?symbol=ETH`
- `GET /api/history?symbol=ETH`
- `GET /api/history.csv?symbol=ETH&limit=1000`
