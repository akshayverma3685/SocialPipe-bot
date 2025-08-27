from telegram import Bot
from core.config import settings
from core.logger import log

_bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def send_text(chat_id: int, text: str):
    try:
        await _bot.send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)
    except Exception as e:
        log.error(f"Telegram send error: {e}")

async def notify_owner(text: str):
    if settings.OWNER_TELEGRAM_ID:
        await send_text(settings.OWNER_TELEGRAM_ID, text)
