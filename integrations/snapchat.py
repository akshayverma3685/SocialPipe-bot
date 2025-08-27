from services.notifier import notify_owner

async def handle_webhook(payload: dict):
    await notify_owner("👻 Snapchat event received.")
