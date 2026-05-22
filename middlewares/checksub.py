from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Awaitable, Callable, Any, Dict
from aiogram.enums import ChatMemberStatus
from baza.homiy import get_all_homiy
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMINS

def sub_keyboard(missing_channels=None):
    kb = InlineKeyboardBuilder()
    if missing_channels is None:
        missing_channels = CHANNELS
    for ch in missing_channels:
        kb.button(text="Kanalga obuna bo‘lish", url=ch["link"])
    kb.button(text="Tekshirish", callback_data="checksub")
    kb.adjust(1)
    return kb.as_markup()

class MultiCheckSubMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        # Faqat Message tipidagi eventlarni tekshiramiz
        if not isinstance(event, Message):
            return await handler(event, data)

        if event.chat.type != "private":
            return await handler(event, data)

        user_id = event.from_user.id
        if user_id in ADMINS:
            return await handler(event, data)
        homiylar = await get_all_homiy()
        CHANNELS = [{"id": h[1], "link": h[2]} for h in homiylar]
        missing_channels = []

        for ch in CHANNELS:
            try:
                member = await event.bot.get_chat_member(ch["id"], user_id)
                if member.status not in (
                    ChatMemberStatus.MEMBER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.CREATOR
                ):
                    missing_channels.append(ch)
            except Exception as e:
                print(f"Xatolik kanal {ch['id']}: {e}")
                missing_channels.append(ch)

        if missing_channels:
            await event.answer(
                "❌ Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:",
                reply_markup=sub_keyboard(missing_channels)
            )
            return None  # handlerni chaqirmaymiz

        # Agar obuna bo‘lsa, xabar handlerga uzatiladi
        return await handler(event, data)
