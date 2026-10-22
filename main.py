from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import requests

app = FastAPI(title="Naira Reality Check API")

# CoinGecko name -> Quidax symbol
COINS = {
    "bitcoin": "btc", "ethereum": "eth", "tether": "usdt",
    "ripple": "xrp", "litecoin": "ltc", "tron": "trx", "dash": "dash",
}


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/check/{coin}")
def check(coin: str):
    coin = coin.lower()
    if coin not in COINS:
        raise HTTPException(404, f"Coin not supported. Try: {', '.join(COINS)}")

    try:
        usd = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin, "vs_currencies": "usd"}, timeout=10,
        ).json()[coin]["usd"]

        rate = requests.get(
            "https://open.er-api.com/v6/latest/USD", timeout=10
        ).json()["rates"]["NGN"]

        q = requests.get(
            f"https://app.quidax.io/api/v1/markets/tickers/{COINS[coin]}ngn",
            timeout=10,
        ).json()
        local = float(q["data"]["ticker"]["last"])
    except Exception:
        raise HTTPException(502, "Could not fetch data from a source. Try again.")

    implied = usd * rate
    gap = (local - implied) / implied * 100

    if gap > 0:
        verdict = f"Quidax is {abs(gap):.2f}% ABOVE the global-implied naira price."
    else:
        verdict = f"Quidax is {abs(gap):.2f}% BELOW the global-implied naira price."

    return {
        "coin": coin,
        "global_price_usd": usd,
        "usd_ngn_rate": rate,
        "global_implied_ngn": round(implied, 2),
        "quidax_ngn": local,
        "premium_percent": round(gap, 2),
        "verdict": verdict,
    }