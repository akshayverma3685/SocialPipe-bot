from fastapi import APIRouter, Request
from integrations.twitter import handle_webhook

router = APIRouter()

@router.post("/")
async def ingest(req: Request):
    payload = await req.json()
    await handle_webhook(payload)
    return {"ok": True}
