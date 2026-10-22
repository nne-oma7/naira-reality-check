# 🇳🇬 Naira Reality Check

**Is the naira price of your crypto actually fair? Let's find out.**

---

## Why I built this

If you've ever tried to buy crypto in Nigeria, you know the feeling. You open a price checker, it says Bitcoin is a certain number of dollars, and then you open your exchange app and the naira price looks... different. Is that normal? Is it a fair price? Should you wait?

Most price trackers speak in dollars. But most of us earn, save and spend in naira. So the number that really matters, "what am I paying compared to what the world is paying?", is the one nobody shows you.

That gap felt like something worth building a tool for. This is my small attempt at it.

## What it does

Pick a coin, and it tells you three things:

1. 🌍 **What the world is paying** (global USD price)
2. 💱 **What that *should* be in naira** (using the USD to NGN exchange rate)
3. 🏦 **What Quidax is actually charging** (real local price)

Then it works out the **premium**, the percentage difference between the last two, and explains it in plain English. The page refreshes the numbers on its own every 30 seconds, so you can leave it open and watch the gap move.

## Two ways to use it

**1. The web page.** Open the home page, choose a coin from the dropdown, press **Check the gap**, and see the result in a simple card.

**2. The API.** If you'd rather get the data directly:

`GET /check/bitcoin`

```json
{
  "coin": "bitcoin",
  "global_price_usd": 81694,
  "usd_ngn_rate": 1334.416429,
  "global_implied_ngn": 109013815.75,
  "quidax_ngn": 111338290,
  "premium_percent": 2.13,
  "verdict": "Quidax is 2.13% ABOVE the global-implied naira price."
}
```

*(Numbers change with the market. This is a snapshot from when I tested it.)*

Other routes: `GET /coins` returns the list of supported coins.

## Supported coins

`bitcoin`, `ethereum`, `tether`, `ripple`, `litecoin`, `tron`, `dash`

I checked Quidax's list of naira markets and kept the coins I could match with CoinGecko's names. Coins Quidax doesn't list against naira (like Solana or Dogecoin) aren't included, because the whole point is comparing against a real local price.

## Where the data comes from

- **CoinGecko**: global USD prices
- **open.er-api.com**: USD to NGN exchange rate
- **Quidax public market API**: live naira prices

## Run it yourself

```bash
git clone https://github.com/nne-oma7/naira-reality-check.git
cd naira-reality-check
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** for the web page, or **http://127.0.0.1:8000/docs** to try the API directly.

## An honest note

The exchange rate I use is a published reference rate. It may not match the rate people actually trade at on a given day, so the "premium" is a helpful signal, not a verdict on whether anyone is overcharging you. A gap can come from exchange-rate differences, demand, fees, or timing.

The page refreshes every 30 seconds on purpose. The free price sources limit how often you can ask, and I'd rather be reliable than flashy.

## What I learned building it

- How to pull data from several APIs and combine it into one answer
- Handling errors gracefully, so one failing source doesn't crash everything
- Checking my data source instead of assuming what it supports (my first coin list had markets that don't exist!)
- Turning raw numbers into something a beginner can understand
- That a small project, finished, beats a big one that isn't

## What's next

- Save prices over time and show whether today's gap is normal or unusual
- A live chart of how the gap moves through the day
- Support more coins as I can verify them

## Built with

Python · FastAPI · Uvicorn · Requests · HTML, CSS and JavaScript

---

Built by **Nneoma**, an economics graduate teaching herself software engineering, one project at a time. 💛