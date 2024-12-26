def calculate_sma(data, period):
    return data["Close"].rolling(window=period).mean()

def calculate_ema(data, period):
    return data["Close"].ewm(span=period, adjust=False).mean()