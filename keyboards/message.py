from aiogram.utils.keyboard import InlineKeyboardBuilder

message_kb = InlineKeyboardBuilder()

message_kb.button(text="Tasdiqlash", callback_data="send")


message_kb.adjust(1)

message_kb = message_kb.as_markup()
