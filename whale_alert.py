import websocket
import json
import requests
import logging
import time
import os
from dotenv import load_dotenv

# 🔹 Load environment variables
load_dotenv()

# 🔹 Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Load credentials from environment variables
ALCHEMY_URL = os.getenv('ALCHEMY_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Validate environment variables
if not all([ALCHEMY_URL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    logging.error("❌ Missing required environment variables. Please check your .env file.")
    exit(1)

# 🔹 List of TOP 10 ERC-20 Tokens on Ethereum
TOP_ERC20_TOKENS = {
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "WBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "LINK": "0x514910771af9ca656af840dff83e8264ecf986ca",
    "UNI": "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984",
    "MATIC": "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0",
    "SHIB": "0x95ad61b0a150d79219dcf64e1e6cc01f0b64c4ce",
    "LDO": "0x5a98fcbea516cf06857215779fd812ca3bef1b32",
    "AAVE": "0x7fc66500c84a76ad7e9c93437bfc5ac33e2ddae9"
}

# 🔹 Function to get real-time ETH/USD price from CoinGecko
def get_eth_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        return response["ethereum"]["usd"] if "ethereum" in response and "usd" in response["ethereum"] else None
    except Exception as e:
        logging.error(f"❌ Error fetching ETH price: {e}")
        return None

# 🔹 Function to send a Telegram alert
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logging.info("✅ Telegram message sent successfully!")
        else:
            logging.error(f"❌ Failed to send Telegram message: {response.text}")
    except Exception as e:
        logging.error(f"❌ Error sending Telegram alert: {e}")

# 🔹 Send test message when script starts
def send_startup_message():
    message = "🚀 Whale Bot Started! Monitoring large ETH and ERC-20 transactions..."
    send_telegram_alert(message)

# 🔹 WebSocket event handlers
def on_open(ws):
    logging.info("🔗 WebSocket connection opened. Subscribing to transactions...")

    # 🔹 Alchemy WebSocket Subscription
    subscription_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_subscribe",
        "params": ["alchemy_minedTransactions"]
    }

    ws.send(json.dumps(subscription_msg))
    logging.info("📡 Subscription request sent!")

def on_message(ws, message):
    logging.info(f"📩 Raw message received: {message}")
    data = json.loads(message)

    if "params" in data and "result" in data["params"]:
        tx = data["params"]["result"]["transaction"]
        logging.info(f"🔍 Processing transaction: {tx}")

        tx_hash = tx.get("hash")
        from_address = tx.get("from", "Unknown")
        to_address = tx.get("to", "Unknown")
        value_hex = tx.get("value", "0x0")
        input_data = tx.get("input", "")

        # Convert ETH value from Wei to ETH
        try:
            eth_amount = int(value_hex, 16) / 10**18
        except ValueError as e:
            logging.error(f"❌ Error converting ETH value: {e}")
            return

        # 🔹 Check if it's an ETH transaction over 50 ETH
        if eth_amount >= 50:
            eth_price = get_eth_price()
            if eth_price:
                usd_value = eth_amount * eth_price
                alert_message = f"""
🚨 *Whale Alert* 🚨
💰 *{eth_amount:.2f} ETH* (${usd_value:,.2f})
📉 1 ETH = ${eth_price:,.2f}
🔄 From: [{from_address[:6]}...{from_address[-4:]}](https://etherscan.io/address/{from_address})
➡️ To: [{to_address[:6]}...{to_address[-4:]}](https://etherscan.io/address/{to_address})
🔗 [View Transaction](https://etherscan.io/tx/{tx_hash})
                """
                send_telegram_alert(alert_message)

        # 🔹 Check if it's a top ERC-20 token transfer
        for token_symbol, contract_address in TOP_ERC20_TOKENS.items():
            if to_address.lower() == contract_address.lower():
                # ERC-20 transfers follow this input pattern: "0xa9059cbb" + (recipient + amount)
                if input_data.startswith("0xa9059cbb"):
                    recipient = "0x" + input_data[34:74]  # Extract recipient address
                    token_amount_hex = input_data[74:138]  # Extract token amount

                    try:
                        token_amount = int(token_amount_hex, 16) / 10**18  # Convert token value
                    except ValueError:
                        token_amount = 0

                    # 🔹 Only alert for large ERC-20 transactions
                    if token_amount >= 10000:
                        alert_message = f"""
🚨 *Whale Alert* 🚨
💰 *{token_amount:,.0f} {token_symbol}* transferred!
🔄 From: [{from_address[:6]}...{from_address[-4:]}](https://etherscan.io/address/{from_address})
➡️ To: [{recipient[:6]}...{recipient[-4:]}](https://etherscan.io/address/{recipient})
🔗 [View Transaction](https://etherscan.io/tx/{tx_hash})
                        """
                        send_telegram_alert(alert_message)

def on_error(ws, error):
    logging.error(f"🚨 WebSocket Error: {error}")

def on_close(ws, close_status, close_msg):
    logging.warning(f"🔴 WebSocket closed: {close_status} - {close_msg}")

# 🔹 WebSocket start function
def start_websocket():
    ws = websocket.WebSocketApp(
        ALCHEMY_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    logging.info("🔗 Connecting to Alchemy WebSocket...")
    ws.run_forever()

# 🔹 Run the bot
if __name__ == "__main__":
    send_startup_message()  # Send a startup message to Telegram
    start_websocket()