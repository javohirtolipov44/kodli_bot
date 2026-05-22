from aiogram.utils.keyboard import InlineKeyboardBuilder

admin_kb = InlineKeyboardBuilder()

admin_kb.button(text="Anime kanallar", callback_data="anime_chanel")
admin_kb.button(text="Homiy kanallar", callback_data="homiy_chanel")
admin_kb.button(text="Xabar yuborish", callback_data="send_message")
admin_kb.button(text="Statistika", callback_data="statistika")

admin_kb.adjust(2)

admin_kb = admin_kb.as_markup()