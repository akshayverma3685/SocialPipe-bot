from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.menu import main_menu_kb

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SocialPipe!\nUse the menu to link accounts, view categories, or reply.",
        reply_markup=main_menu_kb()
    )
