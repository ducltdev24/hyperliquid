# hyperliquid

Project Python nho de crawl gia BTC tu Hyperliquid qua API public.

## 1) Cai dat

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2) Chay 1 lan

```bash
python src/hyperliquid_btc_crawler.py
```

Vi du output:

```text
[2026-04-23T07:00:00.000000+00:00] BTC = 68234.5
```

## 3) Poll lien tuc moi 2 giay

```bash
python src/hyperliquid_btc_crawler.py --interval 2
```

## 4) Output JSON (de day vao log pipeline)

```bash
python src/hyperliquid_btc_crawler.py --interval 2 --json
```

## 5) Giao dien web bang Python (Flask)

Chay local:

```bash
python src/web_app.py
```

Mo tren trinh duyet:

- http://localhost:8000

Trang web se tu dong refresh gia BTC, top 10 coin, va luu lich su BTC vao database.

## 6) Dung Docker

Build image:

```bash
docker build --ignorefile docker/.dockerignore -f docker/Dockerfile -t hyperliquid-btc-crawler .
```

Chay web:

```bash
docker run --rm -p 8000:8000 hyperliquid-btc-crawler
```

Mo trinh duyet:

- http://localhost:8000

Neu muon chay crawler CLI trong container:

```bash
docker run --rm hyperliquid-btc-crawler python src/hyperliquid_btc_crawler.py --interval 2
```

Output JSON:

```bash
docker run --rm hyperliquid-btc-crawler python src/hyperliquid_btc_crawler.py --interval 2 --json
```

## 7) Dung Docker Compose (web)

Start web o background:

```bash
docker compose -f docker/docker-compose.yml up -d --build
```

Mo trinh duyet:

- http://localhost:8000

Xem log:

```bash
docker compose -f docker/docker-compose.yml logs -f
```

Dung va xoa container:

```bash
docker compose -f docker/docker-compose.yml down
```

## 8) Database lich su gia (MySQL)

- Docker Compose da them service `mysql` de dung cho du lieu lon hon.
- Ket noi DB trong app qua env:
  - `DATABASE_URL=mysql+pymysql://hyperliquid:hyperliquid@mysql:3306/hyperliquid`
- MySQL data duoc luu persistent bang volume `mysql_data`.
- API lich su:
  - http://localhost:8000/api/history
  - http://localhost:8000/api/history.csv
- DB Web UI:
  - Adminer: http://localhost:8080
  - phpMyAdmin: http://localhost:8081

Thong tin dang nhap MySQL:

- Server/Host: `mysql` (neu dang nhap trong container UI) hoac `127.0.0.1` (neu dung tool tren may)
- Username: `hyperliquid`
- Password: `hyperliquid`
- Database: `hyperliquid`

Neu ban muon chay local khong MySQL, app van ho tro SQLite voi:

```bash
set DATABASE_URL=sqlite:///D:/Project/hyperliquid/data/prices.db
python src/web_app.py
```

## 9) Xuat file CSV

- Tai CSV truc tiep tren web bang nut `Export CSV`.
- Hoac goi endpoint:
  - http://localhost:8000/api/history.csv?limit=1000
