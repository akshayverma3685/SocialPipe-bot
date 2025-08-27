import httpx
from core.config import settings
from services.categorizer import categorize
from core.logger import log
from services.notifier import notify_owner
from core.database import SessionLocal, Message

GRAPH = "https://graph.facebook.com/v19.0"

def _normalize(entry) -> list[dict]:
    events = []
    for ch in entry.get("changes", []):
        v = ch.get("value", {})
        text = v.get("text") or v.get("message") or str(v)
        username = v.get("username") or "unknown"
        comment_id = v.get("comment_id") or v.get("id") or ""
        thread_key = f"ig:{comment_id or entry.get('id')}"
        events.append({
            "platform": "instagram",
            "text": f"📸 IG • @{username}: {text}",
            "thread_key": thread_key,
            "reply_target": f"ig:comment:{comment_id}" if comment_id else "",
            "raw": v
        })
    return events

async def handle_webhook(payload: dict):
    total = 0
    with SessionLocal() as s:
        for entry in payload.get("entry", []):
            for ev in _normalize(entry):
                cat = categorize("instagram", ev["raw"])
                s.add(Message(platform="instagram", category=cat, thread_key=ev["thread_key"], payload=ev))
                total += 1
        s.commit()
    await notify_owner(f"✅ Instagram: {total} new event(s) received.")

async def ig_reply_comment(comment_id: str, message: str) -> bool:
    if not (settings.FB_PAGE_LONG_LIVED_TOKEN and comment_id):
        return False
    url = f"{GRAPH}/{comment_id}/replies"
    params = {"message": message, "access_token": settings.FB_PAGE_LONG_LIVED_TOKEN}
    async with httpx.AsyncClient() as c:
        r = await c.post(url, params=params, timeout=20)
        log.info(f"IG reply status {r.status_code}: {r.text[:200]}")
        return r.status_code in (200,201)
