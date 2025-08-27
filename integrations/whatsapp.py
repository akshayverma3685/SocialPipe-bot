import httpx
from core.config import settings
from services.categorizer import categorize
from services.notifier import notify_owner
from core.database import SessionLocal, Message
from core.logger import log

API = "https://graph.facebook.com/v19.0"

def _normalize(value) -> list[dict]:
    events = []
    for m in value.get("messages", []) or []:
        frm = m.get("from","")
        text = (m.get("text") or {}).get("body","")
        thread_key = f"wa:{frm}"
        events.append({
            "platform":"whatsapp",
            "text": f"💬 WA • {frm}: {text}",
            "thread_key": thread_key,
            "reply_target": f"wa:chat:{frm}",
            "raw": m
        })
    return events

async def handle_webhook(payload: dict):
    total = 0
    with SessionLocal() as s:
        for entry in payload.get("entry", []):
            for change in entry.get("changes", []):
                for ev in _normalize(change.get("value", {})):
                    cat = categorize("whatsapp", ev["raw"])
                    s.add(Message(platform="whatsapp", category=cat, thread_key=ev["thread_key"], payload=ev))
                    total += 1
        s.commit()
    await notify_owner(f"✅ WhatsApp: {total} new message(s).")

async def wa_send_text(to_number: str, text: str) -> bool:
    url = f"{API}/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"}
    payload = {"messaging_product":"whatsapp","to": to_number,"type":"text","text":{"body": text}}
    async with httpx.AsyncClient() as c:
        r = await c.post(url, headers=headers, json=payload, timeout=20)
        log.info(f"WA send status {r.status_code}: {r.text[:200]}")
        return r.status_code in (200,201)
