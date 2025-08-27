from services.notifier import send_text

async def send_to(chat_id: int, text: str):
    await send_text(chat_id, text)
