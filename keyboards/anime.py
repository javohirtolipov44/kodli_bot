from aiogram.utils.keyboard import InlineKeyboardBuilder

anime_kb = InlineKeyboardBuilder()

anime_kb.button(text="➕", callback_data="anime_chanel_add")
anime_kb.button(text="❌", callback_data="anime_chanel_del")
anime_kb.button(text="Ro'yxat", callback_data="anime_chanel_list")

anime_kb.adjust(2)

anime_kb = anime_kb.as_markup()