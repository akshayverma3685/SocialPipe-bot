import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from core.config import settings
from core.logger import log
from bot.handlers.start import start
from bot.handlers.category import categories
from bot.handlers.reply import reply_cmd

def build_application() -> Application:
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("categories", categories))
    app.add_handler(CommandHandler("reply", reply_cmd))
    app.add_handler(CallbackQueryHandler(lambda u, c: c.bot.send_message(chat_id=u.effective_chat.id, text="📂 DMs, Mentions, Comments, Activity"), pattern="^show_categories$"))
    app.add_handler(CallbackQueryHandler(lambda u, c: c.bot.send_message(chat_id=u.effective_chat.id, text="Use /reply target | message"), pattern="^help$"))
    return app

async def start_application(app: Application):
    await app.start()
    log.info("🤖 Telegram bot started (worker).")
    await app.updater.start_polling()  # for PTB v20 compatibility
    await asyncio.Event().wait()

if __name__ == "__main__":
    application = build_application()
    asyncio.run(start_application(application))
