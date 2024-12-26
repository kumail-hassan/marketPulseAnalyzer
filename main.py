import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("visuals", exist_ok=True)

# Define indicator calculation functions
def calculate_sma(data, period):
    return data["Close"].rolling(window=period).mean()

def calculate_ema(data, period):
    return data["Close"].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = data["Close"].ewm(span=short_period, adjust=False).mean()
    long_ema = data["Close"].ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

def generate_signals(data):
    """Generate trading signals based on technical indicators."""
    data["Signal"] = 0
    data.loc[data["EMA_20"] > data["SMA_20"], "Signal"] = 1
    data.loc[data["EMA_20"] < data["SMA_20"], "Signal"] = -1
    macd_buy = (data["MACD"] > data["Signal_Line"]) & (data["MACD"].shift(1) <= data["Signal_Line"].shift(1))
    macd_sell = (data["MACD"] < data["Signal_Line"]) & (data["MACD"].shift(1) >= data["Signal_Line"].shift(1))
    data.loc[macd_buy, "Signal"] = 1
    data.loc[macd_sell, "Signal"] = -1
    return data

def backtest_strategy(data, initial_balance=10000):
    """Backtest the trading strategy."""
    balance = initial_balance
    position = 0
    data["Portfolio Value"] = 0

    for i in range(len(data)):
        # Extract scalar values explicitly
        signal = int(data["Signal"].iloc[i])
        price = float(data["Close"].iloc[i])

        if signal == 1 and balance > 0:
            position = balance / price
            balance = 0
        elif signal == -1 and position > 0:
            balance = position * price
            position = 0

        # Update portfolio value
        data.loc[data.index[i], "Portfolio Value"] = balance + (position * price)

    data["Cumulative Returns"] = data["Portfolio Value"] / initial_balance - 1
    return data, balance


def plot_portfolio_value(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Portfolio Value"], label="Portfolio Value")
    plt.title("Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.grid()
    plt.savefig("visuals/portfolio_value.png")
    plt.show()

def plot_signals(data):
    plt.figure(figsize=(12, 8))
    plt.plot(data.index, data["Close"], label="Closing Price", alpha=0.5)
    buy_signals = data[data["Signal"] == 1]
    sell_signals = data[data["Signal"] == -1]
    plt.scatter(buy_signals.index, buy_signals["Close"], label="Buy Signal", marker="^", color="green", alpha=1)
    plt.scatter(sell_signals.index, sell_signals["Close"], label="Sell Signal", marker="v", color="red", alpha=1)
    plt.title("Buy/Sell Signals on Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid()
    plt.savefig("visuals/buy_sell_signals.png")
    plt.show()

def plot_macd(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["MACD"], label="MACD", color="blue")
    plt.plot(data.index, data["Signal_Line"], label="Signal Line", color="orange")
    plt.bar(data.index, data["MACD_Histogram"], label="Histogram", color="gray", alpha=0.5)
    plt.title("MACD and Signal Line")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid()
    plt.savefig("visuals/macd_signal_line.png")
    plt.show()

def plot_rsi(data):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["RSI"], label="RSI", color="purple")
    plt.axhline(70, color="red", linestyle="--", label="Overbought (70)")
    plt.axhline(30, color="green", linestyle="--", label="Oversold (30)")
    plt.title("Relative Strength Index (RSI)")
    plt.xlabel("Date")
    plt.ylabel("RSI")
    plt.legend()
    plt.grid()
    plt.savefig("visuals/rsi.png")
    plt.show()

# Main script
ticker_symbol = "AAPL"
start_date = "2020-01-01"
end_date = "2023-12-31"

data = yf.download(ticker_symbol, start=start_date, end=end_date)
data.reset_index(inplace=True)
data.to_csv("data/historical_data.csv", index=False)
data = pd.read_csv("data/historical_data.csv", parse_dates=["Date"], index_col="Date")

data.dropna(inplace=True)
numeric_columns = ["Close", "High", "Low", "Open", "Volume"]
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")
data["Daily Return"] = data["Close"].pct_change()

data["SMA_20"] = calculate_sma(data, 20)
data["EMA_20"] = calculate_ema(data, 20)
data["RSI"] = calculate_rsi(data)
data["MACD"], data["Signal_Line"], data["MACD_Histogram"] = calculate_macd(data)

data = generate_signals(data)

data, final_balance = backtest_strategy(data)

data.to_csv("data/backtested_data.csv")
print(f"Backtested data saved to data/backtested_data.csv. Final balance: ${final_balance:.2f}")

plot_portfolio_value(data)
plot_signals(data)
plot_macd(data)
plot_rsi(data)
