from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from root import config

app = FastAPI(title="SocialPipe UI", version="1.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    integrations = [
        {"name": "Instagram", "status": "✅ Connected" if config.INSTAGRAM_CLIENT_ID else "❌ Not Connected"},
        {"name": "WhatsApp", "status": "✅ Connected" if config.WHATSAPP_TOKEN else "❌ Not Connected"},
        {"name": "Twitter", "status": "✅ Connected" if config.TWITTER_API_KEY else "❌ Not Connected"},
        {"name": "Snapchat", "status": "✅ Connected" if config.SNAPCHAT_API_KEY else "❌ Not Connected"},
        {"name": "Telegram", "status": "✅ Connected" if config.TELEGRAM_BOT_TOKEN else "❌ Not Connected"},
    ]
    return templates.TemplateResponse("dashboard.html", {"request": request, "integrations": integrations})


@app.get("/settings", response_class=HTMLResponse)
async def settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})


@app.post("/settings/save")
async def save_settings(
    request: Request,
    telegram_token: str = Form(...),
    owner_id: str = Form(...)
):
    print(f"New Telegram Token: {telegram_token}")
    print(f"Owner ID: {owner_id}")

    return RedirectResponse(url="/settings", status_code=303)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "SocialPipe UI"}
