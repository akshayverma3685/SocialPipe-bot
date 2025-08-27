import logging
import sys
import traceback
import asyncio
from typing import Callable, Any
from contextlib import asynccontextmanager

from core.logger import get_logger

try:
    log = get_logger()
except Exception:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    log = logging.getLogger("SocialPipe")

def safe_run_sync(fn: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Run a synchronous function safely and log exceptions.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        log.exception("Error in safe_run_sync: %s", e)
        return None

async def safe_run_async(coro: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Run an async coroutine with exception handling.
    """
    try:
        return await coro(*args, **kwargs)
    except Exception as e:
        log.exception("Error in safe_run_async: %s", e)
        return None

def format_exc(e: Exception) -> str:
    tb = traceback.format_exception(type(e), e, e.__traceback__)
    return "".join(tb)

def ensure_event_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.new_event_loop()

@asynccontextmanager
async def lifespan_manager(start: Callable = None, stop: Callable = None):
    """
    Async context manager for startup/shutdown wrappers.
    Usage in FastAPI:
      async with lifespan_manager(start=on_start, stop=on_stop):
          ...
    """
    if start:
        try:
            await safe_run_async(start)
        except Exception:
            log.exception("Startup hook failed.")
    try:
        yield
    finally:
        if stop:
            try:
                await safe_run_async(stop)
            except Exception:
                log.exception("Shutdown hook failed.")
