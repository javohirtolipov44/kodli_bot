from aiogram import Router, F
from aiogram.types import Message
from baza.anime import get_anime_by_hesh
from baza.users import add_user

router = Router()

@router.message(F.text.startswith("/start"))
async def f(message: Message):
    # /start dan keyingi parametrni olish
    args = message.text.split(maxsplit=1)  # ['/start', 'param']
    param = args[1] if len(args) > 1 else None

    if param:
        try:
            await add_user(message.from_user.id)
            anime = await get_anime_by_hesh(param)
            if not anime:
                await message.answer("❌ Anime topilmadi")
                return

            channel_id, message_id = anime
            await message.bot.copy_message(
                chat_id=message.from_user.id,
                from_chat_id=int(channel_id),
                message_id=int(message_id)
            )
        except Exception:
            await message.answer("❌ Anime topilmadi")

    else:
        await add_user(message.from_user.id)
        await message.answer("Botga xush kelibsiz!!!")
