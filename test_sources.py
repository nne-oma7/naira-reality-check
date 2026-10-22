import requests

r = requests.get("https://api.coingecko.com/api/v3/simple/price",
                 params={"ids": "bitcoin", "vs_currencies": "usd"})
print("COINGECKO:", r.json())

r = requests.get("https://open.er-api.com/v6/latest/USD")
print("NGN RATE:", r.json()["rates"]["NGN"])

r = requests.get("https://app.quidax.io/api/v1/markets/tickers/btcngn")
print("QUIDAX:", r.json())