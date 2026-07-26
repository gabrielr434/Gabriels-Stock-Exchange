import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///finance.db")

COMPANIES = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NFLX", "NVDA", "META", "AMD", "INTC", "ORCL", "IBM"]


@app.route("/market")
@login_required
def market():
    quotes = []
    for symbol in COMPANIES:
        stock = lookup(symbol)
        if stock is None:
            continue
        prev_key = f"prev_price_{symbol}"
        prev_price = session.get(prev_key)
        change = None
        if prev_price is not None:
            change = stock["price"] - prev_price
        session[prev_key] = stock["price"]
        quotes.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "price": stock["price"],
            "change": change
        })
    return render_template("market.html", quotes=quotes)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = user[0]["cash"]
    holdings = db.execute(
        """
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """,
        user_id,
    )
    portfolio = []
    grand_total = cash
    for holding in holdings:
        stock = lookup(holding["symbol"])
        if stock is None:
            continue
        total_value = stock["price"] * holding["total_shares"]
        grand_total += total_value
        portfolio.append({
            "symbol": holding["symbol"],
            "name": stock["name"],
            "shares": holding["total_shares"],
            "price": stock["price"],
            "total": total_value
        })
    return render_template("index.html", portfolio=portfolio, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must provide symbol", 400)
        stock = lookup(symbol)
        if stock is None:
            return apology("symbol does not exist", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer", 400)
        shares = int(shares)
        total_cost = stock["price"] * shares
        user_id = session["user_id"]
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        if user_cash < total_cost:
            return apology("can't afford number of shares", 400)
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'BUY')",
            user_id, stock["symbol"], shares, stock["price"]
        )
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        flash(f"Bought {shares} share(s) of {stock['symbol']}!")
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    transactions = db.execute(
        "SELECT symbol, shares, price, type, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp DESC",
        user_id
    )
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)
        return render_template("quoted.html", quote=stock)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return apology("must provide username", 400)
        elif not password or not confirmation:
            return apology("must provide password and confirmation", 400)
        elif password != confirmation:
            return apology("passwords do not match", 400)
        hash_password = generate_password_hash(password)
        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)
        except ValueError:
            return apology("username already exists", 400)
        session["user_id"] = user_id
        flash("Registered successfully!")
        return redirect("/")
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    holdings = db.execute(
        """
        SELECT symbol, SUM(shares) as total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING total_shares > 0
    """,
        user_id,
    )
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("must select a stock", 400)
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("shares must be a positive integer", 400)
        shares = int(shares)
        user_shares = 0
        for holding in holdings:
            if holding["symbol"] == symbol:
                user_shares = holding["total_shares"]
                break
        if shares > user_shares:
            return apology("not enough shares owned", 400)
        stock = lookup(symbol)
        if stock is None:
            return apology("symbol error", 400)
        total_sale = stock["price"] * shares
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'SELL')",
            user_id, stock["symbol"], -shares, stock["price"]
        )
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_sale, user_id)
        flash(f"Sold {shares} share(s) of {symbol}!")
        return redirect("/")
    return render_template("sell.html", holdings=holdings)


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")
        if not current_password or not new_password or not confirmation:
            return apology("all fields are required", 400)
        if new_password != confirmation:
            return apology("new passwords do not match", 400)
        user_id = session["user_id"]
        user = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not check_password_hash(user[0]["hash"], current_password):
            return apology("incorrect current password", 400)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), user_id)
        flash("Password updated successfully!")
        return redirect("/")
    return render_template("change_password.html")
