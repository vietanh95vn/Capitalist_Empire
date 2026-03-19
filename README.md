# 🏛️ Capitalist Empire: Automated Asset Tracking System

> **Stop bleeding money on delayed data.** This is a proactive, zero-friction portfolio auditing system that monitors your assets 24/7, crossing all global timezones without fatigue.

## 🎯 The Solution (Giải pháp)
Traditional asset tracking requires manual logins, complex Excel sheets, and constant human monitoring. This system eliminates that friction by deploying an autonomous Watchdog and a Real-Time Dashboard. 
* **Your Keys, Your Rules:** Everything runs locally on your machine. No third-party cloud apps can access your API keys.
* **Proactive Defense:** The system doesn't just wait for commands; it actively monitors the market and triggers a Telegram siren if your assets fluctuate beyond your set threshold.

## ⚙️ Core Microservices Architecture (Kiến trúc Hệ thống)
1. **The Vault (`database.py`):** A secure, local SQLite database logging every price movement.
2. **The Watchdog (`main_bot.py`):** A multi-threaded Telegram bot that fetches live Binance API data and pushes real-time alerts.
3. **The CEO Dashboard (`wealth_web.py`):** A clean, interactive Streamlit frontend for instant visual auditing.

---

## 🚀 Quick Start Guide (Hướng dẫn Khởi động Nhanh)

### Step 1: Configuration (Cấu hình)
1. Open `config.py`.
2. Insert your Telegram Bot `TOKEN`.
3. Insert your private `CHAT_ID`.
4. Define your asset allocation in the `TREASURE` dictionary.

### Step 2: Ignite the Watchdog (Kích hoạt Chó săn)
Open your terminal and run the background bot process:
```bash
python main_bot.py