import yfinance as yf
import pandas as pd

# Test script
print("Environment is set up and ready to go!")

# Test libraries
print("Testing libraries...")
print("Pandas version:", pd.__version__)
ticker = yf.Ticker("AAPL")  # Fetch data for Apple Inc.
print("Yahoo Finance API is accessible:", ticker.info["symbol"])
