import requests
from zone_calculator import calculate_zone
from datetime import datetime

def fetch_xauusd_ohlcv(interval="15m", limit=50):
    url = f"https://api.binance.com/api/v3/klines?symbol=XAUUSDT&interval={interval}&limit={limit}"
    data = requests.get(url, timeout=5).json()
    candles = []
    for d in data:
        candles.append({
            "open": float(d[1]),
            "high": float(d[2]),
            "low": float(d[3]),
            "close": float(d[4]),
            "time": datetime.fromtimestamp(d[0]/1000)
        })
    return candles

def detect_high_probability_zone(candles):
    last = candles[-1]
    prev = candles[-2]
    if last['close'] > last['open'] and prev['close'] < prev['open']:
        signal_type = "BUY"
    elif last['close'] < last['open'] and prev['close'] > prev['open']:
        signal_type = "SELL"
    else:
        signal_type = None
    if signal_type:
        entry, sl, tp = calculate_zone(last['close'], signal_type)
        return {
            "symbol": "XAUUSD",
            "type": signal_type,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "technique": "Engulfing/RBR/SBR/SBS/DBD/OrderBlock/Breakout"
        }
    return None

def get_trade_signal():
    for interval in ["5m","15m","30m"]:
        candles = fetch_xauusd_ohlcv(interval)
        signal = detect_high_probability_zone(candles)
        if signal:
            return signal
    return {"symbol":"XAUUSD","type":"WAIT","entry":"-","sl":"-","tp":"-","technique":"No clear setup"}
