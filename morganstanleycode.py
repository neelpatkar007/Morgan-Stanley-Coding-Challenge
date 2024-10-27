import json
import requests
import time
import threading
from datetime import datetime, timedelta

URL = "http://fx-trading-game-leicester-challenge.westeurope.azurecontainer.io:443/"
TRADER_ID = "Z88BCsDeSULzDFS04P9isfOnOSn3cqzo"

class Side:
    BUY = "buy"
    SELL = "sell"

stop_trading = False
current_price = 1.0

def get_price():
    global current_price
    now = datetime.now()
    market_open = now.replace(hour=16, minute=30, second=0, microsecond=0)
    price_change_time_up = now.replace(hour=16, minute=50, second=0, microsecond=0)
    price_change_time_down = now.replace(hour=17, minute=10, second=0, microsecond=0)
    market_close = now.replace(hour=17, minute=30, second=0, microsecond=0)

    if market_open <= now < price_change_time_up:
        return current_price
    elif now >= price_change_time_up and now < price_change_time_down:
        current_price *= 1.40
        return current_price
    elif now >= price_change_time_down and now < market_close:
        current_price *= 0.70
        return current_price
    elif now >= market_close:
        return None
    return current_price

def moving_average(prices, window_size=5):
    if len(prices) < window_size:
        return sum(prices) / len(prices)
    return sum(prices[-window_size:]) / window_size

def detect_crash_bounce(price, avg_price, take_profit=0.005, stop_loss=0.005):
    if price > avg_price * (1 + take_profit):
        return "crash"
    elif price < avg_price * (1 - stop_loss):
        return "bounce"
    return None

def trade(trader_id, qty, side):
    api_url = URL + "/trade/EURGBP"
    data = {"trader_id": trader_id, "quantity": qty, "side": side}
    res = requests.post(api_url, json=data)

    if res.status_code == 200:
        resp_json = json.loads(res.content.decode('utf-8'))
        if resp_json["success"]:
            return resp_json["price"]
        else:
            print(f"Trade failed: {resp_json.get('message', 'No message')}")
    else:
        print(f"Failed to execute trade: {res.status_code}, Response: {res.content.decode('utf-8')}")
    return None

def trade_strategy(prices, trader_id, take_profit=0.005, stop_loss=0.005):
    if len(prices) < 2:
        print("Not enough price data to execute trading strategy.")
        return None

    current_price = prices[-1]
    avg_price = moving_average(prices)
    event = detect_crash_bounce(current_price, avg_price, take_profit, stop_loss)

    if event == "crash":
        print("Crash detected! Selling GBP for EUR.")
        return trade(trader_id, 100, Side.SELL)
    elif event == "bounce":
        print("Bounce detected! Buying GBP back.")
        return trade(trader_id, 100, Side.BUY)
    else:
        if current_price > prices[-2]:
            print("Momentum detected: Price increased. Selling GBP.")
            return trade(trader_id, 10000, Side.SELL)
        elif current_price < prices[-2]:
            print("Momentum detected: Price decreased. Buying GBP.")
            return trade(trader_id, 10000, Side.BUY)
        else:
            print("No significant event detected.")
    return None

def trading_loop():
    global stop_trading
    prices = []

    while not stop_trading:
        current_price = get_price()

        if current_price is not None:
            prices.append(current_price)

            if len(prices) > 10:
                prices.pop(0)

            print("Expected to trade at: " + str(current_price))
            traded_price = trade_strategy(prices, TRADER_ID, take_profit=0.005, stop_loss=0.005)
            print("Effectively traded at: " + str(traded_price))
        else:
            print("Market is closed. Waiting for market open.")

        time.sleep(5)

def listen_for_stop():
    global stop_trading

    while True:
        user_input = input()
        if user_input.strip().lower() == 'stop':
            print("Stopping trading loop...")
            stop_trading = True
            break

if __name__ == '__main__':
    trading_thread = threading.Thread(target=trading_loop)
    trading_thread.start()
    listen_for_stop()
    trading_thread.join()
    print("Trading stopped.")