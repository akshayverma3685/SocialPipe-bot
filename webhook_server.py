import json
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from core.config import settings
from core.logger import log
from core.database import init_db, SessionLocal, Message
from integrations import instagram as ig_integ, whatsapp as wa_integ, twitter as tw_integ, snapchat as sc_integ
from services.categorizer import categorize
from services.notifier import notify_owner
from utils import safe_run_async

app = FastAPI(title="SocialPipe - Webhook Server")

@app.on_event("startup")
async def _startup():
    try:
        init_db()
        log.info("Database initialized.")
    except Exception as e:
        log.exception("DB init failed: %s", e)

@app.get("/", response_class=PlainTextResponse)
def root():
    return "SocialPipe webhook server OK"

@app.get("/verify", response_class=PlainTextResponse)
def verify(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="verification failed")

@app.get("/webhook/instagram", response_class=PlainTextResponse)
def instagram_verify(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="verification failed")

@app.post("/webhook/instagram")
async def instagram_webhook(req: Request):
    payload = await req.json()
    log.info("Received Instagram webhook.")
    await safe_run_async(ig_integ.handle_webhook, payload)
    try:
        with SessionLocal() as s:
            for entry in payload.get("entry", []):
                s.add(Message(platform="instagram", category=categorize("instagram", entry), thread_key=str(entry.get("id")), payload=entry))
            s.commit()
    except Exception:
        log.exception("Failed to save IG events")
    return JSONResponse({"ok": True})

@app.get("/webhook/whatsapp", response_class=PlainTextResponse)
def whatsapp_verify(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    raise HTTPException(status_code=403, detail="verification failed")

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(req: Request):
    payload = await req.json()
    log.info("Received WhatsApp webhook.")
    await safe_run_async(wa_integ.handle_webhook, payload)
    try:
        with SessionLocal() as s:
            for entry in payload.get("entry", []):
                for change in entry.get("changes", []):
                    s.add(Message(platform="whatsapp", category=categorize("whatsapp", change.get("value")), thread_key=str(change.get("value").get("messages", [{}])[0].get("from","")), payload=change.get("value")))
            s.commit()
    except Exception:
        log.exception("Failed to save WA events")
    return JSONResponse({"ok": True})

@app.post("/webhook/twitter")
async def twitter_webhook(req: Request):
    payload = await req.json()
    log.info("Received Twitter webhook.")
    await safe_run_async(tw_integ.handle_webhook, payload)
    try:
        with SessionLocal() as s:
            s.add(Message(platform="twitter", category=categorize("twitter", payload), thread_key=str(payload.get("data",{}).get("id","")), payload=payload))
            s.commit()
    except Exception:
        log.exception("Failed to save Twitter events")
    return JSONResponse({"ok": True})

@app.post("/webhook/snapchat")
async def snapchat_webhook(req: Request):
    payload = await req.json()
    log.info("Received Snapchat webhook.")
    await safe_run_async(sc_integ.handle_webhook, payload)
    try:
        with SessionLocal() as s:
            s.add(Message(platform="snapchat", category="general", thread_key=str(payload.get("id","")), payload=payload))
            s.commit()
    except Exception:
        log.exception("Failed to save Snapchat events")
    return JSONResponse({"ok": True})

@app.post("/webhook/telegram")
async def telegram_webhook(req: Request):
    payload = await req.json()
    text = f"📨 Telegram update received: {json.dumps(payload)[:1000]}"
    await safe_run_async(notify_owner, text)
    return JSONResponse({"ok": True})
