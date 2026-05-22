from aiogram.utils.keyboard import InlineKeyboardBuilder

homiy_kb = InlineKeyboardBuilder()

homiy_kb.button(text="➕", callback_data="homiy_add")
homiy_kb.button(text="❌", callback_data="homiy_del")
homiy_kb.button(text="Ro'yxat", callback_data="homiy_list")

homiy_kb.adjust(2)

homiy_kb = homiy_kb.as_markup()