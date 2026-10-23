from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests
from sqlalchemy.orm import Session

from database import SessionLocal
from models import PriceSnapshot
from sqlalchemy import desc

app = FastAPI(title="Naira Reality Check API")

# CoinGecko name -> Quidax symbol
COINS = {
    "bitcoin": "btc", "ethereum": "eth", "tether": "usdt",
    "ripple": "xrp", "litecoin": "ltc", "tron": "trx", "dash": "dash",
}


@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/coins")
def coins():
    return list(COINS)



@app.get("/check/{coin}")
def check(coin: str):
    coin = coin.lower()

    if coin not in COINS:
        raise HTTPException(
            status_code=404,
            detail=f"Coin not supported. Try: {', '.join(COINS)}",
        )

    try:
        usd_response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin, "vs_currencies": "usd"},
            timeout=10,
        )
        usd_response.raise_for_status()
        usd_data = usd_response.json()
        usd = float(usd_data[coin]["usd"])

        rate_response = requests.get(
            "https://open.er-api.com/v6/latest/USD",
            timeout=10,
        )
        rate_response.raise_for_status()
        rate_data = rate_response.json()
        rate = float(rate_data["rates"]["NGN"])

        quidax_response = requests.get(
            f"https://app.quidax.io/api/v1/markets/tickers/{COINS[coin]}ngn",
            timeout=10,
        )
        quidax_response.raise_for_status()
        quidax_data = quidax_response.json()
        local = float(quidax_data["data"]["ticker"]["last"])

        if not all(
            value > 0
            for value in (usd, rate, local)
        ):
            raise ValueError("Prices and exchange rates must be positive.")

    except (requests.RequestException, ValueError, KeyError, TypeError, IndexError):
        raise HTTPException(
            status_code=502,
            detail="Could not fetch valid market data. Please try again.",
        )

    implied = usd * rate
    gap = (local - implied) / implied * 100

    if gap > 0:
        verdict = (
            f"Quidax is {abs(gap):.2f}% ABOVE "
            "the global-implied naira price."
        )
    elif gap < 0:
        verdict = (
            f"Quidax is {abs(gap):.2f}% BELOW "
            "the global-implied naira price."
        )
    else:
        verdict = "Quidax matches the global-implied naira price."

    db: Session = SessionLocal()

    try:
        snapshot = PriceSnapshot(
            coin=coin,
            global_price_usd=usd,
            usd_ngn_rate=rate,
            global_implied_ngn=round(implied, 2),
            quidax_ngn=local,
            premium_percent=round(gap, 2),
        )

        db.add(snapshot)
        db.commit()
        db.refresh(snapshot)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Market data was fetched, but the snapshot could not be saved.",
        )

    finally:
        db.close()

    return {
        "coin": coin,
        "global_price_usd": usd,
        "usd_ngn_rate": rate,
        "global_implied_ngn": round(implied, 2),
        "quidax_ngn": local,
        "premium_percent": round(gap, 2),
        "verdict": verdict,
        "recorded_at": snapshot.recorded_at,
    }



@app.get("/history/{coin}")
def history(coin: str, limit: int = 50):
    coin = coin.lower()

    if coin not in COINS:
        raise HTTPException(
            status_code=404,
            detail=f"Coin not supported. Try: {', '.join(COINS)}",
        )

    if not 1 <= limit <= 500:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 500.",
        )

    db = SessionLocal()

    try:
        snapshots = (
            db.query(PriceSnapshot)
            .filter(PriceSnapshot.coin == coin)
            .order_by(desc(PriceSnapshot.recorded_at))
            .limit(limit)
            .all()
        )

        return {
            "coin": coin,
            "count": len(snapshots),
            "history": [
                {
                    "recorded_at": item.recorded_at,
                    "global_price_usd": item.global_price_usd,
                    "usd_ngn_rate": item.usd_ngn_rate,
                    "global_implied_ngn": item.global_implied_ngn,
                    "quidax_ngn": item.quidax_ngn,
                    "premium_percent": item.premium_percent,
                }
                for item in snapshots
            ],
        }
    finally:
        db.close()



@app.get("/summary/{coin}")
def summary(coin: str):
    coin = coin.lower()

    if coin not in COINS:
        raise HTTPException(
            status_code=404,
            detail=f"Coin not supported. Try: {', '.join(COINS)}",
        )

    db = SessionLocal()

    try:
        snapshots = (
            db.query(PriceSnapshot)
            .filter(PriceSnapshot.coin == coin)
            .order_by(PriceSnapshot.recorded_at.asc())
            .all()
        )

        if not snapshots:
            return {
                "coin": coin,
                "snapshots_count": 0,
                "message": "No price history found. Check this coin first.",
            }

        premiums = [
            snapshot.premium_percent
            for snapshot in snapshots
        ]

        oldest_premium = premiums[0]
        latest_premium = premiums[-1]

        if len(premiums) < 2:
            trend = "insufficient_data"
        elif latest_premium > oldest_premium:
            trend = "increasing"
        elif latest_premium < oldest_premium:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "coin": coin,
            "snapshots_count": len(snapshots),
            "latest_premium_percent": latest_premium,
            "average_premium_percent": round(
                sum(premiums) / len(premiums), 2
            ),
            "highest_premium_percent": max(premiums),
            "lowest_premium_percent": min(premiums),
            "trend": trend,
        }

    finally:
        db.close()

# @app.get("/check/{coin}")
# def check(coin: str):
#     coin = coin.lower()
#     if coin not in COINS:
#         raise HTTPException(404, f"Coin not supported. Try: {', '.join(COINS)}")

#     try:
#         usd = requests.get(
#             "https://api.coingecko.com/api/v3/simple/price",
#             params={"ids": coin, "vs_currencies": "usd"}, timeout=10,
#         ).json()[coin]["usd"]

#         rate = requests.get(
#             "https://open.er-api.com/v6/latest/USD", timeout=10
#         ).json()["rates"]["NGN"]

#         q = requests.get(
#             f"https://app.quidax.io/api/v1/markets/tickers/{COINS[coin]}ngn",
#             timeout=10,
#         ).json()
#         local = float(q["data"]["ticker"]["last"])
#     except Exception:
#         raise HTTPException(502, "Could not fetch data from a source. Try again.")

#     implied = usd * rate
#     gap = (local - implied) / implied * 100

#     if gap > 0:
#         verdict = f"Quidax is {abs(gap):.2f}% ABOVE the global-implied naira price."
#     else:
#         verdict = f"Quidax is {abs(gap):.2f}% BELOW the global-implied naira price."

#     return {
#         "coin": coin,
#         "global_price_usd": usd,
#         "usd_ngn_rate": rate,
#         "global_implied_ngn": round(implied, 2),
#         "quidax_ngn": local,
#         "premium_percent": round(gap, 2),
#         "verdict": verdict,
#     }