import requests

r = requests.get("https://app.quidax.io/api/v1/markets/tickers")
data = r.json()["data"]
print(type(data))
print([m for m in data if str(m).endswith("ngn")])