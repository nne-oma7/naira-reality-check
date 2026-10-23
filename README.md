# 🇳🇬 Naira Reality Check

### Is your crypto really worth what the Nigerian market says it is?

If you've ever tried to buy crypto in Nigeria, you know the feeling. You open a price checker, it says Bitcoin is a certain number of dollars, and then you open your exchange app and the naira price looks... different. Is that normal? Is it a fair price? Should you wait?



Most price trackers speak in dollars. But most of us earn, save and spend in naira. So the number that really matters, "what am I paying compared to what the world is paying?", is the one nobody shows you.



That gap felt like something worth building a tool for. This is my small attempt at it.

Have you ever wondered why the price of a cryptocurrency in Nigeria can be different from its price on the global market?

I built **Naira Reality Check** to explore that question.

It's a small project with a simple idea: take the global price of a cryptocurrency, convert it to naira using a reference exchange rate, compare that amount with its price on Quidax, and show the difference.

And because one price check only tells you what's happening at that moment, I also built a way to save those checks and track how the difference changes over time.

Think of it as a little reality check for crypto prices in Nigeria. 💚

---

## 💭 Why I built it

I wanted to understand something that can be confusing when you're looking at cryptocurrency prices: **why doesn't the price always look the same everywhere?**

A cryptocurrency can have a global price in US dollars, but when you're checking the Nigerian market, you're looking at a price in naira. Simply converting the global price into naira doesn't necessarily mean you'll get exactly the same price on a local exchange.

There can be a difference.

That difference was what I wanted to explore.

Rather than just checking a price and moving on, I wanted to build something that could put the two prices side by side, calculate the gap, and keep a record of previous checks.

That's how Naira Reality Check started: with a question, a little curiosity, and a desire to build something useful while learning software engineering.

## 🧐 So, what does it actually do?

Imagine the global market price of a cryptocurrency works out to ₦1,000,000 when converted using a reference exchange rate, but its price on Quidax is ₦1,050,000.

Naira Reality Check compares those two amounts and calculates the difference.

In this example, the Quidax price is 5% higher than the global implied price.

Here's what the app does:

* **Checks prices:** Fetches cryptocurrency prices from CoinGecko, a reference USD-to-naira exchange rate, and the relevant Quidax market ticker.
* **Compares the prices:** Converts the global USD price to an implied naira price and compares it with the Quidax price.
* **Calculates the gap:** Shows the percentage difference, which can be positive or negative.
* **Explains the result:** Gives a simple verdict to help you understand what the comparison means.
* **Saves each successful check:** Stores the result in a local SQLite database, so you can return to previous observations.
* **Shows a summary:** Calculates the average, highest, and lowest recorded premium, along with a simple overall trend.
* **Plots the history:** Displays saved observations on a line chart so you can see how the price difference changes over time.

No complicated spreadsheet calculations required. Just a clearer way to look at the numbers.

## 🌍 What problem does it solve, and what makes it different?

There are plenty of cryptocurrency price websites and apps already. I'm not trying to reinvent cryptocurrency price tracking.

I'm focusing on a more specific question:

**How does the Quidax naira market price compare with a global cryptocurrency price converted into naira, and how does that difference change over time?**

A global price alone doesn't answer that question. Neither does a single local price.

Naira Reality Check brings the two reference prices together, calculates their percentage difference, and saves the observations so they can be compared later.

The history, summary, and chart are important parts of that idea. Instead of seeing only today's result, you can begin building a picture of previous results as you continue checking the market.

This is the gap my project is designed to address. It isn't a claim that other platforms cannot do something similar.

## 📊 What does the percentage actually mean?

Let's use another simple example.

Suppose the global price, converted to naira, is ₦2,000,000.

| Quidax price | Difference | What it means                                |
| ------------ | ---------: | -------------------------------------------- |
| ₦2,100,000   |        +5% | Quidax is 5% above the global implied price. |
| ₦1,900,000   |        -5% | Quidax is 5% below the global implied price. |
| ₦2,000,000   |         0% | Both reference prices are equal.             |

A positive percentage means the Quidax price is higher. A negative percentage means it is lower.

**One important thing:** a price difference doesn't automatically mean there's an opportunity to make money. Trading fees, spreads, liquidity, transfer costs, and changing prices can all affect the actual outcome. This app is a comparison tool, not a guarantee of profit or a recommendation to trade.

