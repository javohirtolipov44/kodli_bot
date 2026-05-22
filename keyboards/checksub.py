from aiogram.utils.keyboard import InlineKeyboardBuilder
from baza.homiy import get_all_homiy

async def build_sub_keyboard():
    kb = InlineKeyboardBuilder()
    homiylar = await get_all_homiy()
    CHANNELS = [{"id": h[1], "link": h[2]} for h in homiylar]
    for ch in CHANNELS:
        kb.button(text="📢 Kanalga obuna bo‘lish", url=ch["link"])
    kb.button(text="Tekshirish", callback_data="checksub")
    kb.adjust(1)
    return kb.as_markup()

