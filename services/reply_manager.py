from core.logger import log
from integrations.instagram import ig_reply_comment
from integrations.whatsapp import wa_send_text
from integrations.twitter import tw_reply

async def route_reply(target: str, thread_key: str, message: str):
    """
    target format examples:
      ig:comment:<comment_id>
      wa:chat:<phone>
      x:tweet:<tweet_id>
    """
    try:
        p, kind, ref = target.split(":", 2)
    except ValueError:
        p, kind, ref = "unknown", "unknown", thread_key

    if p == "ig" and kind == "comment":
        return await ig_reply_comment(ref, message)
    if p == "wa" and kind == "chat":
        return await wa_send_text(ref, message)
    if p in ("x","tw") and kind == "tweet":
        return await tw_reply(ref, message)
    log.warning(f"Unknown reply route: {target}")
    return False
