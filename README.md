# 🐋 Ethereum Whale Alert Bot

A real-time monitoring bot that tracks large Ethereum and ERC-20 token transactions on the Ethereum mainnet and sends alerts to a Telegram channel.

## 🚀 Features

- Real-time monitoring of Ethereum transactions
- Tracks large ETH transfers (50+ ETH)
- Monitors top 10 ERC-20 token transfers
- Real-time ETH/USD price updates
- Instant Telegram notifications
- Customizable alert thresholds

## 📋 Prerequisites

- Python 3.8+
- Alchemy API key ([Get one here](https://www.alchemy.com/))
- Telegram Bot Token ([Create one here](https://core.telegram.org/bots#how-do-i-create-a-bot))
- Telegram Channel or Group ID

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/NandakishoreN09/Whale-Alert-Bot.git
cd Whale-Alert-Bot
```

2. Create and activate a virtual environment:
```bash
python -m venv whale_bot_env
source whale_bot_env/bin/activate  # On Windows use: whale_bot_env\Scripts\activate
```

3. Install required packages:
```bash
pip install websocket-client requests python-dotenv
```

4. Create a `.env` file in the project root and add your credentials:
```env
ALCHEMY_URL=wss://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_API_KEY
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=@YourChannelName
```

## 🎯 Tracked ERC-20 Tokens

The bot currently tracks these top ERC-20 tokens:
- USDT (Tether)
- USDC (USD Coin)
- WBTC (Wrapped Bitcoin)
- DAI (Dai Stablecoin)
- LINK (Chainlink)
- UNI (Uniswap)
- MATIC (Polygon)
- SHIB (Shiba Inu)
- LDO (Lido DAO)
- AAVE (Aave)

## 🚀 Usage

1. Make sure you're in your virtual environment:
```bash
source whale_bot_env/bin/activate  # On Windows use: whale_bot_env\Scripts\activate
```

2. Run the bot:
```bash
python whale_alert.py
```

## ⚙️ Configuration

- ETH Transfer Threshold: 50 ETH (configurable in `on_message` function)
- ERC-20 Transfer Threshold: 10,000 tokens (configurable in `on_message` function)
- Telegram Message Format: Customizable in the alert message templates

## 📱 Sample Alert Format

```
🚨 Whale Alert 🚨
💰 1,000.00 ETH ($2,000,000.00)
📉 1 ETH = $2,000.00
🔄 From: 0x1234...5678
➡️ To: 0x8765...4321
🔗 View Transaction
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/NandakishoreN09/Whale-Alert-Bot/issues).




