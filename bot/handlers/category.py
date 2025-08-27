from telegram import Update
from telegram.ext import ContextTypes

CATS = ["dm","mentions","comments","activity","general"]

async def categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📂 Categories:\n" + "\n".join(f"• {c}" for c in CATS)
    await update.message.reply_text(text)
