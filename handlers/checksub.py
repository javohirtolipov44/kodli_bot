from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ChatMemberStatus
from aiogram.utils.keyboard import InlineKeyboardBuilder
from baza.homiy import get_all_homiy

router = Router()

@router.callback_query(F.data == "checksub")
async def check_sub_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    homiylar = await get_all_homiy()
    CHANNELS = [{"id": h[1], "link": h[2]} for h in homiylar]
    missing_channels = []

    for ch in CHANNELS:
        member = await callback.bot.get_chat_member(ch["id"], user_id)
        if member.status not in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ):
            missing_channels.append(ch)

    if missing_channels:
        try:
            kb = InlineKeyboardBuilder()
            for ch in missing_channels:
                kb.button(text="📢 Kanalga obuna bo‘lish", url=ch["link"])
            kb.button(text="Tekshirish", callback_data="checksub")
            kb.adjust(1)
            await callback.message.edit_text(
                "❌ Siz hali barcha kanallarga obuna bo‘lmadingiz",
                reply_markup=kb.as_markup()
            )
        except Exception:
            pass
    else:
        await callback.message.edit_text("✅ Obuna bo‘lganingiz uchun rahmat")
