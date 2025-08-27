import asyncio
import uvicorn
from bot.run import build_application, start_application
from api.server import app

async def main():
    tg_app = build_application()
    await tg_app.initialize()
    await tg_app.start()
    server = uvicorn.Server(uvicorn.Config(app, host="0.0.0.0", port=8000))
    await asyncio.gather(server.serve(), start_application(tg_app))

if __name__ == "__main__":
    asyncio.run(main())