## 📈 Why save previous prices?

Imagine checking a coin today and seeing a 2% difference. Tomorrow, it might be 3%. A few days later, it might be 1%.

Looking at just one result wouldn't show you those changes.

That's why I added price history.

Every successful market check is saved in a local database. The dashboard uses those saved observations to display recent checks, calculate summary statistics, and plot the premium or discount over time.

The dashboard refreshes its displayed history periodically while it's open. It also attempts a new market check every five minutes while the page is visible.

The app doesn't download a complete historical market feed, and it doesn't collect prices when the dashboard is closed. The chart shows the observations that the app has actually saved.

## 🪙 Which cryptocurrencies can I check?

The current supported coins are:

* Bitcoin (BTC)
* Ethereum (ETH)
* Tether (USDT)
* Ripple (XRP)
* Litecoin (LTC)
* Tron (TRX)
* Dash (DASH)

The app uses three external data sources:

* **CoinGecko:** for global cryptocurrency prices in USD.
* **ExchangeRate-API:** for a reference USD-to-NGN exchange rate.
* **Quidax:** for the local naira market ticker.

The results depend on those services being available and returning usable data.

## 🖥️ How do I use it?

### Option 1: Use the dashboard

Once the application is running:

1. Open the dashboard in your browser.
2. Choose a cryptocurrency from the dropdown.
3. Click **Check market**.
4. View the global price, global implied naira price, Quidax price, and percentage difference.
5. Scroll down to explore the summary, chart, and recent price history.

### Option 2: Explore the API

The project also exposes API endpoints, which means other software can request data from it.

| Endpoint                       | What it does                                                            |
| ------------------------------ | ----------------------------------------------------------------------- |
| `GET /coins`                   | Lists the supported cryptocurrencies.                                   |
| `GET /check/bitcoin`           | Fetches and compares prices for Bitcoin, then saves a successful check. |
| `GET /history/bitcoin`         | Returns saved Bitcoin price observations.                               |
| `GET /history/bitcoin?limit=5` | Returns up to five saved Bitcoin observations.                          |
| `GET /summary/bitcoin`         | Returns Bitcoin's saved statistics and simple trend.                    |
| `/docs`                        | Opens FastAPI's interactive API documentation.                          |

You can replace `bitcoin` with another supported coin.

## 🛠️ How to run it on your computer

You'll need Python and an internet connection.

### 1. Clone the repository

```bash
git clone https://github.com/nne-oma7/naira-reality-check.git
cd naira-reality-check
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database

```bash
python init_db.py
```

This creates the local SQLite database and the table used to store price observations.

### 5. Start the application

```bash
uvicorn main:app --reload
```

Open the dashboard:

http://127.0.0.1:8000/

Or explore the API:

http://127.0.0.1:8000/docs

The database is stored locally on your computer. Each person running the application creates and maintains their own local price history.

## 🧠 What I learned while building this

This project has helped me practise several parts of software engineering:

* Using Python and FastAPI to build API endpoints.
* Fetching and combining data from multiple external APIs.
* Working with JSON responses and handling errors when data isn't available.
* Calculating price differences and percentage changes.
* Using SQLAlchemy and SQLite to save and retrieve records.
* Building a dashboard with HTML, CSS, and JavaScript.
* Using Chart.js to display saved observations visually.
* Connecting the frontend to the backend and keeping the displayed information updated.
* Thinking about what happens when an API fails, a coin isn't supported, or there isn't enough saved history to calculate a trend.

I'm still learning, so this project isn't the end of the journey. It's one of the ways I'm turning what I learn into something I can actually use and improve.

## 🚧 What's next?

There are still things I'd like to explore:

* Adding automated tests.
* Improving how external API failures are handled.
* Supporting more cryptocurrencies.
* Making the historical analysis more detailed.
* Exploring more reliable ways to collect and store market observations.

For now, I'm happy that a question I was curious about has become a working project with a backend, database, API endpoints, and a dashboard.

## 🧰 Built with

* Python
* FastAPI
* Requests
* SQLAlchemy
* SQLite
* HTML
* CSS
* JavaScript
* Chart.js

---

**Built by Nneoma** — an Economics graduate learning software engineering, asking questions, building projects, and figuring things out one step at a time. 💚
