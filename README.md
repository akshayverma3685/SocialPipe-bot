<h1 align="center">🌍 SocialPipe Bot</h1>

<p align="center">
  <b>A multi-social hub bot that connects all your social media accounts (Instagram, WhatsApp, Twitter, Snapchat, etc.) into Telegram.
You will receive all notifications, DMs, and updates directly in Telegram, organized by category.
You can also reply from Telegram itself 💬</b>
</p>

---

## ✨ Features
- 📩 Get **all social media notifications** in Telegram  
- 🗂 Category-wise organization (Instagram / WhatsApp / Twitter / etc.)  
- 💬 Reply directly from Telegram  
- 🌐 Webhook based integration for real-time updates  
- 🛡 Secure token & DB-based storage  
- 🚀 Deployable on **Railway / Render / VPS**  

---

## 🛠 Installation Guide

### 1️⃣ Clone the repository
```bash
git clone https://github.com/akshayverma3685/SocialPipe-bot.git
cd SocialPipe-bot

2️⃣ Create & activate virtual environment

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Setup .env

Copy the example file and fill with your values:

cp .env.example .env

Required keys in .env:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OWNER_TELEGRAM_ID=123456789
DOMAIN=https://yourdomain.com
WEBHOOK_VERIFY_TOKEN=verify123

INSTAGRAM_CLIENT_ID=xxx
INSTAGRAM_CLIENT_SECRET=xxx
INSTAGRAM_REDIRECT_URI=https://yourdomain.com/webhook/instagram

WHATSAPP_TOKEN=xxx
WHATSAPP_PHONE_NUMBER_ID=xxx
WHATSAPP_BUSINESS_ACCOUNT_ID=xxx

TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_BEARER=xxx

DATABASE_URL=sqlite:///./socialpipe.db


---

▶️ Running Locally

Start the FastAPI server:

uvicorn root.webhook_server:app --host 0.0.0.0 --port 8000 --reload


---

🚀 Deployment (Railway / Render)

Railway

1. Fork this repo


2. Connect to Railway


3. Add environment variables from .env


4. Railway will auto-detect Procfile and deploy



Render

1. Create new Web Service


2. Connect GitHub repo


3. Set Start Command:



uvicorn root.webhook_server:app --host 0.0.0.0 --port $PORT


---

📡 Webhook Setup

Set your bot’s webhook URL:

https://yourdomain.com/webhook/instagram
https://yourdomain.com/webhook/whatsapp
https://yourdomain.com/webhook/twitter
https://yourdomain.com/webhook/snapchat
https://yourdomain.com/webhook/telegram


---

📊 Database

Uses SQLite by default.
For production, set:

DATABASE_URL=postgresql://user:pass@host:port/dbname


---

📜 License

MIT License © 2025 akshayverma3685


---

💡 Future Improvements

✅ Dashboard to manage connections

✅ OAuth login flow for Instagram / Twitter

✅ Reply to all platforms directly from Telegram
