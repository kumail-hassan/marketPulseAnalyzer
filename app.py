import yfinance as yf
from flask import Flask, render_template, request
import pandas as pd
from main import backtest_strategy, generate_signals, calculate_sma, calculate_ema, calculate_rsi, calculate_macd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    ticker = request.form.get("ticker")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    # Fetch and process data
    data = yf.download(ticker, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    data["SMA_20"] = calculate_sma(data, 20)
    data["EMA_20"] = calculate_ema(data, 20)
    data["RSI"] = calculate_rsi(data)
    data["MACD"], data["Signal_Line"], data["MACD_Histogram"] = calculate_macd(data)
    data = generate_signals(data)
    data, final_balance = backtest_strategy(data)

    # Save results for visualization
    data.to_csv("data/backtested_data.csv")

    return render_template("results.html", ticker=ticker, final_balance=f"{final_balance:,.2f}")

if __name__ == "__main__":
    app.run(debug=True)
