from flask import Flask, render_template, request
import yfinance as yf
from main import backtest_strategy, generate_signals, calculate_sma, calculate_ema, calculate_rsi, calculate_macd

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Render input form

@app.route("/analyze", methods=["POST"])
def analyze():
    # Get user inputs
    ticker = request.form.get("ticker").upper()
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    try:
        # Fetch data
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return render_template("error.html", message=f"No data found for {ticker} between {start_date} and {end_date}. Please try again.")

        # Process data
        data.reset_index(inplace=True)
        data["SMA_20"] = calculate_sma(data, 20)
        data["EMA_20"] = calculate_ema(data, 20)
        data["RSI"] = calculate_rsi(data)
        data["MACD"], data["Signal_Line"], data["MACD_Histogram"] = calculate_macd(data)
        data = generate_signals(data)
        data, final_balance = backtest_strategy(data)

        # Save results
        data.to_csv(f"data/{ticker}_backtested_data.csv")

        return render_template(
            "results.html",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            final_balance=f"{final_balance:,.2f}",
        )

    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
