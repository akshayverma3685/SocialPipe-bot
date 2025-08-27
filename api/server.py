from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import PlainTextResponse
from core.database import init_db
from core.config import settings
from api.routes.instagram import router as instagram_router
from api.routes.whatsapp import router as whatsapp_router
from api.routes.twitter import router as twitter_router
from api.routes.snapchat import router as snapchat_router

app = FastAPI(title="SocialPipe API")

@app.on_event("startup")
def on_start():
    init_db()

@app.get("/", response_class=PlainTextResponse)
def health():
    return "SocialPipe running."

app.include_router(instagram_router, prefix="/webhooks/instagram", tags=["instagram"])
app.include_router(whatsapp_router, prefix="/webhooks/whatsapp", tags=["whatsapp"])
app.include_router(twitter_router, prefix="/webhooks/twitter", tags=["twitter"])
app.include_router(snapchat_router, prefix="/webhooks/snapchat", tags=["snapchat"])

@app.get("/verify", response_class=PlainTextResponse)
def verify(
    mode: str = Query(None, alias="hub.mode"),
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if mode == "subscribe" and token == settings.WEBHOOK_VERIFY_TOKEN:
        return challenge
    raise HTTPException(status_code=403, detail="verification failed")
