def calculate_zone(price, signal_type):
    if signal_type == "BUY":
        entry = round(price,2)
        sl = round(price - 5,2)
        tp = round(price + 25,2)
    else:
        entry = round(price,2)
        sl = round(price + 5,2)
        tp = round(price - 25,2)
    return entry, sl, tp
