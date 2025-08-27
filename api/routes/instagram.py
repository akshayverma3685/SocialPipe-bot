from fastapi import APIRouter, Request, Query, HTTPException
from core.config import settings
from integrations.instagram import handle_webhook

router = APIRouter()

@router.get("/")
def verify(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return int(challenge)
    raise HTTPException(status_code=403, detail="verification failed")

@router.post("/")
async def ingest(req: Request):
    payload = await req.json()
    await handle_webhook(payload)
    return {"ok": True}
