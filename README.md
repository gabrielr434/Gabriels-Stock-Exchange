<div align="center">

# 📈 Gabriel's Stock Exchange

### A full-stack simulated trading platform — register, trade, track.

[![Live Demo](https://img.shields.io/badge/demo-live-00c087?style=for-the-badge)](https://gabriels-stock-exchange.onrender.com)
[![Python](https://img.shields.io/badge/python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/sqlite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

**[🔗 Live Demo](https://gabriels-stock-exchange.onrender.com)** &nbsp;•&nbsp; **[📂 Source](https://github.com/gabrielr434/Gabriels-Stock-Exchange)**

</div>

---

## 🖤 Overview

Gabriel's Stock Exchange is a full-stack web app for managing a simulated stock portfolio. Register an account, look up real-time stock quotes, buy and sell shares with virtual cash, and track your complete transaction history — all wrapped in a sleek, dark "trading terminal" interface inspired by real crypto/stock exchanges.

<br>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🔐 Accounts
- Secure registration with hashed passwords
- Session-based login/logout
- Change password from within the app

</td>
<td width="50%" valign="top">

### 💹 Trading
- Real-time stock quote lookups
- Buy shares with live-validated cash balance
- Sell shares with live-validated holdings

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📊 Portfolio
- Live holdings table with current value
- Real-time grand total (cash + holdings)
- Full historical transaction log (buy/sell)

</td>
<td width="50%" valign="top">

### 🌐 Markets
- Grid overview of popular tickers
- Session-tracked price movement indicators
- One-click access into the trade flow

</td>
</tr>
</table>

<br>

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, Flask |
| **Database** | SQLite |
| **Auth** | Werkzeug password hashing, Flask-Session |
| **Frontend** | Jinja2, Bootstrap 5, custom CSS |
| **Deployment** | Render (Gunicorn WSGI) |

<br>

## 🚀 Getting Started Locally

```bash
# Clone the repo
git clone https://github.com/gabrielr434/Gabriels-Stock-Exchange.git
cd Gabriels-Stock-Exchange

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run
```

Visit `http://127.0.0.1:5000` in your browser.

<br>

## 📁 Project Structure

```
Gabriels-Stock-Exchange/
├── app.py                  # Flask routes & application logic
├── helpers.py               # Auth decorator, apology handler, stock lookup
├── requirements.txt          # Python dependencies
├── Procfile                  # Render/Gunicorn start command
├── finance.db                 # SQLite database
├── static/
│   ├── styles.css              # Custom "terminal" theme
│   └── favicon.ico
└── templates/
    ├── layout.html               # Base template + navbar
    ├── login.html / register.html
    ├── quote.html / quoted.html
    ├── buy.html / sell.html
    ├── index.html                 # Portfolio dashboard
    ├── history.html                # Transaction history
    ├── market.html                  # Markets overview
    └── change_password.html
```

<br>

## 🗺️ Route Map

| Route | Method | Description |
|---|---|---|
| `/register` | GET, POST | Create a new account |
| `/login` | GET, POST | Authenticate a user |
| `/logout` | GET | End the session |
| `/` | GET | Portfolio dashboard |
| `/quote` | GET, POST | Look up a stock's current price |
| `/buy` | GET, POST | Purchase shares |
| `/sell` | GET, POST | Sell owned shares |
| `/history` | GET | View all past transactions |
| `/market` | GET | Browse popular tickers |
| `/change_password` | GET, POST | Update account password |

<br>

## 🎨 Design

Built around a dark "trading terminal" aesthetic — deep navy backgrounds, cyan/blue accent gradients, and color-coded buy/sell states — meant to evoke the feel of a modern crypto exchange dashboard rather than a typical CRUD app.

<br>

<div align="center">

**Built by Gabriel** · Powered by Flask & a lot of debugging 🐛

</div>
