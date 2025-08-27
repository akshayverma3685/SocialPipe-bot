import asyncio
from core.logger import log

class Scheduler:
    def __init__(self):
        self._tasks = []

    def every(self, seconds, coro, *args, **kwargs):
        async def runner():
            while True:
                try:
                    await coro(*args, **kwargs)
                except Exception as e:
                    log.error(f"Scheduler task error: {e}")
                await asyncio.sleep(seconds)
        self._tasks.append(asyncio.create_task(runner()))

    async def stop(self):
        for t in self._tasks:
            t.cancel()

scheduler = Scheduler()
