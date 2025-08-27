from telegram import Update
from telegram.ext import ContextTypes
from services.reply_manager import route_reply

HELP = (
    "Reply format:\n"
    "`/reply <target> | <message>`\n"
    "Examples:\n"
    "/reply ig:comment:1789 | Thanks!\n"
    "/reply wa:chat:+1555123456 | Hello\n"
    "/reply tw:tweet:17890 | Appreciate it!"
)

async def reply_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(HELP, parse_mode="Markdown")
        return
    joined = " ".join(context.args)
    if "|" not in joined:
        await update.message.reply_text(HELP, parse_mode="Markdown")
        return
    target, msg = [x.strip() for x in joined.split("|", 1)]
    ok = await route_reply(target, "", msg)
    await update.message.reply_text("✅ Sent." if ok else "❌ Failed.")
