from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from core.config import settings

def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Link Instagram", url=f"{settings.DOMAIN}/oauth/instagram")],
        [InlineKeyboardButton("Categories", callback_data="show_categories")],
        [InlineKeyboardButton("Help", callback_data="help")]
    ])
