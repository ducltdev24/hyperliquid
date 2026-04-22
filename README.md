# hyperliquid

Dashboard giao dich phong cach Hyperliquid bang Python + Flask.

## Tinh nang chinh

- Giao dien trading style: watchlist, chart nen, order book, recent trades
- Ho tro cac cap coin da whitelist:
  - `ETHUSD`, `SOLUSDT`, `XRPUSD`, `HYPEUSDT`, `SUIUSD`, `TAOUSD`, `ZROUSDT`, `MONUSDT`
- Du lieu market theo tung coin:
  - gia hien tai, mark price, funding, open interest, 24h volume
- Luu lich su gia vao database (MySQL/SQLite)
- Export lich su ra CSV theo coin
- DB Web UI: Adminer + phpMyAdmin

## Cau truc chinh

- `src/web_app.py`: Flask app + API
- `src/hyperliquid_btc_crawler.py`: ham fetch du lieu tu Hyperliquid API
- `src/storage.py`: luu/lay lich su gia
- `src/templates/index.html`: giao dien web
- `docker/docker-compose.yml`: web + mysql + adminer + phpmyadmin

## Chay nhanh bang Docker Compose (khuyen dung)

Tu thu muc `docker`:

```bash
docker compose up -d --build
```

Mo giao dien:

- Web app: http://localhost:8000
- Adminer: http://localhost:8080
- phpMyAdmin: http://localhost:8081

Xem log:

```bash
docker compose logs -f btc-crawler
```

Dung he thong:

```bash
docker compose down
```

## MySQL mac dinh

Thong tin ket noi:

- Host: `mysql` (trong compose network) hoac `127.0.0.1` (tu may local)
- Port: `3306`
- Database: `hyperliquid`
- Username: `hyperliquid`
- Password: `hyperliquid`

Env app dang su dung trong compose:

- `DATABASE_URL=mysql+pymysql://hyperliquid:hyperliquid@mysql:3306/hyperliquid`

## API chinh

- Lay du lieu market theo coin:
  - `GET /api/price?symbol=ETH`
- Lay lich su theo coin:
  - `GET /api/history?symbol=ETH`
- Export CSV theo coin:
  - `GET /api/history.csv?symbol=ETH&limit=1000`

Ghi chu:

- `symbol` dung ma coin goc: `ETH`, `SOL`, `XRP`, `HYPE`, `SUI`, `TAO`, `ZRO`, `MON`

## Chay local khong Docker

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python src/web_app.py
```

Mo: http://localhost:8000

Neu muon dung SQLite local:

```bash
set DATABASE_URL=sqlite:///D:/Project/hyperliquid/data/prices.db
python src/web_app.py
```
