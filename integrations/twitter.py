import httpx
from core.config import settings
from services.categorizer import categorize
from services.notifier import notify_owner
from core.database import SessionLocal, Message
from core.logger import log

def _normalize(payload) -> list[dict]:
    data = payload.get("data") or payload
    if not data:
        return []
    text = data.get("text","")
    tid = data.get("id","")
    author = data.get("author_id","unknown")
    thread_key = f"x:{tid}"
    return [{
        "platform": "twitter",
        "text": f"🐦 X • {author}: {text}",
        "thread_key": thread_key,
        "reply_target": f"tw:tweet:{tid}",
        "raw": data
    }]

async def handle_webhook(payload: dict):
    events = _normalize(payload)
    with SessionLocal() as s:
        for ev in events:
            cat = categorize("twitter", ev["raw"])
            s.add(Message(platform="twitter", category=cat, thread_key=ev["thread_key"], payload=ev))
        s.commit()
    await notify_owner(f"✅ Twitter: {len(events)} event(s).")

async def tw_reply(tweet_id: str, text: str) -> bool:
    url = "https://api.twitter.com/2/tweets"
    headers = {"Authorization": f"Bearer {settings.TWITTER_BEARER}"}
    payload = {"text": text, "reply": {"in_reply_to_tweet_id": tweet_id}}
    async with httpx.AsyncClient() as c:
        r = await c.post(url, headers=headers, json=payload, timeout=20)
        log.info(f"X reply status {r.status_code}: {r.text[:200]}")
        return r.status_code in (200,201)
