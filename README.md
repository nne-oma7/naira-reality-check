# 🇳🇬 Naira Reality Check API

**Is the naira price of your crypto actually fair? Let's find out.**

---

## Why I built this

If you've ever tried to buy crypto in Nigeria, you know the feeling. You open a price checker, it says Bitcoin is a certain number of dollars, and then you open your exchange app and the naira price looks... different. Is that normal? Is it a fair price? Should you wait?

Most price trackers speak in dollars. But most of us earn, save and spend in naira. So the number that really matters, "what am I paying compared to what the world is paying?", is the one nobody shows you.

That gap felt like something worth building a tool for. This is my small attempt at it.

## What it does

You ask about a coin, and it tells you three things:

1. 🌍 **What the world is paying** (global USD price)
2. 💱 **What that *should* be in naira** (using the USD to NGN exchange rate)
3. 🏦 **What Quidax is actually charging** (real local price)

Then it works out the **premium**, the percentage difference between the last two, and says it in plain English.

### Example

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

## Supported coins

`bitcoin`, `ethereum`, `tether`, `ripple`, `litecoin`, `tron`, `dash`

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

Then open **http://127.0.0.1:8000/docs** in your browser, click **GET /check/{coin}**, hit **Try it out**, type a coin, and press **Execute**.

## An honest note

The exchange rate I use is a published reference rate. It may not match the rate people actually trade at on a given day, so the "premium" is a helpful signal, not a verdict on whether anyone is overcharging you. A gap can come from exchange-rate differences, demand, fees, or timing.

## What I learned building it

- How to pull data from several APIs and combine it into one answer
- Handling errors gracefully, so one failing source doesn't crash everything
- Turning raw numbers into something a beginner can understand
- That a small project, finished, beats a big one that isn't

## What's next

- Save prices over time and show whether today's gap is normal or unusual
- Support more coins
- A simple front end, so you don't need the docs page

## Built with

Python · FastAPI · Uvicorn · Requests

---

Built by **Nneoma**, an economics graduate teaching herself software engineering, one project at a time. 💛